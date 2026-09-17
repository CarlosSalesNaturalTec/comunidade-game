/// <reference types="vitest/config" />

import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { provisionarModelosDeBiometria } from "comum/biometria/provisionamento";
import { defineConfig, type Plugin } from "vite";

const diretorioDoApp = path.dirname(fileURLToPath(import.meta.url));

// O especificador nu de `@vladmandic/human` resolve, pelas condições de
// `exports` do pacote, para o build `human.node.js` — que exige
// `@tensorflow/tfjs-node` nativo e nunca deveria ir para um bundle de
// navegador. O `alias` força o build ESM de navegador, tanto no `vite
// build` quanto no Vitest (design — decisão 5, primeira biblioteca de
// terceiro no navegador do repositório).
const requerer = createRequire(import.meta.url);
const humanEsm = path.join(
  path.dirname(requerer.resolve("@vladmandic/human")),
  "human.esm.js",
);

// Copia os modelos da Human para `public/`, tanto em `vite dev` quanto em
// `vite build` — sem isso, `comum/biometria` aponta para um
// `modelBasePath` que não existe (change
// `2026-09-17-correcao-de-aulas-canceladas-e-modelos-de-biometria`).
function modelosDeBiometria(): Plugin {
  return {
    name: "modelos-de-biometria",
    buildStart() {
      provisionarModelosDeBiometria(path.join(diretorioDoApp, "public/modelos-de-biometria"));
    },
  };
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), modelosDeBiometria()],
  resolve: {
    alias: {
      "@vladmandic/human": humanEsm,
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/testes/configuracao.ts"],
    css: true,
  },
});
