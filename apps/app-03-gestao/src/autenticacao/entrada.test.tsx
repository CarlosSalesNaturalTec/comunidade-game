import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken, ProvedorDeSessao, useSessao } from "comum/autenticacao";
import * as api from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { TelaDeEntrada } from "./TelaDeEntrada";

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

function Conteudo() {
  const { sessao, restaurando, sair } = useSessao();
  if (restaurando) return <p>Restaurando…</p>;
  if (!sessao) return <TelaDeEntrada />;
  return (
    <div>
      <p>Sessão aberta como {sessao.papel}</p>
      <button type="button" onClick={sair}>
        Sair
      </button>
    </div>
  );
}

function renderizarApp() {
  return render(
    <ProvedorDeSessao>
      <Conteudo />
    </ProvedorDeSessao>,
  );
}

describe("entrada e sessão", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("sem sessão, nenhum dado de gestão aparece — só a entrada", async () => {
    renderizarApp();
    expect(await screen.findByText(/entre com a conta google/i)).toBeInTheDocument();
    expect(screen.queryByText(/sessão aberta/i)).not.toBeInTheDocument();
  });

  it("Admin com cadastro entra e recebe o papel do núcleo", async () => {
    vi.spyOn(api, "loginSocial").mockResolvedValue({
      token: "token-do-admin",
      expira_em: new Date().toISOString(),
      papel: "admin",
    });
    vi.spyOn(api, "eu").mockResolvedValue({
      persona_id: "algum-id",
      papel: "admin",
      permissoes: {},
    });

    renderizarApp();
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    expect(await screen.findByText(/sessão aberta como admin/i)).toBeInTheDocument();
  });

  it("conta social sem cadastro lê a orientação e nenhuma sessão abre", async () => {
    vi.spyOn(api, "loginSocial").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "login_sem_cadastro",
        mensagem:
          "Esta conta não corresponde a nenhum cadastro. Solicite participação pela vitrine.",
      }),
    );

    renderizarApp();
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/vitrine/i);
    expect(screen.queryByText(/sessão aberta/i)).not.toBeInTheDocument();
  });

  it("sessão expirada devolve à entrada", async () => {
    sessionStorage.setItem("comunidade-game:token-de-sessao", "token-vencido");
    vi.spyOn(api, "eu").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "sessao_invalida",
        mensagem: "Sessão inexistente, encerrada ou expirada.",
      }),
    );

    renderizarApp();

    expect(await screen.findByText(/entre com a conta google/i)).toBeInTheDocument();
  });

  it("a saída encerra a sessão no núcleo e volta à entrada", async () => {
    vi.spyOn(api, "loginSocial").mockResolvedValue({
      token: "token-do-admin",
      expira_em: new Date().toISOString(),
      papel: "admin",
    });
    vi.spyOn(api, "eu").mockResolvedValue({
      persona_id: "algum-id",
      papel: "admin",
      permissoes: {},
    });
    const encerrarSessaoEspiado = vi.spyOn(api, "encerrarSessao").mockResolvedValue(undefined);

    renderizarApp();
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));
    await screen.findByText(/sessão aberta como admin/i);

    await usuario.click(screen.getByRole("button", { name: /sair/i }));

    await waitFor(() => expect(encerrarSessaoEspiado).toHaveBeenCalledWith("token-do-admin"));
    expect(await screen.findByText(/entre com a conta google/i)).toBeInTheDocument();
  });
});
