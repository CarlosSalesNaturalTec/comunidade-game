import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it } from "vitest";
import { Dialogo } from "./Dialogo";

function Exemplo({
  telaCheia,
  fecharAoTocarFora,
}: {
  telaCheia?: boolean;
  fecharAoTocarFora?: boolean;
}) {
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
        telaCheia={telaCheia}
        fecharAoTocarFora={fecharAoTocarFora}
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

  it("tela cheia aplica a variante; sem ela, o diálogo segue como era", async () => {
    const usuario = userEvent.setup();
    const { unmount } = render(<Exemplo telaCheia />);
    await usuario.click(screen.getByRole("button", { name: "Abrir" }));
    expect(screen.getByRole("dialog")).toHaveClass("cg-dialogo--tela-cheia");
    unmount();

    render(<Exemplo />);
    await usuario.click(screen.getByRole("button", { name: "Abrir" }));
    expect(screen.getByRole("dialog")).not.toHaveClass("cg-dialogo--tela-cheia");
  });

  it("o toque no fundo fecha e devolve o foco; no corpo e no cabeçalho, não", async () => {
    const usuario = userEvent.setup();
    render(<Exemplo fecharAoTocarFora />);

    const botaoDeAbrir = screen.getByRole("button", { name: "Abrir" });
    await usuario.click(botaoDeAbrir);
    const dialogo = screen.getByRole("dialog");

    await usuario.click(screen.getByRole("button", { name: "Dentro" }));
    await usuario.click(screen.getByRole("heading", { name: "Título do diálogo" }));
    expect(screen.getByRole("dialog")).toBeInTheDocument();

    await usuario.click(dialogo);
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(botaoDeAbrir).toHaveFocus();
  });

  it("sem fecharAoTocarFora, o toque no fundo não fecha", async () => {
    const usuario = userEvent.setup();
    render(<Exemplo />);
    await usuario.click(screen.getByRole("button", { name: "Abrir" }));
    await usuario.click(screen.getByRole("dialog"));
    expect(screen.getByRole("dialog")).toBeInTheDocument();
  });
});
