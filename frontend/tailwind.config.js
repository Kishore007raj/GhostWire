/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx}", "./public/index.html"],
  theme: {
    extend: {
      colors: {
        ghost: {
          900: '#0f172a', /* Deepest background */
          800: '#111827', /* Panel background */
          700: '#1e293b', /* Lighter panel / border */
          text: '#e5e7eb', /* Primary text */
          muted: '#94a3b8', /* Muted text */
          subtle: '#cbd5e1', /* Secondary text */
        },
        accent: {
          blue: '#3b82f6',
          amber: '#f59e0b',
          red: '#ef4444',
          green: '#22c55e',
        }
      },
      fontFamily: {
        sans: ['Inter', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', '"Liberation Mono"', '"Courier New"', 'monospace'],
      },
    },
  },
  plugins: [],
};
