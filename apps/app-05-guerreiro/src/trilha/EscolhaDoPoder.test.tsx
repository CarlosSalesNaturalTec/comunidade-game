import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { EscolhaDoPoder } from "./EscolhaDoPoder";

const CHAVE_DE_SESSAO = "app-05:teste-escolha-do-poder";

async function renderizar(aoInscrever = vi.fn()) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <EscolhaDoPoder aoInscrever={aoInscrever} />
      </ProvedorDeSessao>,
    );
  });
  return aoInscrever;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("escolha do poder", () => {
  it("escolher o poder leva às trilhas dele", async () => {
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Robótica",
        descricao: "Descrição do poder.",
        trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
      },
    ]);

    await renderizar();

    await act(async () => {
      screen.getByRole("button", { name: "Robótica" }).click();
    });

    expect(screen.getByText("Robô Educa")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /inscrever-se/i })).toBeInTheDocument();
  });

  it("inscrição confirmada chama aoInscrever", async () => {
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Robótica",
        descricao: "Descrição do poder.",
        trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
      },
    ]);
    vi.spyOn(trilhaApi, "inscreverNaTrilha").mockResolvedValue({
      id: "inscricao-1",
      trilha_id: "trilha-1",
      momento: "2026-08-27T00:00:00-03:00",
    });

    const aoInscrever = await renderizar();
    await act(async () => {
      screen.getByRole("button", { name: "Robótica" }).click();
    });
    await act(async () => {
      screen.getByRole("button", { name: /inscrever-se/i }).click();
    });

    expect(aoInscrever).toHaveBeenCalledWith("trilha-1");
  });

  it("nenhuma tela oferece desinscrever", async () => {
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Robótica",
        descricao: "Descrição do poder.",
        trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
      },
    ]);

    await renderizar();
    await act(async () => {
      screen.getByRole("button", { name: "Robótica" }).click();
    });

    expect(
      screen.queryByRole("button", { name: /desinscrever|cancelar|sair/i }),
    ).not.toBeInTheDocument();
  });
});
