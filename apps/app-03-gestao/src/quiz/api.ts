import { chamarNucleo } from "comum/api";

export type FormatoDaAtividade = "presencial" | "on_line_assincrona";

export interface AulaDaTurma {
  id: string;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
  situacao: string;
}

export interface AtividadeDoMestre {
  id: string;
  missao_id: string;
  titulo: string;
  formato: FormatoDaAtividade;
  modalidade: string;
  natureza: string;
}

export interface MinhasTurmas {
  itens: AulaDaTurma[];
  proximo_cursor: string | null;
  atividades_presenciais: AtividadeDoMestre[];
  atividades_on_line: AtividadeDoMestre[];
}

// Aulas e atividades do Mestre em sessão — a mesma rota que o painel do dia
// usa, sem leitura nova para a tela de abertura (`RF-02-59`, design —
// decisão 6).
export function listarMinhasTurmas(token: string): Promise<MinhasTurmas> {
  return chamarNucleo<MinhasTurmas>("/v1/minhas-turmas", { token });
}

export interface IntegranteDaEquipe {
  avatar: string | null;
  nick: string;
  papel: string | null;
}

export interface EquipeDaAula {
  id: string;
  aula_id: string | null;
  integrantes: IntegranteDaEquipe[];
}

interface PaginaDeEquipes {
  itens: EquipeDaAula[];
  proximo_cursor: string | null;
}

// Equipes formadas na App 01 naquele encontro, cada integrante só por
// avatar e nick (`RF-02-59`, `RN-02-22`).
export function listarEquipesDaAula(aulaId: string, token: string): Promise<PaginaDeEquipes> {
  return chamarNucleo<PaginaDeEquipes>(`/v1/aulas/${aulaId}/equipes`, { token });
}

export interface PerguntaDeQuiz {
  id: string;
  enunciado: string;
  alternativas: string[];
  alternativa_correta: number;
  missao_id: string;
  trilha_id: string;
  registrado_em: string;
}

interface PaginaDePerguntas {
  itens: PerguntaDeQuiz[];
  proximo_cursor: string | null;
}

// O banco do Mestre em sessão, filtrado pela missão da atividade
// escolhida (`RF-09-40`).
export function listarPerguntasDaMissao(
  missaoId: string,
  token: string,
): Promise<PaginaDePerguntas> {
  return chamarNucleo<PaginaDePerguntas>(`/v1/perguntas/minhas?missao=${missaoId}`, { token });
}

export type SituacaoDaPartida = "aberta" | "encerrada";

export interface PartidaDeQuiz {
  id: string;
  aula_id: string;
  atividade_id: string;
  situacao: SituacaoDaPartida;
  equipes_disputantes: string[];
  encerrada_em: string | null;
  registrado_em: string;
}

// Abre a partida sobre a atividade e as equipes escolhidas
// (`RF-02-59`, `RF-02-61`).
export function abrirPartida(
  aulaId: string,
  atividadeId: string,
  equipes: string[],
  token: string,
): Promise<PartidaDeQuiz> {
  return chamarNucleo<PartidaDeQuiz>("/v1/partidas-de-quiz", {
    metodo: "POST",
    corpo: { aula_id: aulaId, atividade_id: atividadeId, equipes },
    token,
  });
}

export interface PerguntaNoAr {
  id: string;
  pergunta_id: string;
  enunciado: string;
  alternativas: string[];
  ordem: number;
  entrou_em: string;
  resultado_liberado: boolean;
  alternativa_correta: number | null;
  equipes_que_acertaram: string[] | null;
  primeira_equipe_a_acertar: string | null;
}

export interface EstadoDaPartida {
  id: string;
  aula_id: string;
  atividade_id: string;
  situacao: SituacaoDaPartida;
  equipes_disputantes: string[];
  pergunta_no_ar: PerguntaNoAr | null;
  equipes_que_responderam: string[];
}

// Sondada a cada 2 segundos por quem conduz (`RF-02-60`, documento 03 §1).
export function lerEstadoDaPartida(
  idDaPartida: string,
  token: string,
): Promise<EstadoDaPartida> {
  return chamarNucleo<EstadoDaPartida>(`/v1/partidas-de-quiz/${idDaPartida}`, { token });
}

// _Start_ da pergunta corrente, substituindo a anterior sem apagá-la
// (`RF-02-60`).
export function porPerguntaNoAr(
  idDaPartida: string,
  perguntaId: string,
  token: string,
): Promise<EstadoDaPartida> {
  return chamarNucleo<EstadoDaPartida>(`/v1/partidas-de-quiz/${idDaPartida}/perguntas`, {
    metodo: "POST",
    corpo: { pergunta_id: perguntaId },
    token,
  });
}

// Libera o resultado da pergunta no ar — idempotente e sem crédito
// (`RF-02-62`, `RF-04-44`).
export function liberarResultado(
  idDaPartida: string,
  token: string,
): Promise<EstadoDaPartida> {
  return chamarNucleo<EstadoDaPartida>(`/v1/partidas-de-quiz/${idDaPartida}/resultado`, {
    metodo: "POST",
    token,
  });
}

export interface PerguntaAnulada {
  id: string;
  pergunta_id: string;
  registrado_em: string;
}

// Anula a pergunta contestada, sem crédito para ninguém (`RF-02-72`).
export function anularPergunta(
  idDaPartida: string,
  perguntaId: string,
  token: string,
): Promise<PerguntaAnulada> {
  return chamarNucleo<PerguntaAnulada>(`/v1/partidas-de-quiz/${idDaPartida}/anulacoes`, {
    metodo: "POST",
    corpo: { pergunta_id: perguntaId },
    token,
  });
}

// Encerra a partida, com o lançamento automático da pontuação (`RF-02-73`).
export function encerrarPartida(idDaPartida: string, token: string): Promise<PartidaDeQuiz> {
  return chamarNucleo<PartidaDeQuiz>(`/v1/partidas-de-quiz/${idDaPartida}/encerramento`, {
    metodo: "POST",
    token,
  });
}
