import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("comum/api", async () => {
  const real = await vi.importActual<typeof import("comum/api")>("comum/api");
  return { ...real, chamarNucleo: vi.fn() };
});

import { chamarNucleo } from "comum/api";
import { cadastrarTipoDeRecurso } from "../recursos/api";
import { cadastrarTipoDeColeta, listarTodosOsTiposDeColeta, type TipoDeColeta } from "./api";

// As três funções que a área Catálogos estreia. O teste de tela dubla os
// módulos inteiros, então é aqui que a rota, o método e o laço da paginação
// são de fato executados (`RF-02-107`, `RF-02-108`).
const dublada = vi.mocked(chamarNucleo);

function tipoDeColeta(sobrescreve: Partial<TipoDeColeta> = {}): TipoDeColeta {
  return {
    id: "tipo-1",
    nome: "Temperatura",
    forma_de_registro: "numero",
    unidade: "°C",
    faixa_minima: -10,
    faixa_maxima: 55,
    ativo: true,
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.resetAllMocks();
});

describe("listarTodosOsTiposDeColeta", () => {
  it("segue o cursor até o fim e devolve uma lista só", async () => {
    dublada
      .mockResolvedValueOnce({
        itens: [tipoDeColeta({ id: "tipo-1" })],
        proximo_cursor: "cursor-2",
      })
      .mockResolvedValueOnce({
        itens: [tipoDeColeta({ id: "tipo-2" })],
        proximo_cursor: null,
      });

    const tipos = await listarTodosOsTiposDeColeta("token-do-admin");

    expect(tipos.map((tipo) => tipo.id)).toEqual(["tipo-1", "tipo-2"]);
    expect(dublada).toHaveBeenNthCalledWith(1, "/v1/tipos-de-coleta", {
      token: "token-do-admin",
    });
    expect(dublada).toHaveBeenNthCalledWith(2, "/v1/tipos-de-coleta?cursor=cursor-2", {
      token: "token-do-admin",
    });
  });

  it("devolve lista vazia quando o catálogo está vazio", async () => {
    dublada.mockResolvedValueOnce({ itens: [], proximo_cursor: null });

    expect(await listarTodosOsTiposDeColeta("token-do-admin")).toEqual([]);
    expect(dublada).toHaveBeenCalledTimes(1);
  });
});

describe("cadastrarTipoDeColeta", () => {
  it("posta na rota do catálogo com o corpo declarado", async () => {
    dublada.mockResolvedValueOnce(tipoDeColeta());

    await cadastrarTipoDeColeta(
      {
        nome: "Temperatura",
        forma_de_registro: "numero",
        unidade: "°C",
        faixa_minima: -10,
        faixa_maxima: 55,
      },
      "token-do-admin",
    );

    expect(dublada).toHaveBeenCalledWith("/v1/tipos-de-coleta", {
      metodo: "POST",
      corpo: {
        nome: "Temperatura",
        forma_de_registro: "numero",
        unidade: "°C",
        faixa_minima: -10,
        faixa_maxima: 55,
      },
      token: "token-do-admin",
    });
  });
});

describe("cadastrarTipoDeRecurso", () => {
  it("posta o tipo e a primeira vigência num corpo só", async () => {
    dublada.mockResolvedValueOnce({});

    await cadastrarTipoDeRecurso(
      {
        nome: "Lanche",
        natureza: "consumivel",
        unidade: "kit",
        valor_em_moedas: "12.50",
        vigencia_inicio: "2026-09-09",
        exige_comprovante: false,
      },
      "token-do-admin",
    );

    expect(dublada).toHaveBeenCalledWith("/v1/tipos-de-recurso", {
      metodo: "POST",
      corpo: {
        nome: "Lanche",
        natureza: "consumivel",
        unidade: "kit",
        valor_em_moedas: "12.50",
        vigencia_inicio: "2026-09-09",
        exige_comprovante: false,
      },
      token: "token-do-admin",
    });
  });
});
