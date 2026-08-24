import type { Papel } from "comum/api";
import { chamarNucleo } from "comum/api";

interface AberturaDeSessao {
  token: string;
  expira_em: string;
  papel: Papel;
}

// Confirmação humana: o Mestre ou Admin em sessão de trabalho confere a
// identidade pelo nick que o Guerreiro(a) informou. O núcleo resolve o
// nick internamente e nunca devolve, nem exige, um identificador de
// persona — só abre a sessão ou recusa (`RF-04-29`, `RN-01-22`, design —
// decisão 1.1).
export function confirmarSessaoDeGuerreiro(
  nick: string,
  tokenDeTrabalho: string,
): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/guerreiro/confirmacao", {
    metodo: "POST",
    corpo: { nick },
    token: tokenDeTrabalho,
  });
}
