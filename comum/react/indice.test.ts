import { describe, expect, it } from "vitest";
import * as indice from "./indice";

describe("índice de comum/react", () => {
  it("exporta os dez componentes", () => {
    expect(indice.Aviso).toBeTypeOf("function");
    expect(indice.Botao).toBeTypeOf("function");
    expect(indice.Cabecalho).toBeTypeOf("function");
    expect(indice.Campo).toBeTypeOf("function");
    expect(indice.CampoDeDataHora).toBeTypeOf("function");
    expect(indice.Dialogo).toBeTypeOf("function");
    expect(indice.EstadoDaLista).toBeTypeOf("function");
    expect(indice.Moldura).toBeTypeOf("function");
    expect(indice.NavegacaoDeAreas).toBeTypeOf("function");
    expect(indice.Tabela).toBeTypeOf("function");
  });
});
