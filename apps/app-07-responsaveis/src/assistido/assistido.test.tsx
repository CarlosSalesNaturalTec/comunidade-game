import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as termosApi from "../termos/api";
import type { GuerreiroVinculavel, ResponsavelVinculado } from "./api";
import * as assistidoApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const GUERREIRO: GuerreiroVinculavel = { id: "guerreiro-1", nick: "zeferina", avatar: "" };
const RESPONSAVEL: ResponsavelVinculado = {
  id: "responsavel-1",
  nome: "Mãe da Zeferina",
  grau_de_parentesco: "mãe",
};

async function entrarComo(papel: "mestre" | "admin" | "guerreiro" | "apoiador") {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: `token-do-${papel}`,
    expira_em: new Date().toISOString(),
    papel,
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: `${papel}-1`,
    papel,
    permissoes: {},
  });

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), `usuario-${papel}`);
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  return testeDeUsuario;
}

describe("modo assistido", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(assistidoApi, "listarGuerreirosVinculaveis").mockResolvedValue([GUERREIRO]);
    vi.spyOn(assistidoApi, "listarResponsaveisDoGuerreiro").mockResolvedValue([RESPONSAVEL]);
    vi.spyOn(termosApi, "consultarTermos").mockResolvedValue([
      {
        tipo: "autorizacao_de_divulgacao",
        vigente: {
          versao: "2026-08",
          texto: "Texto do termo.",
          vigente_desde: "2026-08-01T10:00:00Z",
        },
        historico: [],
      },
    ]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a sessão de Mestre só alcança o modo assistido", async () => {
    await entrarComo("mestre");

    expect(
      await screen.findByRole("heading", { name: /atendimento assistido/i }),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: /seus vinculados/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByText(/o que a autorização libera/i)).not.toBeInTheDocument();
  });

  it("registra o ato em nome do responsável presente, com quem operou e testemunhou", async () => {
    vi.spyOn(assistidoApi, "registrarAutorizacaoAssistida").mockResolvedValue({
      id: "consentimento-1",
      responsavel_id: RESPONSAVEL.id,
      decisao: "concede",
      registrado_em: "2026-09-01T10:00:00Z",
    });

    const testeDeUsuario = await entrarComo("mestre");
    await testeDeUsuario.click(await screen.findByRole("button", { name: /^zeferina$/i }));
    await testeDeUsuario.click(
      await screen.findByRole("button", { name: /mãe da zeferina — mãe/i }),
    );
    await screen.findByText(/texto do termo/i);
    await testeDeUsuario.click(screen.getByRole("button", { name: /^conceder$/i }));

    expect(assistidoApi.registrarAutorizacaoAssistida).toHaveBeenCalledWith(
      GUERREIRO.id,
      RESPONSAVEL.id,
      "concede",
      "mestre-1",
      "token-do-mestre",
    );
    expect(await screen.findByText(/registrada em nome do responsável/i)).toBeInTheDocument();
  });

  it("Guerreiro(a) continua recusado", async () => {
    await entrarComo("guerreiro");
    expect(await screen.findByText(/área é só para responsáveis/i)).toBeInTheDocument();
  });

  it("Apoiador continua recusado", async () => {
    await entrarComo("apoiador");
    expect(await screen.findByText(/área é só para responsáveis/i)).toBeInTheDocument();
  });

  it("nenhum canal de contato com terceiro aparece no modo assistido", async () => {
    await entrarComo("mestre");
    await screen.findByRole("heading", { name: /atendimento assistido/i });

    expect(
      screen.queryByLabelText(/telefone|whatsapp|e-mail de contato/i),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /mensagem|conversar/i }),
    ).not.toBeInTheDocument();
  });
});
