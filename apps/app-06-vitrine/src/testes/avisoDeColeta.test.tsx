import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";
import App from "../App";

const AVISO = { name: "Aviso de coleta de dados" };

describe("aviso de coleta em toda tela (RN-03-23)", () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
  });

  it.each([
    ["um recorte", "/"],
    ["a página de um Guerreiro(a)", "/guerreiros/zeferina"],
    ["a página de uma comunidade", "/comunidades/abc"],
    ["o formulário de participação", "/participar"],
    ["o formulário de dados", "/solicitar-dados"],
    ["a própria área detalhada", "/o-que-coletamos"],
  ])("aparece em %s, com o acesso à área detalhada", (_nome, caminho) => {
    window.history.pushState(null, "", caminho);
    render(<App />);

    const aviso = screen.getByRole("complementary", AVISO);
    expect(aviso).toHaveTextContent(/não coleta dado de quem visita/);
    expect(aviso).toHaveTextContent(/Só os formulários guardam o que você digita/);
    expect(
      screen.getByRole("button", { name: "Saiba o que a plataforma coleta" }),
    ).toBeVisible();
  });

  it("não bloqueia a tela nem pede confirmação, e não deixa rastro", async () => {
    window.history.pushState(null, "", "/");
    render(<App />);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Sociedade civil" })).toBeEnabled();
    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });
});

describe("área detalhada de coleta (RF-03-52, RF-03-53)", () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    window.history.pushState(null, "", "/");
  });

  it("o aviso leva à área, que tem endereço próprio", async () => {
    render(<App />);
    await userEvent.click(
      screen.getByRole("button", { name: "Saiba o que a plataforma coleta" }),
    );

    expect(window.location.pathname).toBe("/o-que-coletamos");
    expect(screen.getByRole("heading", { name: "O que a plataforma coleta" })).toBeVisible();
  });

  it("lista cada dado com de quem, para quê e por quanto tempo", () => {
    window.history.pushState(null, "", "/o-que-coletamos");
    render(<App />);

    const tabela = screen.getByRole("table", { name: "Dados ligados à vitrine" });
    for (const coluna of ["Dado", "De quem", "Para quê", "Por quanto tempo"]) {
      expect(screen.getAllByRole("columnheader", { name: coluna }).length).toBeGreaterThan(0);
    }
    expect(tabela).toHaveTextContent("Pedido do conjunto de dados");
    expect(tabela).toHaveTextContent("Para sempre, como prova do que foi entregue");
    expect(tabela).toHaveTextContent("Enquanto a autorização durar");
    expect(tabela).toHaveTextContent("Não é guardada: some ao fechar a página");
    expect(screen.getByRole("table", { name: /Prazos de guarda/ })).toHaveTextContent(
      "7 dias",
    );
  });

  it("declara que a vitrine não coleta do visitante", () => {
    window.history.pushState(null, "", "/o-que-coletamos");
    render(<App />);

    const declaracao = screen.getByText(/A vitrine não coleta nada de quem visita/);
    expect(declaracao.parentElement).toHaveTextContent(/sem login/i);
    expect(declaracao.parentElement).toHaveTextContent(/sem cookie de rastreio/i);
    expect(declaracao.parentElement).toHaveTextContent(/sem perfil do visitante/i);
  });

  it("abrir a área e recarregar não deixa rastro no aparelho", () => {
    window.history.pushState(null, "", "/o-que-coletamos");
    const primeira = render(<App />);
    primeira.unmount();
    render(<App />);

    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });
});
