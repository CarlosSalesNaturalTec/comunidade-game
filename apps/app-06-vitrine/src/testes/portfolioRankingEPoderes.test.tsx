import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as leituras from "../api/leituras";

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
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([
    {
      id: "p-1",
      nome: "Poder do Território",
      descricao: "Ler e cuidar do lugar onde se vive.",
      trilhas: [{ id: "t-1", nome: "Trilha da Água" }],
    },
  ]);
}

function secaoDe(titulo: string) {
  const cabecalho = screen.getByRole("heading", { name: titulo, level: 2 });
  const secao = cabecalho.closest("section");
  if (!secao) throw new Error(`Seção não encontrada: ${titulo}`);
  return within(secao);
}

describe("portfólio, ranking e poderes", () => {
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

  it("a seção de poderes traz as trilhas e não promete Mestres (RF-03-02)", async () => {
    render(<App />);

    const poderes = secaoDe("Poderes");
    expect(await poderes.findByText("Poder do Território")).toBeVisible();
    expect(poderes.getByText("Trilha da Água")).toBeVisible();
    expect(poderes.queryByText(/mestre/i)).toBeNull();
  });

  it("nada da visita fica no aparelho (RF-03-14, RN-03-22)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    expect(await screen.findByText("Poder do Território")).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sociedade civil" }));

    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });
});
