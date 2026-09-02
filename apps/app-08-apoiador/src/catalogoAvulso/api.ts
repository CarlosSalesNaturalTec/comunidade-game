import { chamarNucleo } from "comum/api";

export type SituacaoDeHomologacao = "nao_se_aplica" | "pendente" | "homologado" | "recusado";

export interface ItemDeCatalogoAvulso {
  id: string;
  nome: string;
  tipo_de_recurso_id: string;
  estoque: string;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  origem_do_cadastro: string;
  situacao_de_homologacao: SituacaoDeHomologacao;
  homologacao_motivo: string | null;
  ativo: boolean;
  preco_em_pontos_extras: number | null;
  preco_de_referencia_ausente: boolean;
  quantidade_faltante: string | null;
}

export interface MinhaOfertaDeCatalogoAvulso extends ItemDeCatalogoAvulso {
  quantidade_de_trocas: number;
}

export interface OfertarItemEntrada {
  nome: string;
  tipo_de_recurso_id: string;
  estoque: number;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
}

// O item nasce sem preço próprio — o preço vem sempre da tabela de
// referência vigente do tipo de recurso, e a homologação do Admin decide se
// ele entra no catálogo (`RF-14-77` a `RF-14-79`, `RN-14-42`, `RN-14-43`).
export function ofertarItem(
  entrada: OfertarItemEntrada,
  token: string,
): Promise<ItemDeCatalogoAvulso> {
  return chamarNucleo<ItemDeCatalogoAvulso>("/v1/catalogo-avulso", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Só os itens do próprio Apoiador, em qualquer situação, com a contagem
// agregada de trocas — sem identificar quem trocou (`RF-14-80`, `RF-14-81`,
// `RN-14-44`).
export function listarMinhasOfertas(token: string): Promise<MinhaOfertaDeCatalogoAvulso[]> {
  return chamarNucleo<MinhaOfertaDeCatalogoAvulso[]>("/v1/eu/catalogo-avulso", { token });
}
