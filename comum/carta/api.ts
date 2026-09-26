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
// A identificação do Guerreiro(a) vem de `GET /v1/eu`, e o desempenho do
// ranking logado da própria turma — nenhuma das duas depende de ele ter
// aberto série de coleta (`RF-01-76`, decisão do fundador de 2026-09-26, que
// fechou a pendência do documento 09 §1).

/** A posição do próprio Guerreiro(a) no ranking logado da turma. O nick e o
 * avatar **não** vêm daqui: vêm de `GET /v1/eu`, que os serve sem depender da
 * comunidade. */
export interface MinhaPosicaoNoRanking {
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

/** O núcleo deriva a comunidade do vínculo vigente de quem pergunta, e recusa
 * com `403` quem não tem vínculo — a tela não descobre comunidade alguma antes
 * de perguntar (`RF-05-52`, `RF-05-84`, `RN-05-16`). */
export function obterMinhaPosicaoNoRanking(token: string): Promise<RankingComMinhaPosicao> {
  return chamarNucleo<RankingComMinhaPosicao>("/v1/eu/ranking", { token });
}

/** Nível por trilha inscrita e badges emitidos (`RF-05-15`, `RF-05-16`). */
export function obterProgressoDaCarta(token: string): Promise<ProgressoDaTrilhaNaCarta[]> {
  return chamarNucleo<ProgressoDaTrilhaNaCarta[]>("/v1/eu/progresso", { token });
}

/** As criações originais validadas (`RF-05-43`, `RF-05-44`). */
export function obterPortfolioDaCarta(token: string): Promise<ItemDoPortfolioNaCarta[]> {
  return chamarNucleo<ItemDoPortfolioNaCarta[]>("/v1/eu/portfolio", { token });
}
