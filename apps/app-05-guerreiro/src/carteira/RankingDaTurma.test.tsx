import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import * as coletaApi from "../api/coleta";
import { RankingDaTurma } from "./RankingDaTurma";

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
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [
        {
          id: "serie-1",
          desafio_de_coleta_id: "desafio-1",
          local_id: "local-1",
          comunidade_virtual_id: "comunidade-1",
          cadencia: "semanal",
          estado: "ativa",
          pontos: 5,
          proxima_medicao: null,
          tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
        },
      ],
      proximo_cursor: null,
    });
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

  it("sem série aberta, explica em vez de quebrar", async () => {
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(carteiraApi, "listarPoderesPublicos").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/abra uma série de coleta/i)).toBeInTheDocument();
  });

  it("cada colega aparece só por avatar, nick e posição", async () => {
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [
        {
          id: "serie-1",
          desafio_de_coleta_id: "desafio-1",
          local_id: "local-1",
          comunidade_virtual_id: "comunidade-1",
          cadencia: "semanal",
          estado: "ativa",
          pontos: 5,
          proxima_medicao: null,
          tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
        },
      ],
      proximo_cursor: null,
    });
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
