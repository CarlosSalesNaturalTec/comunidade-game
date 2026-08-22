// O token de sessão fica em `sessionStorage`: sobrevive ao recarregar a aba
// e morre quando ela fecha — o comportamento certo para um aparelho que
// pode ser compartilhado (design — Decisions). O papel nunca é guardado
// aqui: cada restauração relê o papel do núcleo por `GET /v1/eu`.
const CHAVE_DE_ARMAZENAMENTO = "comunidade-game:token-de-sessao";

export function lerToken(): string | null {
  return sessionStorage.getItem(CHAVE_DE_ARMAZENAMENTO);
}

export function gravarToken(token: string): void {
  sessionStorage.setItem(CHAVE_DE_ARMAZENAMENTO, token);
}

export function limparToken(): void {
  sessionStorage.removeItem(CHAVE_DE_ARMAZENAMENTO);
}
