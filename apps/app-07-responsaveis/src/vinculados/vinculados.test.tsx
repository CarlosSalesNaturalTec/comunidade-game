import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { EvolucaoDoGuerreiro, OcorrenciaDaEvolucao } from "../evolucao/api";
import * as evolucaoApi from "../evolucao/api";
import type { GuerreiroVinculado } from "./api";
import * as vinculadosApi from "./api";

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

const GUERREIRO_2: GuerreiroVinculado = {
  id: "guerreiro-2",
  nick: "joaozinho",
  avatar: "avatar-2",
  grau_de_parentesco: "avó",
};

const EVOLUCAO_VAZIA: EvolucaoDoGuerreiro = {
  presencas: [],
  atividades: [],
  trilhas: [],
  pontos_por_poder: [],
  criacoes_validadas: [],
};

async function entrarComoResponsavel() {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-responsavel",
    expira_em: new Date().toISOString(),
    papel: "responsavel",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: "algum-id",
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

describe("lista dos vinculados", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("dois vinculados aparecem, cada um com o grau de parentesco", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([
      GUERREIRO_1,
      GUERREIRO_2,
    ]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);

    await entrarComoResponsavel();

    expect(await screen.findByText(/zeferina · mãe/i)).toBeInTheDocument();
    expect(screen.getByText(/joaozinho · avó/i)).toBeInTheDocument();
  });

  it("alternar entre vinculados troca o painel sem sair da aplicação", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([
      GUERREIRO_1,
      GUERREIRO_2,
    ]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockImplementation((guerreiroId) =>
      Promise.resolve({
        ...EVOLUCAO_VAZIA,
        trilhas:
          guerreiroId === GUERREIRO_1.id
            ? [
                {
                  trilha_id: "trilha-1",
                  trilha_nome: "Trilha da Zeferina",
                  nivel_atual: 1,
                  obrigatorias_desbloqueadas: 1,
                  obrigatorias_totais: 3,
                  pontos_regulares: 10,
                  badges: [],
                },
              ]
            : [
                {
                  trilha_id: "trilha-2",
                  trilha_nome: "Trilha do Joãozinho",
                  nivel_atual: 2,
                  obrigatorias_desbloqueadas: 2,
                  obrigatorias_totais: 4,
                  pontos_regulares: 20,
                  badges: [],
                },
              ],
      }),
    );
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);

    const testeDeUsuario = await entrarComoResponsavel();
    await screen.findByText(/trilha da zeferina/i);

    await testeDeUsuario.click(screen.getByRole("button", { name: /joaozinho · avó/i }));

    expect(await screen.findByText(/trilha do joãozinho/i)).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: /seus vinculados/i })).toBeInTheDocument();
  });
});

describe("painel de evolução", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("mostra o percurso da trilha em missões, não em saldo de pontos", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue({
      ...EVOLUCAO_VAZIA,
      trilhas: [
        {
          trilha_id: "trilha-1",
          trilha_nome: "Trilha de Robótica",
          nivel_atual: 2,
          obrigatorias_desbloqueadas: 3,
          obrigatorias_totais: 5,
          pontos_regulares: 40,
          badges: [],
        },
      ],
    });
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);

    await entrarComoResponsavel();

    expect(await screen.findByText(/3 de 5/i)).toBeInTheDocument();
    expect(screen.queryByText(/saldo/i)).not.toBeInTheDocument();
  });

  it("criação validada aparece com título, trilha e data", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue({
      ...EVOLUCAO_VAZIA,
      criacoes_validadas: [
        { trilha_id: "trilha-1", trilha_titulo: "Robótica Básica", validado_em: "2026-08-01" },
      ],
    });
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);

    await entrarComoResponsavel();

    expect(await screen.findByText(/robótica básica/i)).toBeInTheDocument();
  });

  it("ocorrência com motivo aparece com motivo e data", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    const comMotivo: OcorrenciaDaEvolucao = {
      id: "ocorrencia-1",
      motivo: "Desrespeitou um colega.",
      momento_do_fato: "2026-08-01T10:00:00Z",
    };
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([comMotivo]);

    await entrarComoResponsavel();

    expect(await screen.findByText(/desrespeitou um colega/i)).toBeInTheDocument();
  });

  it("ocorrência de ciclo anterior aparece sem motivo e sem texto substituto", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    const expurgada: OcorrenciaDaEvolucao = {
      id: "ocorrencia-2",
      motivo: null,
      momento_do_fato: "2026-01-01T10:00:00Z",
    };
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([expurgada]);

    await entrarComoResponsavel();

    await screen.findByText(/ocorrências de conduta/i);
    const itens = screen.getAllByRole("listitem");
    const itemDaOcorrencia = itens.find((item) => item.textContent?.includes("2026"));
    expect(itemDaOcorrencia).toBeDefined();
    expect(itemDaOcorrencia?.textContent).not.toMatch(/motivo/i);
    expect(itemDaOcorrencia?.textContent).not.toMatch(/apagad[oa]/i);
  });

  it("nenhuma tela apresenta consulta ao assistente, transcrição ou dado de outra criança", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);

    await entrarComoResponsavel();
    await screen.findByRole("heading", { name: /seus vinculados/i });

    expect(screen.queryByText(/assistente/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/apoio escolar/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/ranking/i)).not.toBeInTheDocument();
  });
});
