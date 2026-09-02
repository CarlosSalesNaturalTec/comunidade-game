import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { PainelDeEfetividade } from "./api";
import * as efetividadeApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const PAINEL_VAZIO: PainelDeEfetividade = {
  desafios: { propostos: [], publicados: [], concluidos: [] },
  moedas: { total_em_moedas: "0", aportes: [] },
  cobertura_de_ods: { por_comunidade: [] },
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
  return testeDeUsuario;
}

async function abrirEfetividade(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(screen.getByRole("button", { name: /^efetividade$/i }));
}

describe("painel de efetividade do apoio", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a área reúne desafios, moedas e cobertura de ODS", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue({
      desafios: {
        propostos: [],
        publicados: [
          {
            id: "desafio-1",
            trilha_id: "trilha-1",
            trilha_nome: "Trilha das Águas",
            modalidade: "aberto",
            situacao: "publicado",
            etiquetas_ods: [6],
            quantidade_de_conclusoes: 0,
            primeira_conclusao_em: null,
            ultima_conclusao_em: null,
            concluintes_exibiveis: [],
            concluintes_nao_identificados: 0,
            houve_conclusao: null,
          },
        ],
        concluidos: [],
      },
      moedas: {
        total_em_moedas: "20.00",
        aportes: [
          {
            id: "aporte-1",
            valor_em_moedas: "20.00",
            data_do_aporte: "2026-06-01",
            custeio_tipo: "missao",
            custeio_descricao: "O lanche do encontro",
          },
        ],
      },
      cobertura_de_ods: {
        por_comunidade: [
          {
            comunidade_virtual_id: "comunidade-1",
            comunidade_virtual_nome: "Guerreira Zeferina",
            ciclo_rotulo: "Ciclo 01",
            objetivos: [4, 6],
          },
        ],
      },
    });

    await abrirEfetividade(testeDeUsuario);

    expect(await screen.findByText(/trilha das águas/i)).toBeInTheDocument();
    expect(screen.getByText(/total: 20.00 moedas/i)).toBeInTheDocument();
    expect(screen.getByText(/o lanche do encontro/i)).toBeInTheDocument();
    expect(screen.getByText(/guerreira zeferina/i)).toBeInTheDocument();
    expect(screen.getByText(/objetivos: 4, 6/i)).toBeInTheDocument();
  });

  it("declara que o painel é vivo e que não há relatório fechado", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue(PAINEL_VAZIO);

    await abrirEfetividade(testeDeUsuario);

    expect(await screen.findByText(/atualiza a cada conclus/i)).toBeInTheDocument();
    expect(screen.getByText(/não há relatório fechado/i)).toBeInTheDocument();
  });

  it("orienta quem ainda não propôs nenhum desafio", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue(PAINEL_VAZIO);

    await abrirEfetividade(testeDeUsuario);

    expect(
      await screen.findByText(/ainda não propôs nenhum desafio extra/i),
    ).toBeInTheDocument();
  });

  it("mostra avatar e nick só de quem autorizou a divulgação, e conta os demais", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue({
      desafios: {
        propostos: [],
        publicados: [],
        concluidos: [
          {
            id: "desafio-1",
            trilha_id: "trilha-1",
            trilha_nome: "Trilha das Águas",
            modalidade: "aberto",
            situacao: "publicado",
            etiquetas_ods: [],
            quantidade_de_conclusoes: 2,
            primeira_conclusao_em: "2026-06-01",
            ultima_conclusao_em: "2026-06-10",
            concluintes_exibiveis: [{ avatar: null, nick: "guerreira-autorizada" }],
            concluintes_nao_identificados: 1,
            houve_conclusao: null,
          },
        ],
      },
      moedas: { total_em_moedas: "0", aportes: [] },
      cobertura_de_ods: { por_comunidade: [] },
    });

    await abrirEfetividade(testeDeUsuario);

    expect(await screen.findByText(/guerreira-autorizada/i)).toBeInTheDocument();
    expect(screen.getByText(/1 sem divulgação autorizada/i)).toBeInTheDocument();
  });

  it("mostra o desafio direcionado apenas como concluído ou não", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue({
      desafios: {
        propostos: [],
        publicados: [],
        concluidos: [
          {
            id: "desafio-direcionado",
            trilha_id: "trilha-1",
            trilha_nome: "Trilha das Águas",
            modalidade: "direcionado",
            situacao: "publicado",
            etiquetas_ods: [],
            quantidade_de_conclusoes: null,
            primeira_conclusao_em: null,
            ultima_conclusao_em: null,
            concluintes_exibiveis: null,
            concluintes_nao_identificados: null,
            houve_conclusao: true,
          },
        ],
      },
      moedas: { total_em_moedas: "0", aportes: [] },
      cobertura_de_ods: { por_comunidade: [] },
    });

    await abrirEfetividade(testeDeUsuario);

    expect(await screen.findByText(/^concluído\.$/i)).toBeInTheDocument();
    expect(screen.queryByText(/nick/i)).not.toBeInTheDocument();
  });

  it("nenhuma tela de efetividade oferece campo de mensagem ou contato", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(efetividadeApi, "lerPainelDeEfetividade").mockResolvedValue(PAINEL_VAZIO);

    await abrirEfetividade(testeDeUsuario);
    await screen.findByText(/atualiza a cada conclus/i);

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/telefone/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/e-mail/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /contatar/i })).not.toBeInTheDocument();
  });
});
