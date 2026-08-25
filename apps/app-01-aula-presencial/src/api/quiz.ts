import { chamarNucleo } from "comum/api";

export type SituacaoDaPartida = "aberta" | "encerrada";

export interface PartidaDaAula {
  id: string;
  situacao: SituacaoDaPartida;
  /** Derivada pelo núcleo — o aparelho nunca escolhe nem informa a equipe
   * (`RF-04-41`, `RF-04-42`, design — decisão 1). Nula para quem não
   * disputa nenhuma equipe daquela partida. */
  equipe_id: string | null;
}

// Descoberta da partida da aula, com a equipe do Guerreiro(a) em sessão já
// derivada (`RF-04-41`, `RF-04-42`). A rota devolve uma lista simples, sem
// paginação — a mesma forma de `GET /v1/aulas/{id}/equipes` reexposta aqui
// sem o envelope de página, porque o núcleo não pagina esta leitura.
export function listarPartidasDaAula(aulaId: string, token: string): Promise<PartidaDaAula[]> {
  return chamarNucleo<PartidaDaAula[]>(`/v1/aulas/${aulaId}/partidas`, { token });
}

export interface PerguntaParaEquipe {
  id: string | null;
  enunciado: string | null;
  alternativas: string[] | null;
  /** Ausente (equivale a `false`) enquanto quem conduz não libera o
   * resultado — o corpo omite os três campos abaixo até lá (`RF-04-44`,
   * design — decisão 2). */
  resultado_liberado?: boolean;
  alternativa_correta?: number | null;
  acertou?: boolean | null;
  primeira_equipe_a_acertar?: string | null;
}

// Sondada a cada 2 segundos pelo aparelho da equipe (`RF-04-41`, documento
// 03 §1). Sem pergunta no ar, os três primeiros campos vêm nulos e os
// demais ausentes — é o que faz o aparelho que caiu voltar na pergunta
// corrente assim que ela existir.
export function lerPerguntaDaPartida(
  idDaPartida: string,
  token: string,
): Promise<PerguntaParaEquipe> {
  return chamarNucleo<PerguntaParaEquipe>(`/v1/partidas-de-quiz/${idDaPartida}/pergunta`, {
    token,
  });
}

export interface RespostaDeQuiz {
  id: string;
  equipe_id: string;
  pergunta_id: string;
  alternativa_escolhida: number;
  momento_de_chegada: string;
}

// Uma resposta por equipe e pergunta — o reenvio da mesma alternativa
// devolve o registro já gravado, e alternativa diferente é recusada com
// 422 (`RF-04-43`). O momento de chegada é sempre carimbado pelo núcleo.
export function enviarResposta(
  idDaPartida: string,
  perguntaId: string,
  equipeId: string,
  alternativaEscolhida: number,
  token: string,
): Promise<RespostaDeQuiz> {
  return chamarNucleo<RespostaDeQuiz>(`/v1/partidas-de-quiz/${idDaPartida}/respostas`, {
    metodo: "POST",
    corpo: {
      pergunta_id: perguntaId,
      equipe_id: equipeId,
      alternativa_escolhida: alternativaEscolhida,
    },
    token,
  });
}
