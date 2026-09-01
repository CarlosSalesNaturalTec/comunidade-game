export type PerfilDeApoiador = "pessoa_fisica" | "pessoa_juridica";

// Escala fixa e as duas escadas de valores sugeridos, por perfil declarado
// (documento 04 §2, `RF-14-03`, `RN-14-40`). Valores em reais; o equivalente
// em moedas é sempre derivado daqui, nunca cadastrado no núcleo.
export const REAIS_POR_MOEDA = 10;

export const ESCADA_POR_PERFIL: Record<PerfilDeApoiador, number[]> = {
  pessoa_fisica: [10, 50, 100, 250],
  pessoa_juridica: [500, 1000, 2500, 5000],
};

// Fração de duas casas, como o livro-razão grava qualquer aporte
// (`RN-14-40`).
export function converterReaisEmMoedas(valorEmReais: number): number {
  return Math.round((valorEmReais / REAIS_POR_MOEDA) * 100) / 100;
}

export function formatarMoedas(valorEmReais: number): string {
  const moedas = converterReaisEmMoedas(valorEmReais);
  return `${moedas.toLocaleString("pt-BR", { minimumFractionDigits: 0, maximumFractionDigits: 2 })} moeda${moedas === 1 ? "" : "s"}`;
}
