import { describe, expect, it } from "vitest";
import { formatarMoedas, formatarQuantidade } from "./formatacao";

describe("formatação do número devolvido pelo núcleo", () => {
  it("quantidade sai em pt-BR, sem zeros supérfluos, com a unidade quando houver", () => {
    expect(formatarQuantidade("1.00", "un")).toBe("1 un");
    expect(formatarQuantidade("17.00")).toBe("17");
    expect(formatarQuantidade("1.50", "kg")).toBe("1,5 kg");
  });

  it("valor sai em moedas, com o singular para uma moeda, nunca em reais", () => {
    expect(formatarMoedas("5.00")).toBe("5 moedas");
    expect(formatarMoedas("1.00")).toBe("1 moeda");
    expect(formatarMoedas("1005.5")).toBe("1.005,5 moedas");
  });

  it("valor que não é número volta como o núcleo o devolveu", () => {
    expect(formatarQuantidade("abc", "un")).toBe("abc");
    expect(formatarMoedas("")).toBe("");
  });
});
