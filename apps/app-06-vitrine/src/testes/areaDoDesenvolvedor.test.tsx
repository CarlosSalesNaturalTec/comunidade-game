import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as desenvolvedor from "../api/desenvolvedor";
import { TEXTO_DA_ABERTURA } from "../desenvolvedor/abertura";
import App from "./TelaDaVitrine";

function abrirAArea() {
  window.history.pushState(null, "", "/desenvolvedor");
}

describe("Área do Apoiador Desenvolvedor", () => {
  beforeEach(() => {
    abrirAArea();
  });
  afterEach(() => {
    vi.restoreAllMocks();
    window.localStorage.clear();
  });

  it("abre com as quatro coisas do RF-03-67, sem pedir login", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: /Área do Apoiador Desenvolvedor/ }),
    ).toBeVisible();
    expect(screen.getByRole("heading", { name: /Converse com o assistente/ })).toBeVisible();
    expect(screen.getByRole("link", { name: /Documentação da plataforma/ })).toBeVisible();
    expect(screen.getByRole("link", { name: /Repositório no GitHub/ })).toBeVisible();
    expect(screen.getByRole("heading", { name: /Peça a sua chave/ })).toBeVisible();
    expect(screen.queryByLabelText(/senha/i)).toBeNull();
  });

  it("a abertura chega sem pergunta e sem nenhuma chamada ao núcleo (RF-03-68)", () => {
    const perguntar = vi.spyOn(desenvolvedor, "perguntarAoAssistente");

    render(<App />);

    expect(screen.getByText(new RegExp(TEXTO_DA_ABERTURA.slice(0, 40)))).toBeVisible();
    expect(perguntar).not.toHaveBeenCalled();
  });

  it("toda mensagem termina com a pergunta de múltipla escolha (RF-03-69)", async () => {
    vi.spyOn(desenvolvedor, "perguntarAoAssistente").mockResolvedValue({
      desfecho: "respondida",
      resposta: "A chave vai no cabeçalho de toda chamada.",
      opcoes: ["Como pedir a chave"],
    });
    render(<App />);

    expect(
      screen.getByRole("group", { name: /O que você quer conhecer agora/ }),
    ).toBeVisible();
    await userEvent.click(
      screen.getByRole("button", { name: "Como a API se autentica por chave" }),
    );

    await waitFor(() => expect(screen.getByText(/A chave vai no cabeçalho/)).toBeVisible());
    expect(screen.getByRole("button", { name: "Como pedir a chave" })).toBeVisible();
  });

  it("a recusa fora do corpus também vem com a escolha do próximo passo", async () => {
    vi.spyOn(desenvolvedor, "perguntarAoAssistente").mockResolvedValue({
      desfecho: "fora_do_corpus",
      resposta: "Esse assunto não está na documentação.",
      opcoes: ["Como a plataforma está montada"],
    });
    render(<App />);

    await userEvent.type(
      screen.getByLabelText(/Ou pergunte o que quiser/),
      "Qual o clima hoje?",
    );
    await userEvent.click(screen.getByRole("button", { name: "Perguntar" }));

    await waitFor(() => expect(screen.getByText(/não está na documentação/)).toBeVisible());
    expect(
      screen.getByRole("button", { name: "Como a plataforma está montada" }),
    ).toBeVisible();
  });

  it("a pergunta livre leva os turnos anteriores, e nada vai ao aparelho (RN-03-15)", async () => {
    const perguntar = vi.spyOn(desenvolvedor, "perguntarAoAssistente").mockResolvedValue({
      desfecho: "respondida",
      resposta: "Resposta.",
      opcoes: ["Outra"],
    });
    render(<App />);

    await userEvent.type(screen.getByLabelText(/Ou pergunte o que quiser/), "Como funciona?");
    await userEvent.click(screen.getByRole("button", { name: "Perguntar" }));

    await waitFor(() => expect(perguntar).toHaveBeenCalled());
    const [texto, historico] = perguntar.mock.calls[0];
    expect(texto).toBe("Como funciona?");
    expect(historico).toHaveLength(1);
    expect(historico[0].de).toBe("assistente");
    expect(window.localStorage.length).toBe(0);
  });

  it("recarregar a página perde a conversa inteira (PRD-03 §8)", async () => {
    vi.spyOn(desenvolvedor, "perguntarAoAssistente").mockResolvedValue({
      desfecho: "respondida",
      resposta: "Resposta que não sobrevive.",
      opcoes: ["Outra"],
    });
    const { unmount } = render(<App />);

    await userEvent.type(screen.getByLabelText(/Ou pergunte o que quiser/), "Como funciona?");
    await userEvent.click(screen.getByRole("button", { name: "Perguntar" }));
    await waitFor(() => expect(screen.getByText(/não sobrevive/)).toBeVisible());

    unmount();
    abrirAArea();
    render(<App />);

    expect(screen.queryByText(/não sobrevive/)).toBeNull();
    expect(screen.getByText(new RegExp(TEXTO_DA_ABERTURA.slice(0, 40)))).toBeVisible();
    expect(window.localStorage.length).toBe(0);
  });

  it("a área é alcançada pela vitrine, como seção (RN-03-29)", async () => {
    window.history.pushState(null, "", "/");
    render(<App />);

    await userEvent.click(
      screen.getByRole("button", { name: /Abrir a Área do Apoiador Desenvolvedor/ }),
    );

    expect(
      screen.getByRole("heading", { name: /Área do Apoiador Desenvolvedor/ }),
    ).toBeVisible();
  });
});
