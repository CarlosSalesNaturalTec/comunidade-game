import { render, screen } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SecaoDeMestres } from "../adultos/SecaoDeMestres";
import { SecaoDeGuerreiros } from "../guerreiros/SecaoDeGuerreiros";
import { SecaoDoPortfolio } from "../portfolio/SecaoDoPortfolio";

/**
 * O arquivo que **nunca** chama `configurarAcessoAoNucleo`.
 *
 * É a única forma de afirmar o que a spec exige — "a configuração de acesso ao
 * núcleo alcança as seções no navegador". A App 06 é Astro e não tem
 * `main.tsx`: quando a migração apagou aquele arquivo, a configuração passou a
 * acontecer só no `astro build`, e **toda** seção de leitura passou a falhar no
 * navegador antes de qualquer requisição sair. Nenhum teste viu, porque o único
 * que chegava à camada de rede fornecia a configuração por conta própria.
 *
 * Em arquivo separado de propósito: a configuração vive em estado de módulo, e
 * o registro de módulos do Vitest é por arquivo. Dentro de um arquivo que já
 * configura, este teste passaria por engano (design — decisão 5).
 *
 * Aqui dubla-se **só o `fetch`**. As demais seções de leitura passam pelo mesmo
 * gargalo — `lerDoNucleo` —, então o que vale para esta vale para as nove.
 */

// Como a produção a entrega. Nenhuma chamada de configuração no teste.
vi.mock("../api/configuracao", async () => {
  const real =
    await vi.importActual<typeof import("../api/configuracao")>("../api/configuracao");
  return {
    ...real,
    CHAVE_DE_APLICACAO: "chave-da-app-06",
    URL_DO_NUCLEO: "https://nucleo.example.org",
  };
});

const UM_GUERREIRO = {
  itens: [
    {
      avatar: "avatar-de-teste",
      nick: "ZeBita",
      badges: [{ familia: "de_nivel", poder: "Poder do Código" }],
      poderes: [{ poder: "Poder do Código", nivel: 3 }],
      pontos_regulares: 40,
      posicao_no_ranking: 1,
      criacoes: [{ trilha: "Trilha da Água", validada_em: "2026-08-01T10:00:00Z" }],
    },
  ],
  proximo_cursor: null,
};

function dublarFetch(corpo: unknown, status = 200) {
  return vi.spyOn(globalThis, "fetch").mockResolvedValue(
    new Response(JSON.stringify(corpo), {
      status,
      headers: { "Content-Type": "application/json" },
    }),
  );
}

describe("a configuração de acesso ao núcleo alcança as seções no navegador", () => {
  beforeEach(() => {
    vi.stubGlobal("matchMedia", (consulta: string) => ({
      matches: false,
      media: consulta,
      addEventListener: () => {},
      removeEventListener: () => {},
    }));
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("a chamada sai com a chave da App 06 e sem credencial de persona (RF-03-02, RN-03-33)", async () => {
    const buscar = dublarFetch(UM_GUERREIRO);

    render(<SecaoDeGuerreiros />);
    expect(await screen.findByText("ZeBita")).toBeVisible();

    // Se a configuração não alcançasse o navegador, `chamarNucleo` lançaria
    // antes daqui e `fetch` nunca teria sido chamado.
    expect(buscar).toHaveBeenCalled();
    const [endereco, opcoes] = buscar.mock.calls[0];
    expect(String(endereco)).toBe("https://nucleo.example.org/v1/vitrine/guerreiros");
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-da-app-06");
    expect(cabecalhos.Authorization).toBeUndefined();
  });

  it("a seção apresenta o que leu, e não o aviso de erro (RF-03-02)", async () => {
    dublarFetch(UM_GUERREIRO);

    render(<SecaoDeGuerreiros />);

    expect(await screen.findByText("ZeBita")).toBeVisible();
    expect(
      screen.queryByText("Não foi possível carregar os cards agora. Tente de novo."),
    ).not.toBeInTheDocument();
  });

  it("as seções que leem na visita apresentam o que leram (RF-03-02, RF-03-15)", async () => {
    // O cenário fala das **seções**, no plural: o defeito deixava o
    // institucional de pé — ele vem da publicação — e todas as demais no aviso
    // de erro. Três seções diferentes, cada uma com a sua rota, pelo mesmo
    // gargalo: é o que afirma que a correção vale para as nove, e não para uma.
    const porCaminho: Record<string, unknown> = {
      "/v1/vitrine/guerreiros": UM_GUERREIRO,
      "/v1/vitrine/criacoes": {
        itens: [
          {
            trilha_id: "t-2",
            trilha: "Trilha do Vento",
            validada_em: "2026-08-01T10:00:00Z",
            producao: "Mapa da nascente",
            autores: [{ avatar: "avatar-de-teste", nick: "ZeBita" }],
          },
        ],
        proximo_cursor: null,
      },
      "/v1/vitrine/mestres": {
        itens: [
          {
            id: "m-1",
            avatar: "avatar-de-teste",
            avatar_padrao: false,
            identificacao: { valor: "Dona Rosa", tipo: "nome" },
            areas_de_habilidade: ["Ciências"],
            artefatos: [],
            trilhas_de_autoria: [
              { id: "t-1", nome: "Trilha da Água", area_do_conhecimento: "Ciências" },
            ],
            absorcoes: 2,
          },
        ],
        proximo_cursor: null,
      },
    };

    vi.spyOn(globalThis, "fetch").mockImplementation((endereco) => {
      const { pathname } = new URL(String(endereco));
      const corpo = porCaminho[pathname];
      if (corpo === undefined) throw new Error(`rota não dublada: ${pathname}`);
      return Promise.resolve(
        new Response(JSON.stringify(corpo), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );
    });

    render(
      <>
        <SecaoDeGuerreiros />
        <SecaoDoPortfolio />
        <SecaoDeMestres />
      </>,
    );

    expect(await screen.findByText("ZeBita")).toBeVisible();
    expect(await screen.findByText("Trilha do Vento")).toBeVisible();
    expect(await screen.findByText("Dona Rosa")).toBeVisible();

    for (const aviso of [
      "Não foi possível carregar os cards agora. Tente de novo.",
      "Não foi possível carregar o portfólio agora. Tente de novo.",
    ]) {
      expect(screen.queryByText(aviso), aviso).not.toBeInTheDocument();
    }
  });

  it("a leitura que falha falha pelo núcleo, e não pela configuração (RF-03-02)", async () => {
    // O núcleo recusa. A seção avisa — e o aviso é sobre a resposta do núcleo,
    // não sobre configuração em falta: a requisição chegou a sair.
    const buscar = dublarFetch({ codigo: "erro_interno", mensagem: "Falhou." }, 500);

    render(<SecaoDeGuerreiros />);

    expect(
      await screen.findByText("Não foi possível carregar os cards agora. Tente de novo."),
    ).toBeVisible();
    expect(buscar).toHaveBeenCalled();
  });
});
