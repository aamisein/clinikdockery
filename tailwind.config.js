/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.{html,js}',
      './visits/templates/**/*.{html,js}', // مسیر فایل‌های HTML و JS در اپلیکیشن Django
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  }