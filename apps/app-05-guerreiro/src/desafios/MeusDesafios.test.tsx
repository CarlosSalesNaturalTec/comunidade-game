import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { MeusDesafios as MeusDesafiosResposta } from "../api/desafiosEEquipes";
import * as desafiosEEquipesApi from "../api/desafiosEEquipes";
import { MeusDesafios } from "./MeusDesafios";

const CHAVE_DE_SESSAO = "app-05:teste-meus-desafios";

const DESAFIO_SEMANAL = {
  atividade: {
    id: "atividade-1",
    missao_id: "missao-1",
    titulo: "Construa um robô",
    descricao: null,
    modalidade: "em_equipe",
    formato: "presencial",
    natureza: "construcao",
    producao_esperada: "Um robô de sucata.",
    aula_id: null,
  },
  missao_id: "missao-1",
  missao_titulo: "Missão do robô",
  trilha_id: "trilha-1",
  trilha_titulo: "Trilha da Robótica",
};

const DESAFIO_EXTRA = {
  id: "desafio-extra-1",
  trilha_id: "trilha-1",
  trilha_nome: "Trilha da Robótica",
  missao_id: "missao-1",
  missao_titulo: "Missão do robô",
  modalidade: "aberto",
  formato: "on_line",
  criterio_de_atribuicao: "Quem entregar primeiro.",
  pontos_extras: 5,
  recompensa: {
    tipo_de_recurso_nome: "Kit de robótica",
    ponto_de_apoio_nome: "Biblioteca Central",
  },
  quantidade_disponivel: 5,
  quantidade_restante: 3,
  vigencia_inicio: "2026-01-01",
  vigencia_fim: "2026-12-31",
};

const RESPOSTA_VAZIA: MeusDesafiosResposta = { semanais: [], extras: [] };

async function renderizar(resposta: MeusDesafiosResposta) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  vi.spyOn(desafiosEEquipesApi, "listarMeusDesafios").mockResolvedValue(resposta);
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <MeusDesafios />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("meus desafios", () => {
  it("mostra cada desafio semanal com modalidade e formato em linguagem da criança", async () => {
    await renderizar({ semanais: [DESAFIO_SEMANAL], extras: [] });

    expect(await screen.findByText("Construa um robô")).toBeInTheDocument();
    expect(screen.getByText(/Trilha da Robótica/)).toBeInTheDocument();
    expect(screen.getByText(/Em equipe/)).toBeInTheDocument();
    expect(screen.getByText(/Presencial/)).toBeInTheDocument();
    expect(screen.getByText(/Um robô de sucata\./)).toBeInTheDocument();
  });

  it("sem desafio em aberto a tela explica, nunca lista vazia muda", async () => {
    await renderizar(RESPOSTA_VAZIA);

    expect(await screen.findByText(/não tem nenhum desafio em aberto/i)).toBeInTheDocument();
    expect(screen.getByText(/não tem nenhum desafio extra disponível/i)).toBeInTheDocument();
  });

  it("nenhuma ação de lançar resultado, presença ou mérito é oferecida", async () => {
    await renderizar({ semanais: [DESAFIO_SEMANAL], extras: [DESAFIO_EXTRA] });

    await screen.findByText("Construa um robô");
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("nenhum canal de conversa é oferecido", async () => {
    await renderizar({ semanais: [DESAFIO_SEMANAL], extras: [] });

    await screen.findByText("Construa um robô");
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByText(/mensagem|comentário|conversa/i)).not.toBeInTheDocument();
  });

  it("semanais e extras aparecem em blocos distintos, cada um identificado", async () => {
    await renderizar({ semanais: [DESAFIO_SEMANAL], extras: [DESAFIO_EXTRA] });

    expect(await screen.findByText("Construa um robô")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Desafios da semana" })).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Desafios extras" })).toBeInTheDocument();
    expect(screen.getByText(/Kit de robótica/)).toBeInTheDocument();
  });
});
