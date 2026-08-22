import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configurarAcessoAoNucleo, ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as api from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: ({
      aoReceberIdToken,
    }: {
      aoReceberIdToken: (t: string) => void;
    }) => (
      <button type="button" onClick={() => aoReceberIdToken("id-token-de-teste")}>
        Entrar com Google
      </button>
    ),
  };
});

describe("entrada e sessão da App 09", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    limparToken();
  });

  it("sem sessão, só a entrada aparece", async () => {
    render(<App />);
    expect(await screen.findByText(/entre com a conta google/i)).toBeInTheDocument();
    expect(screen.queryByText(/comunidade game — mestre/i, { selector: "h1" })).not.toBeNull();
  });

  it("a chamada de login leva a chave desta aplicação", async () => {
    configurarAcessoAoNucleo({
      chaveDeAplicacao: "chave-da-app-09",
      urlDoNucleo: "https://nucleo.teste",
    });
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 401,
        json: () =>
          Promise.resolve({ codigo: "sessao_invalida", mensagem: "Sessão inexistente." }),
      }),
    );

    render(<App />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    await waitFor(() => expect(fetch).toHaveBeenCalled());
    const [, opcoes] = vi.mocked(fetch).mock.calls[0];
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-da-app-09");
  });

  it("Mestre com cadastro entra e alcança a autoria", async () => {
    vi.spyOn(api, "loginSocial").mockResolvedValue({
      token: "token-do-mestre",
      expira_em: new Date().toISOString(),
      papel: "mestre",
    });
    vi.spyOn(api, "eu").mockResolvedValue({
      persona_id: "algum-id",
      papel: "mestre",
      permissoes: {},
    });

    render(<App />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    expect(await screen.findByRole("button", { name: /sair/i })).toBeInTheDocument();
  });

  it("Guerreiro(a) é recusado(a) em linguagem simples, e a sessão nunca fica aberta", async () => {
    vi.spyOn(api, "loginSocial").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(api, "eu").mockResolvedValue({
      persona_id: "algum-id",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(api, "encerrarSessao").mockResolvedValue(undefined);

    render(<App />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/mestres/i);
    expect(recusa.textContent).not.toMatch(/guerreiro_|sessao_|erro_de_/i);
    expect(screen.queryByRole("button", { name: /sair/i })).not.toBeInTheDocument();
  });

  it("conta social sem cadastro lê a orientação de solicitar participação pela vitrine", async () => {
    vi.spyOn(api, "loginSocial").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "login_sem_cadastro",
        mensagem:
          "Esta conta não corresponde a nenhum cadastro. Solicite participação pela vitrine.",
      }),
    );

    render(<App />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/vitrine/i);
    expect(recusa.textContent).not.toMatch(/login_sem_cadastro/i);
  });

  it("sessão expirada devolve à entrada", async () => {
    sessionStorage.setItem("comunidade-game:token-de-sessao", "token-vencido");
    vi.spyOn(api, "eu").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "sessao_invalida",
        mensagem: "Sessão inexistente, encerrada ou expirada.",
      }),
    );

    render(<App />);

    expect(await screen.findByText(/entre com a conta google/i)).toBeInTheDocument();
  });

  it("recusa de chave tem desfecho diferente da recusa de sessão", async () => {
    vi.spyOn(api, "loginSocial").mockRejectedValue(
      new ErroDaApi(401, { codigo: "chave_invalida", mensagem: "Chave inválida." }),
    );

    render(<App />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/configuração/i);
    // A recusa de chave não devolve a nenhuma sessão anterior nem apresenta
    // a orientação da vitrine — é falha de implantação, não do cadastro.
    expect(screen.queryByText(/vitrine/i)).not.toBeInTheDocument();
  });
});
