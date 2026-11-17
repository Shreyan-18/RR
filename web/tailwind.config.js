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
          pink: '#EA1A85',
          darkPink: '#C20E6B',
          lightPink: '#FF4DAB',
          blue: '#0A1931',
          darkBlue: '#001C58',
          deep: '#060B14',
          surface: '#0F1A2E',
          card: '#152238',
          border: '#1F314F',
          gold: '#D4AF37',
          cyan: '#00F5D4',
        },
      },
    },
  },
  plugins: [],
};
