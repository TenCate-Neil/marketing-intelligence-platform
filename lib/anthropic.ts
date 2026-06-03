import Anthropic from "@anthropic-ai/sdk";

export const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY!,
});

export const MODELS = {
  generation: "claude-opus-4-8",
  review:     "claude-sonnet-4-6",
  research:   "claude-sonnet-4-6",
  visual:     "claude-sonnet-4-6",
} as const;
