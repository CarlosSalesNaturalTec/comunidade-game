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
import type { EstadoDaBiometria } from "./api";
import * as biometriaApi from "./api";

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

const ESTADO_SEM_MARCA: EstadoDaBiometria = {
  tem_template: true,
  decisao_do_termo: null,
  apagar_em: null,
  gatilho_do_apagamento: null,
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

async function abrirAbaDaImagem(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(
    await screen.findByRole("button", { name: /^imagem do onboarding$/i }),
  );
}

describe("tela da imagem do onboarding", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("não há nenhum caminho de concessão da biometria", async () => {
    vi.spyOn(biometriaApi, "lerEstadoDaBiometria").mockResolvedValue(ESTADO_SEM_MARCA);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDaImagem(testeDeUsuario);

    expect(
      await screen.findByText(/termo impresso, assinado no encontro/i),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^conceder/i })).not.toBeInTheDocument();
  });

  it("a alternativa equivalente é dita no mesmo ato da recusa", async () => {
    vi.spyOn(biometriaApi, "lerEstadoDaBiometria").mockResolvedValue(ESTADO_SEM_MARCA);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDaImagem(testeDeUsuario);

    expect(
      await screen.findByText(/entra por nick e confirmação do mestre ou de um admin/i),
    ).toBeInTheDocument();
  });

  it("a recusa devolve a data do apagamento, e o aviso passa a exibi-la", async () => {
    vi.spyOn(biometriaApi, "lerEstadoDaBiometria")
      .mockResolvedValueOnce(ESTADO_SEM_MARCA)
      .mockResolvedValue({
        tem_template: false,
        decisao_do_termo: "nega",
        apagar_em: "2026-09-06T10:00:00Z",
        gatilho_do_apagamento: "recusa_biometria",
      });
    vi.spyOn(biometriaApi, "recusarBiometria").mockResolvedValue({
      guerreiro_id: GUERREIRO_1.id,
      apagar_em: "2026-09-06T10:00:00Z",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDaImagem(testeDeUsuario);
    await testeDeUsuario.click(
      await screen.findByRole("button", { name: /recusar a imagem/i }),
    );

    expect(await screen.findAllByText(/06\/09\/2026|9\/6\/2026/)).not.toHaveLength(0);
  });

  it("o aviso do apagamento aparece quando a marca já existe, com a data e o gatilho", async () => {
    vi.spyOn(biometriaApi, "lerEstadoDaBiometria").mockResolvedValue({
      tem_template: false,
      decisao_do_termo: null,
      apagar_em: "2026-10-01T10:00:00Z",
      gatilho_do_apagamento: "fim_do_vinculo",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDaImagem(testeDeUsuario);

    expect(await screen.findByText(/fim do vínculo com o projeto/i)).toBeInTheDocument();
    expect(screen.getByText(/01\/10\/2026|10\/1\/2026/)).toBeInTheDocument();
    expect(screen.getByText(/nova captura, com novo termo|novo termo/i)).toBeInTheDocument();
  });

  it("sem marca, nenhum aviso de apagamento é exibido", async () => {
    vi.spyOn(biometriaApi, "lerEstadoDaBiometria").mockResolvedValue(ESTADO_SEM_MARCA);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDaImagem(testeDeUsuario);

    await screen.findByText(/para que serve a imagem/i);
    expect(screen.queryByText(/será apagado em/i)).not.toBeInTheDocument();
  });
});
