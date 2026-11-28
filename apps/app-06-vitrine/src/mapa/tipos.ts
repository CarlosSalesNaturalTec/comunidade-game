/** O contorno como a leitura pública o devolve (`RF-08-34`). */
export interface ContornoPublico {
  geometria: Record<string, unknown>;
  origem_osm: string;
  copiado_em: string;
  credito: string;
  licenca: string;
}

/** O que o mapa recebe de cada comunidade: só o contorno, o nome e o destino
 * — nenhum local, série, ponto ou coletor (`RN-03-44`). */
export interface ComunidadeNoMapa {
  id: string;
  nome: string;
  destino: string;
  contorno: ContornoPublico;
}

export type ModoDoMapa = "listagem" | "destaque";
