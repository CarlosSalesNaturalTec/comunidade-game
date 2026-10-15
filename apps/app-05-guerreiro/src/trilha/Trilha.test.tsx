import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
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
      culminancia: null,
      missoes: [],
    });

    await renderizar();

    expect(await screen.findByRole("heading", { name: "Robô Educa" })).toBeInTheDocument();
    expect(screen.getByText("Primeira Missão")).toBeInTheDocument();
  });

  // --- Fatia 27: o guia não repete o caminho ao catálogo (`RF-04-74`)

  it("o guia não oferece o catálogo, porque trocar de trilha já o alcança", async () => {
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
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue({
      id: "missao-1",
      titulo: "Primeira Missão",
      posicao: 1,
      obrigatoria: true,
      e_sondagem: false,
      desbloqueada: true,
      e_proxima: false,
      aguardando_mestre: false,
      motivo_do_bloqueio: null,
      desafio_de_desbloqueio: null,
    });
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
      id: "trilha-1",
      nome: "Robô Educa",
      licenca: "CC BY-SA",
      autor_nome: "Mestre Ana",
      culminancia: null,
      missoes: [],
    });

    await renderizar();
    const usuario = userEvent.setup();

    // No guia, o rodapé tem só o crédito: a App 05 nunca passa o caminho ao
    // catálogo, porque a sub-tela de trocar de trilha sempre o alcança —
    // decisão do fundador de 2026-10-15.
    expect(await screen.findByText("Crédito e licença")).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Escolher outro poder" }),
    ).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /trocar de trilha/i }));

    // E lá ele continua, que é o outro caminho que torna a condição verdadeira.
    expect(
      await screen.findByRole("button", { name: "Escolher outro poder" }),
    ).toBeInTheDocument();
  });
});
