// Ayrshare MCP client — social analytics for LinkedIn, Instagram, Facebook, YouTube

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
