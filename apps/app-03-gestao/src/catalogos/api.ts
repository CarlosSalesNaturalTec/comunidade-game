import { chamarNucleo } from "comum/api";

interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

export type FormaDeRegistro = "numero" | "foto" | "video";

export const ROTULO_DA_FORMA_DE_REGISTRO: Record<FormaDeRegistro, string> = {
  numero: "Número",
  foto: "Foto",
  video: "Vídeo",
};

export interface TipoDeColeta {
  id: string;
  nome: string;
  forma_de_registro: FormaDeRegistro;
  unidade: string | null;
  faixa_minima: number | null;
  faixa_maxima: number | null;
  ativo: boolean;
}

// A listagem do núcleo é paginada por cursor; o catálogo inteiro cabe numa
// tela de cadastro, então a leitura segue o `proximo_cursor` até o fim,
// como `territorio/api.ts` já faz com os locais (`RF-02-108`, `RF-01-28`,
// design — decisão 3).
export async function listarTodosOsTiposDeColeta(token: string): Promise<TipoDeColeta[]> {
  const tipos: TipoDeColeta[] = [];
  let cursor: string | null = null;
  do {
    const consulta = new URLSearchParams();
    if (cursor) consulta.set("cursor", cursor);
    const sufixo = consulta.toString() ? `?${consulta.toString()}` : "";
    const pagina: Pagina<TipoDeColeta> = await chamarNucleo<Pagina<TipoDeColeta>>(
      `/v1/tipos-de-coleta${sufixo}`,
      { token },
    );
    tipos.push(...pagina.itens);
    cursor = pagina.proximo_cursor;
  } while (cursor);
  return tipos;
}

export interface CadastrarTipoDeColetaEntrada {
  nome: string;
  forma_de_registro: FormaDeRegistro;
  unidade?: string;
  faixa_minima?: number;
  faixa_maxima?: number;
}

export function cadastrarTipoDeColeta(
  entrada: CadastrarTipoDeColetaEntrada,
  token: string,
): Promise<TipoDeColeta> {
  return chamarNucleo<TipoDeColeta>("/v1/tipos-de-coleta", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Campo ausente mantém; `null` retira — é assim que a troca para foto ou
// vídeo leva a unidade e a faixa embora (`RF-02-114`, `RF-08-32`).
export interface AlterarTipoDeColetaEntrada {
  nome?: string;
  forma_de_registro?: FormaDeRegistro;
  unidade?: string | null;
  faixa_minima?: number | null;
  faixa_maxima?: number | null;
}

export function alterarTipoDeColeta(
  id: string,
  entrada: AlterarTipoDeColetaEntrada,
  token: string,
): Promise<TipoDeColeta> {
  return chamarNucleo<TipoDeColeta>(`/v1/tipos-de-coleta/${id}`, {
    metodo: "PATCH",
    corpo: entrada,
    token,
  });
}

export function desativarTipoDeColeta(id: string, token: string): Promise<TipoDeColeta> {
  return chamarNucleo<TipoDeColeta>(`/v1/tipos-de-coleta/${id}/desativacao`, {
    metodo: "POST",
    token,
  });
}

export function reativarTipoDeColeta(id: string, token: string): Promise<TipoDeColeta> {
  return chamarNucleo<TipoDeColeta>(`/v1/tipos-de-coleta/${id}/reativacao`, {
    metodo: "POST",
    token,
  });
}

// Só o tipo que nenhum desafio escolheu sai (`RN-08-30`).
export function excluirTipoDeColeta(id: string, token: string): Promise<void> {
  return chamarNucleo<void>(`/v1/tipos-de-coleta/${id}`, { metodo: "DELETE", token });
}
