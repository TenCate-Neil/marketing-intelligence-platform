# TenCate Marketing Intelligence Platform — CLAUDE.md

This file is the primary context document for all Claude Code sessions working on this project. Read it fully before writing any code or making architectural decisions.

---

## What This Platform Is

An internal AI-powered marketing platform for TenCate Grass that combines social media analytics, industry trend research, brand-aware content generation, and a structured approval workflow into one repeatable system. It is designed to start with TenCate Grass and extend to other TenCate group companies in Phase 2.

The platform's value proposition: TenCate's brand rules, performance signals, and industry trends are combined at generation time — not patched on afterward. Every marketer on the team can produce on-brand content without being a brand expert, and the system gets better as it learns what gets approved.

**What it is not:** a generic AI writing tool, a social media scheduler, or a reporting dashboard bolted onto an AI chat interface. It is a structured workflow with AI agents at specific steps.

---

## Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| Frontend | Next.js 14 (App Router) + React | Deployed to Vercel. Internal only, behind SSO. |
| Auth | Azure AD / Entra ID SSO | Roles: `marketer`, `reviewer`, `admin` |
| AI orchestration | Anthropic Messages API (Claude Enterprise) | claude-opus-4-8 for generation; claude-sonnet-4-6 for review, research, visual analysis |
| Database | Supabase (PostgreSQL) | All structured data — analytics, content records, approvals, trend research, brand-fit scores |
| File storage | OneDrive (Microsoft Graph API) | Reference images + approved content assets. Path stored in Supabase, file stays in OneDrive. |
| Skill repository | Git (this repo) | Skill files are markdown in `/skills/`. Version tag logged to DB at every generation. |
| MCP — social analytics | Ayrshare (primary) | LinkedIn, Instagram, Facebook, YouTube analytics + future publishing |
| MCP — web search | Tavily | Powers the Trend Research Agent |
| MCP — image generation | TBD (behind MCP boundary) | Imagen 3 / DALL-E 3 / Stable Diffusion — benchmarked in prototype phase |
| Secrets | Vercel environment variables (MVP) | Upgrade to Azure Key Vault in Phase 2 |

---

## Repository Structure

```
/
├── CLAUDE.md                        # This file
├── app/                             # Next.js app router
│   ├── (auth)/                      # SSO login flow
│   ├── dashboard/                   # Main analytics + trend summary screen
│   ├── trends/                      # Full weekly trend report
│   ├── generate/                    # Content generator screen
│   ├── review/                      # Brand reviewer queue
│   ├── library/                     # Approved content library
│   └── analytics/                   # Full analytics screen
├── api/                             # Next.js API routes (server-side only)
│   ├── analytics/                   # Social analytics ingestion + queries
│   ├── content/                     # Content generation, saving, approval
│   ├── trends/                      # Trend research trigger + fetch
│   └── files/                       # OneDrive file upload/retrieve via Graph API
├── agents/                          # Agent definitions and orchestration logic
│   ├── content-generation/          # Content Generation Agent
│   ├── brand-review/                # Brand Review Agent
│   ├── trend-research/              # Trend Research Agent
│   └── visual-analysis/             # Visual Analysis Agent
├── skills/                          # Skill files (markdown). Owned by brand team.
│   ├── brands/
│   │   └── tencate-grass/
│   │       ├── tencate-brand.md     # Master brand skill
│   │       ├── esg-language.md      # ESG/sustainability claim rules
│   │       └── regional/            # Future: regional sub-skills
│   ├── platforms/
│   │   ├── platform-linkedin.md
│   │   ├── platform-instagram.md
│   │   ├── platform-facebook.md
│   │   └── platform-youtube.md
│   └── workflows/
│       ├── content-generation.md    # Generation workflow instructions
│       ├── brand-review.md          # Brand-fit scoring checklist
│       ├── trend-research.md        # Trend research instructions
│       └── visual-inspiration.md    # Reference image analysis rules
├── mcp/                             # MCP server configuration
│   ├── ayrshare.ts                  # Social analytics MCP client
│   ├── tavily.ts                    # Web search MCP client
│   ├── graph.ts                     # Microsoft Graph (OneDrive) client
│   └── image-gen.ts                 # Image generation MCP client (swappable)
├── lib/
│   ├── supabase.ts                  # Supabase client (server + client)
│   ├── anthropic.ts                 # Anthropic client setup
│   └── auth.ts                      # Entra ID session helpers
├── hooks/                           # Claude Code hooks (not React hooks)
│   ├── pre-generation.ts            # Fetch skill versions, log generation start
│   ├── post-generation.ts           # Trigger Brand Review Agent automatically
│   └── post-approval.ts             # Export to OneDrive, write to content library
├── prompts/                         # System prompts + regression tests
│   ├── regression/                  # CI prompt regression tests
│   └── system/                      # Base system prompts per agent
└── supabase/
    └── migrations/                  # Database schema migrations
```

