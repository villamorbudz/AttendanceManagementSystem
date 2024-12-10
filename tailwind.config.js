/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './AMSystem/**/*.html',
    './AMSystem/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'coral': '#EE6C4D',
        'coral-dark': '#D85C3D',
        'coral-light': '#FF8D70',
        'navy': '#293241',
        'navy-light': '#3D4B63',
        'blue': '#3D5A80',
        'blue-light': '#5B7BA8',
        'lightblue': '#98C1D9',
        'ice': '#E0FBFC',
        'gray': {
          850: '#1B2433',
          950: '#0A0F17'
        }
      },
      boxShadow: {
        'inner-top': 'inset 0 2px 4px 0 rgba(0, 0, 0, 0.06)',
        'glow': '0 0 15px rgba(238, 108, 77, 0.5)',
        'glow-light': '0 0 15px rgba(152, 193, 217, 0.5)'
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-in': 'slideIn 0.3s ease-in-out'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideIn: {
          '0%': { transform: 'translateX(-10px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' }
        }
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    require('daisyui'),
  ],
}
