-- ============================================================
-- TenCate Marketing Intelligence Platform — Initial Schema
-- ============================================================

-- Social analytics from Ayrshare (daily ingestion)
CREATE TABLE social_analytics (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  platform          TEXT NOT NULL CHECK (platform IN ('linkedin','instagram','facebook','youtube')),
  post_id           TEXT NOT NULL,
  post_url          TEXT,
  post_date         DATE NOT NULL,
  impressions       INTEGER,
  reach             INTEGER,
  engagement        INTEGER,
  engagement_rate   NUMERIC(6,4),
  likes             INTEGER,
  comments          INTEGER,
  shares            INTEGER,
  saves             INTEGER,
  link_clicks       INTEGER,
  follower_count    INTEGER,
  content_type      TEXT,
  ingested_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (tenant_id, platform, post_id)
);

-- GA4 website traffic (daily ingestion)
CREATE TABLE ga4_analytics (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id             UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  date                  DATE NOT NULL,
  sessions              INTEGER,
  users                 INTEGER,
  bounce_rate           NUMERIC(6,4),
  avg_session_duration  NUMERIC(10,2),
  source_medium         TEXT,
  landing_page          TEXT,
  conversions           INTEGER,
  ingested_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Weekly trend research output from Trend Research Agent
CREATE TABLE trend_reports (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id     UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  week_starting DATE NOT NULL,
  topics        JSONB NOT NULL DEFAULT '[]',
  raw_research  TEXT,
  skill_version TEXT,
  model         TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Input for each content generation request
CREATE TABLE content_briefs (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id             UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  user_id               UUID NOT NULL,
  platform              TEXT NOT NULL CHECK (platform IN ('linkedin','instagram','facebook','youtube')),
  objective             TEXT NOT NULL,
  key_message           TEXT NOT NULL,
  trend_topic_id        UUID REFERENCES trend_reports(id),
  reference_image_path  TEXT,
  analytics_context     JSONB,
  created_at            TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Three generated variants per brief
CREATE TABLE content_variants (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  brief_id        UUID NOT NULL REFERENCES content_briefs(id) ON DELETE CASCADE,
  variant_index   SMALLINT NOT NULL CHECK (variant_index IN (1,2,3)),
  copy_text       TEXT NOT NULL,
  visual_brief    TEXT,
  brand_fit_score JSONB,
  skill_versions  JSONB,
  model           TEXT,
  status          TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft','in_review','approved','rejected')),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (brief_id, variant_index)
);

-- Brand Review Agent scores per variant
CREATE TABLE brand_fit_scores (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id           UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  variant_id          UUID NOT NULL REFERENCES content_variants(id) ON DELETE CASCADE,
  tone_alignment      TEXT CHECK (tone_alignment IN ('pass','fail','warning')),
  naming_spelling     TEXT CHECK (naming_spelling IN ('pass','fail','warning')),
  claim_integrity     TEXT CHECK (claim_integrity IN ('pass','fail','warning')),
  palette_compliance  TEXT CHECK (palette_compliance IN ('pass','fail','warning')),
  visual_style        TEXT CHECK (visual_style IN ('pass','fail','warning')),
  platform_fit        TEXT CHECK (platform_fit IN ('pass','fail','warning')),
  generic_ai_detection TEXT CHECK (generic_ai_detection IN ('pass','fail','warning')),
  flags               JSONB,
  overall             TEXT NOT NULL CHECK (overall IN ('pass','fail')),
  scored_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Full audit trail of reviewer actions
CREATE TABLE review_events (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id   UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  variant_id  UUID NOT NULL REFERENCES content_variants(id) ON DELETE CASCADE,
  reviewer_id UUID NOT NULL,
  action      TEXT NOT NULL CHECK (action IN ('approve','reject','request_changes')),
  comment     TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Approved and exported final content
CREATE TABLE content_library (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id      UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  variant_id     UUID NOT NULL REFERENCES content_variants(id),
  brief_id       UUID NOT NULL REFERENCES content_briefs(id),
  platform       TEXT NOT NULL,
  copy_text      TEXT NOT NULL,
  visual_brief   TEXT,
  asset_path     TEXT,
  approved_by    UUID NOT NULL,
  approved_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  skill_versions JSONB,
  tags           TEXT[],
  campaign       TEXT
);

-- Immutable generation event log for lineage tracing
CREATE TABLE generation_log (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id      UUID NOT NULL DEFAULT '00000000-0000-0000-0000-000000000001',
  brief_id       UUID NOT NULL REFERENCES content_briefs(id),
  model          TEXT NOT NULL,
  skill_versions JSONB NOT NULL,
  prompt_hash    TEXT,
  tokens_used    INTEGER,
  duration_ms    INTEGER,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- ── Indexes ──────────────────────────────────────────────────────────────────
CREATE INDEX idx_social_analytics_platform_date ON social_analytics (tenant_id, platform, post_date DESC);
CREATE INDEX idx_ga4_analytics_date ON ga4_analytics (tenant_id, date DESC);
CREATE INDEX idx_trend_reports_week ON trend_reports (tenant_id, week_starting DESC);
CREATE INDEX idx_content_briefs_user ON content_briefs (tenant_id, user_id, created_at DESC);
CREATE INDEX idx_content_variants_brief ON content_variants (brief_id);
CREATE INDEX idx_content_variants_status ON content_variants (tenant_id, status);
CREATE INDEX idx_review_events_variant ON review_events (variant_id, created_at DESC);
CREATE INDEX idx_content_library_platform ON content_library (tenant_id, platform, approved_at DESC);
CREATE INDEX idx_generation_log_brief ON generation_log (brief_id);

