/**
 * This is a minimal config for Tailwind CSS.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
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
};
