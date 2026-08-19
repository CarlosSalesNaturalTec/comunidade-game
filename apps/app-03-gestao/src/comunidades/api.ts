import { chamarNucleo } from "../api/cliente";

export interface ComunidadeDaLista {
  id: string;
  nome: string;
  localizacao: string;
  series_abertas: number | null;
  series_ativas: number | null;
  registros_validos: number | null;
  continuidade: number | null;
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
