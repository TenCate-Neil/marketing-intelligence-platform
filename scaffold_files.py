"""
Run from the root of your marketing-intelligence-platform repo.
Creates all config files, app pages, lib/mcp stubs, and pushes to GitHub.

Usage:
    python scaffold_files.py
"""

import os

if not os.path.isdir(".git"):
    print("ERROR: run this from the root of your repo.")
    raise SystemExit(1)

FILES = {}

# ── package.json ────────────────────────────────────────────────────────────
FILES["package.json"] = '''{
  "name": "marketing-intelligence-platform",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "^14.2.29",
    "react": "^18",
    "react-dom": "^18"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "eslint": "^8",
    "eslint-config-next": "^14.2.29",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "typescript": "^5"
  }
}
'''

# ── next.config.ts ───────────────────────────────────────────────────────────
FILES["next.config.ts"] = '''import type { NextConfig } from "next";

const nextConfig: NextConfig = {};

export default nextConfig;
'''

# ── tsconfig.json ────────────────────────────────────────────────────────────
FILES["tsconfig.json"] = '''{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
'''

# ── tailwind.config.ts ───────────────────────────────────────────────────────
FILES["tailwind.config.ts"] = '''import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "tc-blue": "#003087",
        "tc-blue-light": "#0050B3",
        "tc-orange": "#E87722",
      },
    },
  },
  plugins: [],
};

export default config;
'''

# ── postcss.config.mjs ───────────────────────────────────────────────────────
FILES["postcss.config.mjs"] = '''const config = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};

export default config;
'''

# ── .eslintrc.json ───────────────────────────────────────────────────────────
FILES[".eslintrc.json"] = '{"extends": "next/core-web-vitals"}\n'

# ── .gitignore ───────────────────────────────────────────────────────────────
FILES[".gitignore"] = '''/node_modules
/.next/
/out/
/build
.env
.env.local
.env*.local
.DS_Store
npm-debug.log*
.vercel
'''

# ── .env.local.example ───────────────────────────────────────────────────────
FILES[".env.local.example"] = '''# Anthropic
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
GA4_SERVICE_ACCOUNT_KEY=

# Image generation (TBD)
IMAGE_GEN_API_KEY=
IMAGE_GEN_ENDPOINT=
'''

# ── app/globals.css ──────────────────────────────────────────────────────────
FILES["app/globals.css"] = '''@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900 antialiased;
  }
}
'''

# ── app/layout.tsx ───────────────────────────────────────────────────────────
FILES["app/layout.tsx"] = '''import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "TenCate Marketing Intelligence Platform",
  description: "Internal AI-powered marketing platform for TenCate Grass",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
'''

# ── app/page.tsx ─────────────────────────────────────────────────────────────
FILES["app/page.tsx"] = '''import Link from "next/link";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-[#003087]">
      <div className="text-center space-y-6">
        <h1 className="text-4xl font-bold text-white tracking-tight">
          TenCate Marketing Intelligence
        </h1>
        <p className="text-blue-200 text-lg max-w-md">
          AI-powered content generation and brand analytics for TenCate Grass.
        </p>
        <Link
          href="/dashboard"
          className="inline-block bg-[#E87722] text-white px-8 py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors"
        >
          Go to Dashboard
        </Link>
      </div>
    </main>
  );
}
'''

# ── App pages ─────────────────────────────────────────────────────────────────
PAGES = {
    "app/dashboard/page.tsx": ("Dashboard", "Analytics summary and trend report."),
    "app/analytics/page.tsx": ("Analytics", "Social and web analytics will appear here."),
    "app/trends/page.tsx":    ("Trend Research", "Weekly trend reports will appear here."),
    "app/generate/page.tsx":  ("Content Generator", "Content generation interface coming soon."),
    "app/review/page.tsx":    ("Review Queue", "Brand review queue coming soon."),
    "app/library/page.tsx":   ("Content Library", "Approved content library coming soon."),
}

for path, (title, desc) in PAGES.items():
    name = title.replace(" ", "") + "Page"
    FILES[path] = f'''export default function {name}() {{
  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold text-[#003087]">{title}</h1>
      <p className="text-gray-500 mt-2">{desc}</p>
    </div>
  );
}}
'''

# ── lib/ ──────────────────────────────────────────────────────────────────────
FILES["lib/supabase.ts"] = '''import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);

// Server-side only — never expose service role key to the browser
export function createServerClient() {
  return createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  );
}
'''

FILES["lib/anthropic.ts"] = '''import Anthropic from "@anthropic-ai/sdk";

export const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!,
});

export const MODELS = {
  generation: "claude-opus-4-8",
  review:     "claude-sonnet-4-6",
  research:   "claude-sonnet-4-6",
  visual:     "claude-sonnet-4-6",
} as const;
'''

FILES["lib/auth.ts"] = '''// Azure AD / Entra ID session helpers — full implementation added with NextAuth in step 2

export type UserRole = "marketer" | "reviewer" | "admin";

export interface UserSession {
  id: string;
  email: string;
  name: string;
  role: UserRole;
  tenantId: string;
}

export function hasRole(session: UserSession, required: UserRole): boolean {
  const hierarchy: UserRole[] = ["marketer", "reviewer", "admin"];
  return hierarchy.indexOf(session.role) >= hierarchy.indexOf(required);
}
'''

