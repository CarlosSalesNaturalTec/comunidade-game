/// <reference types="vitest/config" />

import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import react from "@vitejs/plugin-react";
import { provisionarModelosDeBiometria } from "comum/biometria/provisionamento";
import { provisionarFavicon } from "comum/marca/provisionamento";
import { defineConfig, type Plugin } from "vite";

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

const diretorioDoApp = path.dirname(fileURLToPath(import.meta.url));

// Copia os modelos da Human para `public/`, tanto em `vite dev` quanto em
// `vite build` — mesmo plugin da App 01 (change
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
    // `restore` vinha primeiro e devolvia os espiões à função de verdade
    // com a árvore ainda montada — medido aqui nas 136 ocorrências desta
    // aplicação, nenhuma em zero e a maior com 6.985 caracteres no ar.
    // Qualquer efeito que chegue nessa janela refaz a leitura sem os
    // espiões, e a rejeição solta derruba a esteira com a suíte verde.
    sequence: { hooks: "list" },
    // Sem valor padrão no código (design — decisão 3, `RF-05-05`): os testes
    // fornecem o parâmetro como a implantação forneceria.
    env: {
      VITE_DURACAO_DE_INATIVIDADE_EM_MINUTOS: "5",
    },
  },
});
