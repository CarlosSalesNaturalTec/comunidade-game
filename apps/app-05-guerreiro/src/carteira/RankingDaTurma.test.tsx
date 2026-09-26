import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { RankingDaTurma } from "./RankingDaTurma";

// A comunidade é derivada pelo núcleo do vínculo vigente: a tela não a
// descobre antes de perguntar, e por isso nenhuma leitura de série de coleta
// aparece aqui (`RF-05-52`, `RN-05-16`, decisão do fundador de 2026-09-26).

const CHAVE_DE_SESSAO = "app-05:teste-ranking-da-turma";

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
        <RankingDaTurma />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("ranking logado da turma", () => {
  it("mostra a própria posição sempre, mesmo fora da página exibida", async () => {
    vi.spyOn(carteiraApi, "listarPoderesPublicos").mockResolvedValue([]);
    vi.spyOn(carteiraApi, "listarRankingDaTurma").mockResolvedValue({
      itens: [{ avatar: null, nick: "primeiro-lugar", posicao: 1, pontos_regulares: 100 }],
      proximo_cursor: null,
      minha_posicao: { avatar: null, nick: "eu-mesma", posicao: 4, pontos_regulares: 1 },
    });

    await renderizar();

    expect(await screen.findByText(/sua posição/i)).toHaveTextContent("4º");
    expect(screen.getByText(/primeiro-lugar/i)).toBeInTheDocument();
  });

  it("abre sem série de coleta e sem declarar comunidade alguma", async () => {
    // O defeito que esta fatia corrige: quem nunca abriu série de coleta lia
    // "abra uma série de coleta para ver o ranking da sua turma".
    vi.spyOn(carteiraApi, "listarPoderesPublicos").mockResolvedValue([]);
    const ranking = vi.spyOn(carteiraApi, "listarRankingDaTurma").mockResolvedValue({
      itens: [{ avatar: null, nick: "colega", posicao: 1, pontos_regulares: 0 }],
      proximo_cursor: null,
      minha_posicao: {
        avatar: null,
        nick: "acabei-de-chegar",
        posicao: 2,
        pontos_regulares: 0,
      },
    });

    await renderizar();

    expect(await screen.findByText(/sua posição/i)).toHaveTextContent("2º");
    expect(screen.queryByText(/série de coleta/i)).not.toBeInTheDocument();
    // Só o token e o recorte: nenhum identificador de comunidade sai da tela.
    expect(ranking).toHaveBeenCalledWith("token-do-guerreiro", {
      trilhaId: undefined,
      poderId: undefined,
    });
  });

  it("o recorte por poder não reintroduz a comunidade na chamada", async () => {
    vi.spyOn(carteiraApi, "listarPoderesPublicos").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Poder da IA e Robótica",
        descricao: "Programação, eletrônica, robótica e IA",
        trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
      },
    ]);
    const ranking = vi.spyOn(carteiraApi, "listarRankingDaTurma").mockResolvedValue({
      itens: [{ avatar: null, nick: "colega", posicao: 1, pontos_regulares: 50 }],
      proximo_cursor: null,
      minha_posicao: { avatar: null, nick: "eu-mesma", posicao: 2, pontos_regulares: 10 },
    });

    await renderizar();
    await act(async () => {
      const seletor = screen.getByLabelText(/recorte/i) as HTMLSelectElement;
      seletor.value = "poder:poder-1";
      seletor.dispatchEvent(new Event("change", { bubbles: true }));
    });

    expect(ranking).toHaveBeenLastCalledWith("token-do-guerreiro", {
      trilhaId: undefined,
      poderId: "poder-1",
    });
  });

  it("cada colega aparece só por avatar, nick e posição", async () => {
    vi.spyOn(carteiraApi, "listarPoderesPublicos").mockResolvedValue([]);
    vi.spyOn(carteiraApi, "listarRankingDaTurma").mockResolvedValue({
      itens: [
        {
          avatar: "avatar-x",
          nick: "colega-sem-divulgacao",
          posicao: 1,
          pontos_regulares: 50,
        },
      ],
      proximo_cursor: null,
      minha_posicao: { avatar: null, nick: "eu-mesma", posicao: 2, pontos_regulares: 10 },
    });

    await renderizar();

    expect(await screen.findByText(/colega-sem-divulgacao/i)).toBeInTheDocument();
  });
});
