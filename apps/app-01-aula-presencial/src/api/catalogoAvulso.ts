import { chamarNucleo } from "comum/api";

export interface ItemDeCatalogoAvulso {
  id: string;
  nome: string;
  tipo_de_recurso_id: string;
  estoque: string;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  origem_do_cadastro: string;
  situacao_de_homologacao: string;
  homologacao_motivo: string | null;
  ativo: boolean;
  preco_em_pontos_extras: number | null;
  preco_de_referencia_ausente: boolean;
  quantidade_faltante: string | null;
}

// Sem declarar comunidade — o núcleo filtra pela do vínculo de quem
// consulta (`RF-04-50`, design — decisão 4). Usado com o token de
// trabalho na sondagem da abertura do momento de troca, e com o token do
// Guerreiro(a) na leitura que a tela da troca exibe.
export function listarCatalogoAvulso(token: string): Promise<ItemDeCatalogoAvulso[]> {
  return chamarNucleo<ItemDeCatalogoAvulso[]>("/v1/catalogo-avulso", { token });
}
