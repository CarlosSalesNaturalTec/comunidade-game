import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as cartaApi from "comum/carta/api";
import * as trilhaComumApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import { MinhaCarta } from "./MinhaCarta";

// As leituras que montam a carta foram promovidas a `comum/carta/api` quando a
// App 01 passou a apresentar a mesma carta (decisão do fundador de
// 2026-09-25); é de lá que os mocks partem. A identificação vem de
// `comum/autenticacao/api`, e nenhuma delas passa pelas séries de coleta
// (`RF-01-76`, decisão do fundador de 2026-09-26).

const CHAVE_DE_SESSAO = "app-05:teste-minha-carta";

function mockarLeituras(
  opcoes: { posicao?: { posicao: number; pontos_regulares: number } } = {},
) {
  vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue([
    {
      id: "poder-1",
      nome: "Poder da IA e Robótica",
      descricao: "Programação, eletrônica, robótica e IA",
      trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
    },
  ]);

  vi.spyOn(cartaApi, "obterMinhaPosicaoNoRanking").mockResolvedValue({
    minha_posicao: opcoes.posicao ?? { posicao: 3, pontos_regulares: 40 },
  });

  vi.spyOn(cartaApi, "obterProgressoDaCarta").mockResolvedValue([
    {
      trilha_id: "trilha-1",
      trilha_nome: "Robô Educa",
      nivel_atual: 3,
      badges: ["de_nivel", "de_autoria"],
    },
  ]);

  vi.spyOn(cartaApi, "obterPortfolioDaCarta").mockResolvedValue([
    { producao: "Robô de reuso da praça" },
  ]);
}

async function renderizar(identidade: { nick?: string; avatar?: string } = {}) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    divulgacao_autorizada: true,
    nick: "nick" in identidade ? identidade.nick : "Zeferina",
    avatar: "avatar" in identidade ? identidade.avatar : '{"v":1,"tom":"t3"}',
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <MinhaCarta />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("a carta do próprio Guerreiro(a) (`RF-05-50`, `RF-05-51`)", () => {
  it("o Guerreiro(a) vê a própria carta", async () => {
    mockarLeituras();

    await renderizar();

    const carta = await screen.findByRole("article", { name: /carta de zeferina/i });
    // Avatar, nick, badges, poderes com níveis, desempenho e criações
    // originais — a tabela da variante Guerreiro(a) do documento 11 §8.2.
    expect(carta.querySelector(".cg-carta__avatar svg")).not.toBeNull();
    expect(screen.getByText("Zeferina")).toBeInTheDocument();
    expect(screen.getByText(/3º na comunidade, com 40 pontos/)).toBeInTheDocument();
    expect(screen.getByText("Nível 3")).toBeInTheDocument();
    expect(carta.querySelectorAll("[data-marca]")).toHaveLength(3);
    expect(screen.getByText(/Badge de nível/)).toBeInTheDocument();
    expect(screen.getByText(/Badge de autoria/)).toBeInTheDocument();
    expect(screen.getByText("Robô de reuso da praça")).toBeInTheDocument();
  });

  it("a carta do Guerreiro(a) não expõe o que é vedado", async () => {
    mockarLeituras();

    await renderizar();

    const carta = await screen.findByRole("article", { name: /carta de zeferina/i });
    // Nem imagem real, nem nome civil, nem rede social, nem canal de contato
    // (documento 11 §8.2, invariantes 9 e 10). O avatar é SVG composto no
    // aparelho, e nenhum endereço sai da carta.
    expect(carta.querySelector("img, picture, video")).toBeNull();
    expect(carta.querySelector("a[href]")).toBeNull();
    expect(carta.textContent).not.toMatch(/@|https?:\/\//);
  });

  it("sem avatar, a carta usa o padrão do projeto", async () => {
    mockarLeituras();

    await renderizar({ avatar: undefined });

    const carta = await screen.findByRole("article", { name: /carta de zeferina/i });
    // Nenhum espaço vazio no lugar do avatar: o padrão do projeto ocupa a
    // mesma moldura, com as nove camadas desenhadas (documento 15 §7.3).
    const avatar = carta.querySelector(".cg-carta__avatar svg");
    expect(avatar).not.toBeNull();
    expect(avatar?.querySelectorAll("[data-camada]").length).toBeGreaterThan(0);
  });

  it("faltando o que a variante exige, nenhuma carta pela metade aparece", async () => {
    mockarLeituras();
    // Sem desempenho a variante do documento 11 §8.2 não fecha — a Área diz o
    // que tem, em outra forma.
    vi.spyOn(cartaApi, "obterMinhaPosicaoNoRanking").mockRejectedValue(
      Object.assign(new Error("sem vínculo"), { codigo: "permissao_negada" }),
    );

    await renderizar();

    expect(await screen.findByText(/A sua carta aparece aqui quando/i)).toBeInTheDocument();
    expect(screen.queryByRole("article")).not.toBeInTheDocument();
  });

  it("a carta aparece sem série de coleta aberta, com desempenho zerado", async () => {
    // O defeito que esta fatia corrige: a comunidade vinha das séries de
    // coleta, e quem nunca abriu série não tinha carta (decisão do fundador de
    // 2026-09-26). Nenhuma leitura de série é chamada aqui.
    mockarLeituras({ posicao: { posicao: 7, pontos_regulares: 0 } });

    await renderizar();

    const carta = await screen.findByRole("article", { name: /carta de zeferina/i });
    expect(carta).toBeInTheDocument();
    expect(screen.getByText(/7º na comunidade, com 0 pontos/)).toBeInTheDocument();
    expect(cartaApi).not.toHaveProperty("listarMinhasSeriesDaCarta");
  });
});
