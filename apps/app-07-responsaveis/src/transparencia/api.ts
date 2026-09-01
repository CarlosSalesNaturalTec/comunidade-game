import { chamarNucleo } from "comum/api";

export interface ItemDoCatalogoDeDados {
  dado: string;
  finalidade: string;
  prazo: string;
  restrito_a_gestao: boolean;
  guardado: boolean;
}

// O catálogo declarado do que o núcleo guarda daquele vinculado, com
// finalidade e prazo, e a marca do que está guardado hoje — nunca o
// conteúdo (`RF-13-29`, `RN-13-20`).
export function listarDadosDoVinculado(
  guerreiroId: string,
  token: string,
): Promise<ItemDoCatalogoDeDados[]> {
  return chamarNucleo<ItemDoCatalogoDeDados[]>(`/v1/eu/guerreiros/${guerreiroId}/dados`, {
    token,
  });
}

export interface AcessoDoResponsavel {
  id: string;
  momento: string;
  autor_id: string;
  autor_nome: string | null;
  papel_do_autor: string;
  acao: string;
  entidade_afetada: string;
}

interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

// O histórico de acessos do vinculado, da mais recente para a mais antiga
// — nunca o conteúdo do dado, nunca linha de outra criança (`RF-13-30`).
export function listarAcessosDoVinculado(
  guerreiroId: string,
  token: string,
): Promise<AcessoDoResponsavel[]> {
  return chamarNucleo<Pagina<AcessoDoResponsavel>>(
    `/v1/eu/guerreiros/${guerreiroId}/acessos`,
    {
      token,
    },
  ).then((pagina) => pagina.itens);
}
