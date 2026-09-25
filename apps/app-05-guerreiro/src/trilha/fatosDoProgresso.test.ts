import { afterEach, describe, expect, it } from "vitest";
import { fatosDoProgresso, type ProgressoParaComparar } from "./fatosDoProgresso";

const ROBO: ProgressoParaComparar = {
  trilha_id: "trilha-1",
  nivel_atual: 3,
  badges: ["de_nivel"],
};

afterEach(() => {
  sessionStorage.clear();
});

describe("que fato aconteceu desde a última leitura (documento 11 §8.5)", () => {
  // Cenário: Não há retorno sem fato
  it("a primeira leitura da sessão não rende fato nenhum", () => {
    // Abrir a tela não é conquistar: sem marca anterior não há com o que
    // comparar, e nenhuma conquista se inventa.
    expect(fatosDoProgresso([ROBO])).toEqual({});
  });

  it("reler o mesmo progresso não rende fato nenhum", () => {
    fatosDoProgresso([ROBO]);
    expect(fatosDoProgresso([ROBO])).toEqual({});
  });

  it("nível que subiu é fato", () => {
    fatosDoProgresso([ROBO]);
    expect(fatosDoProgresso([{ ...ROBO, nivel_atual: 4 }])).toEqual({
      "trilha-1": "nivel_que_subiu",
    });
  });

  it("badge novo é fato", () => {
    fatosDoProgresso([ROBO]);
    expect(fatosDoProgresso([{ ...ROBO, badges: ["de_nivel", "de_autoria"] }])).toEqual({
      "trilha-1": "badge_certificado",
    });
  });

  it("subir de nível tem precedência sobre o badge que veio junto", () => {
    // O núcleo emite um badge por nível alcançado: os dois fatos chegam
    // juntos, e o §8.5 não manda empilhar dois retornos no mesmo lugar.
    fatosDoProgresso([ROBO]);
    expect(
      fatosDoProgresso([{ ...ROBO, nivel_atual: 4, badges: ["de_nivel", "de_nivel"] }]),
    ).toEqual({ "trilha-1": "nivel_que_subiu" });
  });

  it("trilha recém-inscrita não rende fato — inscrever-se não é subir", () => {
    fatosDoProgresso([ROBO]);
    const fatos = fatosDoProgresso([
      ROBO,
      { trilha_id: "trilha-2", nivel_atual: 1, badges: ["de_nivel"] },
    ]);
    expect(fatos).toEqual({});
  });

  it("armazenamento indisponível não inventa conquista", () => {
    const original = sessionStorage.getItem;
    sessionStorage.getItem = () => {
      throw new Error("indisponível");
    };
    try {
      expect(fatosDoProgresso([ROBO])).toEqual({});
    } finally {
      sessionStorage.getItem = original;
    }
  });
});
