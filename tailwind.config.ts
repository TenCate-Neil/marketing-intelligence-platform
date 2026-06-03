import type { Config } from "tailwindcss";

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