# ── mcp/ ──────────────────────────────────────────────────────────────────────
FILES["mcp/ayrshare.ts"] = '''// Ayrshare MCP client — social analytics for LinkedIn, Instagram, Facebook, YouTube

const AYRSHARE_BASE = "https://app.ayrshare.com/api";

async function ayrshareRequest(path: string, options: RequestInit = {}) {
  const res = await fetch(`${AYRSHARE_BASE}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${process.env.AYRSHARE_API_KEY}`,
      "Content-Type": "application/json",
      ...options.headers,
    },
  });
  if (!res.ok) throw new Error(`Ayrshare ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function getPostAnalytics(platform: string, startDate: string, endDate: string) {
  return ayrshareRequest(`/analytics/post?platforms=${platform}&startDate=${startDate}&endDate=${endDate}`);
}

export async function getSocialAnalytics(platform: string) {
  return ayrshareRequest(`/analytics/social?platforms=${platform}`);
}
'''

FILES["mcp/tavily.ts"] = '''// Tavily MCP client — web search for the Trend Research Agent

export async function tavilySearch(
  query: string,
  options: { maxResults?: number; includeRawContent?: boolean } = {}
) {
  const res = await fetch("https://api.tavily.com/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      api_key: process.env.TAVILY_API_KEY,
      query,
      max_results: options.maxResults ?? 5,
      include_raw_content: options.includeRawContent ?? true,
    }),
  });
  if (!res.ok) throw new Error(`Tavily ${res.status}: ${await res.text()}`);
  return res.json();
}
'''

FILES["mcp/graph.ts"] = '''// Microsoft Graph API — OneDrive operations scoped to the shared marketing team folder

const GRAPH_BASE = "https://graph.microsoft.com/v1.0";

async function getAccessToken(): Promise<string> {
  const res = await fetch(
    `https://login.microsoftonline.com/${process.env.AZURE_AD_TENANT_ID}/oauth2/v2.0/token`,
    {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({
        grant_type: "client_credentials",
        client_id: process.env.AZURE_AD_CLIENT_ID!,
        client_secret: process.env.AZURE_AD_CLIENT_SECRET!,
        scope: "https://graph.microsoft.com/.default",
      }),
    }
  );
  const data = await res.json();
  return data.access_token;
}

export async function uploadToOneDrive(fileName: string, content: Buffer, mimeType: string) {
  const token = await getAccessToken();
  const folderId = process.env.ONEDRIVE_FOLDER_ID;
  const res = await fetch(`${GRAPH_BASE}/drives/${folderId}/root:/${fileName}:/content`, {
    method: "PUT",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": mimeType },
    body: content,
  });
  if (!res.ok) throw new Error(`Graph ${res.status}: ${await res.text()}`);
  return res.json();
}

export async function getOneDriveFileUrl(fileId: string): Promise<string> {
  const token = await getAccessToken();
  const res = await fetch(`${GRAPH_BASE}/me/drive/items/${fileId}/createLink`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ type: "view", scope: "organization" }),
  });
  const data = await res.json();
  return data.link.webUrl;
}
'''

FILES["mcp/image-gen.ts"] = '''// Image generation MCP client — abstracted so the underlying model can be swapped
// Interface is fixed: { prompt, style_notes } → { image_url }

export interface ImageGenRequest {
  prompt: string;
  style_notes: string;
}

export interface ImageGenResponse {
  image_url: string;
}

export async function generateImage(request: ImageGenRequest): Promise<ImageGenResponse> {
  const res = await fetch(process.env.IMAGE_GEN_ENDPOINT!, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.IMAGE_GEN_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
  });
  if (!res.ok) throw new Error(`ImageGen ${res.status}: ${await res.text()}`);
  return res.json();
}
'''

# ── Skill file placeholders ───────────────────────────────────────────────────
SKILL_FILES = [
    "skills/brands/tencate-grass/tencate-brand.md",
    "skills/brands/tencate-grass/esg-language.md",
    "skills/platforms/platform-linkedin.md",
    "skills/platforms/platform-instagram.md",
    "skills/platforms/platform-facebook.md",
    "skills/platforms/platform-youtube.md",
    "skills/workflows/content-generation.md",
    "skills/workflows/brand-review.md",
    "skills/workflows/trend-research.md",
    "skills/workflows/visual-inspiration.md",
]
for p in SKILL_FILES:
    FILES[p] = "# TODO: fill in this skill file\n"

# ── .gitkeep for otherwise-empty folders ─────────────────────────────────────
EMPTY_DIRS = [
    "app/(auth)",
    "agents/content-generation",
    "agents/brand-review",
    "agents/trend-research",
    "agents/visual-analysis",
    "api/analytics",
    "api/content",
    "api/trends",
    "api/files",
    "components",
    "hooks",
    "prompts/regression",
    "prompts/system",
    "supabase/migrations",
    "skills/brands/tencate-grass/regional",
]

# ── Write everything ──────────────────────────────────────────────────────────
for path, content in FILES.items():
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  wrote  {path}")

for d in EMPTY_DIRS:
    os.makedirs(d, exist_ok=True)
    gk = os.path.join(d, ".gitkeep")
    if not os.path.exists(gk):
        open(gk, "w").close()
    print(f"  dir    {d}/")

# ── Git ───────────────────────────────────────────────────────────────────────
import subprocess

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if r.stdout.strip():
        print(r.stdout.strip())
    if r.returncode != 0:
        print(f"ERROR: {r.stderr.strip()}")
        raise SystemExit(1)

run("git add .")
run('git commit -m "scaffold: Next.js 14 app with full folder structure and MCP stubs"')
run("git push -u origin main")
print("\nDone — scaffold pushed to GitHub.")