---

## Database Schema (Supabase / PostgreSQL)

### `social_analytics`
Stores ingested social data from Ayrshare on a daily schedule.
```sql
id, platform, post_id, post_url, post_date, impressions, reach,
engagement, engagement_rate, likes, comments, shares, saves,
link_clicks, follower_count, content_type, ingested_at
```

### `ga4_analytics`
Website traffic data from the Google Analytics Data API.
```sql
id, date, sessions, users, bounce_rate, avg_session_duration,
source_medium, landing_page, conversions, ingested_at
```

### `trend_reports`
Weekly trend research output from the Trend Research Agent.
```sql
id, week_starting, topics (jsonb), raw_research (text),
skill_version, model, created_at
```
Each `topics` entry: `{ topic, why_trending, tencate_angle, engagement_signal, sensitivity_flag }`

### `content_briefs`
Records the input for each content generation request.
```sql
id, user_id, platform, objective, key_message,
trend_topic_id (nullable), reference_image_path (nullable),
analytics_context (jsonb), created_at
```

### `content_variants`
The three generated variants for each brief.
```sql
id, brief_id, variant_index (1|2|3), copy_text, visual_brief,
brand_fit_score (jsonb), skill_versions (jsonb), model, status,
created_at
```
`status`: `draft | in_review | approved | rejected`

### `brand_fit_scores`
One row per variant, written by the Brand Review Agent.
```sql
id, variant_id, tone_alignment (pass|fail|warning), naming_spelling,
claim_integrity, palette_compliance, visual_style, platform_fit,
generic_ai_detection, flags (jsonb), overall (pass|fail), scored_at
```

### `review_events`
Full audit trail of reviewer actions.
```sql
id, variant_id, reviewer_id, action (approve|reject|request_changes),
comment, created_at
```

### `content_library`
Approved and exported final content.
```sql
id, variant_id, brief_id, platform, copy_text, visual_brief,
asset_path (OneDrive path), approved_by, approved_at,
skill_versions (jsonb), tags (text[]), campaign
```

### `generation_log`
Immutable log of every generation event for lineage tracing.
```sql
id, brief_id, model, skill_versions (jsonb), prompt_hash,
tokens_used, duration_ms, created_at
```

---

## The Four Agents

### 1. Content Generation Agent

**Model:** `claude-opus-4-8`
**Location:** `agents/content-generation/`

**Purpose:** Takes a content brief and produces three platform-specific, brand-aware variants — each with copy and a visual brief.

**Input context assembled before the API call:**
1. `tencate-brand.md` — always included
2. Platform skill file (`platform-linkedin.md` etc.) — selected by `platform` field in brief
3. `content-generation.md` workflow skill
4. Analytics context — top 5 performing posts for that platform in the last 30 days, fetched from `social_analytics` table
5. Trend context — if `trend_topic_id` is set, the full topic object from `trend_reports`
6. Visual brief — if a reference image was uploaded, the Visual Analysis Agent output is included here

