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

interface AbrirSessaoPorReconhecimentoEntrada {
  nick: string;
  descritor: number[];
}

// Reconhecimento facial: nick digitado e descritor gerado no aparelho —
// só ele viaja, nunca a fotografia (`RN-04-12`). Pública quanto à
// persona — dispensa credencial, nunca a chave de aplicação (`RF-01-04`,
// `RF-01-05`) —, e a recusa não diferencia nick inexistente,
// Guerreiro(a) sem _template_ e descritor que não confere (`RN-01-22`).
export function abrirSessaoPorReconhecimento(
  entrada: AbrirSessaoPorReconhecimentoEntrada,
): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/guerreiro", {
    metodo: "POST",
    corpo: entrada,
  });
}
