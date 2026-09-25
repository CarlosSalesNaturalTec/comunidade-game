import { chamarNucleo } from "comum/api";

// As leituras que **montam a carta do Guerreiro(a)**, promovidas do App 05
// para o `comum` porque as duas aplicações da Arena que apresentam a carta —
// Apps 01 e 05 — precisam das mesmas (design — decisão 4, decisão do fundador
// de 2026-09-25). Mesmo movimento que `comum/trilha/api` já fez com o que o
// percurso compartilha.
//
// Os tipos aqui trazem **só os campos que a carta lê**. Quem precisa do resto
// de cada leitura continua importando do módulo da própria aplicação: a carta
// não é dona do contrato inteiro dessas rotas, e alargar o tipo aqui faria do
// `comum` o lugar onde toda leitura do Guerreiro(a) acaba morando.
//
// Nenhuma rota nova: as quatro já são servidas pelo núcleo e já eram
// consumidas pelo App 05.

/** A posição do próprio Guerreiro(a) no ranking logado da turma — a única
 * leitura logada que lhe devolve o **próprio** avatar e nick. `GET /v1/eu`
 * devolve papel, permissões e a autorização de divulgação, e nunca os dois;
 * pendência registrada no documento 09 §1. */
export interface MinhaPosicaoNoRanking {
  avatar: string | null;
  nick: string;
  posicao: number;
  pontos_regulares: number;
}

interface RankingComMinhaPosicao {
  minha_posicao: MinhaPosicaoNoRanking;
}

export interface ProgressoDaTrilhaNaCarta {
  trilha_id: string;
  trilha_nome: string;
  nivel_atual: number | null;
  badges: string[];
}

interface ItemDoPortfolioNaCarta {
  producao: string | null;
}

interface SerieDoGuerreiroNaCarta {
  comunidade_virtual_id: string;
}

interface PaginaDeSeries {
  itens: SerieDoGuerreiroNaCarta[];
}

/** O ranking logado é segmentado por comunidade na URL, e o núcleo recusa com
 * `403` qualquer comunidade que não seja a do Guerreiro(a) em sessão
 * (`RF-05-52`, `RF-05-84`). */
export function obterMinhaPosicaoNoRanking(
  comunidadeId: string,
  token: string,
): Promise<RankingComMinhaPosicao> {
  return chamarNucleo<RankingComMinhaPosicao>(
    `/v1/rankings/${encodeURIComponent(comunidadeId)}`,
    { token },
  );
}

/** A comunidade do Guerreiro(a) vem das séries de coleta dele, o mesmo
 * caminho que a tela do ranking já usa. */
export function listarMinhasSeriesDaCarta(token: string): Promise<PaginaDeSeries> {
  return chamarNucleo<PaginaDeSeries>("/v1/series-de-coleta/minhas", { token });
}

/** Nível por trilha inscrita e badges emitidos (`RF-05-15`, `RF-05-16`). */
export function obterProgressoDaCarta(token: string): Promise<ProgressoDaTrilhaNaCarta[]> {
  return chamarNucleo<ProgressoDaTrilhaNaCarta[]>("/v1/eu/progresso", { token });
}

/** As criações originais validadas (`RF-05-43`, `RF-05-44`). */
export function obterPortfolioDaCarta(token: string): Promise<ItemDoPortfolioNaCarta[]> {
  return chamarNucleo<ItemDoPortfolioNaCarta[]>("/v1/eu/portfolio", { token });
}
