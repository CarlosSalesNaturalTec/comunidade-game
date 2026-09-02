import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { SustentoDoApoiador } from "./api";
import * as sustentoApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const SUSTENTO_BASE: SustentoDoApoiador = {
  nivel: 2,
  nome_do_nivel: "Sustenta o encontro",
  frente_que_falta: "Cubra uma missão de outro nível de necessidade.",
  selos: {
    frente: [
      {
        selo_nome: "Lanche garantido",
        missao_do_apoiador_id: "missao-1",
        creditado_em: "2026-06-01T12:00:00Z",
      },
    ],
    modalidade: [],
    ato: [],
    multiplicacao: [],
  },
};

async function entrarComoApoiador() {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-apoiador",
    expira_em: new Date().toISOString(),
    papel: "apoiador",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: "algum-id",
    papel: "apoiador",
    permissoes: {},
  });

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "apoiadora");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  await screen.findByRole("button", { name: /propor desafio extra/i });
  await testeDeUsuario.click(screen.getByRole("button", { name: /^sustento$/i }));
  return testeDeUsuario;
}

describe("Tela de sustento", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("mostra o nível, os selos por família e a frente que falta", async () => {
    vi.spyOn(sustentoApi, "consultarMeuSustento").mockResolvedValue(SUSTENTO_BASE);

    await entrarComoApoiador();

    expect(await screen.findByText(/nível 2 — sustenta o encontro/i)).toBeInTheDocument();
    expect(screen.getByText(/cubra uma missão de outro nível/i)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "De frente" })).toBeInTheDocument();
    expect(screen.getByText(/lanche garantido/i)).toBeInTheDocument();
  });

  it("sem selo a tela diz", async () => {
    vi.spyOn(sustentoApi, "consultarMeuSustento").mockResolvedValue({
      nivel: 0,
      nome_do_nivel: "Sem aporte",
      frente_que_falta: "Faça o primeiro aporte.",
      selos: { frente: [], modalidade: [], ato: [], multiplicacao: [] },
    });

    await entrarComoApoiador();

    expect(await screen.findByText(/nenhum selo conquistado ainda/i)).toBeInTheDocument();
  });

  it("nenhuma leitura ordena ou compara apoiadores por valor", async () => {
    vi.spyOn(sustentoApi, "consultarMeuSustento").mockResolvedValue(SUSTENTO_BASE);

    await entrarComoApoiador();
    await screen.findByText(/nível 2/i);

    expect(screen.queryByText(/ranking/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/pódio/i)).not.toBeInTheDocument();
  });
});
