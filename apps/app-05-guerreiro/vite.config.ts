/// <reference types="vitest/config" />

import { createRequire } from "node:module";
import path from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// O especificador nu de `@vladmandic/human` resolve, pelas condições de
// `exports` do pacote, para o build `human.node.js` — que exige
// `@tensorflow/tfjs-node` nativo e nunca deveria ir para um bundle de
// navegador. O `alias` força o build ESM de navegador, tanto no `vite
// build` quanto no Vitest — replicado da App 01, porque o Vite não
// compartilha configuração entre aplicações (design — decisão 1, tarefa
// 2.2).
const requerer = createRequire(import.meta.url);
const humanEsm = path.join(
  path.dirname(requerer.resolve("@vladmandic/human")),
  "human.esm.js",
);

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@vladmandic/human": humanEsm,
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/testes/configuracao.ts"],
    css: true,
    // Sem valor padrão no código (design — decisão 3, `RF-05-05`): os testes
    // fornecem o parâmetro como a implantação forneceria.
    env: {
      VITE_DURACAO_DE_INATIVIDADE_EM_MINUTOS: "5",
    },
  },
});
