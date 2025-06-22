/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./casestudies/templates/**/*.html",
    "./casestudies/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#4285f2',
      }
    },
  },
  plugins: [],
} 