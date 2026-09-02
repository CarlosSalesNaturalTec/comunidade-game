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
  parecer_do_mestre: string | null;
  motivo_da_recusa: string | null;
  lastro_provido: boolean;
  lastro_faltante: string | null;
}

// Os desafios em validação das trilhas de que o Mestre em sessão é autor —
// nunca de trilha alheia (`RF-09-51`, `RN-09-11`).
export function listarFilaDeValidacao(token: string): Promise<DesafioExtra[]> {
  return chamarNucleo<DesafioExtra[]>("/v1/desafios-extras/a-validar", { token });
}

// Um só ato, com o desfecho no corpo: `parecer` leva à aprovação do Admin,
// `motivo` leva a recusado, sem passar por ela (`RF-09-51`, `RF-09-52`).
export function validarDesafioExtra(
  idDoDesafio: string,
  parecer: string,
  token: string,
): Promise<DesafioExtra> {
  return chamarNucleo<DesafioExtra>(`/v1/desafios-extras/${idDoDesafio}/validacao`, {
    metodo: "POST",
    corpo: { situacao: "em_aprovacao_do_admin", parecer },
    token,
  });
}

export function recusarDesafioExtraPeloMestre(
  idDoDesafio: string,
  motivo: string,
  token: string,
): Promise<DesafioExtra> {
  return chamarNucleo<DesafioExtra>(`/v1/desafios-extras/${idDoDesafio}/validacao`, {
    metodo: "POST",
    corpo: { situacao: "recusado", motivo },
    token,
  });
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

// O Mestre propõe pela mesma rota do Apoiador — a situação de nascimento
// depende de ele ser ou não o autor da trilha, decidida no núcleo
// (`RF-09-105` a `RF-09-109`).
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

// Só os desafios do próprio Mestre, com a situação, o parecer e o motivo
// da recusa quando houver (`RF-09-105`, `RF-09-112`).
export function listarMeusDesafiosExtras(token: string): Promise<DesafioExtra[]> {
  return chamarNucleo<DesafioExtra[]>("/v1/eu/desafios-extras", { token });
}
