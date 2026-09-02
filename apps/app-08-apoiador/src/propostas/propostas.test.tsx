import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as preCadastroApi from "../preCadastro/api";
import type { PropostaDoAutor } from "./api";
import * as propostasApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

async function entrarComoApoiador() {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-apoiador",
    expira_em: new Date().toISOString(),
    papel: "apoiador",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: "apoiador-1",
    papel: "apoiador",
    permissoes: {},
  });

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "apoiadora");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^propostas$/i }));
  return testeDeUsuario;
}

describe("tela de propostas", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(preCadastroApi, "listarNecessidadesEmAberto").mockResolvedValue([]);
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a proposta é registrada e entra na fila única, sem promessa de e-mail nem de ponto", async () => {
    vi.spyOn(propostasApi, "registrarProposta").mockResolvedValue({
      id: "proposta-1",
      prazo: "2026-09-08T10:00:00Z",
    });

    const testeDeUsuario = await entrarComoApoiador();
    await testeDeUsuario.type(
      screen.getByLabelText(/^proposta$/i),
      "Que tal um mural de recados da comunidade?",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar proposta/i }));

    expect(propostasApi.registrarProposta).toHaveBeenCalledWith(
      "Que tal um mural de recados da comunidade?",
      "token-do-apoiador",
    );
    expect(
      screen.queryByText(/\b(ponto[s]?|badge|moeda[s]?|selo|nível)\b/i),
    ).not.toBeInTheDocument();
  });

  it("o retorno chega com o motivo em linguagem simples, dentro da plataforma", async () => {
    const propostaNaoAdotada: PropostaDoAutor = {
      id: "proposta-2",
      alvo_tipo: "plataforma",
      alvo_id: null,
      texto: "Proposta antiga.",
      situacao: "nao_adotada",
      prazo: "2026-09-01T10:00:00Z",
      em_atraso: false,
      motivo_do_retorno: "Já existe um recurso parecido no momento.",
      decidido_em: "2026-08-20T10:00:00Z",
    };
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([propostaNaoAdotada]);

    await entrarComoApoiador();

    expect(
      await screen.findByText(/já existe um recurso parecido no momento/i),
    ).toBeInTheDocument();
  });

  it("a tela não promete aviso por e-mail", async () => {
    await entrarComoApoiador();

    expect(
      await screen.findByText(/o retorno chega dentro da plataforma/i),
    ).toBeInTheDocument();
  });

  it("o aviso de coleta nomeia o dado desta tela e leva a Direitos e dados, sem bloquear o envio", async () => {
    vi.spyOn(propostasApi, "registrarProposta").mockResolvedValue({
      id: "proposta-3",
      prazo: "2026-09-08T10:00:00Z",
    });

    const testeDeUsuario = await entrarComoApoiador();

    expect(await screen.findByText(/coleta o texto da sua proposta/i)).toBeInTheDocument();

    await testeDeUsuario.click(
      screen.getByRole("button", { name: /ver em direitos e dados/i }),
    );
    expect(
      await screen.findByRole("heading", { name: /^direitos e dados$/i }),
    ).toBeInTheDocument();

    await testeDeUsuario.click(screen.getByRole("button", { name: /^propostas$/i }));
    await testeDeUsuario.type(screen.getByLabelText(/^proposta$/i), "Proposta nova.");
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar proposta/i }));
    expect(propostasApi.registrarProposta).toHaveBeenCalled();
  });
});
