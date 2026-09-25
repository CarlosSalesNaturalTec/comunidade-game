import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { escreverAvatar } from "comum/avatar";
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

  // O avatar desenhado do colega, pelo objeto do documento 15 §7.2, e nunca o
  // texto opaco que o núcleo guarda (`RF-05-23`).
  it("o avatar de cada integrante aparece desenhado ao lado do nick", async () => {
    const avatar = JSON.stringify({
      formaDeTratamento: "guerreira",
      avatar: escreverAvatar({ cabelo: "black-power", tom: "t1", roupa: "moletom" }),
    });
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([
      { ...EQUIPE_DA_AULA, integrantes: [{ avatar, nick: "zeferina", papel: null }] },
    ]);

    await renderizar();

    const linha = (await screen.findByText("zeferina")).closest("li");
    expect(linha).not.toBeNull();
    // biome-ignore lint/style/noNonNullAssertion: verificado na linha acima
    expect(linha!.querySelectorAll("svg.cg-avatar > g[data-camada]")).toHaveLength(9);
    // biome-ignore lint/style/noNonNullAssertion: verificado acima
    expect(linha!.textContent).not.toMatch(/black-power|formaDeTratamento|\{/);
  });

  it("avatar que falta, ou no formato antigo, cai no padrão do projeto", async () => {
    vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([
      {
        ...EQUIPE_DA_AULA,
        integrantes: [
          { avatar: null, nick: "sem-avatar", papel: null },
          {
            avatar: JSON.stringify({ caracteristicasDoAvatar: "trança-e-capa" }),
            nick: "do-texto-livre",
            papel: null,
          },
        ],
      },
    ]);

    await renderizar();

    const lista = (await screen.findByText("sem-avatar")).closest("ul");
    expect(lista).not.toBeNull();
    // biome-ignore lint/style/noNonNullAssertion: verificado na linha acima
    const desenhos = lista!.querySelectorAll("svg.cg-avatar");
    expect(desenhos).toHaveLength(2);
    expect(desenhos[0].outerHTML).toBe(desenhos[1].outerHTML);
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
