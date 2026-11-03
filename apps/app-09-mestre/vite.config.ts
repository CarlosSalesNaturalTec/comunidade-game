/// <reference types="vitest/config" />

import path from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { provisionarFavicon } from "comum/marca/provisionamento";
import { defineConfig, type Plugin } from "vite";

// https://vite.dev/config/
// O favicon do projeto é arquivo único de `comum/marca/`, provisionado para
// `public/` em `dev` e em `build` — nunca uma cópia versionada por aplicação
// (change `2026-10-02-marca-do-projeto-e-silhueta-de-nivel`, design — decisão 5).
function faviconDoProjeto(): Plugin {
  return {
    name: "favicon-do-projeto",
    buildStart() {
      provisionarFavicon(path.join(path.dirname(fileURLToPath(import.meta.url)), "public"));
    },
  };
}

export default defineConfig({
  plugins: [react(), faviconDoProjeto()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/testes/configuracao.ts"],
    css: true,
    // Os `afterEach` rodam na ordem em que foram registrados, e não em
    // pilha: assim o `cleanup()` do `setupFiles` desmonta a tela **antes**
    // do `vi.restoreAllMocks()` de cada arquivo de teste. Em pilha, o
    // `restore` vinha primeiro e devolvia os espiões à função de verdade
    // com a árvore ainda montada — o efeito do rascunho do
    // `FormularioDeConteudo` relia `localStorage` nessa janela, já fora do
    // ambiente, e derrubava a esteira. Mesma correção da App 01.
    sequence: { hooks: "list" },
  },
});
