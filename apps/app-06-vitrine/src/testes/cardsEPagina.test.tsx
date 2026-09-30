import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { GuerreiroPublico } from "../api/leituras";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12 para os cards e a página individual:
// Guerreiro(a) com autorização aparece em card e página; o card abre a
// página; e nenhuma tela exibe imagem real, nome civil, rede social ou
// contato.

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

function comLeituras(guerreiros: GuerreiroPublico[]) {
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: guerreiros,
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "obterGuerreiroPorNick").mockImplementation(async (nick) => {
    const achado = guerreiros.find((item) => item.nick === nick);
    if (!achado) throw new Error("não encontrado");
    return achado;
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);
}

/** O efeito que arma a rotação só corre depois que a leitura chega: o
 * primeiro `act` descarrega os efeitos pendentes, e o segundo faz o tempo
 * passar sobre o temporizador já armado. */
async function passarOTempo(ms: number) {
  await act(async () => {});
  await act(async () => {
    vi.advanceTimersByTime(ms);
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
    vi.useFakeTimers({ shouldAdvanceTime: true });
    declararMovimentoReduzido(false);
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("os cards rotacionam a cada 5 segundos (RF-03-04)", async () => {
    comLeituras([guerreiro("primeira"), guerreiro("segunda", 2)]);
    render(<App />);

    expect(await screen.findByText("primeira")).toBeVisible();
    await passarOTempo(5000);

    expect(screen.getByText("segunda")).toBeVisible();
    expect(screen.queryByText("primeira")).toBeNull();
  });

  it("com movimento reduzido não há rotação, e todos seguem alcançáveis (RF-03-04)", async () => {
    declararMovimentoReduzido(true);
    comLeituras([guerreiro("primeira"), guerreiro("segunda", 2)]);
    render(<App />);

    expect(await screen.findByText("primeira")).toBeVisible();
    await passarOTempo(20000);

    expect(screen.getByText("primeira")).toBeVisible();
    // A rotação nunca é a única via ao conteúdo (documento 15 §§5, 8.1).
    expect(screen.getByRole("button", { name: /próximo card/i })).toBeVisible();
  });

  it("o card exibe só avatar, nick, badges, poderes e desempenho (RF-03-05, RF-03-06)", async () => {
    comLeituras([guerreiro("guerreira-do-card")]);
    const { container } = render(<App />);

    expect(await screen.findByText("guerreira-do-card")).toBeVisible();
    expect(screen.getByText(/1º no ranking · 40 pontos regulares/)).toBeVisible();
    expect(screen.getByText("Poder do Código", { selector: "*" })).toBeTruthy();

    expect(container.textContent).not.toMatch(/nome civil|nascimento|whatsapp|instagram/i);
    expect(container.querySelector('a[href^="mailto:"]')).toBeNull();
    expect(container.querySelector('a[href^="tel:"]')).toBeNull();
  });

  it("o card abre a página individual, em endereço próprio (RF-03-03)", async () => {
    comLeituras([guerreiro("guerreira-da-pagina")]);
    render(<App />);
    const testeDeUsuario = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: /abrir a página de guerreira-da-pagina/i }),
    );

    expect(window.location.pathname).toBe("/guerreiros/guerreira-da-pagina");
    expect(
      await screen.findByRole("heading", { name: "guerreira-da-pagina", level: 2 }),
    ).toBeVisible();
  });

  it("o endereço direto resolve a página (RF-03-03)", async () => {
    comLeituras([guerreiro("guerreira-direta")]);
    window.history.pushState(null, "", "/guerreiros/guerreira-direta");
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "guerreira-direta", level: 2 }),
    ).toBeVisible();
    // A trilha aparece na carta e no portfólio da página — as duas leituras
    // vêm da mesma composição.
    expect(screen.getAllByText(/Trilha da Água/).length).toBeGreaterThan(0);
  });

  it("carta incompleta não se apresenta (documento 11 §8.2)", async () => {
    const incompleta = {
      avatar: null,
      nick: "guerreira-incompleta",
    } as unknown as GuerreiroPublico;
    vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
      itens: [incompleta],
      proximo_cursor: null,
    });
    vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
    vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);

    render(<App />);

    expect(await screen.findByText(/veio incompleta/i)).toBeVisible();
    expect(document.querySelector(".cg-carta")).toBeNull();
  });
});
