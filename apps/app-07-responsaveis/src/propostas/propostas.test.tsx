import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { EvolucaoDoGuerreiro } from "../evolucao/api";
import * as evolucaoApi from "../evolucao/api";
import * as transparenciaApi from "../transparencia/api";
import type { GuerreiroVinculado } from "../vinculados/api";
import * as vinculadosApi from "../vinculados/api";
import type { PropostaDoAutor } from "./api";
import * as propostasApi from "./api";

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

async function abrirAbaDePropostas(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^propostas$/i }));
}

describe("tela de propostas", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a proposta é registrada e entra na fila única, sem promessa de e-mail nem de ponto", async () => {
    vi.spyOn(propostasApi, "registrarProposta").mockResolvedValue({
      id: "proposta-1",
      prazo: "2026-09-08T10:00:00Z",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDePropostas(testeDeUsuario);
    await testeDeUsuario.type(
      screen.getByLabelText(/^proposta$/i),
      "Que tal um mural de recados da turma?",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar proposta/i }));

    expect(propostasApi.registrarProposta).toHaveBeenCalledWith(
      "Que tal um mural de recados da turma?",
      "token-do-responsavel",
    );
    expect(screen.queryByText(/e-mail/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/\bponto[s]?\b/i)).not.toBeInTheDocument();
  });

  it("o retorno chega com o motivo em linguagem simples, dentro da plataforma", async () => {
    const propostaNaoAdotada: PropostaDoAutor = {
      id: "proposta-2",
      alvo_tipo: "plataforma",
      alvo_id: null,
      texto: "Proposta antiga.",
      situacao: "nao_adotada",
      prazo: "2026-09-01T10:00:00Z",
      em_atraso: false,
      motivo_do_retorno: "Já existe um recurso parecido no momento.",
      decidido_em: "2026-08-20T10:00:00Z",
    };
    vi.spyOn(propostasApi, "listarMinhasPropostas").mockResolvedValue([propostaNaoAdotada]);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDePropostas(testeDeUsuario);

    expect(
      await screen.findByText(/já existe um recurso parecido no momento/i),
    ).toBeInTheDocument();
  });

  it("o aviso de coleta nomeia o dado desta tela e leva à transparência, sem bloquear o envio", async () => {
    vi.spyOn(propostasApi, "registrarProposta").mockResolvedValue({
      id: "proposta-3",
      prazo: "2026-09-08T10:00:00Z",
    });
    vi.spyOn(transparenciaApi, "listarDadosDoVinculado").mockResolvedValue([]);
    vi.spyOn(transparenciaApi, "listarAcessosDoVinculado").mockResolvedValue([]);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDePropostas(testeDeUsuario);

    expect(await screen.findByText(/coleta o texto da sua proposta/i)).toBeInTheDocument();

    await testeDeUsuario.click(screen.getByRole("button", { name: /ver na transparência/i }));
    expect(
      await screen.findByRole("heading", { name: /o que a plataforma guarda/i }),
    ).toBeInTheDocument();

    // O aviso não bloqueou o envio de volta na aba de propostas.
    await testeDeUsuario.click(screen.getByRole("button", { name: /^propostas$/i }));
    await testeDeUsuario.type(screen.getByLabelText(/^proposta$/i), "Proposta nova.");
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar proposta/i }));
    expect(propostasApi.registrarProposta).toHaveBeenCalled();
  });
});
