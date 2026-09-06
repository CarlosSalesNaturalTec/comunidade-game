import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { NavegacaoDeAreas } from "./NavegacaoDeAreas";

const AREAS = [
  { chave: "comunidades", rotulo: "Comunidades" },
  { chave: "poderes", rotulo: "Poderes" },
];

describe("NavegacaoDeAreas", () => {
  it("marca a área corrente por aria-current e por outro sinal além da cor", () => {
    render(
      <NavegacaoDeAreas
        rotulo="Áreas da gestão"
        areas={AREAS}
        areaAtual="poderes"
        aoSelecionarArea={vi.fn()}
        aoSair={vi.fn()}
      />,
    );

    const atual = screen.getByRole("button", { name: "Poderes", current: true });
    expect(atual).toHaveClass("cg-navegacao-de-areas__item");
    expect(screen.getByRole("button", { name: "Comunidades" })).not.toHaveAttribute(
      "aria-current",
    );
  });

  it("apresenta a saída da sessão uma única vez, ao fim da navegação", async () => {
    const usuario = userEvent.setup();
    const aoSair = vi.fn();
    render(
      <NavegacaoDeAreas
        rotulo="Áreas da gestão"
        areas={AREAS}
        areaAtual="comunidades"
        aoSelecionarArea={vi.fn()}
        aoSair={aoSair}
      />,
    );

    expect(screen.getAllByRole("button", { name: "Sair" })).toHaveLength(1);
    await usuario.click(screen.getByRole("button", { name: "Sair" }));
    expect(aoSair).toHaveBeenCalledOnce();
  });
});
