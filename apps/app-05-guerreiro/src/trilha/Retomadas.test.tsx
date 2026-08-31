import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { Retomadas } from "./Retomadas";

const CHAVE_DE_SESSAO = "app-05:teste-retomadas";

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
        <Retomadas />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("retomadas", () => {
  it("mostra a missão, a trilha e o prazo de cada retomada em aberto", async () => {
    vi.spyOn(trilhaApi, "listarMinhasRetomadas").mockResolvedValue([
      {
        missao_id: "missao-1",
        missao_titulo: "A Primeira Missão",
        trilha_id: "trilha-1",
        trilha_titulo: "Robô Educa",
        prazo: "2026-02-01T00:00:00Z",
      },
    ]);

    await renderizar();

    expect(await screen.findByText("A Primeira Missão")).toBeInTheDocument();
    expect(screen.getByText(/robô educa/i)).toBeInTheDocument();
    expect(screen.getByText(/fixar o que aprendeu/i)).toBeInTheDocument();
  });

  it("sem retomada em aberto, avisa em vez de mostrar lista vazia muda", async () => {
    vi.spyOn(trilhaApi, "listarMinhasRetomadas").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/não tem nenhuma retomada agora/i)).toBeInTheDocument();
  });

  it("diz que refazer por conta própria não rende ponto novo, sem palavra de punição", async () => {
    vi.spyOn(trilhaApi, "listarMinhasRetomadas").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/não rende ponto novo/i)).toBeInTheDocument();
    expect(screen.queryByText(/atraso|dívida|punição|castigo/i)).not.toBeInTheDocument();
  });
});
