import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { Conquistas } from "./Conquistas";

const CHAVE_DE_SESSAO = "app-05:teste-conquistas";

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
        <Conquistas />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("recompensas de marco conquistadas", () => {
  it("mostra a conquista aguardando o Mestre, sem caminho de compra", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([
      {
        recompensa_de_marco_id: "recompensa-1",
        trilha_id: "trilha-1",
        missao_id: "missao-1",
        tipo_de_recurso_id: "recurso-1",
        quantidade: 1,
        entregue: false,
        entregue_em: null,
      },
    ]);

    await renderizar();

    expect(await screen.findByText(/aguardando o mestre confirmar/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /comprar/i })).not.toBeInTheDocument();
  });

  it("mostra a entrega confirmada com a data", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([
      {
        recompensa_de_marco_id: "recompensa-1",
        trilha_id: "trilha-1",
        missao_id: "missao-1",
        tipo_de_recurso_id: "recurso-1",
        quantidade: 1,
        entregue: true,
        entregue_em: "2026-08-01T10:00:00Z",
      },
    ]);

    await renderizar();

    expect(await screen.findByText(/entregue em/i)).toBeInTheDocument();
  });

  it("sem conquista nenhuma, explica em vez de mostrar tela vazia", async () => {
    vi.spyOn(carteiraApi, "listarMinhasRecompensas").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/ainda não conquistou/i)).toBeInTheDocument();
  });
});
