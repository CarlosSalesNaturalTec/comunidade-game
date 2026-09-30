import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { GuerreiroPublico } from "../api/leituras";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12: a busca por nick inexistente e por nick
// sem autorização devolvem **a mesma** resposta, e repetir a busca da mesma
// origem produz espera crescente, sem CAPTCHA e sem pedir cadastro.

const GUERREIRA: GuerreiroPublico = {
  avatar: "avatar-de-teste",
  nick: "guerreira-procurada",
  badges: [],
  poderes: [],
  pontos_regulares: 10,
  posicao_no_ranking: 1,
  criacoes: [],
};

function semNadaNasOutrasSecoes() {
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);
}

function recusa(status: number, codigo: string, tempoDeEsperaEmSegundos?: number) {
  return new ErroDaApi(
    status,
    { codigo, mensagem: "Guerreiro(a) não encontrado(a)." },
    tempoDeEsperaEmSegundos,
  );
}

describe("a busca é por nick exato", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    semNadaNasOutrasSecoes();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("o nick exato leva à página pública (RF-03-11)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockResolvedValue(GUERREIRA);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.type(screen.getByLabelText("Nick exato"), "guerreira-procurada");
    await testeDeUsuario.click(screen.getByRole("button", { name: "Procurar" }));

    expect(window.location.pathname).toBe("/guerreiros/guerreira-procurada");
    expect(
      await screen.findByRole("heading", { name: "guerreira-procurada", level: 2 }),
    ).toBeVisible();
  });

  it("não sugere, não completa e não lista nicks (RF-03-12, RN-03-06)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockResolvedValue(GUERREIRA);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.type(screen.getByLabelText("Nick exato"), "guerr");

    expect(screen.queryByRole("listbox")).toBeNull();
    expect(screen.queryByRole("option")).toBeNull();
    expect(document.querySelector("datalist")).toBeNull();
    expect(leituras.obterGuerreiroPorNick).not.toHaveBeenCalled();
  });

  it("nick inexistente e nick sem autorização recebem a mesma tela (RN-03-07)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockRejectedValue(
      recusa(404, "nao_encontrado"),
    );

    window.history.pushState(null, "", "/guerreiros/nao-existe");
    const inexistente = render(<App />);
    const textoDoInexistente = (await screen.findByRole("alert")).textContent;
    inexistente.unmount();

    window.history.pushState(null, "", "/guerreiros/sem-autorizacao");
    render(<App />);
    const textoDoSemAutorizacao = (await screen.findByRole("alert")).textContent;

    expect(textoDoInexistente).toBe(textoDoSemAutorizacao);
    expect(textoDoSemAutorizacao).toMatch(/não encontrado/i);
    expect(textoDoSemAutorizacao).not.toMatch(/autoriza|revog|consentimento/i);
  });

  it("a repetição freada explica motivo e espera, sem CAPTCHA nem cadastro (RF-03-36, RF-03-37)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockRejectedValue(
      recusa(429, "freio_por_origem_acionado", 8),
    );
    window.history.pushState(null, "", "/guerreiros/guerreira-procurada");
    const { container } = render(<App />);

    const aviso = await screen.findByRole("alert");
    expect(aviso.textContent).toMatch(/muitas consultas seguidas/i);
    expect(aviso.textContent).toMatch(/8 segundos/);

    expect(container.textContent).not.toMatch(/captcha/i);
    expect(
      screen.queryByRole("button", { name: /cadastrar|criar conta|entrar para ver/i }),
    ).toBeNull();
    expect(screen.queryByLabelText(/senha/i)).not.toBeInTheDocument();
  });

  it("a espera em minutos sai em linguagem simples (RF-03-36)", async () => {
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockRejectedValue(
      recusa(429, "freio_por_origem_acionado", 120),
    );
    window.history.pushState(null, "", "/guerreiros/guerreira-procurada");
    render(<App />);

    expect((await screen.findByRole("alert")).textContent).toMatch(/2 minutos/);
  });
});
