// Chave de aplicação e endereço do núcleo entram por variável de ambiente do
// Vite, uma por ambiente (documento 03, princípio 2; design — decisão 1). A
// vitrine **não** declara `VITE_GOOGLE_CLIENT_ID`: ela não autentica ninguém
// (`RN-03-27`, `RN-03-33`).
export const CHAVE_DE_APLICACAO = import.meta.env.VITE_CHAVE_DE_APLICACAO ?? "";
export const URL_DO_NUCLEO = import.meta.env.VITE_URL_DO_NUCLEO ?? "";

// Os seis destinos do "Entrar" (PRD-03 §5.9). O documento 03 §1.1 fixa os
// endereços, mas as esteiras de publicação usam hoje os `*.web.app` enquanto o
// domínio não passa no filtro da rede corporativa: gravá-los aqui quebraria em
// um dos dois ambientes (design — decisão 4). Vazio é caso previsto — a tela
// nomeia o destino em texto, sem link quebrado.
export const URL_DA_APP_01_AULA = import.meta.env.VITE_URL_DA_APP_01_AULA ?? "";
export const URL_DA_APP_03_GESTAO = import.meta.env.VITE_URL_DA_APP_03_GESTAO ?? "";
export const URL_DA_APP_05_GUERREIRO = import.meta.env.VITE_URL_DA_APP_05_GUERREIRO ?? "";
export const URL_DA_APP_07_RESPONSAVEL = import.meta.env.VITE_URL_DA_APP_07_RESPONSAVEL ?? "";
export const URL_DA_APP_08_APOIADOR = import.meta.env.VITE_URL_DA_APP_08_APOIADOR ?? "";
export const URL_DA_APP_09_MESTRE = import.meta.env.VITE_URL_DA_APP_09_MESTRE ?? "";
