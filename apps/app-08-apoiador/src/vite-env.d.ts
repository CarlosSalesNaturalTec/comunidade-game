/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CHAVE_DE_APLICACAO: string;
  readonly VITE_GOOGLE_CLIENT_ID: string;
  readonly VITE_URL_DO_NUCLEO: string;
  readonly VITE_URL_DO_FORMULARIO_DA_VITRINE: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
