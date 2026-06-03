// Tavily MCP client — web search for the Trend Research Agent

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
