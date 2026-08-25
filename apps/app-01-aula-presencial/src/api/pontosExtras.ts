import { chamarNucleo } from "comum/api";

export interface PontosExtras {
  acumulado: number;
  saldo_disponivel: number;
}

// Sempre com o token do Guerreiro(a) — a rota devolve as contas de quem
// está em sessão e não recebe identificador de persona; o token de
// trabalho nunca assina esta leitura (`RF-04-51`, design — decisão 4).
export function consultarMeusPontosExtras(tokenDoGuerreiro: string): Promise<PontosExtras> {
  return chamarNucleo<PontosExtras>("/v1/eu/pontos-extras", { token: tokenDoGuerreiro });
}
