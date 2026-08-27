import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as criacaoOriginalApi from "../api/criacaoOriginal";
import * as trilhaApi from "../api/trilha";
import { Culminancia } from "./Culminancia";

const CHAVE_DE_SESSAO = "app-05:teste-culminancia";

const TRILHA_BASE: trilhaApi.TrilhaPublicaComMissoes = {
  id: "trilha-1",
  nome: "Robô Educa",
  licenca: "CC BY-SA",
  autor_nome: "Mestre Ana",
  missoes: [],
  culminancia: null,
};

async function renderizar(trilha: trilhaApi.TrilhaPublicaComMissoes, criacao = null) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilha);
  vi.spyOn(criacaoOriginalApi, "obterMinhaCriacaoDaTrilha").mockResolvedValue(criacao);
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <Culminancia trilhaId="trilha-1" />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("culminância", () => {
  it("trilha sem culminância declarada não oferece entrega", async () => {
    await renderizar(TRILHA_BASE);

    expect(await screen.findByText(/ainda não declarou/i)).toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });

  it("traz descrição, critério e modalidade", async () => {
    await renderizar({
      ...TRILHA_BASE,
      culminancia: {
        id: "culminancia-1",
        trilha_id: "trilha-1",
        descricao: "Um robô que resolve um problema do bairro.",
        modalidade: "individual",
        criterio_de_validacao: "Funciona e resolve o problema.",
      },
    });

    expect(
      await screen.findByText("Um robô que resolve um problema do bairro."),
    ).toBeInTheDocument();
    expect(screen.getByText(/Funciona e resolve o problema\./)).toBeInTheDocument();
    expect(screen.getByText(/individual/)).toBeInTheDocument();
  });

  it("entrega já feita mostra que aguarda o Mestre, sem oferecer novo formulário", async () => {
    await renderizar(
      {
        ...TRILHA_BASE,
        culminancia: {
          id: "culminancia-1",
          trilha_id: "trilha-1",
          descricao: "Descrição.",
          modalidade: "individual",
          criterio_de_validacao: "Critério.",
        },
      },
      {
        id: "criacao-1",
        trilha_id: "trilha-1",
        equipe_id: null,
        guerreiro_id: "guerreiro-1",
        tipo: "texto",
        producao: "Minha produção.",
        referencia: null,
        tamanho: null,
        situacao: "entregue",
        motivo_da_devolucao: null,
      },
    );

    expect(await screen.findByText(/esperar o Mestre autor validar/i)).toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });

  it("criação devolvida mostra o motivo e reabre o formulário de reenvio", async () => {
    await renderizar(
      {
        ...TRILHA_BASE,
        culminancia: {
          id: "culminancia-1",
          trilha_id: "trilha-1",
          descricao: "Descrição.",
          modalidade: "individual",
          criterio_de_validacao: "Critério.",
        },
      },
      {
        id: "criacao-1",
        trilha_id: "trilha-1",
        equipe_id: null,
        guerreiro_id: "guerreiro-1",
        tipo: "texto",
        producao: "Minha produção.",
        referencia: null,
        tamanho: null,
        situacao: "devolvida",
        motivo_da_devolucao: "Falta explicar como funciona.",
      },
    );

    expect(await screen.findByText(/Falta explicar como funciona/)).toBeInTheDocument();
    expect(
      screen.getByRole("form", { name: /entrega da criação original/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /reenviar/i })).toBeInTheDocument();
  });
});
