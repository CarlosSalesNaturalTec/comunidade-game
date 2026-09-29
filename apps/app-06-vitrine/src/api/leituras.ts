import { lerDoNucleo } from "./nucleo";

// As leituras públicas que esta fatia consome. Todas passam por
// `lerDoNucleo`, que leva a chave da aplicação e **nenhuma** credencial de
// persona: o visitante segue anônimo (`RN-03-33`).
//
// Os tipos trazem só o que as telas leem. A projeção do Guerreiro(a) é a
// **carta do documento 11 §8.2 inteira**, a mesma no card e na página
// (`RF-03-03`, `RF-03-05`, decisão do fundador, 2026-09-28) — a vitrine não
// cruza `trilha_id` com o catálogo de poderes para montá-la.

export interface PaginaDoNucleo<Item> {
  itens: Item[];
  proximo_cursor: string | null;
}

export interface BadgeNaCartaPublica {
  familia: string;
  poder: string | null;
}

export interface PoderComNivelPublico {
  poder: string;
  nivel: number;
}

export interface CriacaoNaCartaPublica {
  trilha: string;
  validada_em: string;
}

export interface GuerreiroPublico {
  avatar: string | null;
  nick: string;
  badges: BadgeNaCartaPublica[];
  poderes: PoderComNivelPublico[];
  pontos_regulares: number;
  posicao_no_ranking: number;
  criacoes: CriacaoNaCartaPublica[];
}

export interface AutorPublico {
  avatar: string | null;
  nick: string;
}

/** O portfólio do `RF-03-08`: trilha, data e autoria por nick. **Sem
 * título** — a criação original não tem esse campo no modelo. */
export interface CriacaoPublica {
  trilha_id: string;
  trilha: string;
  validada_em: string;
  producao: string;
  autores: AutorPublico[];
}

export interface ItemDeRankingPublico {
  avatar: string | null;
  nick: string;
  pontos_regulares: number;
  posicao: number;
}

export interface TrilhaPublica {
  id: string;
  nome: string;
}

export interface PoderPublico {
  id: string;
  nome: string;
  descricao: string;
  trilhas: TrilhaPublica[];
}

/** Os cards da seção, com a carta de cada um **na mesma resposta**: montar a
 * composição com uma consulta por nick para cada card cairia no freio por
 * origem (`RF-03-02`, `RF-03-04`, design — decisão 1). */
export function listarGuerreiros(): Promise<PaginaDoNucleo<GuerreiroPublico>> {
  return lerDoNucleo<PaginaDoNucleo<GuerreiroPublico>>("/v1/vitrine/guerreiros");
}

/** A página individual, por **nick exato**. Nick inexistente e nick sem
 * autorização devolvem o mesmo 404 (`RF-03-11`, `RN-03-07`), e a repetição
 * da consulta encontra o freio por origem (`RF-03-36`). */
export function obterGuerreiroPorNick(nick: string): Promise<GuerreiroPublico> {
  return lerDoNucleo<GuerreiroPublico>(`/v1/vitrine/guerreiros/${encodeURIComponent(nick)}`);
}

export function listarCriacoes(): Promise<PaginaDoNucleo<CriacaoPublica>> {
  return lerDoNucleo<PaginaDoNucleo<CriacaoPublica>>("/v1/vitrine/criacoes");
}

export function listarRanking(): Promise<PaginaDoNucleo<ItemDeRankingPublico>> {
  return lerDoNucleo<PaginaDoNucleo<ItemDeRankingPublico>>("/v1/vitrine/rankings");
}

export function listarPoderes(): Promise<PoderPublico[]> {
  return lerDoNucleo<PoderPublico[]>("/v1/vitrine/poderes");
}

/** A comunidade na lista pública: nome, localização, os quatro indicadores
 * do documento 02 §1 — nulos abaixo do piso de coletores — e a
 * **vitalidade**, que não é indicador e por isso nunca vem nula
 * (`RF-03-02`). */
export interface ComunidadeNaLista {
  id: string;
  nome: string;
  localizacao: string;
  series_abertas: number | null;
  series_ativas: number | null;
  registros_validos: number | null;
  continuidade: number | null;
  guerreiros_vinculados: number;
}

export interface ListaDeComunidades {
  itens: ComunidadeNaLista[];
  proximo_cursor: string | null;
  ciclo_rotulo: string;
}

