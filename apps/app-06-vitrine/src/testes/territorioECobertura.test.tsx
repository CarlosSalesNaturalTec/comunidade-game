import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type {
  CoberturaDeOds,
  ComunidadeNaLista,
  ComunidadePublica,
  MetodologiaDoRecorte,
  SeriePublica,
} from "../api/leituras";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12 para o painel do território, a cobertura
// da Agenda 2030 e o bloco do gestor: o dado sai agregado até o bairro e sem
// coletor, cada recorte declara a metodologia, a série interrompida continua
// visível e o gestor lê os limites antes do painel.

const ID_DA_COMUNIDADE = "11111111-1111-1111-1111-111111111111";

function comunidadeNaLista(parcial: Partial<ComunidadeNaLista> = {}): ComunidadeNaLista {
  return {
    id: ID_DA_COMUNIDADE,
    nome: "Guerreira Zeferina",
    localizacao: "Salvador, Bahia",
    series_abertas: 6,
    series_ativas: 4,
    registros_validos: 40,
    continuidade: 0.75,
    guerreiros_vinculados: 23,
    ...parcial,
  };
}

function metodologia(parcial: Partial<MetodologiaDoRecorte> = {}): MetodologiaDoRecorte {
  return {
    recorte: {
      tipo_de_coleta_id: "tipo-1",
      tipo_de_coleta_nome: "Temperatura",
      local_publicado_id: "bairro-1",
      local_publicado_nivel: "bairro",
      local_publicado_rotulo: "Bairro A",
    },
    unidade: "°C",
    cadencias: ["semanal"],
    origens: ["manual", "sensor"],
    primeira_medicao: "2026-06-01T12:00:00Z",
    ultima_medicao: "2026-08-30T12:00:00Z",
    registros_validos: 30,
    ativo: true,
    ...parcial,
  };
}

function comLeituras({
  comunidades = [comunidadeNaLista()],
  recortes = [metodologia()],
  cobertura = [
    {
      comunidade_id: ID_DA_COMUNIDADE,
      comunidade_nome: "Guerreira Zeferina",
      objetivos: [6, 11, 13],
      ciclo: "Ciclo 01",
    } satisfies CoberturaDeOds,
  ],
}: {
  comunidades?: ComunidadeNaLista[];
  recortes?: MetodologiaDoRecorte[];
  cobertura?: CoberturaDeOds[];
} = {}) {
  const serie: SeriePublica = {
    itens: recortes.map((item) => ({
      momento_da_medicao: item.primeira_medicao,
      valor: 27.5,
      recorte: item.recorte,
    })),
    proximo_cursor: null,
    recortes,
  };
  const ficha: ComunidadePublica = {
    id: ID_DA_COMUNIDADE,
    nome: "Guerreira Zeferina",
    locais: [
      { id: "raiz", nivel: "comunidade", rotulo: "Comunidade", local_pai_id: null },
      { id: "bairro-1", nivel: "bairro", rotulo: "Bairro A", local_pai_id: "raiz" },
    ],
    tipos_de_coleta: [{ id: "tipo-1", nome: "Temperatura" }],
    guerreiros_vinculados: 23,
  };
  vi.spyOn(leituras, "listarComunidades").mockResolvedValue({
    itens: comunidades,
    proximo_cursor: null,
    ciclo_rotulo: "Ciclo 01",
  });
  vi.spyOn(leituras, "obterComunidade").mockResolvedValue(ficha);
  vi.spyOn(leituras, "lerSerieDaComunidade").mockResolvedValue(serie);
  vi.spyOn(leituras, "lerCoberturaDeOds").mockResolvedValue(cobertura);
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);
}

describe("a seção de Comunidades Virtuais", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });
  afterEach(() => vi.restoreAllMocks());

  it("apresenta cada comunidade em card, com uma única leitura (RF-03-02)", async () => {
    comLeituras({ comunidades: [comunidadeNaLista(), comunidadeNaLista({ id: "outra" })] });
    render(<App />);

    expect(await screen.findAllByText("Guerreira Zeferina")).toHaveLength(2);
    expect(screen.getAllByText("Salvador, Bahia")).toHaveLength(2);
    expect(screen.getAllByText("23")).toHaveLength(2);
    // Uma leitura monta todos os cards — nunca uma por card (`RF-03-36`).
    expect(leituras.listarComunidades).toHaveBeenCalledTimes(1);
    expect(leituras.obterComunidade).not.toHaveBeenCalled();
  });

  it("o card abre a página da comunidade, em endereço próprio (RF-03-15)", async () => {
    comLeituras();
    render(<App />);

    const abrir = await screen.findAllByRole("button", { name: /Ver o território/ });
    await userEvent.click(abrir[0]);

    expect(window.location.pathname).toBe(`/comunidades/${ID_DA_COMUNIDADE}`);
    expect(await screen.findByText("Séries do território")).toBeVisible();
  });

  it("comunidade recém-criada aparece como território vazio (RF-03-20)", async () => {
    comLeituras({
      comunidades: [
        comunidadeNaLista({
          series_abertas: 0,
          series_ativas: 0,
          registros_validos: 0,
          continuidade: null,
          guerreiros_vinculados: 0,
        }),
      ],
    });
    render(<App />);

    // Nome e contorno, sem preenchimento — e nada de erro nem de ausência.
    expect(await screen.findByText(/Território ainda vazio/)).toBeVisible();
    expect(
      screen.getByRole("img", { name: /Território de Guerreira Zeferina, ainda vazio/ }),
    ).toBeVisible();
  });

  it("cada recorte de leitura lê a lista uma única vez (design — Decisão 7)", async () => {
    comLeituras();
    window.history.pushState(null, "", "/pesquisadores");
    render(<App />);

    expect(await screen.findByText("Séries do território e metodologia")).toBeVisible();
    expect(leituras.listarComunidades).toHaveBeenCalledTimes(1);
  });

  it("comunidade abaixo do piso sai em outra forma, não em card incompleto (RN-08-28)", async () => {
    comLeituras({
      comunidades: [
        comunidadeNaLista({
          series_abertas: null,
          series_ativas: null,
          registros_validos: null,
          continuidade: null,
        }),
      ],
    });
    const { container } = render(<App />);

    expect(await screen.findByText(/Indicadores ainda não publicados/)).toBeVisible();
    expect(screen.getByText("Guerreira Zeferina")).toBeVisible();
    expect(container.querySelector(".cg-carta")).toBeNull();
  });
});

