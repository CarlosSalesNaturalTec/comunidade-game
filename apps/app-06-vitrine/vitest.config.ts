/// <reference types="vitest/config" />

import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// O Vitest fica em arquivo próprio, como em `comum/`: o `astro.config.mjs`
// governa o build, e os testes de ilha continuam sendo React sobre jsdom.
export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/testes/configuracao.ts"],
    css: true,
  },
});
