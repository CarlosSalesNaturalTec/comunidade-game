import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12: a vitrine abre inteira sem login, e
// nenhuma tela oferece cadastro ou área restrita.
describe("a vitrine abre pública, no recorte padrão", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  it("abre inteira sem pedir login nem cadastro (RF-03-01, RN-03-01)", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: "Comunidade Game", level: 1 })).toBeVisible();
    expect(screen.queryByLabelText(/senha/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /cadastrar|criar conta|sair/i })).toBeNull();
  });

  it("a raiz é o recorte sociedade civil (RF-03-25)", () => {
    render(<App />);

    expect(screen.getByRole("button", { name: "Sociedade civil" })).toHaveAttribute(
      "aria-current",
      "true",
    );
    expect(screen.getByRole("heading", { name: "Guerreiros e Guerreiras" })).toBeVisible();
  });

  it("os três recortes estão na navegação (RF-03-25)", () => {
    render(<App />);

    const recortes = screen.getByRole("navigation", { name: /recortes de leitura/i });
    expect(recortes).toBeVisible();
    for (const rotulo of ["Sociedade civil", "Pesquisadores", "Gestores públicos"]) {
      expect(screen.getByRole("button", { name: rotulo })).toBeVisible();
    }
  });

  it("nenhuma tela exibe publicidade ou patrocínio (RF-03-50, RN-03-21)", () => {
    const { container } = render(<App />);

    expect(container.textContent).not.toMatch(/publicidade|patrocínio|anúncio/i);
    expect(container.querySelector("iframe")).toBeNull();
  });
});

describe("trocar de recorte é navegação", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  it("muda a ordem de entrada sem bloquear nada nem pedir cadastro (RF-03-26)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Gestores públicos" }));

    expect(window.location.pathname).toBe("/gestores-publicos");
    const titulos = screen.getAllByRole("heading", { level: 2 }).map((no) => no.textContent);
    expect(titulos[0]).toMatch(/serve ao município/i);
    expect(screen.queryByLabelText(/senha/i)).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Entrar" })).toBeVisible();
  });

  it("o recorte pesquisadores abre pelas séries do território (RF-03-26)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));

    const titulos = screen.getAllByRole("heading", { level: 2 }).map((no) => no.textContent);
    expect(titulos[0]).toMatch(/séries do território/i);
  });

  it("voltar à raiz devolve ao recorte padrão (RF-03-26, RF-03-51)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sociedade civil" }));

    expect(window.location.pathname).toBe("/");
    expect(screen.getByRole("button", { name: "Sociedade civil" })).toHaveAttribute(
      "aria-current",
      "true",
    );
  });
});