**Output format (structured JSON):**
```json
{
  "variants": [
    {
      "index": 1,
      "copy": "...",
      "visual_brief": "...",
      "hashtags": ["..."],
      "cta": "..."
    }
  ]
}
```

**Post-generation:** The pre-generation hook logs the skill versions and brief ID to `generation_log`. The post-generation hook immediately passes all three variants to the Brand Review Agent before they are shown to the user.

**Important constraints:**
- Never generate content without the brand skill loaded
- Always produce exactly 3 variants
- YouTube output: script outline + description + title options, not a caption

---

### 2. Brand Review Agent

**Model:** `claude-sonnet-4-6`
**Location:** `agents/brand-review/`

**Purpose:** Scores every generated variant against TenCate's brand checklist before it reaches a human reviewer. Runs automatically — never skipped.

**Input:**
- The variant copy and visual brief
- `tencate-brand.md`
- `brand-review.md` (the scoring checklist skill)
- Platform skill file (for platform-fit dimension)

**Scoring dimensions:**
| Dimension | What it checks |
|---|---|
| `tone_alignment` | Transparent, clear, fact-driven, formal yet friendly. American English. Active voice. |
| `naming_spelling` | "TenCate" (capital T and C). Product names correct. Trademarks applied. |
| `claim_integrity` | Sustainability and performance claims are specific and supportable. Vague claims flagged. |
| `palette_compliance` | TC Blue dominant. TC Orange accent only. No orange backgrounds or orange text on blue. |
| `visual_style` | Brief calls for real people, real environments, natural daylight — not staged or generic. |
| `platform_fit` | Copy length, tone, hashtag and CTA conventions match the target platform. |
| `generic_ai_detection` | Free of vague superlatives, filler phrases, and generic marketing language. |

**Output format:**
```json
{
  "variant_id": "...",
  "scores": {
    "tone_alignment": { "result": "pass|fail|warning", "reason": "..." },
    "naming_spelling": { "result": "...", "reason": "..." },
    "claim_integrity": { "result": "...", "reason": "...", "flagged_claims": [] },
    "palette_compliance": { "result": "...", "reason": "..." },
    "visual_style": { "result": "...", "reason": "..." },
    "platform_fit": { "result": "...", "reason": "..." },
    "generic_ai_detection": { "result": "...", "reason": "..." }
  },
  "overall": "pass|fail",
  "summary": "One sentence summary for the reviewer"
}
```

**Rules:**
- A `fail` on `claim_integrity` or `naming_spelling` always sets `overall` to `fail`
- ESG-related content always gets a `claim_integrity` flag for reviewer attention, even if it passes
- The score is a checklist, not a blocker — a reviewer can approve a flagged draft but the record is kept

---

### 3. Trend Research Agent

**Model:** `claude-sonnet-4-6`
**Location:** `agents/trend-research/`

**Purpose:** Weekly automated scan of trending topics in the artificial turf industry. Produces a ranked list of 5–8 topics with suggested TenCate content angles.

**Trigger:** Scheduled cron job (weekly, e.g., Monday 06:00 UTC). Not user-initiated.

**MCP tool used:** Tavily web search

**Search scope defined in `trend-research.md` skill:**
- Industry publications (artificial turf, synthetic surfaces, sports facilities)
- Sports facility construction and renovation news
- Sustainability and environmental news relevant to synthetic turf
- Social media discussions where signals are accessible
- Time window: past 2–4 weeks

**Process:**
1. Run 4–6 targeted searches across the defined topic areas
2. Identify recurring topics, emerging themes, discussions gaining engagement
3. Filter for relevance to TenCate's positioning (B2B sports surfaces, sustainability, performance)
4. Flag any ESG or regulatory topics with `sensitivity_flag: true`
5. Produce ranked list with `topic`, `why_trending`, `tencate_angle`, `engagement_signal`

**Output stored in `trend_reports` table.**

