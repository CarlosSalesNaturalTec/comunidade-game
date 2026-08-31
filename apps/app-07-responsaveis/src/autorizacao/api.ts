import { chamarNucleo } from "comum/api";

export type EstadoDaAutorizacao = "vigente" | "suspensa" | "nao_autorizada";
export type DecisaoDeAutorizacao = "concede" | "nega";

export interface QuemMotivouASuspensao {
  responsavel_id: string;
  decidido_em: string;
}

export interface ItemDoHistoricoDaAutorizacao {
  id: string;
  responsavel_id: string;
  decisao: DecisaoDeAutorizacao;
  versao_do_termo: string;
  origem: "propria" | "assistida" | "impressa";
  registrado_em: string;
}

export interface Autorizacao {
  estado: EstadoDaAutorizacao;
  suspensa_por: QuemMotivouASuspensao | null;
  historico: ItemDoHistoricoDaAutorizacao[];
}

// O estado derivado, quem motivou a suspensão e o histórico, numa só
// chamada (`RF-13-18`, `RF-13-21`).
export function lerAutorizacao(guerreiroId: string, token: string): Promise<Autorizacao> {
  return chamarNucleo<Autorizacao>(`/v1/eu/guerreiros/${guerreiroId}/autorizacao`, { token });
}

export interface DecisaoDeAutorizacaoSaida {
  id: string;
  decisao: DecisaoDeAutorizacao;
  registrado_em: string;
  estado: EstadoDaAutorizacao;
}

// A versão do termo é carimbada pelo núcleo; a chamada nunca a envia
// (`RF-13-14`, `RF-13-15`, design — decisão 2).
export function decidirAutorizacao(
  guerreiroId: string,
  decisao: DecisaoDeAutorizacao,
  token: string,
): Promise<DecisaoDeAutorizacaoSaida> {
  return chamarNucleo<DecisaoDeAutorizacaoSaida>(
    `/v1/eu/guerreiros/${guerreiroId}/autorizacao`,
    {
      metodo: "POST",
      corpo: { decisao },
      token,
    },
  );
}
