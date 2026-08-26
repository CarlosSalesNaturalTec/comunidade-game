import type { Papel } from "comum/api";
import { chamarNucleo } from "comum/api";

interface AberturaDeSessao {
  token: string;
  expira_em: string;
  papel: Papel;
}

// Confirmação humana: o Mestre ou Admin presente, autenticado só para este
// ato, confere a identidade pelo nick que o Guerreiro(a) informou. O núcleo
// resolve o nick internamente e nunca devolve, nem exige, um identificador
// de persona — só abre a sessão ou recusa (`RF-05-03`, `RF-05-04`,
// `RN-01-22`).
export function confirmarSessaoDeGuerreiro(
  nick: string,
  tokenDoAdulto: string,
): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/guerreiro/confirmacao", {
    metodo: "POST",
    corpo: { nick },
    token: tokenDoAdulto,
  });
}

interface AbrirSessaoPorReconhecimentoEntrada {
  nick: string;
  descritor: number[];
}

// Reconhecimento facial: nick digitado e descritor gerado no aparelho — só
// ele viaja, nunca a fotografia (`RF-05-01`, `RN-05-01`). Pública quanto à
// persona — dispensa credencial, nunca a chave de aplicação —, e a recusa
// não diferencia nick inexistente, Guerreiro(a) sem _template_ e descritor
// que não confere (`RN-01-22`).
export function abrirSessaoPorReconhecimento(
  entrada: AbrirSessaoPorReconhecimentoEntrada,
): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/guerreiro", {
    metodo: "POST",
    corpo: entrada,
  });
}
