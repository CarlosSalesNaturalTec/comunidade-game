import { chamarNucleo } from "comum/api";

export interface PerguntaDeQuiz {
  id: string;
  enunciado: string;
  alternativas: string[];
  alternativa_correta: number;
  missao_id: string;
  trilha_id: string;
  registrado_em: string;
}

export interface PaginaDePerguntas {
  itens: PerguntaDeQuiz[];
  proximo_cursor: string | null;
}

export interface CriarPerguntaEntrada {
  enunciado: string;
  alternativas: string[];
  alternativa_correta: number;
  missao_id: string;
}

// A trilha nunca é enviada: o núcleo a deriva da missão declarada
// (`RF-09-36`, `RF-09-39`).
export function cadastrarPergunta(
  entrada: CriarPerguntaEntrada,
  token: string,
): Promise<PerguntaDeQuiz> {
  return chamarNucleo<PerguntaDeQuiz>("/v1/perguntas", {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export interface FiltroDoBanco {
  trilhaId?: string;
  missaoId?: string;
}

// O banco é sempre do Mestre em sessão, por autoria — o filtro só recorta
// dentro dele (`RF-09-40`).
export function listarBancoDeQuiz(
  filtro: FiltroDoBanco,
  token: string,
): Promise<PaginaDePerguntas> {
  const parametros = new URLSearchParams();
  if (filtro.trilhaId) parametros.set("trilha", filtro.trilhaId);
  if (filtro.missaoId) parametros.set("missao", filtro.missaoId);
  const consulta = parametros.toString();
  return chamarNucleo<PaginaDePerguntas>(
    `/v1/perguntas/minhas${consulta ? `?${consulta}` : ""}`,
    { token },
  );
}
