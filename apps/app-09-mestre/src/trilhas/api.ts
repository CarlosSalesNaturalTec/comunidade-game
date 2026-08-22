import { chamarNucleo } from "comum/api";

export type EtapaDoCiclo = "abertura" | "desenvolvimento" | "marcos" | "fechamento";

// O objetivo vai de 1 a 18 e a meta é livre e opcional; quem recusa o
// objetivo fora da faixa é o núcleo (`RF-09-92`, `RF-09-98`).
export interface EtiquetaOds {
  id: string;
  objetivo: number;
  meta: string | null;
  trilha_id: string | null;
  missao_id: string | null;
}

export interface EtiquetaOdsDeclarada {
  objetivo: number;
  meta?: string | null;
}

// A cobertura é sempre da trilha — a união dos objetivos dela e das missões
// dela —, nunca por Guerreiro(a) (`RF-09-94`, `RN-01-24`).
export interface CoberturaOdsDaTrilha {
  objetivos: number[];
  ciclo: string;
}

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
  // As etiquetas **próprias** da missão: a leitura não cai para as da
  // trilha, ainda que a missão sem etiqueta própria responda por elas nos
  // vínculos (`RF-09-98`, `RF-01-45`).
  etiquetas_ods: EtiquetaOds[];
}

export interface TrilhaDaLista {
  id: string;
  nome: string;
  objetivo: string;
  area_do_conhecimento: string;
  poder_id: string;
  situacao: string;
  motivo_da_situacao: string | null;
  etiquetas_ods: EtiquetaOds[];
  cobertura_ods: CoberturaOdsDaTrilha;
}

export interface TrilhaDoMestre extends TrilhaDaLista {
  missoes: MissaoDaTrilha[];
  // Nunca vem de `GET /trilhas/minhas` — só é conhecida depois que o Mestre
  // a declara nesta sessão (`POST /trilhas/{id}/culminancia` não tem par de
  // leitura, PRD-09 §9). `undefined` é "ainda não declarada nesta sessão",
  // distinto de `null`, que o núcleo nunca devolve.
  culminancia?: CulminanciaDaTrilha | null;
}

export type ModalidadeDaCulminancia = "individual" | "em_equipe";

export interface CulminanciaDaTrilha {
  id: string;
  trilha_id: string;
  descricao: string;
  modalidade: ModalidadeDaCulminancia;
  criterio_de_validacao: string;
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

export interface DeclararCulminanciaEntrada {
  descricao: string;
  modalidade: ModalidadeDaCulminancia;
  criterio_de_validacao: string;
}

// Privativa do Mestre autor; a segunda declaração substitui a anterior, e
// não cria uma segunda culminância (`RF-09-29`, `RF-09-30`).
export function declararCulminancia(
  idDaTrilha: string,
  entrada: DeclararCulminanciaEntrada,
  token: string,
): Promise<CulminanciaDaTrilha> {
  return chamarNucleo<CulminanciaDaTrilha>(`/v1/trilhas/${idDaTrilha}/culminancia`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Publica ou republica, a partir de rascunho ou despublicada — a mesma
// rota para as duas origens (`RF-09-05`, `RF-09-11`).
export function publicarTrilha(idDaTrilha: string, token: string): Promise<TrilhaDaLista> {
  return chamarNucleo<TrilhaDaLista>(`/v1/trilhas/${idDaTrilha}/publicacao`, {
    metodo: "POST",
    token,
  });
}

// As duas rotas recebem a **lista completa** e substituem o conjunto do
// alvo: o que estava é apagado, o que veio é gravado. Lista vazia deixa o
// alvo sem etiqueta, situação legal no Ciclo 01 (`RF-09-92`, `RF-09-93`).
export function substituirEtiquetasOdsDaTrilha(
  idDaTrilha: string,
  etiquetas: EtiquetaOdsDeclarada[],
  token: string,
): Promise<EtiquetaOds[]> {
  return chamarNucleo<EtiquetaOds[]>(`/v1/trilhas/${idDaTrilha}/ods`, {
    metodo: "POST",
    corpo: { etiquetas },
    token,
  });
}

// Escopada à missão: nunca alcança as etiquetas da trilha (`RF-09-98`).
export function substituirEtiquetasOdsDaMissao(
  idDaMissao: string,
  etiquetas: EtiquetaOdsDeclarada[],
  token: string,
): Promise<EtiquetaOds[]> {
  return chamarNucleo<EtiquetaOds[]>(`/v1/missoes/${idDaMissao}/ods`, {
    metodo: "POST",
    corpo: { etiquetas },
    token,
  });
}
