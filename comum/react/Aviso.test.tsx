import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Aviso } from "./Aviso";

describe("Aviso", () => {
  it("erro interrompe: role=alert, com rótulo textual que o identifica sem depender da cor", () => {
    render(<Aviso tipo="erro">Não foi possível salvar.</Aviso>);

    const aviso = screen.getByRole("alert");
    expect(aviso).toHaveTextContent("Erro:");
    expect(aviso).toHaveTextContent("Não foi possível salvar.");
  });

  it("andamento apenas informa: role=status, nunca role=alert", () => {
    render(<Aviso tipo="andamento">Entrando…</Aviso>);

    expect(screen.getByRole("status")).toHaveTextContent("Entrando…");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});
