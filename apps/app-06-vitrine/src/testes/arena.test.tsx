import { render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as leituras from "../api/leituras";
import { PaginaDoGuerreiro } from "../guerreiros/PaginaDoGuerreiro";
import { SecaoDePoderes } from "../poderes/SecaoDePoderes";

/**
 * O **nível 1** da Arena na vitrine (design — decisão 6): o que se afirma
 * sobre componente montado, e não sobre o arquivo servido.
 *
 * A moldura de fundo e a presença dela em toda rota são afirmação sobre o
 * `dist/`, e ficam no `saidaDoBuild.test.ts`.
 */

const GUERREIRA: leituras.GuerreiroPublico = {
  avatar: null,
  nick: "ZeBita",
  badges: [{ familia: "percurso", poder: null }],
  poderes: [{ poder: "Poder do Território", nivel: 2 }],
  pontos_regulares: 40,
  posicao_no_ranking: 1,
  criacoes: [{ trilha: "Trilha 1", validada_em: "2026-09-01" }],
};

afterEach(() => {
  vi.restoreAllMocks();
});

describe("a carta domina a página individual", () => {
  it("apresenta a carta no palco, e o portfólio abaixo dela (RF-03-03, RF-03-05)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockResolvedValue(GUERREIRA);
    render(<PaginaDoGuerreiro nick="ZeBita" />);

    const palco = await screen.findByRole("region", { name: "Página de ZeBita" });
    expect(palco).toBeVisible();

    // A apresentação vem antes do apoio no documento, que é o que põe a
    // carta em primeiro plano e o portfólio abaixo dela.
    const apresentacao = palco.querySelector(".cg-palco__personagem");
    const apoio = palco.querySelector(".cg-palco__apoio");
    expect(apresentacao).not.toBeNull();
    expect(apoio).not.toBeNull();
    expect(apresentacao?.compareDocumentPosition(apoio as Node)).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING,
    );
    expect(
      within(apoio as HTMLElement).getByRole("heading", { name: "Portfólio" }),
    ).toBeVisible();
  });

  it("pede uma decisão só, e sair não é decisão (documento 15 §6)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockResolvedValue(GUERREIRA);
    render(<PaginaDoGuerreiro nick="ZeBita" />);

    const palco = await screen.findByRole("region", { name: "Página de ZeBita" });
    const decisao = palco.querySelector(".cg-palco__decisao");
    expect(decisao).not.toBeNull();

    // "Voltar à vitrine" existe, e fica **fora** do palco: é saída.
    expect(screen.getByRole("button", { name: "Voltar à vitrine" })).toBeVisible();
    expect(palco.contains(screen.getByRole("button", { name: "Voltar à vitrine" }))).toBe(
      false,
    );
  });

  it("a tela de não encontrado não monta palco nem convida a nada (RF-03-11)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockRejectedValue(new Error("fora"));
    render(<PaginaDoGuerreiro nick="nao-existe" />);

    expect(await screen.findByText(/Não foi possível carregar a página/)).toBeVisible();
    expect(screen.queryByRole("region", { name: /Página de/ })).toBeNull();
  });
});

describe("o glifo de poder acompanha o nome", () => {
  it("apresenta o glifo ao lado do nome, nunca no lugar dele (documento 15 §8.4)", async () => {
    vi.spyOn(leituras, "listarPoderes").mockResolvedValue([
      {
        id: "p-1",
        nome: "Poder do Território",
        descricao: "Ler o lugar onde se vive.",
        trilhas: [],
        mestres_responsaveis: [],
      } as unknown as leituras.PoderPublico,
    ]);
    render(<SecaoDePoderes />);

    const titulo = await screen.findByRole("heading", { name: "Poder do Território" });
    expect(titulo).toBeVisible();
    // O nome segue no documento: o glifo é acompanhamento, e o texto é o que
    // identifica o poder.
    expect(titulo.textContent).toContain("Poder do Território");
    expect(titulo.querySelector("svg")).not.toBeNull();
  });
});
