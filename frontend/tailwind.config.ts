import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          purple: "#6C3CE1",
          purpleLight: "#8B5FE8"
        },
        accent: {
          orange: "#FF6B35",
          coral: "#FF5C5C",
          green: "#22C55E",
          yellow: "#FACC15"
        },
        ink: {
          primary: "#1A1A2E",
          secondary: "#4A4A6A",
          muted: "#9CA3AF"
        },
        surface: {
          white: "#FFFFFF",
          offWhite: "#F8F9FA",
          lightGray: "#F1F3F5",
          purpleTint: "#F3F0FF",
          peachTint: "#FFF3EE",
          graySection: "#F5F5FA",
          darkFooter: "#1A1A2E"
        },
        border: {
          default: "#E5E7EB"
        }
      },
      fontFamily: {
        sans: ["var(--font-inter)", "sans-serif"]
      },
      boxShadow: {
        card: "0 2px 8px rgba(0,0,0,0.06)",
        lift: "0 8px 24px rgba(0,0,0,0.1)",
        button: "0 4px 12px rgba(108,60,225,0.3)"
      },
      borderRadius: {
        xl: "16px",
        "2xl": "20px"
      }
    }
  },
  plugins: []
};

export default config;
