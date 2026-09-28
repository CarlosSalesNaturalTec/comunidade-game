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
