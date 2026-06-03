// Image generation MCP client — abstracted so the underlying model can be swapped
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
