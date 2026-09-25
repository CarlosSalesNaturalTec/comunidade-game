import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as cartaApi from "comum/carta/api";
import * as trilhaComumApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import { MinhaCarta } from "./MinhaCarta";

// As quatro leituras que montam a carta foram promovidas a `comum/carta/api`
// quando a App 01 passou a apresentar a mesma carta (decisão do fundador de
// 2026-09-25); é de lá que os mocks partem.

const CHAVE_DE_SESSAO = "app-05:teste-minha-carta";

const SERIE = { comunidade_virtual_id: "comunidade-1" };

function mockarLeituras(opcoes: { avatar?: string | null } = {}) {
  vi.spyOn(cartaApi, "listarMinhasSeriesDaCarta").mockResolvedValue({ itens: [SERIE] });

  vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue([
    {
      id: "poder-1",
      nome: "Poder da IA e Robótica",
      descricao: "Programação, eletrônica, robótica e IA",
      trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
    },
  ]);

  vi.spyOn(cartaApi, "obterMinhaPosicaoNoRanking").mockResolvedValue({
    minha_posicao: {
      avatar: opcoes.avatar === undefined ? '{"v":1,"tom":"t3"}' : opcoes.avatar,
      nick: "Zeferina",
      posicao: 3,
      pontos_regulares: 40,
    },
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

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    divulgacao_autorizada: true,
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
    mockarLeituras({ avatar: null });

    await renderizar();

    const carta = await screen.findByRole("article", { name: /carta de zeferina/i });
    // Nenhum espaço vazio no lugar do avatar: o padrão do projeto ocupa a
    // mesma moldura, com as nove camadas desenhadas (documento 15 §7.3).
    const avatar = carta.querySelector(".cg-carta__avatar svg");
    expect(avatar).not.toBeNull();
    expect(avatar?.querySelectorAll("[data-camada]").length).toBeGreaterThan(0);
  });

  it("faltando o que a variante exige, nenhuma carta pela metade aparece", async () => {
    mockarLeituras();
    // Sem comunidade não há ranking, e sem ranking não há avatar, nick nem
    // desempenho — a Área diz o que tem, em outra forma.
    vi.spyOn(cartaApi, "listarMinhasSeriesDaCarta").mockResolvedValue({ itens: [] });

    await renderizar();

    expect(await screen.findByText(/A sua carta aparece aqui quando/i)).toBeInTheDocument();
    expect(screen.queryByRole("article")).not.toBeInTheDocument();
  });
});
