import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ComunidadeNaLista } from "../api/leituras";
import * as leituras from "../api/leituras";
import { MapaDaListagem } from "./MapaDaListagem";
import type { MontagemDoMapa } from "./motorDoMapa";

// Critérios do PRD-03 §12 para o mapa (`RF-03-89` a `RF-03-92`, `RN-03-44` a
// `RN-03-46`). O jsdom não tem WebGL: o motor do MapLibre é substituído, e o
// que se confere é o que a tela entrega a ele (design — Decisão 4).

const montarMapa = vi.fn<(montagem: MontagemDoMapa) => () => void>(() => () => {});
vi.mock("./motorDoMapa", () => ({ montarMapa: (m: MontagemDoMapa) => montarMapa(m) }));

const CONTORNO = {
  geometria: {
    type: "Polygon",
    coordinates: [
      [
        [-38.5, -12.9],
        [-38.4, -12.9],
        [-38.4, -12.8],
        [-38.5, -12.9],
      ],
    ],
  },
  origem_osm: "relation/12582832",
  copiado_em: "2026-11-27T15:00:00-03:00",
  credito: "© colaboradores do OpenStreetMap",
  licenca: "ODbL",
};

function comunidade(parcial: Partial<ComunidadeNaLista> = {}): ComunidadeNaLista {
  return {
    id: "c1",
    nome: "Guerreira Zeferina",
    localizacao: "Salvador, Bahia",
    series_abertas: 6,
    series_ativas: 4,
    registros_validos: 40,
    continuidade: 0.75,
    guerreiros_vinculados: 23,
    contorno: CONTORNO,
    ...parcial,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
  montarMapa.mockClear();
});

describe("o mapa da listagem (RF-03-89, RF-03-90)", () => {
  it("desenha só as comunidades com contorno, com o nome e o destino", async () => {
    vi.spyOn(leituras, "listarTodasAsComunidades").mockResolvedValue([
      comunidade(),
      comunidade({ id: "c2", nome: "Sem Contorno", contorno: null }),
    ]);

    render(<MapaDaListagem />);

    await waitFor(() => expect(montarMapa).toHaveBeenCalledTimes(1));
    const { comunidades, modo } = montarMapa.mock.calls[0][0];
    expect(modo).toBe("listagem");
    expect(comunidades).toEqual([
      { id: "c1", nome: "Guerreira Zeferina", destino: "/comunidades/c1", contorno: CONTORNO },
    ]);
    expect(
      screen.getByRole("region", { name: "Mapa das Comunidades Virtuais" }),
    ).toBeVisible();
  });

  it("o contorno abre a página da comunidade", async () => {
    vi.spyOn(leituras, "listarTodasAsComunidades").mockResolvedValue([comunidade()]);
    const irPara = vi.fn();

    render(<MapaDaListagem irPara={irPara} />);

    await waitFor(() => expect(montarMapa).toHaveBeenCalled());
    montarMapa.mock.calls[0][0].irPara("c1");
    expect(irPara).toHaveBeenCalledWith("/comunidades/c1");
  });

  it("sem contorno cadastrado não monta mapa nem aviso", async () => {
    const lida = vi
      .spyOn(leituras, "listarTodasAsComunidades")
      .mockResolvedValue([comunidade({ contorno: null })]);

    const { container } = render(<MapaDaListagem />);

    await waitFor(() => expect(lida).toHaveBeenCalled());
    expect(container).toBeEmptyDOMElement();
    expect(montarMapa).not.toHaveBeenCalled();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("o crédito e a licença do OSM acompanham o mapa, em texto (RF-03-92)", async () => {
    vi.spyOn(leituras, "listarTodasAsComunidades").mockResolvedValue([comunidade()]);

    render(<MapaDaListagem />);

    expect(
      await screen.findByText("© colaboradores do OpenStreetMap · ODbL"),
    ).toBeInTheDocument();
  });

  it("o motor recebe só contorno, nome e destino — nenhum local, ponto ou coletor (RN-03-44)", async () => {
    vi.spyOn(leituras, "listarTodasAsComunidades").mockResolvedValue([comunidade()]);

    render(<MapaDaListagem />);

    await waitFor(() => expect(montarMapa).toHaveBeenCalled());
    for (const item of montarMapa.mock.calls[0][0].comunidades) {
      expect(Object.keys(item).sort()).toEqual(["contorno", "destino", "id", "nome"]);
    }
  });
});

describe("o fundo servido pela plataforma (RN-03-45)", () => {
  const estilo = JSON.parse(
    readFileSync(resolve(__dirname, "../../public/mapa/estilo.json"), "utf8"),
  );

  it("o recorte sai da própria origem da App 06", () => {
    expect(estilo.sources.recorte.url).toBe("pmtiles:///mapa/salvador.pmtiles");
  });

  it("o estilo não aponta para servidor de terceiros, nem glifo nem sprite", () => {
    expect(JSON.stringify(estilo)).not.toMatch(/https?:\/\//);
    expect(estilo.glyphs).toBeUndefined();
    expect(estilo.sprite).toBeUndefined();
  });

  it("o estilo declara o crédito e a licença do OSM", () => {
    expect(estilo.sources.recorte.attribution).toBe("© colaboradores do OpenStreetMap · ODbL");
  });
});
