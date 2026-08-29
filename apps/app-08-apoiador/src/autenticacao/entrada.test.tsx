import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as api from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

async function entrarComCredencial(usuario = "apoiadora", senha = "senha-provisoria") {
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), usuario);
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), senha);
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
}

describe("entrada e sessão da App 08", () => {
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
      await screen.findByRole("heading", { name: /comunidade game — apoiador/i }),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/^usuário$/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^sair$/i })).not.toBeInTheDocument();
  });

  it("Apoiador com senha provisória cai na troca, e nenhuma outra tela aparece", async () => {
    vi.spyOn(api, "loginPorCredencial").mockResolvedValue({
      token: "token-provisorio",
      expira_em: new Date().toISOString(),
      papel: "apoiador",
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
    expect(screen.queryByText(/propor desafio extra/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/meus desafios/i)).not.toBeInTheDocument();
  });

  it("trocada a senha, a área do Apoiador abre", async () => {
    vi.spyOn(api, "loginPorCredencial").mockResolvedValue({
      token: "token-provisorio",
      expira_em: new Date().toISOString(),
      papel: "apoiador",
    });
    vi.spyOn(api, "eu")
      .mockRejectedValueOnce(
        new ErroDaApi(403, {
          codigo: "troca_de_senha_pendente",
          mensagem: "Troque a senha provisória antes de continuar.",
        }),
      )
      .mockResolvedValue({ persona_id: "algum-id", papel: "apoiador", permissoes: {} });
    vi.spyOn(api, "trocarSenha").mockResolvedValue(undefined);

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

    expect(
      await screen.findByRole("button", { name: /propor desafio extra/i }),
    ).toBeInTheDocument();
  });

  it("login sem cadastro é recusado com a orientação do pré-cadastro", async () => {
    vi.spyOn(api, "loginPorCredencial").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "login_sem_cadastro",
        mensagem:
          "Esta conta não corresponde a nenhum cadastro. Solicite participação pelo pré-cadastro.",
      }),
    );

    render(<App />);
    await entrarComCredencial();

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/pré-cadastro/i);
    expect(recusa.textContent).not.toMatch(/login_sem_cadastro/i);
  });

  it("nenhuma tela oferece convite, delegação ou segundo acesso", async () => {
    vi.spyOn(api, "loginPorCredencial").mockResolvedValue({
      token: "token-do-apoiador",
      expira_em: new Date().toISOString(),
      papel: "apoiador",
    });
    vi.spyOn(api, "eu").mockResolvedValue({
      persona_id: "algum-id",
      papel: "apoiador",
      permissoes: {},
    });

    render(<App />);
    await entrarComCredencial();
    await screen.findByRole("button", { name: /propor desafio extra/i });

    expect(screen.queryByText(/convidar/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/delegar/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/segundo acesso/i)).not.toBeInTheDocument();
  });
});
