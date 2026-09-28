/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_CHAVE_DE_APLICACAO: string;
  readonly VITE_URL_DO_NUCLEO: string;
  readonly VITE_URL_DA_APP_01_AULA: string;
  readonly VITE_URL_DA_APP_03_GESTAO: string;
  readonly VITE_URL_DA_APP_05_GUERREIRO: string;
  readonly VITE_URL_DA_APP_07_RESPONSAVEL: string;
  readonly VITE_URL_DA_APP_08_APOIADOR: string;
  readonly VITE_URL_DA_APP_09_MESTRE: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
