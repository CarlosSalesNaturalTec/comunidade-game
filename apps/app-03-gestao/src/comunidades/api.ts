import { chamarNucleo } from "comum/api";

// O contorno copiado do OSM, como o núcleo o devolve: a atribuição vem
// pronta, e a tela não a escreve (`RF-02-122`, `RN-08-31`).
export interface ContornoDaComunidade {
  geometria: Record<string, unknown>;
  origem_osm: string;
  copiado_em: string;
  credito: string;
  licenca: string;
}

export interface ComunidadeDaLista {
  id: string;
  nome: string;
  localizacao: string;
  series_abertas: number | null;
  series_ativas: number | null;
  registros_validos: number | null;
  continuidade: number | null;
  // Nulo enquanto o Admin não grava; o núcleo sempre devolve o campo.
  contorno?: ContornoDaComunidade | null;
}

interface ListaDeComunidades {
  itens: ComunidadeDaLista[];
  proximo_cursor: string | null;
  ciclo_rotulo: string;
}

export function listarComunidades(): Promise<ListaDeComunidades> {
  return chamarNucleo<ListaDeComunidades>("/v1/comunidades");
}

export interface CriarComunidadeEntrada {
  nome: string;
  localizacao: string;
  granularidade_maxima: string;
}

interface ComunidadeCriada {
  id: string;
  nome: string;
  localizacao: string;
  granularidade_maxima: string;
}

export function criarComunidade(
  entrada: CriarComunidadeEntrada,
  token: string,
): Promise<ComunidadeCriada> {
  return chamarNucleo<ComunidadeCriada>("/v1/comunidades", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface GravarContornoEntrada {
  geometria: unknown;
  origem_osm: string;
}

// Cadastra ou substitui o contorno; a validade da geometria e da origem é do
// núcleo (`RF-02-122`, `RF-08-33`).
export function gravarContorno(
  idDaComunidade: string,
  entrada: GravarContornoEntrada,
  token: string,
): Promise<ContornoDaComunidade> {
  return chamarNucleo<ContornoDaComunidade>(`/v1/comunidades/${idDaComunidade}/contorno`, {
    metodo: "PUT",
    corpo: entrada,
    token,
  });
}
