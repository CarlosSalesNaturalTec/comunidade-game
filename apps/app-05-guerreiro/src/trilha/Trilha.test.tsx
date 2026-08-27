import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { Trilha } from "./Trilha";

const CHAVE_DE_SESSAO = "app-05:teste-trilha";

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
        <Trilha />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("bloco da trilha", () => {
  it("sem inscrição, a tela leva à escolha do poder", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/escolha um poder/i)).toBeInTheDocument();
  });

  it("com inscrição, abre no guia da trilha", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([
      {
        id: "trilha-1",
        nome: "Robô Educa",
        poder_id: "poder-1",
        proxima_missao_id: "missao-1",
        proxima_missao_titulo: "Primeira Missão",
        proxima_missao_posicao: 1,
      },
    ]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, ordem) =>
      Promise.resolve({
        id: ordem === 1 ? "missao-1" : "missao-2",
        titulo: ordem === 1 ? "Primeira Missão" : "Segunda Missão",
        posicao: ordem,
        obrigatoria: true,
        e_sondagem: false,
        desbloqueada: false,
        e_proxima: ordem === 1,
        aguardando_mestre: false,
        motivo_do_bloqueio: ordem === 1 ? null : 'Desbloqueie "Primeira Missão" primeiro.',
        desafio_de_desbloqueio: null,
      }),
    );
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
      id: "trilha-1",
      nome: "Robô Educa",
      licenca: "CC BY-SA",
      autor_nome: "Mestre Ana",
      missoes: [],
    });

    await renderizar();

    expect(await screen.findByRole("heading", { name: "Robô Educa" })).toBeInTheDocument();
    expect(screen.getByText("Primeira Missão")).toBeInTheDocument();
  });
});
