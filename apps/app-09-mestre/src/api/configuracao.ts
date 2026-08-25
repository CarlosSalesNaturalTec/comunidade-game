// Chave de aplicação e client ID entram por variável de ambiente do Vite, uma
// por ambiente (documento 03, princípio 2; design — Decisions).
export const CHAVE_DE_APLICACAO = import.meta.env.VITE_CHAVE_DE_APLICACAO ?? "";
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";
export const URL_DO_NUCLEO = import.meta.env.VITE_URL_DO_NUCLEO ?? "";
// Endereço próprio da App 03, para o caminho até o painel do dia
// (`RF-09-50`, documento 03 §1: `gestao.comunidadegame.org`).
export const URL_DA_APP_03 = import.meta.env.VITE_URL_DA_APP_03 ?? "";
