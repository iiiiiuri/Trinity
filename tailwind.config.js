/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html',
    './**/*.js',
  ],
  theme: {
    extend: {
      backgroundImage: theme => ({
        'alpha': "url('/static/img/background.png')",
      }),
    },
  },
  variants: {
    extend: {
      fill: ['responsive', 'print'],
    },
  },
  plugins: [],
}

//npx tailwindcss -i ./src/input.css -o ./src/output.css --watch