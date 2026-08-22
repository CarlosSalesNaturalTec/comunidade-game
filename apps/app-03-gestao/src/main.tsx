import { configurarAcessoAoNucleo } from "comum/api";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { CHAVE_DE_APLICACAO, URL_DO_NUCLEO } from "./api/configuracao";
import "./index.css";

// Chamado uma vez, antes de renderizar: toda chamada ao núcleo depois disso
// leva a chave e a URL desta aplicação (design — decisão 6).
configurarAcessoAoNucleo({ chaveDeAplicacao: CHAVE_DE_APLICACAO, urlDoNucleo: URL_DO_NUCLEO });

// biome-ignore lint/style/noNonNullAssertion: o `#root` é o próprio contrato de `index.html`
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
