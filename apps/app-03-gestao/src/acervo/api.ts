import { chamarNucleo } from "comum/api";

export type TeorDaAnotacao = "cuidado" | "perda" | "dano";

export interface AnotacaoDaFichaDeVida {
  id: string;
  teor: TeorDaAnotacao;
  estado_de_conservacao: string;
  autor_id: string;
  registrado_em: string;
}

export interface ItemPatrimonialDaLista {
  id: string;
  aporte_de_origem_id: string | null;
  titulo: string;
  numero_de_tombo: string;
  ponto_de_apoio_id: string;
  estado_de_conservacao: string;
  responsavel_id: string | null;
  ficha_de_vida: AnotacaoDaFichaDeVida[];
  autor_id: string;
  registrado_em: string;
}

// `GET /v1/itens-patrimoniais` devolve lista simples, não paginada, com a
// ficha de vida completa e o responsável já derivado do ponto de apoio — a
// App 03 não monta nem ordena nada disso (`RF-02-52`, `RF-02-53`; design —
// Context).
export function listarAcervo(
  comunidadeId: string,
  token: string,
): Promise<ItemPatrimonialDaLista[]> {
  const consulta = new URLSearchParams({ comunidade_virtual_id: comunidadeId });
  return chamarNucleo<ItemPatrimonialDaLista[]>(
    `/v1/itens-patrimoniais?${consulta.toString()}`,
    { token },
  );
}

export interface TombarItemEntrada {
  titulo: string;
  numero_de_tombo: string;
  ponto_de_apoio_id: string;
  estado_de_conservacao: string;
}

export function tombarItem(
  entrada: TombarItemEntrada,
  token: string,
): Promise<ItemPatrimonialDaLista> {
  return chamarNucleo<ItemPatrimonialDaLista>("/v1/itens-patrimoniais", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface AnotarFichaDeVidaEntrada {
  teor: TeorDaAnotacao;
  estado_de_conservacao: string;
}

export function anotarFichaDeVida(
  idDoItem: string,
  entrada: AnotarFichaDeVidaEntrada,
  token: string,
): Promise<ItemPatrimonialDaLista> {
  return chamarNucleo<ItemPatrimonialDaLista>(
    `/v1/itens-patrimoniais/${idDoItem}/ficha-de-vida`,
    { metodo: "POST", corpo: entrada, token },
  );
}
