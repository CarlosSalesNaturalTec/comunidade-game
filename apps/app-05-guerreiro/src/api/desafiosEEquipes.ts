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

// As atividades em aberto do Guerreiro(a) em sessão — desbloqueadas, de
// trilha inscrita, sem Resultado lançado para ele. Conjunto vazio é "nada
// em aberto agora", nunca erro (`RF-05-19`, `RN-05-21`).
export function listarMeusDesafios(token: string): Promise<Desafio[]> {
  return chamarNucleo<Desafio[]>("/v1/eu/desafios", { token });
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
