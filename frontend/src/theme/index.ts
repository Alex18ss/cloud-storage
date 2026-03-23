import { createSystem, defaultConfig, defineConfig, defineRecipe } from "@chakra-ui/react";

const inputRecipe = defineRecipe({
  variants: {
    variant: {
      auth: {
        color: "white",
        fontSize: "sm",
        bg: "transparent",
        border: "none",
        _focusVisible: { outline: "none" },
        _placeholder: { color: "whiteAlpha.400" },
      },
    },
  },
});

const config = defineConfig({
  globalCss: {
    "html, body": {
      margin: 0,
      padding: 0,
      minHeight: "100vh",
      fontFamily: "'Inter', sans-serif",
    },
  },
  theme: {
    tokens: {
      colors: {
        brand: {
          50: { value: "#e0f2ff" },
          100: { value: "#b3d9ff" },
          200: { value: "#80bfff" },
          300: { value: "#4da6ff" },
          400: { value: "#1a8cff" },
          500: { value: "#0073e6" },
          600: { value: "#005bb4" },
          700: { value: "#004282" },
          800: { value: "#002a51" },
          900: { value: "#001221" },
        },
      },
    },
    recipes: {
      input: inputRecipe,
    },
  },
});

export const system = createSystem(defaultConfig, config);
