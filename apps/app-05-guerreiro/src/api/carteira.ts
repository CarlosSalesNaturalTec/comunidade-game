import { chamarNucleo } from "comum/api";

export interface PontosExtras {
  acumulado: number;
  saldo_disponivel: number;
}

// A carteira do próprio Guerreiro(a) — acumulado e saldo disponível, nunca
// somados nem confundidos com o ponto regular (`RF-05-82`).
export function listarMeusPontosExtras(token: string): Promise<PontosExtras> {
  return chamarNucleo<PontosExtras>("/v1/eu/pontos-extras", { token });
}

export interface ItemDeCatalogoAvulso {
  id: string;
  nome: string;
  tipo_de_recurso_id: string;
  estoque: number;
  ativo: boolean;
  preco_em_pontos_extras: number | null;
  preco_de_referencia_ausente: boolean;
}

// O catálogo já resolve a comunidade do vínculo vigente de quem pergunta —
// o Guerreiro(a) nunca declara a própria comunidade (`RF-05-83`).
export function listarCatalogoAvulso(token: string): Promise<ItemDeCatalogoAvulso[]> {
  return chamarNucleo<ItemDeCatalogoAvulso[]>("/v1/catalogo-avulso", { token });
}

export interface Troca {
  id: string;
  item_de_catalogo_avulso_id: string;
  preco_cobrado: number;
  registrado_em: string;
}

export function listarMinhasTrocas(token: string): Promise<Troca[]> {
  return chamarNucleo<Troca[]>("/v1/trocas", { token });
}

export interface RecompensaConquistada {
  recompensa_de_marco_id: string;
  trilha_id: string;
  missao_id: string;
  tipo_de_recurso_id: string;
  quantidade: number;
  entregue: boolean;
  entregue_em: string | null;
}

export function listarMinhasRecompensas(token: string): Promise<RecompensaConquistada[]> {
  return chamarNucleo<RecompensaConquistada[]>("/v1/eu/recompensas", { token });
}

export interface ItemDoRankingDaTurma {
  avatar: string | null;
  nick: string;
  posicao: number;
  pontos_regulares: number;
}

export interface RankingDaTurma {
  itens: ItemDoRankingDaTurma[];
  proximo_cursor: string | null;
  minha_posicao: ItemDoRankingDaTurma;
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

// Leitura pública, para montar as opções de recorte do ranking por trilha
// ou por poder (`RF-05-52`, `RF-05-53`).
export function listarPoderesPublicos(): Promise<PoderPublico[]> {
  return chamarNucleo<PoderPublico[]>("/v1/vitrine/poderes");
}

interface RecorteDoRanking {
  trilhaId?: string;
  poderId?: string;
}

// O ranking logado é a única leitura restrita à própria Comunidade Virtual
// por segmento na URL, e não por filtro de query — o núcleo recusa com 403
// qualquer comunidade que não seja a do Guerreiro(a) em sessão (`RF-05-52`,
// `RF-05-84`).
export function listarRankingDaTurma(
  comunidadeId: string,
  token: string,
  recorte?: RecorteDoRanking,
): Promise<RankingDaTurma> {
  const parametros = new URLSearchParams();
  if (recorte?.trilhaId) parametros.set("trilha", recorte.trilhaId);
  if (recorte?.poderId) parametros.set("poder", recorte.poderId);
  const consulta = parametros.toString();
  return chamarNucleo<RankingDaTurma>(
    `/v1/rankings/${encodeURIComponent(comunidadeId)}${consulta ? `?${consulta}` : ""}`,
    { token },
  );
}
