import { describe, expect, it } from "vitest";
import { distanciaEntreDescritores } from "./distancia";

// Os valores abaixo vêm do cálculo do núcleo (`_distancia_euclidiana` em
// `backend/src/nucleo/biometria/regra.py`) e estão escritos aqui de propósito:
// são eles que prendem as duas implementações. Mudar o cálculo de um lado sem
// o outro quebra este arquivo — que é exatamente o ponto (`RF-04-63`,
// design — Riscos).
describe("distância entre descritores", () => {
  it("é a euclidiana: o triângulo 3-4-5 dá 5", () => {
    expect(distanciaEntreDescritores([0, 0, 0], [3, 4, 0])).toBe(5);
  });

  it("descritores idênticos ficam a zero", () => {
    expect(distanciaEntreDescritores([0.1, 0.2], [0.1, 0.2])).toBe(0);
  });

  it("tamanhos diferentes devolvem nulo, como o núcleo", () => {
    expect(distanciaEntreDescritores([1], [1, 2])).toBeNull();
  });

  // Na dimensão real do descritor da Human, uma diferença de 0,1 por posição
  // já dá 3,2 — mais de seis vezes o limiar de 0,5 que a convenção do
  // `face-api.js` sugeria. É a ordem de grandeza que a bancada existe para
  // medir com rostos de verdade.
  it("na dimensão da biblioteca, 0,1 por posição dá 3,2", () => {
    const a = new Array(1024).fill(0.1);
    const b = new Array(1024).fill(0.2);
    expect(distanciaEntreDescritores(a, b)).toBeCloseTo(3.2, 10);
  });

  it("na dimensão da biblioteca, rostos muito distintos passam de 280", () => {
    const a = new Array(1024).fill(0.1);
    const b = new Array(1024).fill(9);
    expect(distanciaEntreDescritores(a, b)).toBeCloseTo(284.8, 8);
  });
});
