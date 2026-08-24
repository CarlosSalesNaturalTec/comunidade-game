// O token de sessão fica em `sessionStorage`: sobrevive ao recarregar a aba
// e morre quando ela fecha — o comportamento certo para um aparelho que
// pode ser compartilhado (design — Decisions). O papel nunca é guardado
// aqui: cada restauração relê o papel do núcleo por `GET /v1/eu`.
export const CHAVE_DE_ARMAZENAMENTO_PADRAO = "comunidade-game:token-de-sessao";

// A App 01 sustenta duas sessões vivas no mesmo aparelho — a de trabalho do
// Mestre ou Admin e a do Guerreiro(a) em atendimento —, cada uma sob sua
// própria chave de `sessionStorage`; as demais aplicações seguem usando a
// chave padrão, sem passar nada (openspec — esqueleto-da-aula-presencial-e-
// equipe-da-aula, design — decisão 1).
export function lerToken(chave: string = CHAVE_DE_ARMAZENAMENTO_PADRAO): string | null {
  return sessionStorage.getItem(chave);
}

export function gravarToken(
  token: string,
  chave: string = CHAVE_DE_ARMAZENAMENTO_PADRAO,
): void {
  sessionStorage.setItem(chave, token);
}

export function limparToken(chave: string = CHAVE_DE_ARMAZENAMENTO_PADRAO): void {
  sessionStorage.removeItem(chave);
}
