import { chamarNucleo } from "comum/api";

export interface RecursoFaltante {
  tipo_de_recurso_id: string;
  quantidade_declarada: string;
  quantidade_disponivel: string;
}

export interface AulaDaTurma {
  id: string;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
  situacao: string;
  cancelamento_motivo: string | null;
  recursos_faltantes: RecursoFaltante[];
}

export type FormatoDaAtividade = "presencial" | "on_line_assincrona";

export interface AtividadeDoMestre {
  id: string;
  missao_id: string;
  titulo: string;
  formato: FormatoDaAtividade;
  modalidade: string;
}

export interface MinhasTurmas {
  itens: AulaDaTurma[];
  proximo_cursor: string | null;
  atividades_presenciais: AtividadeDoMestre[];
  atividades_on_line: AtividadeDoMestre[];
}

// Aulas das comunidades do Mestre em sessão e as atividades de que é autor,
// já separadas por formato — presencial do encontro e on-line entre
// encontros (`RF-09-42`, `RF-09-73`).
export function listarMinhasTurmas(token: string): Promise<MinhasTurmas> {
  return chamarNucleo<MinhasTurmas>("/v1/minhas-turmas", { token });
}

export type DesfechoDoResultado =
  | "realizada"
  | "realizada_com_merito"
  | "merito_extra_por_auxilio";

export interface ParticipanteDoLancamento {
  guerreiro_id: string;
  momento_do_fato: string;
  producao: string;
  desfecho: DesfechoDoResultado;
}

export interface Resultado {
  id: string;
  guerreiro_id: string;
  atividade_id: string;
  aula_id: string;
  momento_do_fato: string;
  producao: string;
  desfecho: string;
}

// A equipe inteira num só envio — o Mestre autor lança a atividade que
// propôs, sem consumir reserva nem mudar a situação da aula
// (`RF-09-43`, `RF-09-44`, `RF-09-74`).
export function lancarResultadosDaAtividade(
  idDaAtividade: string,
  aulaId: string,
  participantes: ParticipanteDoLancamento[],
  token: string,
): Promise<Resultado[]> {
  return chamarNucleo<Resultado[]>(`/v1/atividades/${idDaAtividade}/lancamentos`, {
    metodo: "POST",
    corpo: { aula_id: aulaId, participantes },
    token,
  });
}

export interface Presenca {
  id: string;
  aula_id: string;
  guerreiro_id: string;
  modo: string;
  confirmador_id: string | null;
  momento_do_fato: string;
}

// Só o modo confirmação alcança o Mestre — o reconhecimento continua
// exclusivo do App 01 (`RF-09-45`).
export function confirmarPresenca(
  idDaAula: string,
  guerreiroId: string,
  momentoDoFato: string,
  token: string,
): Promise<Presenca> {
  return chamarNucleo<Presenca>(`/v1/aulas/${idDaAula}/presencas`, {
    metodo: "POST",
    corpo: { guerreiro_id: guerreiroId, modo: "confirmacao", momento_do_fato: momentoDoFato },
    token,
  });
}

export interface OcorrenciaDeConduta {
  id: string;
  guerreiro_id: string;
  aula_id: string;
  atividade_id: string;
  valor: number;
  motivo: string | null;
  momento_do_fato: string;
}

// O valor nunca é enviado — é fixo no núcleo — e o lançamento já vale no
// ato, sem revisão de outro Admin (`RF-09-46`, `RN-09-09`).
export function lancarOcorrenciaDeConduta(
  guerreiroId: string,
  aulaId: string,
  atividadeId: string,
  motivo: string,
  momentoDoFato: string,
  token: string,
): Promise<OcorrenciaDeConduta> {
  return chamarNucleo<OcorrenciaDeConduta>("/v1/ocorrencias-de-conduta", {
    metodo: "POST",
    corpo: {
      guerreiro_id: guerreiroId,
      aula_id: aulaId,
      atividade_id: atividadeId,
      motivo,
      momento_do_fato: momentoDoFato,
    },
    token,
  });
}
