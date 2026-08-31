import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as desafiosEEquipesApi from "../api/desafiosEEquipes";
import { MinhasEquipes } from "./MinhasEquipes";

const CHAVE_DE_SESSAO = "app-05:teste-minhas-equipes";

const EQUIPE_DA_AULA = {
  id: "equipe-1",
  aula_id: "aula-1",
  trilha_id: null,
  meu_papel: "capitã",
  integrantes: [{ avatar: "avatar-1", nick: "zeferina", papel: null }],
  atividades: [
    {
      atividade: {
        id: "atividade-1",
        missao_id: "missao-1",
        titulo: "Construa um robô",
        descricao: null,
        modalidade: "em_equipe",
        formato: "presencial",
        natureza: "construcao",
        producao_esperada: "Um robô de sucata.",
        aula_id: "aula-1",
      },
      missao_id: "missao-1",
      missao_titulo: "Missão do robô",
      trilha_id: "trilha-1",
      trilha_titulo: "Trilha da Robótica",
      corrente: true,
    },
  ],
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
        <MinhasEquipes />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("minhas equipes", () => {
  it("mostra cada equipe com o papel e as atividades, com a corrente marcada", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([EQUIPE_DA_AULA]);

    await renderizar();

    expect(await screen.findByText("Equipe da aula")).toBeInTheDocument();
    expect(screen.getByText(/capitã/)).toBeInTheDocument();
    expect(screen.getByText("Construa um robô")).toBeInTheDocument();
    expect(screen.getByText("Atividade corrente")).toBeInTheDocument();
  });

  it("cada integrante aparece só por avatar e nick", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([EQUIPE_DA_AULA]);

    await renderizar();

    expect(await screen.findByText("zeferina")).toBeInTheDocument();
  });

  it("sem equipe a tela diz isso e onde ela se forma", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/ainda não integra nenhuma equipe/i)).toBeInTheDocument();
    expect(
      screen.getByText(/se forma no encontro presencial, no App 01/i),
    ).toBeInTheDocument();
  });

  it("nenhuma ação de formar, editar, entrar, sair ou homologar equipe é oferecida", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([EQUIPE_DA_AULA]);

    await renderizar();

    await screen.findByText("Equipe da aula");
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("nenhum canal de conversa é oferecido", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([EQUIPE_DA_AULA]);

    await renderizar();

    await screen.findByText("Equipe da aula");
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByText(/mensagem|comentário|conversa/i)).not.toBeInTheDocument();
  });
});