describe("o painel do território de uma comunidade", () => {
  beforeEach(() => {
    window.history.pushState(null, "", `/comunidades/${ID_DA_COMUNIDADE}`);
  });
  afterEach(() => vi.restoreAllMocks());

  it("declara a metodologia e os registros válidos de cada recorte (RF-03-17, RF-03-18)", async () => {
    comLeituras();
    render(<App />);

    expect(await screen.findByText(/Temperatura — Bairro A/)).toBeVisible();
    expect(screen.getByText("Temperatura (°C)")).toBeVisible();
    expect(screen.getByText("semanal")).toBeVisible();
    expect(screen.getByText("2026-06-01 a 2026-08-30")).toBeVisible();
    expect(screen.getByText("manual, sensor")).toBeVisible();
    expect(screen.getByText("30")).toBeVisible();
  });

  it("o recorte inativo aparece sinalizado, sem sumir (RF-03-19)", async () => {
    comLeituras({ recortes: [metodologia({ ativo: false })] });
    render(<App />);

    expect(await screen.findByText(/Temperatura — Bairro A/)).toBeVisible();
    // A condição se lê em texto, não por cor.
    expect(screen.getByText(/Série inativa — a coleta parou, o dado permanece/)).toBeVisible();
  });

  it("não apresenta recorte abaixo do bairro nem identifica coletor (RF-03-16, RN-03-09)", async () => {
    comLeituras({
      recortes: [
        metodologia(),
        metodologia({
          recorte: {
            tipo_de_coleta_id: "tipo-2",
            tipo_de_coleta_nome: "Resíduos",
            local_publicado_id: "raiz",
            local_publicado_nivel: "comunidade",
            local_publicado_rotulo: "Comunidade",
          },
        }),
      ],
    });
    const { container } = render(<App />);

    expect(await screen.findByText(/Temperatura — Bairro A/)).toBeVisible();
    // Todo recorte apresentado para no bairro: a rota não serve nível mais
    // fino, e a tela não monta nenhum.
    const recortes = [...container.querySelectorAll(".cg-territorio-painel__recorte h4")].map(
      (titulo) => titulo.textContent ?? "",
    );
    expect(recortes).toEqual(["Temperatura — Bairro A", "Resíduos — Comunidade"]);
    for (const titulo of recortes) {
      expect(titulo).not.toMatch(/rua|condomínio|bloco|quadra/i);
    }
    // Nenhum campo de coletor chega à tela, e quem precisa de granularidade
    // fina lê por onde pedir o conjunto completo.
    const pontos = container.querySelector(".cg-territorio-painel__pontos")?.textContent ?? "";
    expect(pontos).not.toMatch(/nick|avatar|coletor/i);
    expect(container.textContent).toMatch(
      /Rua, condomínio, bloco e quadra só saem no conjunto completo/,
    );
  });

  it("a cobertura da comunidade sai por ciclo, sem etiqueta por pessoa (RF-03-22, RF-03-24)", async () => {
    comLeituras();
    render(<App />);

    expect(await screen.findByText(/Ciclo Ciclo 01: objetivos 6, 11, 13/)).toBeVisible();
    expect(screen.getByText(/Meta 17.18/)).toBeVisible();
    expect(screen.getByText(/adoção voluntária do Brasil/)).toBeVisible();
  });
});

describe("o recorte de gestores públicos", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/gestores-publicos");
  });
  afterEach(() => vi.restoreAllMocks());

  it("abre com o bloco em destaque, antes do painel (RF-03-63, RF-03-64)", async () => {
    comLeituras();
    const { container } = render(<App />);

    const titulos = [...container.querySelectorAll("h2")].map((titulo) => titulo.textContent);
    expect(titulos[0]).toBe("Para que a plataforma serve ao município");
    expect(screen.getByText(/Resíduos acumulados/)).toBeVisible();
    expect(screen.getByText(/Como pedir o conjunto completo/)).toBeVisible();
  });

  it("o bloco declara os dois limites do dado (RF-03-65, RN-03-28)", async () => {
    comLeituras();
    render(<App />);

    expect(screen.getByText(/agregado e anonimizado/)).toBeVisible();
    expect(screen.getByText(/não substitui indicador oficial/)).toBeVisible();
  });

  it("a cobertura agregada lista as comunidades do ciclo (RF-03-22)", async () => {
    comLeituras();
    render(<App />);

    expect(await screen.findByText("Objetivos cobertos: 6, 11, 13")).toBeVisible();
    expect(screen.getByText("Ciclo Ciclo 01")).toBeVisible();
  });
});
