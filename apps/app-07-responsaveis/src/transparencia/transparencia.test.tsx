import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { EvolucaoDoGuerreiro } from "../evolucao/api";
import * as evolucaoApi from "../evolucao/api";
import * as solicitacoesApi from "../solicitacoes/api";
import type { GuerreiroVinculado } from "../vinculados/api";
import * as vinculadosApi from "../vinculados/api";
import type { AcessoDoResponsavel, ItemDoCatalogoDeDados } from "./api";
import * as transparenciaApi from "./api";

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

const DADOS: ItemDoCatalogoDeDados[] = [
  {
    dado: "Nick",
    finalidade: "Identificação pública",
    prazo: "Enquanto durar o vínculo",
    restrito_a_gestao: false,
    guardado: true,
  },
  {
    dado: "Consulta ao assistente de trilhas",
    finalidade: "Apoio à jornada da missão",
    prazo: "7 dias",
    restrito_a_gestao: true,
    guardado: false,
  },
];

const ACESSO: AcessoDoResponsavel = {
  id: "acesso-1",
  momento: "2026-09-01T10:00:00Z",
  autor_id: "mestre-1",
  autor_nome: "Mestre José",
  papel_do_autor: "mestre",
  acao: "POST confirmar_presenca_rota",
  entidade_afetada: "confirmar_presenca_rota",
};

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

async function abrirAbaDeTransparencia(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^transparência$/i }));
}

describe("tela de transparência", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);
    vi.spyOn(transparenciaApi, "listarDadosDoVinculado").mockResolvedValue(DADOS);
    vi.spyOn(transparenciaApi, "listarAcessosDoVinculado").mockResolvedValue([ACESSO]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("apresenta cada dado com finalidade e prazo", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTransparencia(testeDeUsuario);

    const linha = await screen.findByRole("row", { name: /^nick$/i });
    expect(linha).toHaveTextContent("Identificação pública");
    expect(linha).toHaveTextContent("Enquanto durar o vínculo");
  });

  it("o que a criança faz sozinha aparece restrito à gestão", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTransparencia(testeDeUsuario);

    const linha = await screen.findByRole("row", { name: /consulta ao assistente/i });
    expect(linha).toHaveTextContent(/restrito à gestão/i);
  });

  it("o histórico de acessos mostra data, hora, quem acessou, papel e dado", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTransparencia(testeDeUsuario);

    const lista = await screen.findByRole("list", { name: /acessos a zeferina/i });
    expect(lista).toHaveTextContent("Mestre José");
    expect(lista).toHaveTextContent("mestre");
    expect(lista).toHaveTextContent("confirmar_presenca_rota");
  });

  it("o esclarecimento é aberto direto da linha, sem sair da tela", async () => {
    vi.spyOn(solicitacoesApi, "abrirSolicitacao").mockResolvedValue({
      id: "protocolo-1",
      prazo: "2026-09-08T10:00:00Z",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeTransparencia(testeDeUsuario);

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: /pedir esclarecimento/i }),
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar esclarecimento/i }));

    expect(await screen.findByText(/protocolo-1/)).toBeInTheDocument();
    expect(solicitacoesApi.abrirSolicitacao).toHaveBeenCalledWith(
      GUERREIRO_1.id,
      "esclarecimento",
      expect.stringContaining("Mestre José"),
      "token-do-responsavel",
    );
    // Continua na mesma tela de transparência, sem navegar para fora dela.
    expect(screen.getByRole("row", { name: /^nick$/i })).toBeInTheDocument();
  });
});
