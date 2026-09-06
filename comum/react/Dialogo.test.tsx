import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it } from "vitest";
import { Dialogo } from "./Dialogo";

function Exemplo() {
  const [aberto, definirAberto] = useState(false);
  return (
    <div>
      <button type="button" onClick={() => definirAberto(true)}>
        Abrir
      </button>
      <Dialogo
        aberto={aberto}
        titulo="Título do diálogo"
        aoFechar={() => definirAberto(false)}
      >
        <button type="button">Dentro</button>
      </Dialogo>
    </div>
  );
}

describe("Dialogo", () => {
  it("o foco não escapa do diálogo ao percorrer pelo teclado", async () => {
    const usuario = userEvent.setup();
    render(<Exemplo />);

    await usuario.click(screen.getByRole("button", { name: "Abrir" }));
    const dialogo = screen.getByRole("dialog", { name: "Título do diálogo" });

    await usuario.tab();
    await usuario.tab();
    await usuario.tab();

    expect(dialogo).toContainElement(document.activeElement as HTMLElement);
  });

  it("fechar pela tecla de escape devolve o foco a quem abriu", async () => {
    const usuario = userEvent.setup();
    render(<Exemplo />);

    const botaoDeAbrir = screen.getByRole("button", { name: "Abrir" });
    await usuario.click(botaoDeAbrir);
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    await usuario.keyboard("{Escape}");

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDeAbrir).toHaveFocus();
  });

  it("fechar pelo botão rotulado devolve o foco a quem abriu", async () => {
    const usuario = userEvent.setup();
    render(<Exemplo />);

    const botaoDeAbrir = screen.getByRole("button", { name: "Abrir" });
    await usuario.click(botaoDeAbrir);
    await usuario.click(screen.getByRole("button", { name: "Fechar" }));

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDeAbrir).toHaveFocus();
  });
});