**Constraints:**
- The trend report is a signal for human judgement, not a directive
- ESG/regulatory topics are flagged — any content generated from them is routed through extra claim-integrity checking
- The agent never publishes anything; it only informs
- Quality over quantity: 5 high-confidence topics beats 10 weak ones

---

### 4. Visual Analysis Agent

**Model:** `claude-sonnet-4-6` (multimodal)
**Location:** `agents/visual-analysis/`

**Purpose:** When a marketer uploads a reference image for inspiration, this agent analyses it and produces an original TenCate-aligned visual brief. It must never reproduce or closely imitate the reference.

**Trigger:** Fires when a reference image is uploaded during content generation. Output is included in the Content Generation Agent's context.

**Input:**
- The uploaded image (base64 or URL)
- `visual-inspiration.md` skill file
- `tencate-brand.md` (for palette and visual style alignment)

**What it extracts from the image:**
- Mood and emotional tone
- Colour palette (but remapped to TenCate brand palette)
- Composition and framing approach
- Subject matter and setting type (not the specific subjects)
- Lighting character

**Output format:**
```json
{
  "mood": "...",
  "palette_direction": "TC Blue dominant, natural greens as supporting...",
  "composition_notes": "...",
  "lighting": "...",
  "setting_type": "...",
  "tencate_brief": "Full visual brief paragraph ready to include in content generation context"
}
```

**Hard rules from `visual-inspiration.md`:**
- Never describe specific people, faces, or identifiable individuals from the reference
- Never reproduce brand marks, logos, or text from the reference
- The `tencate_brief` must describe an original scene, not the reference image
- If the reference is flagged as potentially derivative, return a warning and a generic brief instead

---

## Content Generation Workflow (Full Flow)

This is the end-to-end user journey and system flow for producing one piece of content.

### Mode A — Trend-Driven (minimal human input)

1. Marketer opens dashboard, sees the weekly trend report summary
2. Clicks "Create content from this trend" on a topic
3. Platform pre-selects: trend topic, default platform (LinkedIn for B2B topics, Instagram for visual topics)
4. Marketer can adjust platform and optionally upload a reference image
5. Clicks Generate → jumps to step 6 below

### Mode B — Original Brief (marketer-directed)

1. Marketer opens Content Generator
2. Fills in: target platform, objective (one line), key message (one line)
3. Optionally uploads a reference image
4. Optionally pre-loads a trend topic
5. Clicks Generate → continues to step 6 below

### Steps 6 onwards (same for both modes)

6. **Pre-generation hook fires:**
   - Fetches current skill file version tags from Git
   - Fetches top 5 performing posts for the selected platform (last 30 days) from `social_analytics`
   - Writes generation-start record to `generation_log`

7. **If reference image uploaded:** Visual Analysis Agent runs first, produces visual brief JSON

8. **Content Generation Agent runs (Opus 4.8):**
   - Context assembled: brand skill + platform skill + workflow skill + analytics context + trend context + visual brief (if any)
   - Returns 3 variants as structured JSON

9. **Post-generation hook fires:**
   - Passes all 3 variants immediately to Brand Review Agent (Sonnet 4.6)
   - Variants are not shown to the marketer until brand scores are ready

10. **Brand Review Agent runs on all 3 variants in parallel**
    - Writes `brand_fit_scores` rows to Supabase
    - Sets `overall: pass|fail` per variant

11. **Marketer sees 3 variants side by side**, each with:
    - Copy text
    - Visual brief
    - Brand-fit score checklist (pass/fail per dimension)
    - Any flags explained in plain language

12. **Marketer actions:**
    - Select a variant and submit to review
    - Request refinement: enter natural-language instruction → loops back to step 8 with the instruction appended to context (previous variants retained)
    - Discard and start over

13. **Brand Reviewer receives notification:**
    - Sees the selected variant, brand-fit checklist, full prompt lineage, brief details
    - Actions: Approve / Reject / Request changes (with comment)
    - All actions written to `review_events`

