// Chave de aplicação e client ID entram por variável de ambiente do Vite, uma
// por ambiente (documento 03, princípio 2; design — decisão 6). O client ID
// do Google serve a sessão assistida: o Mestre ou Admin presente se
// autentica para confirmar a identidade do Guerreiro(a) (`RF-05-03`,
// `RF-05-04`).
export const CHAVE_DE_APLICACAO = import.meta.env.VITE_CHAVE_DE_APLICACAO ?? "";
export const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID ?? "";
export const URL_DO_NUCLEO = import.meta.env.VITE_URL_DO_NUCLEO ?? "";

// O encerramento por inatividade é UX do aparelho compartilhado, distinto da
// duração do token no núcleo (`sessao_guerreiro_duracao`, sem rota de
// renovação nesta fatia): sem valor padrão no código, como toda duração de
// sessão do projeto (`RF-05-05`, `RF-05-71`, `RF-01-04`).
export const DURACAO_DE_INATIVIDADE_EM_MINUTOS = Number(
  import.meta.env.VITE_DURACAO_DE_INATIVIDADE_EM_MINUTOS,
);
