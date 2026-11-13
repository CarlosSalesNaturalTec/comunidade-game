import { chamarNucleo } from "../api/cliente";

export type ContaDoLancamento = "regular" | "extra";

export type OrigemDoLancamento =
  | "resultado"
  | "merito_do_resultado"
  | "criacao_original"
  | "partida_de_quiz"
  | "registro_de_coleta"
  | "estorno_de_coleta"
  | "desafio_pratico"
  | "ocorrencia_de_conduta"
  | "presenca"
  | "estorno_de_presenca"
  | "cuidado_do_bem"
  | "proposta_adotada"
  | "troca"
  | "saldo_anterior";

export interface LancamentoDePontuacao {
  id: string;
  registrado_em: string;
  conta: ContaDoLancamento;
  origem: OrigemDoLancamento;
  valor: number;
  valor_no_acumulado: number | null;
  trilha_id: string | null;
  poder_id: string | null;
  nome_da_trilha_ou_poder: string | null;
  detalhe: string | null;
  motivo: string | null;
}

export interface SaldoRegular {
  trilha_id: string | null;
  poder_id: string | null;
  nome: string;
  total: number;
}

export interface HistoricoDePontuacao {
  saldos: {
    regular: SaldoRegular[];
    extra: { acumulado: number; saldo_disponivel: number };
  };
  itens: LancamentoDePontuacao[];
  proximo_cursor: string | null;
}

/** Uma página do histórico; `cursor` nulo é a primeira (`RF-01-89`). */
export type LerHistorico = (cursor: string | null) => Promise<HistoricoDePontuacao>;

function comCursor(caminho: string, cursor: string | null): string {
  return cursor ? `${caminho}?cursor=${encodeURIComponent(cursor)}` : caminho;
}

// O próprio Guerreiro(a), sem identificador de persona (`RF-05-104`).
export function lerMeuHistoricoDePontuacao(
  token: string,
  cursor: string | null,
): Promise<HistoricoDePontuacao> {
  return chamarNucleo<HistoricoDePontuacao>(
    comCursor("/v1/eu/historico-de-pontuacao", cursor),
    { token },
  );
}

// O Mestre do vínculo e o Admin, pelo identificador (`RF-09-144`, `RF-02-116`).
export function lerHistoricoDePontuacaoDoGuerreiro(
  token: string,
  guerreiroId: string,
  cursor: string | null,
): Promise<HistoricoDePontuacao> {
  return chamarNucleo<HistoricoDePontuacao>(
    comCursor(`/v1/guerreiros/${guerreiroId}/historico-de-pontuacao`, cursor),
    { token },
  );
}
