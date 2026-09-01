import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { EvolucaoDoGuerreiro } from "../evolucao/api";
import * as evolucaoApi from "../evolucao/api";
import type { GuerreiroVinculado } from "../vinculados/api";
import * as vinculadosApi from "../vinculados/api";
import type { CatalogoDeTermo } from "./api";
import * as termosApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const GUERREIRO_1: GuerreiroVinculado = {
  id: "guerreiro-1",
  nick: "zeferina",
  avatar: "avatar-1",
  grau_de_parentesco: "mãe",
};

const EVOLUCAO_VAZIA: EvolucaoDoGuerreiro = {
  presencas: [],
  atividades: [],
  trilhas: [],
  pontos_por_poder: [],
  criacoes_validadas: [],
};

const CATALOGO: CatalogoDeTermo[] = [
  {
    tipo: "autorizacao_de_divulgacao",
    vigente: {
      versao: "2026-08",
      texto:
        "Os dados podem ser entregues gratuitos e anonimizados a pesquisadores e gestores " +
        "públicos, mediante aprovação de um Admin, sob licença CC BY-SA.",
      vigente_desde: "2026-08-01T10:00:00Z",
    },
    historico: [
      {
        versao: "2026-07",
        texto: "Texto da versão anterior.",
        vigente_desde: "2026-07-01T10:00:00Z",
      },
    ],
  },
];

async function entrarComoResponsavel() {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-responsavel",
    expira_em: new Date().toISOString(),
    papel: "responsavel",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: "responsavel-1",
    papel: "responsavel",
    permissoes: {},
  });

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "mae-da-zeferina");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  return testeDeUsuario;
}

async function abrirAbaDeTermo(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^termo$/i }));
}

describe("tela do termo", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);
    vi.spyOn(termosApi, "consultarTermos").mockResolvedValue(CATALOGO);
    vi.spyOn(termosApi, "registrarLeituraDeTermo").mockResolvedValue({
      id: "leitura-1",
      versao: "2026-08",
      lida_em: "2026-09-01T10:00:00Z",
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("apresenta o texto vigente em linguagem simples", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTermo(testeDeUsuario);

    expect(await screen.findByText(/entregues gratuitos e anonimizados/i)).toBeInTheDocument();
  });

  it("registra a leitura ao abrir e mostra a confirmação com data", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTermo(testeDeUsuario);

    expect(await screen.findByText(/leitura registrada em/i)).toBeInTheDocument();
    expect(termosApi.registrarLeituraDeTermo).toHaveBeenCalledWith(
      "2026-08",
      "token-do-responsavel",
    );
  });

  it("mostra o histórico das versões anteriores", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTermo(testeDeUsuario);

    expect(await screen.findByText(/versão 2026-07/i)).toBeInTheDocument();
  });

  it("a declaração da entrega de dados aparece sem decisão separada", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTermo(testeDeUsuario);

    await screen.findByText(/entregues gratuitos e anonimizados/i);
    expect(
      screen.queryByRole("button", { name: /aceitar entrega|recusar entrega/i }),
    ).not.toBeInTheDocument();
  });
});
