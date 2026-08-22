import { chamarNucleo } from "comum/api";

export type EtapaDoCiclo = "abertura" | "desenvolvimento" | "marcos" | "fechamento";

export interface AtividadeDaMissao {
  id: string;
  missao_id: string;
  titulo: string;
  descricao: string | null;
  modalidade: string;
  formato: string;
  natureza: string;
  producao_esperada: string;
}

export interface MissaoDaTrilha {
  id: string;
  trilha_id: string;
  titulo: string;
  posicao: number;
  nivel_de_dificuldade: number;
  obrigatoria: boolean;
  e_sondagem: boolean;
  etapa_do_ciclo: EtapaDoCiclo;
  cadencia_de_retomada: number[] | null;
  atividades: AtividadeDaMissao[];
}

export interface TrilhaDaLista {
  id: string;
  nome: string;
  objetivo: string;
  area_do_conhecimento: string;
  poder_id: string;
  situacao: string;
}

export interface TrilhaDoMestre extends TrilhaDaLista {
  missoes: MissaoDaTrilha[];
}

// `GET /trilhas/minhas` já traz missões e atividades aninhadas — o PRD-09
// §9 não declara rota própria para nenhuma das duas (design — decisão 2).
export function listarMinhasTrilhas(token: string): Promise<TrilhaDoMestre[]> {
  return chamarNucleo<TrilhaDoMestre[]>("/v1/trilhas/minhas", { token });
}

export interface CriarTrilhaEntrada {
  nome: string;
  objetivo: string;
  area_do_conhecimento: string;
  poder_id: string;
}

export function criarTrilha(
  entrada: CriarTrilhaEntrada,
  token: string,
): Promise<TrilhaDaLista> {
  return chamarNucleo<TrilhaDaLista>("/v1/trilhas", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface CriarMissaoEntrada {
  titulo: string;
  posicao: number;
  nivel_de_dificuldade: number;
  obrigatoria: boolean;
  etapa_do_ciclo: EtapaDoCiclo;
  e_sondagem?: boolean;
}

export function criarMissao(
  idDaTrilha: string,
  entrada: CriarMissaoEntrada,
  token: string,
): Promise<MissaoDaTrilha> {
  return chamarNucleo<MissaoDaTrilha>(`/v1/trilhas/${idDaTrilha}/missoes`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface CriarAtividadeEntrada {
  titulo: string;
  descricao?: string;
  modalidade: string;
  formato: string;
  natureza: string;
  producao_esperada: string;
}

export function criarAtividade(
  idDaMissao: string,
  entrada: CriarAtividadeEntrada,
  token: string,
): Promise<AtividadeDaMissao> {
  return chamarNucleo<AtividadeDaMissao>(`/v1/missoes/${idDaMissao}/atividades`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// `cadenciaDeRetomada` nulo deixa a missão sem retomada — o caminho que
// `RF-09-83` exige preservar (design — decisão 4).
export function declararCadenciaDeRetomada(
  idDaMissao: string,
  cadenciaDeRetomada: number[] | null,
  token: string,
): Promise<MissaoDaTrilha> {
  return chamarNucleo<MissaoDaTrilha>(`/v1/missoes/${idDaMissao}/retomada`, {
    metodo: "POST",
    corpo: { cadencia_de_retomada: cadenciaDeRetomada },
    token,
  });
}
