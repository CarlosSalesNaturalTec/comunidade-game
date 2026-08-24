import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App, { CHAVE_DE_SESSAO_DE_TRABALHO } from "../App";
import type { AulaVigente } from "../api/aulas";
import * as aulasApi from "../api/aulas";
import * as comunidadesApi from "../api/comunidades";

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

function aula(sobrescreve: Partial<AulaVigente> = {}): AulaVigente {
  return {
    id: "aula-1",
    comunidade_virtual_id: "comunidade-1",
    inicio_em: "2026-08-24T10:00:00-03:00",
    fim_em: "2026-08-24T12:00:00-03:00",
    ...sobrescreve,
  };
}

async function entrarComoMestre() {
  const usuario = userEvent.setup();
  await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));
}

beforeEach(() => {
  limparToken(CHAVE_DE_SESSAO_DE_TRABALHO);
  limparToken("app-01:sessao-guerreiro");
  sessionStorage.removeItem("app-01:sessao-trabalho:aula");
});

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("sessão de trabalho do aparelho", () => {
  it("sem aula vigente, a aplicação não abre e explica em uma frase", async () => {
    vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
      token: "token-do-mestre",
      expira_em: new Date().toISOString(),
      papel: "mestre",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "mestre-1",
      papel: "mestre",
      permissoes: {},
    });
    vi.spyOn(aulasApi, "listarAulasVigentes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<App />);
    await entrarComoMestre();

    expect(await screen.findByText(/não há aula agendada/i)).toBeInTheDocument();
    expect(screen.queryByText(/o que você quer fazer/i)).not.toBeInTheDocument();
  });

  it("uma aula vigente dispensa a pergunta e abre a tela inicial", async () => {
    vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
      token: "token-do-mestre",
      expira_em: new Date().toISOString(),
      papel: "mestre",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "mestre-1",
      papel: "mestre",
      permissoes: {},
    });
    vi.spyOn(aulasApi, "listarAulasVigentes").mockResolvedValue({
      itens: [aula()],
      proximo_cursor: null,
    });

    render(<App />);
    await entrarComoMestre();

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
  });

  it("duas aulas vigentes perguntam uma única vez em qual comunidade", async () => {
    vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
      token: "token-do-mestre",
      expira_em: new Date().toISOString(),
      papel: "mestre",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "mestre-1",
      papel: "mestre",
      permissoes: {},
    });
    vi.spyOn(aulasApi, "listarAulasVigentes").mockResolvedValue({
      itens: [
        aula({ id: "aula-1", comunidade_virtual_id: "comunidade-1" }),
        aula({ id: "aula-2", comunidade_virtual_id: "comunidade-2" }),
      ],
      proximo_cursor: null,
    });
    vi.spyOn(comunidadesApi, "buscarNomeDaComunidade").mockImplementation(
      async (id: string) =>
        id === "comunidade-1" ? "Comunidade das Flores" : "Comunidade do Rio",
    );

    render(<App />);
    await entrarComoMestre();

    expect(await screen.findByText(/em qual comunidade/i)).toBeInTheDocument();
    const opcaoUm = await screen.findByRole("button", { name: /comunidade das flores/i });
    const opcaoDois = screen.getByRole("button", { name: /comunidade do rio/i });

    const usuario = userEvent.setup();
    await usuario.click(opcaoUm);

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(screen.queryByText(/em qual comunidade/i)).not.toBeInTheDocument();
    expect(opcaoDois).toBeDefined();
  });

  it("Guerreiro(a) é recusado na abertura da sessão de trabalho", async () => {
    vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(sessaoApi, "encerrarSessao").mockResolvedValue(undefined);

    render(<App />);
    await entrarComoMestre();

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/mestre ou admin/i);
    expect(screen.queryByText(/o que você quer fazer/i)).not.toBeInTheDocument();
  });

  it("a aula escolhida sai das vigentes e a sessão de trabalho encerra", async () => {
    vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
      token: "token-do-mestre",
      expira_em: new Date().toISOString(),
      papel: "mestre",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "mestre-1",
      papel: "mestre",
      permissoes: {},
    });
    vi.spyOn(sessaoApi, "encerrarSessao").mockResolvedValue(undefined);
    vi.spyOn(aulasApi, "listarAulasVigentes")
      .mockResolvedValueOnce({ itens: [aula()], proximo_cursor: null })
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null });

    render(<App />);
    await entrarComoMestre();
    await screen.findByText(/o que você quer fazer/i);

    // A volta ao início relê `aulas/vigentes`, que desta vez não traz mais
    // a aula escolhida — a sessão de trabalho cai (`RN-04-29`).
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas/i }));
    await usuario.click(await screen.findByRole("button", { name: /voltar/i }));

    await waitFor(() =>
      expect(screen.getByRole("button", { name: /entrar com google/i })).toBeInTheDocument(),
    );
  });
});