14. **On approval:**
    - Post-approval hook fires
    - File (if any) written to OneDrive via Graph API
    - Record written to `content_library` with full lineage
    - Variant status set to `approved`
    - Marketer notified

15. **On rejection or request-changes:**
    - Marketer sees reviewer comment
    - Can refine (loops back to step 12) or start a new brief

---

## Scheduled Workflows

### Social Analytics Ingestion
- **Schedule:** Daily, 02:00 UTC
- **Process:** Call Ayrshare MCP → fetch previous day's post-level analytics for all four platforms → upsert into `social_analytics` table
- **Error handling:** If Ayrshare call fails, log error and retry once after 10 minutes. Alert admin if second attempt fails.

### GA4 Ingestion
- **Schedule:** Daily, 02:30 UTC
- **Process:** Call Google Analytics Data API → fetch sessions, sources, bounce rate, top pages → upsert into `ga4_analytics` table
- **Auth:** OAuth service account with read-only access scoped to the GA4 property

### Trend Research
- **Schedule:** Weekly, Monday 06:00 UTC
- **Process:** Trigger Trend Research Agent → store output in `trend_reports` → dashboard shows latest report
- **Manual trigger:** Admin can trigger ad-hoc from the dashboard

---

## Skill File Governance

Skill files are markdown files in `/skills/`. They are the primary mechanism for brand-awareness — they are not prompts buried in code.

**Ownership:** Brand team owns and approves all changes to `/skills/brands/tencate-grass/`. Platform and workflow skills are owned jointly by brand and development teams.

**Change process:** Pull request required for all skill file changes. CI runs prompt regression tests on every change. Failed regression tests block the merge.

**Version tracking:** Every generation event logs the exact Git commit SHA of each skill file used. This means any approved piece of content can be traced back to the exact brand rules in effect at the time.

**Skill file loading in code:** Skill files are read from the filesystem at request time (not cached in the database). This means skill updates take effect immediately on the next generation without a deployment. In production, the Git repo is the source of truth — use `fs.readFileSync` from the Next.js API route, not a database copy.

---

## MCP Integration Details

### Ayrshare (Social Analytics)
- Single authenticated integration covering LinkedIn, Instagram, Facebook, YouTube
- Used for: analytics retrieval (MVP), publishing (Phase 3)
- Auth: API key stored in Vercel environment variables
- Rate limits: check Ayrshare docs; schedule ingestion jobs to respect limits
- Fallback: if Ayrshare is unavailable, CSV export from native dashboards is the manual fallback for analytics

### Tavily (Web Search)
- Used exclusively by the Trend Research Agent
- API key in Vercel environment variables
- Configure search to return full content where possible (not just snippets) for better synthesis quality

### Microsoft Graph API (OneDrive)
- Used for: reference image upload, approved content asset export
- Auth: OAuth with a registered Azure AD app (service principal)
- Scopes needed: `Files.ReadWrite` scoped to the designated OneDrive folder
- The app never accesses the user's personal OneDrive — only the shared marketing team folder
- Retrieve files using short-lived access URLs generated via Graph at display time

### Google Analytics Data API
- Used for: GA4 metrics ingestion
- Auth: OAuth service account, read-only
- No third-party intermediary required
- Property ID stored in environment variables

### Image Generation MCP (TBD)
- The specific model is intentionally abstracted behind an MCP boundary in `mcp/image-gen.ts`
- The interface is fixed: `{ prompt: string, style_notes: string } → { image_url: string }`
- Swap the underlying model without touching any agent or UI code
- Benchmark Imagen 3, DALL-E 3, and Stable Diffusion XL in the prototype phase against TenCate visual style requirements

---

## Authentication and Roles

All users authenticate via Azure AD / Entra ID SSO. No local accounts.

| Role | Capabilities |
|---|---|
| `marketer` | Create briefs, generate content, submit to review, view analytics, view trend report, view content library |
| `reviewer` | All marketer capabilities + approve/reject content, request changes |
| `admin` | All reviewer capabilities + manage users, trigger manual trend research run, view full audit logs, manage MCP connections |

