import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App, { CHAVE_DE_SESSAO_DE_TRABALHO } from "../App";
import type { AulaVigente } from "../api/aulas";
import * as aulasApi from "../api/aulas";
import * as comunidadesApi from "../api/comunidades";
import { verificadorDeTeste } from "../pin/paraTestes";
import * as pinApi from "../pin/pinDeConfirmacao";

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
    await usuario.click(screen.getByRole("button", { name: /presença — entrar/i }));
    await usuario.click(await screen.findByRole("button", { name: /voltar/i }));

    await waitFor(() =>
      expect(screen.getByRole("button", { name: /entrar com google/i })).toBeInTheDocument(),
    );
  });
});

describe("verificador do PIN de quem abriu a sessão de trabalho (RN-04-38)", () => {
  function mockarMestreComUmaAula() {
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
  }

  it("o verificador chega com a sessão de trabalho, e nenhum PIN", async () => {
    mockarMestreComUmaAula();
    const verificador = await verificadorDeTeste("4821");
    const buscar = vi.spyOn(pinApi, "buscarVerificadorDoPin").mockResolvedValue(verificador);

    render(<App />);
    await entrarComoMestre();
    await screen.findByText(/o que você quer fazer/i);

    await waitFor(() => expect(pinApi.verificadorGuardado()).toEqual(verificador));
    expect(buscar).toHaveBeenCalledWith("token-do-mestre");
    const guardado = JSON.stringify({ ...sessionStorage });
    expect(guardado).not.toContain("4821");
    expect(screen.queryByText(/ainda não tem pin/i)).not.toBeInTheDocument();
  });

  it("sem PIN cadastrado, o aparelho abre e avisa", async () => {
    mockarMestreComUmaAula();
    vi.spyOn(pinApi, "buscarVerificadorDoPin").mockRejectedValue(
      new ErroDaApi(403, { codigo: "pin_nao_cadastrado", mensagem: "Sem PIN." }),
    );

    render(<App />);
    await entrarComoMestre();

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(await screen.findByText(/ainda não tem pin de confirmação/i)).toBeInTheDocument();
    expect(pinApi.verificadorGuardado()).toBeNull();
  });

  // A saída do aparelho, pelo caminho novo: o encerramento pedido na tela
  // inicial descarta o verificador e devolve a tela de abertura, que só reabre
  // por login Google (`RF-04-71`, `RF-04-28`, `RN-04-38`, `RN-04-41`).
  it("encerrar pela tela inicial derruba a sessão de trabalho e o verificador", async () => {
    mockarMestreComUmaAula();
    vi.spyOn(sessaoApi, "encerrarSessao").mockResolvedValue(undefined);
    vi.spyOn(pinApi, "buscarVerificadorDoPin").mockResolvedValue(
      await verificadorDeTeste("4821"),
    );

    render(<App />);
    await entrarComoMestre();
    await screen.findByText(/o que você quer fazer/i);
    await waitFor(() => expect(pinApi.verificadorGuardado()).not.toBeNull());

    const usuario = userEvent.setup();
    await usuario.click(
      screen.getByRole("button", { name: /encerrar a sessão de trabalho/i }),
    );
    await usuario.type(await screen.findByLabelText(/pin de quem abriu o aparelho/i), "4821");
    await usuario.click(
      screen.getByRole("button", { name: /^encerrar a sessão de trabalho$/i }),
    );

    // A tela de abertura do aparelho, sem dado de atendimento algum.
    expect(
      await screen.findByRole("button", { name: /entrar com google/i }),
    ).toBeInTheDocument();
    expect(pinApi.verificadorGuardado()).toBeNull();
    expect(sessionStorage.getItem("app-01:sessao-trabalho:aula")).toBeNull();
    expect(sessaoApi.encerrarSessao).toHaveBeenCalledWith("token-do-mestre");
  });

  it("sem sessão de trabalho, o verificador sai do aparelho", async () => {
    pinApi.guardarVerificadorDoPin("mestre-1", await verificadorDeTeste());

    render(<App />);
    await screen.findByRole("button", { name: /entrar com google/i });

    await waitFor(() => expect(pinApi.verificadorGuardado()).toBeNull());
  });
});
