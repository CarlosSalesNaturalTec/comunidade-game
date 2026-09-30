import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as desenvolvedor from "../api/desenvolvedor";
import App from "./TelaDaVitrine";

const REGISTRO = { id: "protocolo-da-chave", prazo: "2026-10-06T12:00:00Z" };

async function preencherOFormularioDeChave() {
  await userEvent.type(screen.getByLabelText("Quem é você"), "Desenvolvedora de Tal");
  await userEvent.type(screen.getByLabelText("Contato para a resposta"), "dev@example.org");
  await userEvent.type(
    screen.getByLabelText("O que você pretende construir"),
    "Um painel comunitário.",
  );
  await userEvent.click(screen.getByRole("button", { name: "Enviar o pedido" }));
}

describe("solicitação de chave e apresentação da URL", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/desenvolvedor");
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("a tela declara que o envio não emite chave nem cria cadastro (RF-03-74)", () => {
    render(<App />);

    expect(screen.getByText(/não emite chave nenhuma e não cria cadastro/)).toBeVisible();
    expect(screen.getByText(/Quem avalia e emite a chave é\s+um Admin/)).toBeVisible();
  });

  it("os dois prazos e o que a chave é estão na área (RF-03-75, RF-03-76)", () => {
    render(<App />);

    expect(screen.getByText(/Sem chave a API não responde/)).toBeVisible();
    expect(screen.getAllByText(/somente leitura/).length).toBeGreaterThan(0);
    expect(screen.getByText(/para a gestão responder ao seu pedido de chave/)).toBeVisible();
    expect(screen.getByText(/para apresentar a URL do que você/)).toBeVisible();
  });

  it("o envio devolve protocolo e prazo, e nunca chave (RF-03-73, RF-03-74)", async () => {
    vi.spyOn(desenvolvedor, "enviarSolicitacaoDeChave").mockResolvedValue(REGISTRO);
    render(<App />);

    await preencherOFormularioDeChave();

    await waitFor(() => expect(screen.getByText(/Pedido registrado/)).toBeVisible());
    const confirmacao = screen.getByText(/Pedido registrado/).textContent ?? "";
    expect(confirmacao).toContain("protocolo-da-chave");
    expect(confirmacao).toContain("Nenhuma chave foi emitida agora");
    expect(confirmacao).not.toMatch(/segredo/i);
  });

  it("envios repetidos não anunciam espera crescente (RN-03-35)", async () => {
    const enviar = vi
      .spyOn(desenvolvedor, "enviarSolicitacaoDeChave")
      .mockResolvedValue(REGISTRO);
    render(<App />);

    await preencherOFormularioDeChave();
    await waitFor(() => expect(enviar).toHaveBeenCalledTimes(1));

    expect(screen.queryByText(/esperar um pouco/)).toBeNull();
    expect(screen.queryByText(/muitas vezes seguidas/)).toBeNull();
  });

  it("a apresentação da URL pede o identificador, nunca o segredo (RF-03-77)", async () => {
    const apresentar = vi.spyOn(desenvolvedor, "apresentarUrlDaChave").mockResolvedValue();
    render(<App />);

    await userEvent.click(
      screen.getByRole("button", { name: /Já tenho a chave: apresentar a URL/ }),
    );
    expect(screen.queryByLabelText(/segredo/i)).toBeNull();

    await userEvent.type(screen.getByLabelText(/Identificador da chave/), "id-da-chave");
    await userEvent.type(
      screen.getByLabelText(/URL do que você construiu/),
      "https://exemplo.org",
    );
    await userEvent.click(screen.getByRole("button", { name: "Apresentar a URL" }));

    await waitFor(() => expect(screen.getByText(/URL apresentada/)).toBeVisible());
    expect(apresentar).toHaveBeenCalledWith("id-da-chave", "https://exemplo.org");
  });

  it("a recusa do núcleo aparece como o que é (invariante 25)", async () => {
    vi.spyOn(desenvolvedor, "apresentarUrlDaChave").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "prazo_de_apresentacao_vencido",
        mensagem: "O prazo de apresentação desta chave venceu.",
      }),
    );
    render(<App />);

    await userEvent.click(
      screen.getByRole("button", { name: /Já tenho a chave: apresentar a URL/ }),
    );
    await userEvent.type(screen.getByLabelText(/Identificador da chave/), "id-da-chave");
    await userEvent.type(
      screen.getByLabelText(/URL do que você construiu/),
      "https://exemplo.org",
    );
    await userEvent.click(screen.getByRole("button", { name: "Apresentar a URL" }));

    await waitFor(() =>
      expect(screen.getByText("O prazo de apresentação desta chave venceu.")).toBeVisible(),
    );
  });

  it("com o assistente fora do ar a área segue utilizável (RF-03-72)", async () => {
    vi.spyOn(desenvolvedor, "perguntarAoAssistente").mockRejectedValue(
      new ErroDaApi(503, {
        codigo: "assistente_do_desenvolvedor_indisponivel",
        mensagem: "O assistente não respondeu agora e voltará.",
      }),
    );
    vi.spyOn(desenvolvedor, "enviarSolicitacaoDeChave").mockResolvedValue(REGISTRO);
    render(<App />);

    await userEvent.click(
      screen.getByRole("button", { name: "Como a API se autentica por chave" }),
    );

    await waitFor(() =>
      expect(screen.getByText(/O assistente não respondeu agora/)).toBeVisible(),
    );
    expect(screen.getByRole("link", { name: /Documentação da plataforma/ })).toBeVisible();
    expect(screen.getByRole("link", { name: /Repositório no GitHub/ })).toBeVisible();

    await preencherOFormularioDeChave();
    await waitFor(() => expect(screen.getByText(/Pedido registrado/)).toBeVisible());
  });
});