Role is stored on the user's session after SSO. Enforce at the API route level, not just the UI.

---

## Environment Variables

```
# Anthropic
ANTHROPIC_API_KEY=

# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Ayrshare
AYRSHARE_API_KEY=

# Tavily
TAVILY_API_KEY=

# Microsoft (Entra ID SSO + Graph API)
AZURE_AD_CLIENT_ID=
AZURE_AD_CLIENT_SECRET=
AZURE_AD_TENANT_ID=
ONEDRIVE_FOLDER_ID=

# Google Analytics
GA4_PROPERTY_ID=
GA4_SERVICE_ACCOUNT_KEY=   # JSON stringified

# Image generation (TBD — add when model is selected)
IMAGE_GEN_API_KEY=
IMAGE_GEN_ENDPOINT=
```

---

## What to Build First (Prototype Sequence)

The proposal specifies a deliberate build order. Do not deviate from this without a good reason.

**Week 1–2 — Content generator only**
- Content Generation Agent (Opus 4.8) with TenCate brand skill and LinkedIn + Instagram platform skills
- Brand Review Agent (Sonnet 4.6) running post-generation
- Minimal UI: brief form → 3 variants with brand-fit scores
- No analytics ingestion, no trend module, no review queue, no database yet
- Goal: validate that output quality justifies the investment before building infrastructure

**Week 3–4 — Data layer**
- Supabase schema and migrations
- Ayrshare ingestion pipeline → `social_analytics` table
- GA4 ingestion → `ga4_analytics` table
- Content records, generation log, brand-fit scores persisted to DB
- Generation lineage (skill versions logged)

**Week 5–6 — Trend research and dashboard**
- Trend Research Agent (Sonnet 4.6) with Tavily MCP
- Weekly scheduled run
- Analytics dashboard: filterable chart, top-performing posts
- Trend report screen

**Week 7–8 — Review workflow and content library**
- Review queue screen for brand reviewers
- Approval/rejection flow → `review_events`
- Post-approval hook → OneDrive export via Graph API
- Content library screen

---

## Multi-Tenancy (Phase 2)

The architecture supports multiple TenCate companies without a rebuild. Each company gets:
- Its own brand skill pack at `/skills/brands/<company-name>/`
- Its own rows in all Supabase tables (all tables include a `tenant_id` column from day one — add this even in the MVP)
- Its own user set and roles (scoped by `tenant_id`)
- Shared platform skills, workflow skills, and MCP infrastructure

Add `tenant_id` to every database table in the initial migration even though Phase 1 only has one tenant. Retrofitting multi-tenancy onto a schema is painful.

---

## Key Constraints and Rules

- **Never skip brand review.** The Brand Review Agent runs on every variant, every time. It is not optional and must not be bypassed by any code path.
- **Never publish directly.** The platform has no publishing capability in MVP or Phase 2. Content is exported to OneDrive. Automated publishing is Phase 3 only, behind hard approval gates.
- **Skill files are the source of truth.** Brand rules live in markdown, not in prompts hardcoded in TypeScript files. If you find yourself hardcoding brand guidance in agent code, move it to the appropriate skill file.
- **Never reproduce reference images.** The Visual Analysis Agent must always produce an original brief. Add explicit instructions in both `visual-inspiration.md` and the agent system prompt.
- **ESG claims need extra care.** Any content touching sustainability, recycling, PFAS, or environmental topics must have `claim_integrity` flagged for reviewer attention regardless of whether the automated check passes.
- **Lineage is non-negotiable.** Every generation event must log: brief ID, model, skill file versions (Git SHAs), prompt hash, reviewer, timestamp. This is the audit trail that makes the brand governance claim credible.
- **Build for the scale that exists.** MVP does not need a vector database, model fine-tuning, a service mesh, or microservices. Supabase + Vercel + Claude covers everything needed. Do not over-engineer.
