import { chamarNucleo } from "comum/api";

export interface AtividadeDoDesafio {
  id: string;
  missao_id: string;
  titulo: string;
  descricao: string | null;
  modalidade: string;
  formato: string;
  natureza: string;
  producao_esperada: string;
  aula_id: string | null;
}

export interface Desafio {
  atividade: AtividadeDoDesafio;
  missao_id: string;
  missao_titulo: string;
  trilha_id: string;
  trilha_titulo: string;
}

export interface RecompensaDoDesafioExtra {
  tipo_de_recurso_nome: string;
  ponto_de_apoio_nome: string;
}

export interface DesafioExtraDoGuerreiro {
  id: string;
  trilha_id: string;
  trilha_nome: string;
  missao_id: string | null;
  missao_titulo: string | null;
  modalidade: string;
  formato: string;
  criterio_de_atribuicao: string;
  pontos_extras: number;
  recompensa: RecompensaDoDesafioExtra;
  quantidade_disponivel: number;
  quantidade_restante: number;
  vigencia_inicio: string;
  vigencia_fim: string;
}

export interface MeusDesafios {
  semanais: Desafio[];
  extras: DesafioExtraDoGuerreiro[];
}

// Os dois conjuntos em aberto do Guerreiro(a) em sessão — os semanais,
// desbloqueados, de trilha inscrita e sem Resultado lançado para ele, e os
// extras, publicados, vigentes e elegíveis a ele. Sem nada em aberto, os
// dois conjuntos vazios, nunca erro (`RF-05-19`, `RF-05-20`, `RN-05-21`).
export function listarMeusDesafios(token: string): Promise<MeusDesafios> {
  return chamarNucleo<MeusDesafios>("/v1/eu/desafios", { token });
}

export interface IntegranteDaMinhaEquipe {
  avatar: string | null;
  nick: string;
  papel: string | null;
}

export interface ItemDaProgramacaoDaMinhaEquipe {
  atividade: AtividadeDoDesafio;
  missao_id: string;
  missao_titulo: string;
  trilha_id: string;
  trilha_titulo: string;
  corrente: boolean;
}

export interface MinhaEquipe {
  id: string;
  aula_id: string | null;
  trilha_id: string | null;
  meu_papel: string | null;
  integrantes: IntegranteDaMinhaEquipe[];
  atividades: ItemDaProgramacaoDaMinhaEquipe[];
}

// As equipes de que o Guerreiro(a) em sessão participa — da aula e da
// trilha —, cada uma com o papel dele nela e as atividades dela. Nenhuma
// escrita nasce daqui: formar, entrar, sair e homologar seguem no App 01 e
// na App 09 (`RF-05-22`, `RF-05-23`, `RF-05-24`, `RN-05-12`, `RN-05-15`).
export function listarMinhasEquipes(token: string): Promise<MinhaEquipe[]> {
  return chamarNucleo<MinhaEquipe[]>("/v1/eu/equipes", { token });
}
