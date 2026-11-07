import { describe, expect, it } from "vitest";
import { ligarFalaAAlternativa } from "./ligarFalaAAlternativa";

const ALTERNATIVAS = ["Fotossíntese", "Respiração", "Evaporação", "Chuva ácida"];

describe("ligarFalaAAlternativa (RF-05-98)", () => {
  it("o texto da alternativa a marca, sem distinguir caixa, acento ou pontuação", () => {
    expect(ligarFalaAAlternativa("respiracao!", ALTERNATIVAS)).toBe(2);
    expect(ligarFalaAAlternativa("CHUVA ÁCIDA", ALTERNATIVAS)).toBe(4);
  });

  it("o texto aproximado marca a alternativa mais próxima", () => {
    expect(ligarFalaAAlternativa("foto síntese", ALTERNATIVAS)).toBe(1);
    expect(ligarFalaAAlternativa("é a evaporação", ALTERNATIVAS)).toBe(3);
  });

  it("a letra, o número e o ordinal marcam a posição", () => {
    expect(ligarFalaAAlternativa("letra B", ALTERNATIVAS)).toBe(2);
    expect(ligarFalaAAlternativa("letra a", ALTERNATIVAS)).toBe(1);
    expect(ligarFalaAAlternativa("d", ALTERNATIVAS)).toBe(4);
    expect(ligarFalaAAlternativa("a segunda", ALTERNATIVAS)).toBe(2);
    expect(ligarFalaAAlternativa("alternativa 3", ALTERNATIVAS)).toBe(3);
    expect(ligarFalaAAlternativa("quatro", ALTERNATIVAS)).toBe(4);
  });

  it("silêncio não marca nada", () => {
    expect(ligarFalaAAlternativa("", ALTERNATIVAS)).toBeNull();
    expect(ligarFalaAAlternativa("   ", ALTERNATIVAS)).toBeNull();
  });

  it("fala sem correspondência não marca nada", () => {
    expect(ligarFalaAAlternativa("não sei, acho que é a lua", ALTERNATIVAS)).toBeNull();
  });

  it("empate entre alternativas parecidas não marca nada", () => {
    expect(ligarFalaAAlternativa("casa", ["Casaco", "Casal", "Rio", "Mar"])).toBeNull();
  });
});
