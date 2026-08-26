import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as coletaApi from "../api/coleta";
import { HistoricoDaSerie } from "./HistoricoDaSerie";

const CHAVE_DE_SESSAO = "app-05:teste-historico-da-serie";

const SERIE: coletaApi.SerieDoGuerreiro = {
  id: "serie-1",
  desafio_de_coleta_id: "desafio-1",
  local_id: "local-1",
  comunidade_virtual_id: "comunidade-1",
  cadencia: "semanal",
  estado: "ativa",
  pontos: 5,
  proxima_medicao: null,
  tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
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
        <HistoricoDaSerie serie={SERIE} aoVoltar={() => {}} />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("histórico da série", () => {
  it("mostra o motivo do registro invalidado, e que só ele perdeu os pontos", async () => {
    vi.spyOn(coletaApi, "listarHistoricoDaSerie").mockResolvedValue({
      itens: [
        {
          id: "registro-invalidado",
          momento_do_fato: "2026-08-10T12:00:00Z",
          valor: 200,
          unidade: "°C",
          midia_referencia: null,
          origem: "manual",
          situacao: "invalidada",
          a_conferir: false,
          pontos_creditados: 0,
          motivo_da_invalidacao: "Medição fora do padrão do sensor da rua.",
        },
        {
          id: "registro-valido",
          momento_do_fato: "2026-08-03T12:00:00Z",
          valor: 25,
          unidade: "°C",
          midia_referencia: null,
          origem: "manual",
          situacao: "valida",
          a_conferir: false,
          pontos_creditados: 5,
          motivo_da_invalidacao: null,
        },
      ],
      proximo_cursor: null,
    });

    await renderizar();

    expect(
      await screen.findByText(/medição fora do padrão do sensor da rua/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/só ele perdeu os pontos/i)).toBeInTheDocument();
    expect(screen.getByText(/pontos: 5/i)).toBeInTheDocument();
  });
});
