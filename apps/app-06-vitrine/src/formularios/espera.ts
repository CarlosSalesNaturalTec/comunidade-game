import type { ErroDaApi } from "comum/api";

/** O tempo de espera que o núcleo devolveu, em linguagem simples
 * (`RF-03-35`, `RF-03-36`). */
export function esperaEmLinguagemSimples(erro: ErroDaApi): string {
  const segundos = erro.tempoDeEsperaEmSegundos ?? 0;
  if (segundos <= 0) return "Tente de novo em instantes.";
  if (segundos < 60) {
    return `Tente de novo em ${segundos} ${segundos === 1 ? "segundo" : "segundos"}.`;
  }
  const minutos = Math.round(segundos / 60);
  return `Tente de novo em ${minutos} ${minutos === 1 ? "minuto" : "minutos"}.`;
}
