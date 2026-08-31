import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as api from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as vinculadosApi from "../vinculados/api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

async function entrarComCredencial(usuario = "mae-da-zeferina", senha = "senha-provisoria") {
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), usuario);
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), senha);
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
}

describe("entrada e sessão da App 07", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("sem sessão, só a entrada aparece", async () => {
    render(<App />);
    expect(
      await screen.findByRole("heading", { name: /comunidade game — responsáveis/i }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/^usuário$/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^sair$/i })).not.toBeInTheDocument();
  });

  it("responsável com senha provisória cai na troca, e nenhuma outra tela aparece", async () => {
    vi.spyOn(api, "loginPorCredencial").mockResolvedValue({
      token: "token-provisorio",
      expira_em: new Date().toISOString(),
      papel: "responsavel",
    });
    vi.spyOn(api, "eu").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "troca_de_senha_pendente",
        mensagem: "Troque a senha provisória antes de continuar.",
      }),
    );

    render(<App />);
    await entrarComCredencial();

    expect(
      await screen.findByRole("heading", { name: /troque sua senha/i }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/seus vinculados/i)).not.toBeInTheDocument();
  });

  it("trocada a senha, a lista dos vinculados abre", async () => {
    vi.spyOn(api, "loginPorCredencial").mockResolvedValue({
      token: "token-provisorio",
      expira_em: new Date().toISOString(),
      papel: "responsavel",
    });
    vi.spyOn(api, "eu")
      .mockRejectedValueOnce(
        new ErroDaApi(403, {
          codigo: "troca_de_senha_pendente",
          mensagem: "Troque a senha provisória antes de continuar.",
        }),
      )
      .mockResolvedValue({ persona_id: "algum-id", papel: "responsavel", permissoes: {} });
    vi.spyOn(api, "trocarSenha").mockResolvedValue(undefined);
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([]);

    render(<App />);
    await entrarComCredencial();
    await screen.findByRole("heading", { name: /troque sua senha/i });

    const testeDeUsuario = userEvent.setup();
    await testeDeUsuario.type(screen.getByLabelText(/^senha nova$/i), "senha-nova-123");
    await testeDeUsuario.type(
      screen.getByLabelText(/confirme a senha nova/i),
      "senha-nova-123",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /trocar senha/i }));

    expect(await screen.findByText(/nenhum vinculado ainda/i)).toBeInTheDocument();
  });

  it("login sem cadastro é recusado com a orientação de procurar a gestão", async () => {
    vi.spyOn(api, "loginPorCredencial").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "login_sem_cadastro",
        mensagem:
          "Esta conta não corresponde a nenhum cadastro. Procure a gestão no encontro.",
      }),
    );

    render(<App />);
    await entrarComCredencial();

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/procure a gestão/i);
    expect(recusa.textContent).not.toMatch(/login_sem_cadastro/i);
  });

  it("nenhuma tela oferece autocadastro, cadastro de responsável ou de vínculo", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — responsáveis/i });

    expect(screen.queryByText(/cadastr(e|ar)-se/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /criar vínculo/i })).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /cadastrar responsável/i }),
    ).not.toBeInTheDocument();
  });
});
