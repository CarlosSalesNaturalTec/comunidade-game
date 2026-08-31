import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as desafiosEEquipesApi from "../api/desafiosEEquipes";
import { MeusDesafios } from "./MeusDesafios";

const CHAVE_DE_SESSAO = "app-05:teste-meus-desafios";

const DESAFIO = {
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

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
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
  it("mostra cada desafio com modalidade e formato em linguagem da criança", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMeusDesafios").mockResolvedValue([DESAFIO]);

    await renderizar();

    expect(await screen.findByText("Construa um robô")).toBeInTheDocument();
    expect(screen.getByText(/Trilha da Robótica/)).toBeInTheDocument();
    expect(screen.getByText(/Em equipe/)).toBeInTheDocument();
    expect(screen.getByText(/Presencial/)).toBeInTheDocument();
    expect(screen.getByText(/Um robô de sucata\./)).toBeInTheDocument();
  });

  it("sem desafio em aberto a tela explica, nunca lista vazia muda", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMeusDesafios").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/não tem nenhum desafio em aberto/i)).toBeInTheDocument();
  });

  it("nenhuma ação de lançar resultado, presença ou mérito é oferecida", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMeusDesafios").mockResolvedValue([DESAFIO]);

    await renderizar();

    await screen.findByText("Construa um robô");
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("nenhum canal de conversa é oferecido", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMeusDesafios").mockResolvedValue([DESAFIO]);

    await renderizar();

    await screen.findByText("Construa um robô");
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByText(/mensagem|comentário|conversa/i)).not.toBeInTheDocument();
  });
});
