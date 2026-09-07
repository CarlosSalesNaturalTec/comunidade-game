import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { BlocoRecolhivel } from "./BlocoRecolhivel";

describe("BlocoRecolhivel", () => {
  it("nasce fechado, com o resumo na linha, e o conteúdo não é alcançável", () => {
    render(
      <BlocoRecolhivel titulo="Cadência de retomada" resumo="Retomada em 2, 7, 21 dias">
        <button type="button">Ação do bloco</button>
      </BlocoRecolhivel>,
    );

    expect(screen.getByText("Cadência de retomada")).toBeInTheDocument();
    expect(screen.getByText("Retomada em 2, 7, 21 dias")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Ação do bloco" })).not.toBeInTheDocument();
  });

  it("bloco sem conteúdo declara que está vazio, e continua alcançável", () => {
    render(
      <BlocoRecolhivel
        titulo="Recompensa pelo desbloqueio"
        resumo="Nenhuma recompensa declarada."
      >
        <p>Formulário da recompensa</p>
      </BlocoRecolhivel>,
    );

    expect(screen.getByText("Nenhuma recompensa declarada.")).toBeInTheDocument();
  });

  it("o operador abre e fecha o bloco pelo controle", async () => {
    const usuario = userEvent.setup();
    render(
      <BlocoRecolhivel titulo="Bibliografia" resumo="Nenhuma bibliografia declarada.">
        <button type="button">Ação do bloco</button>
      </BlocoRecolhivel>,
    );

    await usuario.click(screen.getByText("Bibliografia"));
    expect(screen.getByRole("button", { name: "Ação do bloco" })).toBeInTheDocument();

    await usuario.click(screen.getByText("Bibliografia"));
    expect(screen.queryByRole("button", { name: "Ação do bloco" })).not.toBeInTheDocument();
  });

  it("o controle é anunciado com rótulo textual e com o estado, sem ícone", async () => {
    const usuario = userEvent.setup();
    const { container } = render(
      <BlocoRecolhivel titulo="Conteúdo" resumo="Nenhum conteúdo declarado.">
        <p>Conteúdo do bloco</p>
      </BlocoRecolhivel>,
    );
    const bloco = container.querySelector("details") as HTMLDetailsElement;

    expect(screen.getByText("Mostrar")).toBeInTheDocument();
    expect(bloco).not.toHaveAttribute("open");

    await usuario.click(screen.getByText("Conteúdo"));

    expect(screen.getByText("Ocultar")).toBeInTheDocument();
    expect(screen.queryByText("Mostrar")).not.toBeInTheDocument();
    expect(bloco).toHaveAttribute("open");
  });
});
