/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './index.html',
  ],
  theme: {
    extend: {
      colors: {
        rr: {
          pink: '#E11D74',
          darkPink: '#B8145B',
          lightPink: '#F43F5E',
          glowPink: '#FB7185',
          blue: '#0F1A30',
          darkBlue: '#0A1224',
          obsidian: '#080D1A',
          surface: '#0E172A',
          card: '#131F37',
          cardHover: '#1A2A4A',
          border: '#1E2E4F',
          borderLight: '#2C426E',
          gold: '#EAB308',
          goldLight: '#FACC15',
          cyan: '#38BDF8',
          cyanGlow: '#7DD3FC',
        },
      },
    },
  },
  plugins: [],
};
