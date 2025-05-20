/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      './templates/**/*.{html,js}',
      './visits/templates/**/*.{html,js}', // مسیر فایل‌های HTML و JS در اپلیکیشن Django
    ],
    darkMode: 'class',
    theme: {
      extend: {},
    },
    plugins: [],
  }