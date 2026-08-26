import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as coletaApi from "../api/coleta";
import { ListaDeSeries } from "./ListaDeSeries";

const CHAVE_DE_SESSAO = "app-05:teste-lista-de-series";

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
        <ListaDeSeries
          aoAbrirNovaSerie={() => {}}
          aoVerSolicitacoes={() => {}}
          aoRegistrarNaSerie={() => {}}
          aoVerHistorico={() => {}}
        />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("lista das minhas séries", () => {
  it("mostra o que mede, o local, o estado, a próxima medição e os pontos", async () => {
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [
        {
          id: "serie-1",
          desafio_de_coleta_id: "desafio-1",
          local_id: "local-1",
          comunidade_virtual_id: "comunidade-1",
          cadencia: "semanal",
          estado: "ativa",
          pontos: 15,
          proxima_medicao: "2026-09-01T00:00:00Z",
          tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
        },
      ],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "listarLocaisDaComunidade").mockResolvedValue({
      itens: [
        {
          id: "local-1",
          comunidade_virtual_id: "comunidade-1",
          nivel: "rua",
          rotulo: "Rua das Flores",
          local_pai_id: null,
        },
      ],
      proximo_cursor: null,
    });

    await renderizar();

    expect(await screen.findByText(/temperatura/i)).toBeInTheDocument();
    expect(screen.getByText(/rua das flores/i)).toBeInTheDocument();
    expect(screen.getByText(/próxima medição/i)).toBeInTheDocument();
    expect(screen.getByText(/pontos rendidos: 15/i)).toBeInTheDocument();
  });

  it("série interrompida é sinalizada, com os pontos preservados e o caminho de retomada", async () => {
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [
        {
          id: "serie-1",
          desafio_de_coleta_id: "desafio-1",
          local_id: "local-1",
          comunidade_virtual_id: "comunidade-1",
          cadencia: "semanal",
          estado: "interrompida",
          pontos: 5,
          proxima_medicao: null,
          tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
        },
      ],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "listarLocaisDaComunidade").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    await renderizar();

    expect(await screen.findByRole("alert")).toHaveTextContent(/pontos.*continuam valendo/i);
    expect(screen.getByText(/pontos rendidos: 5/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /registrar de novo/i })).toBeInTheDocument();
  });

  it("mostra só as séries que o núcleo devolveu para esta sessão", async () => {
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [
        {
          id: "serie-minha",
          desafio_de_coleta_id: "desafio-1",
          local_id: "local-1",
          comunidade_virtual_id: "comunidade-1",
          cadencia: "semanal",
          estado: "ativa",
          pontos: 0,
          proxima_medicao: null,
          tipo_de_coleta: { nome: "Só a minha", forma_de_registro: "numero", unidade: null },
        },
      ],
      proximo_cursor: null,
    });
    vi.spyOn(coletaApi, "listarLocaisDaComunidade").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    await renderizar();

    expect(await screen.findAllByRole("listitem")).toHaveLength(1);
  });
});
