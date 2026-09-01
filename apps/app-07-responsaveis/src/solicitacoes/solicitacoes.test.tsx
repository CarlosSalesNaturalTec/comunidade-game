import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { EvolucaoDoGuerreiro } from "../evolucao/api";
import * as evolucaoApi from "../evolucao/api";
import type { GuerreiroVinculado } from "../vinculados/api";
import * as vinculadosApi from "../vinculados/api";
import type { MinhaSolicitacao } from "./api";
import * as solicitacoesApi from "./api";

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

async function abrirAbaDeSolicitacoes(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^solicitações$/i }));
}

describe("tela de solicitações", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);
    vi.spyOn(solicitacoesApi, "listarMinhasSolicitacoes").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a abertura de acesso apresenta protocolo e prazo devolvidos pelo núcleo", async () => {
    vi.spyOn(solicitacoesApi, "abrirSolicitacao").mockResolvedValue({
      id: "protocolo-123",
      prazo: "2026-09-08T10:00:00Z",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeSolicitacoes(testeDeUsuario);
    await testeDeUsuario.type(
      screen.getByLabelText(/descreva o pedido/i),
      "Quero ver os dados registrados.",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar solicitação/i }));

    expect(await screen.findByText(/protocolo-123/)).toBeInTheDocument();
    expect(screen.getByText(/08\/09\/2026|9\/8\/2026/)).toBeInTheDocument();
  });

  it("a duplicata em aberto é explicada, sem protocolo novo", async () => {
    vi.spyOn(solicitacoesApi, "abrirSolicitacao").mockRejectedValue(
      new ErroDaApi(409, {
        codigo: "solicitacao_do_responsavel_duplicada",
        mensagem: "Já existe uma solicitação deste tipo em aberto para este Guerreiro(a).",
      }),
    );

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeSolicitacoes(testeDeUsuario);
    await testeDeUsuario.type(screen.getByLabelText(/descreva o pedido/i), "De novo.");
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar solicitação/i }));

    expect(await screen.findByText(/já existe uma solicitação/i)).toBeInTheDocument();
    expect(screen.queryByText(/protocolo protocolo-123/i)).not.toBeInTheDocument();
  });

  it("o limite da exclusão aparece antes do botão de envio, só nesse tipo", async () => {
    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeSolicitacoes(testeDeUsuario);

    expect(screen.queryByText(/despersonalizado, não apagado/i)).not.toBeInTheDocument();

    await testeDeUsuario.selectOptions(screen.getByLabelText(/^tipo$/i), "exclusao");

    const limite = await screen.findByText(/despersonalizado, não apagado/i);
    const botaoDeEnvio = screen.getByRole("button", { name: /enviar solicitação/i });
    expect(
      limite.compareDocumentPosition(botaoDeEnvio) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();

    await testeDeUsuario.selectOptions(screen.getByLabelText(/^tipo$/i), "acesso");
    expect(screen.queryByText(/despersonalizado, não apagado/i)).not.toBeInTheDocument();
  });

  it("a lista mostra o atraso exatamente como o núcleo devolveu", async () => {
    const solicitacaoEmAtraso: MinhaSolicitacao = {
      id: "protocolo-atrasado",
      guerreiro_id: GUERREIRO_1.id,
      tipo: "acesso",
      texto: "Pedido antigo.",
      situacao: "recebida",
      prazo: "2026-01-01T10:00:00Z",
      em_atraso: true,
      desfecho: null,
      tratado_em: null,
    };
    vi.spyOn(solicitacoesApi, "listarMinhasSolicitacoes").mockResolvedValue([
      solicitacaoEmAtraso,
    ]);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeSolicitacoes(testeDeUsuario);

    expect(await screen.findByText(/em atraso/i)).toBeInTheDocument();
  });

  it("o desfecho aparece com a data quando a gestão trata o pedido", async () => {
    const solicitacaoTratada: MinhaSolicitacao = {
      id: "protocolo-tratado",
      guerreiro_id: GUERREIRO_1.id,
      tipo: "correcao",
      texto: "Corrija o nome.",
      situacao: "aceita",
      prazo: "2026-09-08T10:00:00Z",
      em_atraso: false,
      desfecho: "Nome corrigido.",
      tratado_em: "2026-09-05T10:00:00Z",
    };
    vi.spyOn(solicitacoesApi, "listarMinhasSolicitacoes").mockResolvedValue([
      solicitacaoTratada,
    ]);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeSolicitacoes(testeDeUsuario);

    expect(await screen.findByText(/nome corrigido/i)).toBeInTheDocument();
  });
});
