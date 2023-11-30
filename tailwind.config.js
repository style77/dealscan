/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './accounts/templates/**/*.html',
      './dealscan/templates/**/*.html',
      './crawler/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#b5e48c',  // https://coolors.co/palette/d9ed92-b5e48c-99d98c-76c893-52b69a-34a0a4-168aad-1a759f-1e6091-184e77
        'secondary': '#76c893'
      }
    },
  },
  safelist: [
    'px-3.5',

  ],
  plugins: [],
}
