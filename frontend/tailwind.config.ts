import type { Config } from "tailwindcss";

// Colours are driven by CSS variables defined in globals.css so the whole app
// shares one token system. The palette: near-white "paper", ink text, a single
// deep indigo signal accent, and a semantic trio for review confidence.
const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        paper: "var(--paper)",
        surface: "var(--surface)",
        ink: "var(--ink)",
        muted: "var(--muted)",
        line: "var(--line)",
        accent: "var(--accent)",
        "status-ok": "var(--status-ok)",
        "status-warn": "var(--status-warn)",
        "status-risk": "var(--status-risk)",
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "monospace"],
      },
      borderRadius: {
        card: "10px",
      },
    },
  },
  plugins: [],
};

export default config;
