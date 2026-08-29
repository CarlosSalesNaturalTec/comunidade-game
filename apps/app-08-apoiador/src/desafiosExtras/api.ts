import { chamarNucleo } from "comum/api";

export type Modalidade = "aberto" | "direcionado";
export type FormatoDoDesafioExtra = "presencial" | "on_line";
export type CusteioDoDesafioExtra = "aporte_do_proponente" | "saldo_de_recurso";
export type SituacaoDoDesafioExtra =
  | "em_validacao_do_mestre"
  | "em_aprovacao_do_admin"
  | "publicado"
  | "recusado";

export interface DesafioExtra {
  id: string;
  trilha_id: string;
  missao_id: string | null;
  modalidade: Modalidade;
  nick_do_destinatario: string | null;
  justificativa_do_vinculo: string | null;
  tipo_de_recurso_id: string;
  ponto_de_apoio_id: string;
  quantidade_disponivel: number;
  quantidade_restante: number;
  criterio_de_atribuicao: string;
  pontos_extras: number;
  formato: FormatoDoDesafioExtra;
  custeio: CusteioDoDesafioExtra;
  aporte_id: string | null;
  vigencia_inicio: string;
  vigencia_fim: string;
  situacao: SituacaoDoDesafioExtra;
  motivo_da_recusa: string | null;
  lastro_provido: boolean;
  lastro_faltante: string | null;
}

export interface ProporDesafioExtraEntrada {
  trilha_id: string;
  missao_id?: string | null;
  modalidade: Modalidade;
  nick_do_destinatario?: string | null;
  justificativa_do_vinculo?: string | null;
  tipo_de_recurso_id: string;
  ponto_de_apoio_id: string;
  quantidade_disponivel: number;
  criterio_de_atribuicao: string;
  pontos_extras: number;
  formato: FormatoDoDesafioExtra;
  custeio: CusteioDoDesafioExtra;
  aporte_id?: string | null;
  vigencia_inicio: string;
  vigencia_fim: string;
}

// O Apoiador propõe o desafio extra sobre uma trilha em andamento (`RF-14-29`
// a `RF-14-34`, `RF-14-74` a `RF-14-76`).
export function proporDesafioExtra(
  entrada: ProporDesafioExtraEntrada,
  token: string,
): Promise<DesafioExtra> {
  return chamarNucleo<DesafioExtra>("/v1/desafios-extras", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Só os desafios do próprio proponente, com a situação, o motivo da recusa
// e o que falta de lastro (`RF-14-35` a `RF-14-39`).
export function listarMeusDesafiosExtras(token: string): Promise<DesafioExtra[]> {
  return chamarNucleo<DesafioExtra[]>("/v1/eu/desafios-extras", { token });
}
