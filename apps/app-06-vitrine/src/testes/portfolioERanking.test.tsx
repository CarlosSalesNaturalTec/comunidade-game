import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12: quem não autorizou não aparece em card,
// página, portfólio nem ranking; o ranking é de ponto regular; e, depois de
// navegar e recarregar, nada da visita ficou no aparelho.

function comConteudo() {
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({
    itens: [
      {
        trilha_id: "t-1",
        trilha: "Trilha da Água",
        validada_em: "2026-08-01T10:00:00Z",
        producao: "Produção de teste.",
        autores: [{ avatar: "avatar-de-teste", nick: "autora-da-obra" }],
      },
    ],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({
    itens: [
      { avatar: null, nick: "primeira-colocada", pontos_regulares: 40, posicao: 1 },
      { avatar: null, nick: "segunda-colocada", pontos_regulares: 20, posicao: 2 },
    ],
    proximo_cursor: null,
  });
}

function secaoDe(titulo: string) {
  const cabecalho = screen.getByRole("heading", { name: titulo, level: 2 });
  const secao = cabecalho.closest("section");
  if (!secao) throw new Error(`Seção não encontrada: ${titulo}`);
  return within(secao);
}

describe("portfólio e ranking", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    comConteudo();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    window.localStorage.clear();
    window.sessionStorage.clear();
  });

  it("a criação aparece com trilha, data e autoria por nick (RF-03-08)", async () => {
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    expect(await portfolio.findByText("Trilha da Água")).toBeVisible();
    expect(portfolio.getByText(/01\/08\/2026/)).toBeVisible();
    expect(portfolio.getByText(/autora-da-obra/)).toBeVisible();
  });

  it("o ranking é de ponto regular, em ordem (RF-03-09)", async () => {
    render(<App />);

    const ranking = secaoDe("Ranking");
    expect(await ranking.findByText(/primeira-colocada/)).toBeVisible();
    const posicoes = ranking.getAllByRole("listitem").map((item) => item.textContent);
    expect(posicoes[0]).toMatch(/1º.*primeira-colocada.*40 pontos regulares/);
    expect(posicoes[1]).toMatch(/2º.*segunda-colocada.*20 pontos regulares/);
    expect(ranking.queryByText(/ponto extra|moeda|R\$/i)).toBeNull();
  });

  it("a abertura não traz seção de poderes (RF-03-02)", async () => {
    render(<App />);

    // A seção saiu em 2026-10-11: ela prometia uma página individual de poder
    // que nunca existiu. O poder segue público como atributo do Guerreiro(a).
    expect(await screen.findByRole("heading", { name: "Ranking", level: 2 })).toBeVisible();
    expect(screen.queryByRole("heading", { name: "Poderes", level: 2 })).toBeNull();
    expect(screen.queryByText(/Mestres responsáveis/)).toBeNull();
  });

  it("a abertura abre pelo que o projeto produziu, e fecha no institucional", async () => {
    render(<App />);

    await screen.findByText(/primeira-colocada/);

    // A ordem é decisão do fundador de 2026-10-11, e mora na página do
    // recorte — nenhum `RF` a fixa. "Como apoiar" não tem tela pública.
    const titulos = screen
      .getAllByRole("heading", { level: 2 })
      .map((cabecalho) => cabecalho.textContent);
    expect(titulos).toEqual([
      "Ranking",
      "Portfólio de criações originais",
      "Guerreiros e Guerreiras",
      "Apoiadores",
      "Necessidades em aberto",
      "Mestres",
      "Comunidades Virtuais",
      "Construir sobre a API",
      "Quem somos",
      "Contatos",
    ]);
  });

  it("nada da visita fica no aparelho (RF-03-14, RN-03-22)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    expect(await screen.findByText(/primeira-colocada/)).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Início" }));

    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });
});
