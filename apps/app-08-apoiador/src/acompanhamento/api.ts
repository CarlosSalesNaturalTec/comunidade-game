import { chamarNucleo } from "comum/api";

export type TipoDeNovidade = "criacao_original" | "badge" | "nivel" | "trilha";

export interface Novidade {
  tipo: TipoDeNovidade;
  data: string;
  trilha_id: string | null;
  trilha_nome: string | null;
  badge_tipo: string | null;
  nivel_valor: number | null;
}

export interface FavoritoDeGuerreiro {
  id: string;
  avatar: string | null;
  nick: string;
  novidades: Novidade[];
}

export interface FavoritoDeMestre {
  id: string;
  avatar: string | null;
  nome: string | null;
  novidades: Novidade[];
}

export interface Favoritos {
  guerreiros: FavoritoDeGuerreiro[];
  mestres: FavoritoDeMestre[];
}

// As três rotas de favorito, restritas ao Apoiador em sessão (`RF-14-49`,
// `RF-14-52`, `RF-14-55`).
export function listarMeusFavoritos(token: string): Promise<Favoritos> {
  return chamarNucleo<Favoritos>("/v1/eu/favoritos", { token });
}

export function favoritarGuerreiroPeloNick(
  token: string,
  nick: string,
): Promise<FavoritoDeGuerreiro> {
  return chamarNucleo<FavoritoDeGuerreiro>("/v1/eu/favoritos", {
    metodo: "POST",
    corpo: { nick },
    token,
  });
}

export function removerFavorito(token: string, favoritoId: string): Promise<void> {
  return chamarNucleo<void>(`/v1/eu/favoritos/${favoritoId}`, { metodo: "DELETE", token });
}

export interface AvatarENick {
  avatar: string | null;
  nick: string;
}

interface PaginaDeResultado<T> {
  itens: T[];
  proximo_cursor: string | null;
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

export interface CriacaoPublica {
  trilha_id: string;
  producao: string;
  autores: AvatarENick[];
}

export interface CoberturaPublicaDeOds {
  comunidade_id: string;
  comunidade_nome: string;
  objetivos: number[];
  ciclo: string;
}

// O mesmo painel público que qualquer visitante consulta, sem token de
// sessão e sem parâmetro que identifique o Apoiador (`RF-14-48`,
// `RN-14-24`, design — decisão 9).
export function listarGuerreirosPublicos(): Promise<PaginaDeResultado<AvatarENick>> {
  return chamarNucleo<PaginaDeResultado<AvatarENick>>("/v1/vitrine/guerreiros");
}

export function listarPoderesPublicos(): Promise<PoderPublico[]> {
  return chamarNucleo<PoderPublico[]>("/v1/vitrine/poderes");
}

export function listarCriacoesPublicas(): Promise<PaginaDeResultado<CriacaoPublica>> {
  return chamarNucleo<PaginaDeResultado<CriacaoPublica>>("/v1/vitrine/criacoes");
}

export function listarCoberturaPublicaDeOds(): Promise<CoberturaPublicaDeOds[]> {
  return chamarNucleo<CoberturaPublicaDeOds[]>("/v1/vitrine/ods/cobertura");
}
