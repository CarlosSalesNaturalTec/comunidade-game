import { chamarNucleo } from "comum/api";

export type TipoDeSolicitacao = "acesso" | "correcao" | "exclusao" | "esclarecimento";
export type SituacaoDaSolicitacao = "recebida" | "em_avaliacao" | "aceita" | "recusada";

export interface AbrirSolicitacaoSaida {
  id: string;
  prazo: string;
}

// Só o protocolo e o prazo que o núcleo devolveu — a tela nunca inventa
// nenhum dos dois (`RF-13-22`, `RF-13-24`).
export function abrirSolicitacao(
  guerreiroId: string,
  tipo: TipoDeSolicitacao,
  texto: string,
  token: string,
): Promise<AbrirSolicitacaoSaida> {
  return chamarNucleo<AbrirSolicitacaoSaida>("/v1/solicitacoes", {
    metodo: "POST",
    corpo: { guerreiro_id: guerreiroId, tipo, texto },
    token,
  });
}

export interface MinhaSolicitacao {
  id: string;
  guerreiro_id: string;
  tipo: TipoDeSolicitacao;
  texto: string;
  situacao: SituacaoDaSolicitacao;
  prazo: string;
  em_atraso: boolean;
  desfecho: string | null;
  tratado_em: string | null;
}

// Só as próprias, com o atraso já derivado pelo núcleo — a aplicação nunca
// calcula por conta própria (`RF-13-25`, `RF-13-26`, `RN-13-13`, `RN-13-14`).
export function listarMinhasSolicitacoes(token: string): Promise<MinhaSolicitacao[]> {
  return chamarNucleo<MinhaSolicitacao[]>("/v1/eu/solicitacoes", { token });
}
