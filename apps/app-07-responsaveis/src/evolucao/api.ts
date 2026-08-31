import { chamarNucleo } from "comum/api";

export type DesfechoDoResultado =
  | "realizada"
  | "realizada_com_merito"
  | "merito_extra_por_auxilio";

export interface ItemDePresenca {
  aula_id: string;
  momento_do_fato: string;
}

export interface ItemDeAtividadeRealizada {
  atividade_id: string;
  atividade_titulo: string;
  desfecho: DesfechoDoResultado;
  momento_do_fato: string;
}

export interface ProgressoDaTrilha {
  trilha_id: string;
  trilha_nome: string;
  nivel_atual: number | null;
  obrigatorias_desbloqueadas: number;
  obrigatorias_totais: number;
  pontos_regulares: number;
  badges: string[];
}

export interface ItemDePontosPorPoder {
  poder_id: string;
  poder_nome: string;
  total: number;
}

export interface ItemDeCriacaoValidada {
  trilha_id: string;
  trilha_titulo: string;
  validado_em: string;
}

export interface EvolucaoDoGuerreiro {
  presencas: ItemDePresenca[];
  atividades: ItemDeAtividadeRealizada[];
  trilhas: ProgressoDaTrilha[];
  pontos_por_poder: ItemDePontosPorPoder[];
  criacoes_validadas: ItemDeCriacaoValidada[];
}

export interface OcorrenciaDaEvolucao {
  id: string;
  motivo: string | null;
  momento_do_fato: string;
}

// Payload consolidado numa só chamada, como o PRD-13 §9 declara — nunca
// sete chamadas para montar uma tela (`RF-13-07`, `RF-13-08`, `RF-13-10`).
export function obterEvolucao(
  guerreiroId: string,
  token: string,
): Promise<EvolucaoDoGuerreiro> {
  return chamarNucleo<EvolucaoDoGuerreiro>(`/v1/eu/guerreiros/${guerreiroId}/evolucao`, {
    token,
  });
}

// As ocorrências de conduta, separadas: o motivo vem `null` quando o
// expurgo do ciclo já o apagou (`RF-13-09`, `RN-13-21`).
export function listarOcorrencias(
  guerreiroId: string,
  token: string,
): Promise<OcorrenciaDaEvolucao[]> {
  return chamarNucleo<OcorrenciaDaEvolucao[]>(`/v1/eu/guerreiros/${guerreiroId}/ocorrencias`, {
    token,
  });
}
