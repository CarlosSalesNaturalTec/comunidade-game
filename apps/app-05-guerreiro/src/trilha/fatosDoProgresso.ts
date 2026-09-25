import type { FatoDaArena } from "comum/react";

// **Qual fato aconteceu desde a última vez que este aparelho mostrou o
// progresso** (documento 11 §8.5). Sem esta comparação não há como distinguir
// "subi de nível agora" de "abri a tela e o nível já era esse" — e é essa
// distinção que o documento 15 §5 exige para o retorno não virar movimento
// decorativo.
//
// A marca fica em `sessionStorage`, na sessão do Guerreiro(a): o que se quer
// saber é se o fato é novo **para quem está olhando agora**, e a sessão é
// exatamente esse recorte. Aparelho compartilhado não carrega a marca de uma
// criança para a seguinte.

const CHAVE = "app-05:progresso-ja-visto";

/** O que a tela já mostrou de cada trilha: nível e quantos badges. */
type JaVisto = Record<string, { nivel: number | null; badges: number }>;

export interface ProgressoParaComparar {
  trilha_id: string;
  nivel_atual: number | null;
  badges: string[];
}

function lerJaVisto(): JaVisto | null {
  try {
    const bruto = sessionStorage.getItem(CHAVE);
    return bruto === null ? null : (JSON.parse(bruto) as JaVisto);
  } catch {
    // Armazenamento indisponível ou marca ilegível: trata-se como primeira
    // leitura, que não rende fato nenhum. Nunca inventa conquista.
    return null;
  }
}

function gravarJaVisto(progresso: ProgressoParaComparar[]): void {
  const marca: JaVisto = {};
  for (const item of progresso) {
    marca[item.trilha_id] = { nivel: item.nivel_atual, badges: item.badges.length };
  }
  try {
    sessionStorage.setItem(CHAVE, JSON.stringify(marca));
  } catch {
    // Não poder gravar só faz a próxima leitura não render fato. A tela
    // continua inteira.
  }
}

/**
 * O fato de cada trilha, por `trilha_id`, e a gravação da nova marca.
 *
 * **A primeira leitura da sessão não rende fato nenhum**: não há com o que
 * comparar, e abrir a tela não é conquistar. Trilha que o Guerreiro(a) acabou
 * de inscrever também não: ela não estava na marca anterior, e nível novo de
 * quem nunca teve nível é inscrição, não subida.
 *
 * Nível que subiu tem precedência sobre badge certificado quando os dois
 * acontecem na mesma leitura: subir de nível é o fato maior, e o §8.5 não
 * manda empilhar dois retornos no mesmo lugar.
 */
export function fatosDoProgresso(
  progresso: ProgressoParaComparar[],
): Record<string, FatoDaArena> {
  const anterior = lerJaVisto();
  gravarJaVisto(progresso);
  if (anterior === null) return {};

  const fatos: Record<string, FatoDaArena> = {};
  for (const item of progresso) {
    const antes = anterior[item.trilha_id];
    if (antes === undefined) continue;
    if (item.nivel_atual !== null && antes.nivel !== null && item.nivel_atual > antes.nivel) {
      fatos[item.trilha_id] = "nivel_que_subiu";
      continue;
    }
    if (item.badges.length > antes.badges) fatos[item.trilha_id] = "badge_certificado";
  }
  return fatos;
}