export interface LocalPublico {
  id: string;
  nivel: string;
  rotulo: string;
  local_pai_id: string | null;
}

/** A ficha pública da comunidade: locais **até o bairro** — a rota não serve
 * nível mais fino —, os tipos de coleta ativos e a vitalidade
 * (`RF-03-15`, `RN-03-09`). */
export interface ComunidadePublica {
  id: string;
  nome: string;
  locais: LocalPublico[];
  tipos_de_coleta: { id: string; nome: string }[];
  guerreiros_vinculados: number;
}

export interface RecortePublicado {
  tipo_de_coleta_id: string;
  tipo_de_coleta_nome: string;
  local_publicado_id: string;
  local_publicado_nivel: string;
  local_publicado_rotulo: string;
}

export interface PontoDaSerie {
  momento_da_medicao: string;
  valor: number | null;
  recorte: RecortePublicado;
}

/** A metodologia que cada recorte declara (`RF-03-17`, `RF-03-18`) e o sinal
 * de série inativa (`RF-03-19`). Vale para a consulta inteira, não para a
 * página: o núcleo a apura antes do corte. */
export interface MetodologiaDoRecorte {
  recorte: RecortePublicado;
  unidade: string | null;
  cadencias: string[];
  origens: string[];
  primeira_medicao: string;
  ultima_medicao: string;
  registros_validos: number;
  ativo: boolean;
}

export interface SeriePublica {
  itens: PontoDaSerie[];
  proximo_cursor: string | null;
  recortes: MetodologiaDoRecorte[];
}

/** A cobertura da Agenda 2030, por comunidade e por ciclo (`RF-03-22`). É
 * sempre agregada: nenhum recorte por Guerreiro(a) existe nesta rota
 * (`RF-03-24`, `RN-03-19`). */
export interface CoberturaDeOds {
  comunidade_id: string;
  comunidade_nome: string;
  objetivos: number[];
  ciclo: string;
}

export function listarComunidades(): Promise<ListaDeComunidades> {
  return lerDoNucleo<ListaDeComunidades>("/v1/comunidades");
}

export function obterComunidade(id: string): Promise<ComunidadePublica> {
  return lerDoNucleo<ComunidadePublica>(`/v1/comunidades/${encodeURIComponent(id)}`);
}

export function lerSerieDaComunidade(id: string): Promise<SeriePublica> {
  return lerDoNucleo<SeriePublica>(`/v1/comunidades/${encodeURIComponent(id)}/series`);
}

export function lerCoberturaDeOds(): Promise<CoberturaDeOds[]> {
  return lerDoNucleo<CoberturaDeOds[]>("/v1/vitrine/ods/cobertura");
}

/** As três seções do conteúdo institucional (`RF-03-45`). O texto chega
 * `null` quando a seção ainda não foi publicada, e o vídeo só existe em
 * "Quem somos" (`RF-03-49`). O núcleo nunca devolve quem publicou. */
export type ChaveDeSecaoInstitucional = "quem-somos" | "contatos" | "como-apoiar";

export interface SecaoInstitucionalPublica {
  secao: ChaveDeSecaoInstitucional;
  texto: string | null;
  video_url: string | null;
}

export function lerConteudoInstitucional(): Promise<SecaoInstitucionalPublica[]> {
  return lerDoNucleo<SecaoInstitucionalPublica[]>("/v1/vitrine/conteudo-institucional");
}

/** As necessidades de recurso em aberto (`RF-03-47`). O núcleo devolve o nome
 * ao lado de cada identificador, e o **valor em moedas chega `null`** quando o
 * tipo de recurso não tem vigência de referência na data da leitura: a vitrine
 * mostra a falta e **nenhum valor arbitrado** (`RN-03-18`). Nenhum campo traz
 * reais, e nenhum identifica Guerreiro(a), responsável ou provedor. */
export interface NecessidadePublica {
  aula_id: string;
  tipo_de_recurso_id: string;
  tipo_de_recurso_nome: string;
  quantidade_faltante: string;
  valor_em_moedas: string | null;
  comunidade_virtual_id: string;
  comunidade_virtual_nome: string;
  ponto_de_apoio_id: string;
  ponto_de_apoio_nome: string;
  inicio_em: string;
  fim_em: string;
}

export function listarNecessidades(): Promise<NecessidadePublica[]> {
  return lerDoNucleo<NecessidadePublica[]>("/v1/vitrine/necessidades");
}
