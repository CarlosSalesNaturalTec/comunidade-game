import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { type ColunaDaTabela, Tabela } from "./Tabela";

interface Pessoa {
  id: string;
  nome: string;
  papel: string;
}

const PESSOAS: Pessoa[] = [
  { id: "1", nome: "Ana", papel: "Mestre" },
  { id: "2", nome: "Bia", papel: "Gestão" },
];

const COLUNAS: ColunaDaTabela<Pessoa>[] = [
  { chave: "nome", rotulo: "Nome", cabecalhoDeLinha: true, renderizar: (p) => p.nome },
  { chave: "papel", rotulo: "Papel", recolhida: true, renderizar: (p) => p.papel },
];

describe("Tabela", () => {
  it("é marcação semântica de tabela, com legenda e cabeçalho de coluna em th[scope=col]", () => {
    render(
      <Tabela
        legenda="Pessoas"
        colunas={COLUNAS}
        linhas={PESSOAS}
        chaveDaLinha={(p) => p.id}
      />,
    );

    expect(screen.getByRole("table", { name: "Pessoas" })).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "Nome" })).toBeInTheDocument();
    expect(screen.getByRole("columnheader", { name: "Papel" })).toBeInTheDocument();
    expect(screen.getByRole("rowheader", { name: "Ana" })).toBeInTheDocument();
  });

  it("confina a rolagem horizontal ao próprio componente, não à página", () => {
    const { container } = render(
      <Tabela colunas={COLUNAS} linhas={PESSOAS} chaveDaLinha={(p) => p.id} />,
    );

    const rolagem = container.querySelector(".cg-tabela__rolagem");
    expect(rolagem).toContainElement(screen.getByRole("table"));
  });
});
