import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { CriacaoPublica, GuerreiroPublico, ItemDeRankingPublico } from "../api/leituras";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12 para a seção de Guerreiros e Guerreiras e
// a página individual: a seção traz **só a consulta por nick exato**, nenhuma
// tela pública rotaciona conteúdo, e a página individual segue alcançável
// pela consulta, pela linha do ranking e pelo nick do autor no portfólio
// (`RF-03-03`, `RF-03-11`, `RF-03-12`, `RF-03-13`).

function guerreiro(nick: string, posicao = 1): GuerreiroPublico {
  return {
    avatar: "avatar-de-teste",
    nick,
    badges: [{ familia: "de_nivel", poder: "Poder do Código" }],
    poderes: [{ poder: "Poder do Código", nivel: 3 }],
    pontos_regulares: 40,
    posicao_no_ranking: posicao,
    criacoes: [{ trilha: "Trilha da Água", validada_em: "2026-08-01T10:00:00Z" }],
  };
}

function noRanking(nick: string, posicao = 1): ItemDeRankingPublico {
  return { avatar: "avatar-de-teste", nick, pontos_regulares: 40, posicao };
}

function noPortfolio(nick: string): CriacaoPublica {
  return {
    trilha_id: "t-1",
    trilha: "Trilha da Água",
    validada_em: "2026-08-01T10:00:00Z",
    producao: "Produção de teste.",
    autores: [{ avatar: "avatar-de-teste", nick }],
  };
}

function comLeituras({
  guerreiros = [] as GuerreiroPublico[],
  ranking = [] as ItemDeRankingPublico[],
  criacoes = [] as CriacaoPublica[],
} = {}) {
  vi.spyOn(leituras, "obterGuerreiroPorNick").mockImplementation(async (nick) => {
    const achado = guerreiros.find((item) => item.nick === nick);
    if (!achado) throw new Error("não encontrado");
    return achado;
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({
    itens: criacoes,
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({
    itens: ranking,
    proximo_cursor: null,
  });
}

function declararMovimentoReduzido(reduzido: boolean) {
  vi.stubGlobal("matchMedia", (consulta: string) => ({
    matches: reduzido && consulta.includes("prefers-reduced-motion"),
    media: consulta,
    addEventListener: () => {},
    removeEventListener: () => {},
  }));
}

describe("a seção de Guerreiros e Guerreiras", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    declararMovimentoReduzido(false);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("traz a consulta por nick exato e nenhum Guerreiro(a) (RF-03-12, RF-03-13)", async () => {
    comLeituras({ guerreiros: [guerreiro("heroina-do-bairro")] });
    render(<App />);

    const secao = (
      await screen.findByRole("heading", { name: "Guerreiros e Guerreiras" })
    ).closest("section") as HTMLElement;

    expect(secao.querySelector('form[aria-label="Procurar por nick"]')).not.toBeNull();
    expect(secao.textContent).toMatch(/A vitrine não lista quem está cadastrado/);
    // Nenhum Guerreiro(a) é apresentado: nem lista, nem card, nem paginação.
    expect(secao.textContent).not.toContain("heroina-do-bairro");
    expect(secao.querySelector(".cg-lista-de-registros")).toBeNull();
    expect(secao.querySelector(".cg-carta")).toBeNull();
  });

  it("nenhuma tela pública rotaciona conteúdo (RF-03-13)", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    comLeituras({
      guerreiros: [guerreiro("primeira"), guerreiro("segunda", 2)],
      ranking: [noRanking("primeira"), noRanking("segunda", 2)],
      criacoes: [noPortfolio("primeira")],
    });
    const { container } = render(<App />);

    expect(await screen.findAllByText("primeira")).not.toHaveLength(0);
    const antes = container.textContent;
    await act(async () => {
      vi.advanceTimersByTime(20000);
    });

    // Nada troca sozinho: a rotação saiu com a listagem (`RF-03-04`
    // removido), e nenhuma outra seção a reintroduziu.
    expect(container.textContent).toBe(antes);
    expect(screen.queryByRole("button", { name: /próximo card|card anterior/i })).toBeNull();
    vi.useRealTimers();
  });

  it("a consulta por nick exato leva à página individual (RF-03-11, RF-03-12)", async () => {
    comLeituras({ guerreiros: [guerreiro("guerreira-da-consulta")] });
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.type(screen.getByLabelText("Nick exato"), "guerreira-da-consulta");
    await testeDeUsuario.click(screen.getByRole("button", { name: "Procurar" }));

    expect(window.location.pathname).toBe("/guerreiros/guerreira-da-consulta");
    expect(
      await screen.findByRole("heading", { name: "guerreira-da-consulta", level: 2 }),
    ).toBeVisible();
  });

  it("a linha do ranking e o nick do portfólio apontam à página (RF-03-03)", async () => {
    comLeituras({
      guerreiros: [guerreiro("guerreira-da-linha")],
      ranking: [noRanking("guerreira-da-linha")],
      criacoes: [noPortfolio("guerreira-da-linha")],
    });
    render(<App />);

    const portas = await screen.findAllByRole("link", { name: /guerreira-da-linha/ });
    // Duas portas: a linha do ranking e o nick do autor no portfólio. As duas
    // levam ao **mesmo endereço próprio** (`RF-03-03`).
    expect(portas).toHaveLength(2);
    for (const porta of portas) {
      expect(porta).toHaveAttribute("href", "/guerreiros/guerreira-da-linha");
    }
  });

  it("o endereço direto resolve a página (RF-03-03)", async () => {
    comLeituras({ guerreiros: [guerreiro("guerreira-direta")] });
    window.history.pushState(null, "", "/guerreiros/guerreira-direta");
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "guerreira-direta", level: 2 }),
    ).toBeVisible();
    // A trilha aparece na carta e no portfólio da página — as duas leituras
    // vêm da mesma composição.
    expect(screen.getAllByText(/Trilha da Água/).length).toBeGreaterThan(0);
  });

  it("a página exibe só avatar, nick, badges, poderes e desempenho (RF-03-05, RF-03-06)", async () => {
    comLeituras({ guerreiros: [guerreiro("guerreira-da-pagina")] });
    window.history.pushState(null, "", "/guerreiros/guerreira-da-pagina");
    const { container } = render(<App />);

    expect(
      await screen.findByRole("heading", { name: "guerreira-da-pagina", level: 2 }),
    ).toBeVisible();
    expect(screen.getByText(/1º no ranking · 40 pontos regulares/)).toBeVisible();
    // O poder continua público **como atributo do Guerreiro(a)**, embora a
    // seção de poderes tenha saído da vitrine em 2026-10-11: é aqui que o
    // `RF-03-05` o exige, e não numa seção própria.
    expect(screen.getByText("Poder do Código", { selector: "*" })).toBeTruthy();

    expect(container.textContent).not.toMatch(/nome civil|nascimento|whatsapp|instagram/i);
    expect(container.querySelector('a[href^="mailto:"]')).toBeNull();
    expect(container.querySelector('a[href^="tel:"]')).toBeNull();
  });

  it("carta incompleta não se apresenta (documento 11 §8.2)", async () => {
    const incompleta = {
      avatar: null,
      nick: "guerreira-incompleta",
    } as unknown as GuerreiroPublico;
    comLeituras({ guerreiros: [incompleta] });
    window.history.pushState(null, "", "/guerreiros/guerreira-incompleta");
    render(<App />);

    expect(await screen.findByText(/veio incompleta/i)).toBeVisible();
    expect(document.querySelector(".cg-carta")).toBeNull();
  });
});
