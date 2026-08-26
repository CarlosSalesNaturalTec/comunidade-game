import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { CatalogoAvulso } from "./CatalogoAvulso";

const CHAVE_DE_SESSAO = "app-05:teste-catalogo-avulso";

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
        <CatalogoAvulso />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("catálogo avulso e histórico de trocas", () => {
  it("mostra os itens ativos com preço e estoque, sem ação de trocar", async () => {
    vi.spyOn(carteiraApi, "listarCatalogoAvulso").mockResolvedValue([
      {
        id: "item-1",
        nome: "Caderno personalizado",
        tipo_de_recurso_id: "recurso-1",
        estoque: 5,
        ativo: true,
        preco_em_pontos_extras: 20,
        preco_de_referencia_ausente: false,
      },
    ]);
    vi.spyOn(carteiraApi, "listarMinhasTrocas").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/caderno personalizado/i)).toBeInTheDocument();
    expect(screen.getByText(/20 pontos extras/i)).toBeInTheDocument();
    expect(screen.getByText(/estoque: 5/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /trocar/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reservar/i })).not.toBeInTheDocument();
    expect(screen.getByText(/presencialmente, com o mestre/i)).toBeInTheDocument();
  });

  it("catálogo vazio explica a ausência, sem erro", async () => {
    vi.spyOn(carteiraApi, "listarCatalogoAvulso").mockResolvedValue([]);
    vi.spyOn(carteiraApi, "listarMinhasTrocas").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/ainda não há recompensa avulsa/i)).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("histórico mostra o preço cobrado na época, sem moedas nem reais", async () => {
    vi.spyOn(carteiraApi, "listarCatalogoAvulso").mockResolvedValue([
      {
        id: "item-1",
        nome: "Caderno personalizado",
        tipo_de_recurso_id: "recurso-1",
        estoque: 5,
        ativo: true,
        preco_em_pontos_extras: 20,
        preco_de_referencia_ausente: false,
      },
    ]);
    vi.spyOn(carteiraApi, "listarMinhasTrocas").mockResolvedValue([
      {
        id: "troca-1",
        item_de_catalogo_avulso_id: "item-1",
        preco_cobrado: 15,
        registrado_em: "2026-08-01T10:00:00Z",
      },
    ]);

    await renderizar();

    expect(await screen.findByText(/preço cobrado: 15 pontos extras/i)).toBeInTheDocument();
    expect(screen.queryByText(/r\$/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/moeda/i)).not.toBeInTheDocument();
  });
});
