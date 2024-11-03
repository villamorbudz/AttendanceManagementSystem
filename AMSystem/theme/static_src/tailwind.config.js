/**
<<<<<<< HEAD
 * This is a minimal config for Tailwind CSS.
=======
 * This is a minimal config.
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
<<<<<<< HEAD
  darkMode: "class", // Enable dark mode via a class
  content: [
    // HTML templates
    "../templates/**/*.html",
    "../../templates/**/*.html",
    "../../**/templates/**/*.html", // Uncomment below if using Tailwind CSS in JS or Python // '!../../**/node_modules', // '../../**/*.js', // '../../**/*.py'
  ],
  theme: {
    extend: {
      animation: {
        blob: "blob 7s infinite",
      },
      keyframes: {
        blob: {
          "0%": {
            transform: "translate(0px, 0px) scale(1)",
          },
          "33%": {
            transform: "translate(30px, -50px) scale(2.2)",
          },
          "66%": {
            transform: "translate(-20px, 20px) scale(0.9)",
          },
          "100%": {
            transform: "translate(0px, 0px) scale(1)",
          },
        },
      },
      colors: {
        primary: {
          50: "#EE6C4D", // Light shade
          100: "#FF5733", // Medium shade
          200: "#FF3333", // Darker shade
          300: "#FF0000", // Bright Red
        },
      },
    },
  },
  variants: {
    extend: {
      // Add any specific variants you need
    },
  },
  plugins: [
    require("@tailwindcss/forms"), // Forms plugin
    require("@tailwindcss/typography"), // Typography plugin
    require("@tailwindcss/aspect-ratio"), // Aspect ratio plugin
    require("daisyui"), // DaisyUI plugin
  ],
  daisyui: {
    themes: [
      "light",
      "dark",
      "cupcake",
      "bumblebee",
      "emerald",
      "corporate",
      "synthwave",
      "retro",
      "cyberpunk",
      "valentine",
      "halloween",
      "garden",
      "forest",
      "aqua",
      "lofi",
      "pastel",
      "fantasy",
      "wireframe",
      "black",
      "luxury",
      "dracula",
      "cmyk",
      "autumn",
      "business",
      "acid",
      "lemonade",
      "night",
      "coffee",
      "winter",
      "dim",
      "nord",
      "sunset",
    ],
    darkTheme: "dark", // Set the default dark theme
    base: true, // Applies background color and foreground color for root element
    styled: true, // Include DaisyUI colors and design decisions for all components
    utils: true, // Adds responsive and modifier utility classes
    prefix: "", // Prefix for DaisyUI class names
    logs: true, // Shows info about DaisyUI version and used config in the console
    themeRoot: ":root", // The element that receives theme color CSS variables
  },
=======
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        // '!../../**/node_modules',
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            animation: {
                blob: "blob 7s infinite",
            },
            keyframes: {
                blob: {
                    "0%": {
                        transform: "translate(0px, 0px) scale(1)",
                    },
                    "33%": {
                        transform: "translate(30px, -50px) scale(2.2)",
                    },
                    "66%": {
                        transform: "translate(-20px, 20px) scale(0.9)",
                    },
                    "100%": {
                        transform: "translate(0px, 0px) scale(1)",
                    },
                },
            },
            
            colors:{
                primary: {
                    50: '#EE6C4D',
                    100: 'orange',
                }            
            
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have your own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('daisyui'),
    ],
>>>>>>> 43e58055dc4f399f298c567cdd630f3f495d2045
};
