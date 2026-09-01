// Chave de aplicação e client ID entram por variável de ambiente do Vite, uma
// por ambiente (documento 03, princípio 2; design — Decisions).
export const CHAVE_DE_APLICACAO = import.meta.env.VITE_CHAVE_DE_APLICACAO ?? "";
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";
export const URL_DO_NUCLEO = import.meta.env.VITE_URL_DO_NUCLEO ?? "";
// Vazia no Ciclo 01, até a App 06 existir; sem valor, a porta pública explica o
// caminho em texto, sem link quebrado (`RF-14-07`, design — decisão 7).
export const URL_DO_FORMULARIO_DA_VITRINE =
  import.meta.env.VITE_URL_DO_FORMULARIO_DA_VITRINE ?? "";
