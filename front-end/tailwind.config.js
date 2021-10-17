module.exports = {
  purge: ["./src/**/*.vue"],
  darkMode: false,
  theme: {
    extend: {},
  },
  variants: {
    extend: {
      opacity: ["disabled"],
      cursor: ["disabled"],
      scale: ["group-hover"],
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
