import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as trilhaComumApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { Progresso } from "./Progresso";

const CATALOGO = [
  {
    id: "poder-1",
    nome: "Poder da IA e Robótica",
    descricao: "Programação, eletrônica, robótica e IA",
    trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
  },
];

const CHAVE_DE_SESSAO = "app-05:teste-progresso";

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue(CATALOGO);
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <Progresso />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("progresso", () => {
  it("mostra o nível e quantas faltam, nunca saldo de pontos como nível", async () => {
    vi.spyOn(trilhaApi, "obterProgresso").mockResolvedValue([
      {
        trilha_id: "trilha-1",
        trilha_nome: "Robô Educa",
        nivel_atual: 2,
        obrigatorias_desbloqueadas: 2,
        obrigatorias_totais: 5,
        pontos_regulares: 40,
        badges: ["de_nivel", "de_nivel"],
      },
    ]);

    await renderizar();

    expect(await screen.findByText("Robô Educa")).toBeInTheDocument();
    expect(screen.getByText(/nível 2/i)).toBeInTheDocument();
    expect(screen.getByText(/faltam 3 de 5/i)).toBeInTheDocument();
    expect(screen.getByText(/pontos: 40/i)).toBeInTheDocument();
  });

  it("sem trilha inscrita, avisa sem erro", async () => {
    vi.spyOn(trilhaApi, "obterProgresso").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/não está inscrito/i)).toBeInTheDocument();
  });
});

describe("o nível e o badge do documento 15 §§8.2, 8.3", () => {
  it("o nível aparece como marcas contáveis", async () => {
    vi.spyOn(trilhaApi, "obterProgresso").mockResolvedValue([
      {
        trilha_id: "trilha-1",
        trilha_nome: "Robô Educa",
        nivel_atual: 3,
        obrigatorias_desbloqueadas: 3,
        obrigatorias_totais: 5,
        pontos_regulares: 60,
        badges: [],
      },
    ]);

    await renderizar();

    const emblema = await screen.findByText("Nível 3");
    const moldura = emblema.closest(".cg-emblema-de-nivel");
    expect(moldura).not.toBeNull();
    // Três marcas, contáveis, **além** do numeral — nunca só o numeral.
    expect(moldura?.querySelectorAll("[data-marca]")).toHaveLength(3);
    // E a moldura carrega o nome do poder: emblema global não existe.
    expect(screen.getByText("Poder da IA e Robótica")).toBeInTheDocument();
  });

  it("o badge aparece pela silhueta da família, não como texto solto", async () => {
    vi.spyOn(trilhaApi, "obterProgresso").mockResolvedValue([
      {
        trilha_id: "trilha-1",
        trilha_nome: "Robô Educa",
        nivel_atual: 2,
        obrigatorias_desbloqueadas: 2,
        obrigatorias_totais: 5,
        pontos_regulares: 40,
        badges: ["de_nivel", "de_autoria"],
      },
    ]);

    await renderizar();

    await screen.findByText("Robô Educa");
    const silhuetas = [...document.querySelectorAll("[data-silhueta]")];
    expect(silhuetas.map((forma) => forma.getAttribute("data-silhueta"))).toEqual([
      "escudo",
      "folha-com-canto-dobrado",
    ]);
    // Cada badge leva o glifo do poder dentro da silhueta e o rótulo ao lado —
    // nunca a contagem crua de antes.
    expect(document.querySelectorAll(".cg-badge__glifo svg")).toHaveLength(2);
    expect(screen.getByText(/Badge de nível — Poder da IA e Robótica/)).toBeInTheDocument();
    expect(screen.queryByText(/^Badges: /)).not.toBeInTheDocument();
  });
});
