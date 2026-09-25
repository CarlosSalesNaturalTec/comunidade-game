import { describe, expect, it } from "vitest";
import * as indice from "./indice";

describe("índice de comum/react", () => {
  it("exporta os vinte e um componentes", () => {
    expect(indice.Aviso).toBeTypeOf("function");
    expect(indice.BadgeDaFamilia).toBeTypeOf("function");
    expect(indice.BlocoRecolhivel).toBeTypeOf("function");
    expect(indice.Botao).toBeTypeOf("function");
    expect(indice.Cabecalho).toBeTypeOf("function");
    expect(indice.Campo).toBeTypeOf("function");
    expect(indice.CampoDeDataHora).toBeTypeOf("function");
    expect(indice.CartaDoPersonagem).toBeTypeOf("function");
    expect(indice.Dialogo).toBeTypeOf("function");
    expect(indice.EmblemaDeNivel).toBeTypeOf("function");
    expect(indice.EstadoDaLista).toBeTypeOf("function");
    expect(indice.FundoDeComunidade).toBeTypeOf("function");
    expect(indice.GlifoDePoder).toBeTypeOf("function");
    expect(indice.Icone).toBeTypeOf("function");
    expect(indice.MarcaDeGravacao).toBeTypeOf("function");
    expect(indice.MidiaDoNucleo).toBeTypeOf("function");
    expect(indice.Moldura).toBeTypeOf("function");
    expect(indice.NavegacaoDeAreas).toBeTypeOf("function");
    expect(indice.PalcoDoPersonagem).toBeTypeOf("function");
    expect(indice.RetornoDeConquista).toBeTypeOf("function");
    expect(indice.Tabela).toBeTypeOf("function");
  });
});
