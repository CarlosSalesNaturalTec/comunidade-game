/// <reference types="vitest/config" />

import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { provisionarModelosDeBiometria } from "comum/biometria/provisionamento";
import { provisionarFavicon } from "comum/marca/provisionamento";
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
  plugins: [react(), modelosDeBiometria(), faviconDoProjeto()],
  resolve: {
    alias: {
      "@vladmandic/human": humanEsm,
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: ["./src/testes/configuracao.ts"],
    css: true,
    // Os `afterEach` rodam na ordem em que foram registrados, e não em
    // pilha: assim o `cleanup()` do `setupFiles` desmonta a tela **antes**
    // do `vi.restoreAllMocks()` de cada arquivo de teste. Em pilha, o
    // `restore` vinha primeiro e devolvia o cliente do núcleo à função de
    // verdade com a árvore ainda montada — qualquer atualização de estado
    // nessa janela refazia a leitura sem `configurarAcessoAoNucleo`, e a
    // rejeição solta derrubava a esteira com a suíte toda verde.
    sequence: { hooks: "list" },
  },
});
