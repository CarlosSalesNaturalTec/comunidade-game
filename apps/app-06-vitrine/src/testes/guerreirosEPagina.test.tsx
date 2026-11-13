import { act, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CartaDoPersonagem, cartaEstaCompleta } from "comum/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { CriacaoPublica, GuerreiroPublico, ItemDeRankingPublico } from "../api/leituras";
import * as leituras from "../api/leituras";
import { cartaDoGuerreiro } from "../guerreiros/carta";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12 para a seção de Guerreiros e Guerreiras e
// a página individual: a seção traz **só a consulta por nick exato**, nenhuma
// tela pública rotaciona conteúdo, e a página individual segue alcançável
// pela consulta, pela linha do ranking e pelo nick do autor no portfólio
// (`RF-03-03`, `RF-03-11`, `RF-03-12`, `RF-03-13`).

function guerreiro(nick: string, posicao = 1): GuerreiroPublico {
  return {
    avatar: "avatar-de-teste",
    nick,
    badges: [{ familia: "de_nivel", poder: "Poder do Código" }],
    poderes: [{ poder: "Poder do Código", nivel: 3 }],
    pontos_regulares: 40,
    posicao_no_ranking: posicao,
    criacoes: [noPortfolio(nick)],
  };
}

function noRanking(nick: string, posicao = 1): ItemDeRankingPublico {
  return { avatar: "avatar-de-teste", nick, pontos_regulares: 40, posicao };
}

function noPortfolio(nick: string): CriacaoPublica {
  return {
    id: `c-${nick}`,
    fonte: "criacao_original",
    // Na criação da culminância o título **é** o nome da trilha
    // (`RN-03-43`).
    titulo: "Trilha da Água",
    tipo: "texto",
    trilha_id: "t-1",
    trilha: "Trilha da Água",
    validada_em: "2026-08-01T10:00:00Z",
    producao: "Produção de teste.",
    autores: [{ avatar: "avatar-de-teste", nick }],
  };
}

function comLeituras({
  guerreiros = [] as GuerreiroPublico[],
  ranking = [] as ItemDeRankingPublico[],
  criacoes = [] as CriacaoPublica[],
} = {}) {
  vi.spyOn(leituras, "obterGuerreiroPorNick").mockImplementation(async (nick) => {
    const achado = guerreiros.find((item) => item.nick === nick);
    if (!achado) throw new Error("não encontrado");
    return achado;
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({
    itens: criacoes,
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({
    itens: ranking,
    proximo_cursor: null,
  });
}

function declararMovimentoReduzido(reduzido: boolean) {
  vi.stubGlobal("matchMedia", (consulta: string) => ({
    matches: reduzido && consulta.includes("prefers-reduced-motion"),
    media: consulta,
    addEventListener: () => {},
    removeEventListener: () => {},
  }));
}

describe("a seção de Guerreiros e Guerreiras", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    declararMovimentoReduzido(false);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("traz a consulta por nick exato e nenhum Guerreiro(a) (RF-03-12, RF-03-13)", async () => {
    comLeituras({ guerreiros: [guerreiro("heroina-do-bairro")] });
    render(<App />);

    const secao = (
      await screen.findByRole("heading", { name: "Guerreiros e Guerreiras" })
    ).closest("section") as HTMLElement;

    expect(secao.querySelector('form[aria-label="Procurar por nick"]')).not.toBeNull();
    expect(secao.textContent).toMatch(/A vitrine não lista quem está cadastrado/);
    // Nenhum Guerreiro(a) é apresentado: nem lista, nem card, nem paginação.
    expect(secao.textContent).not.toContain("heroina-do-bairro");
    expect(secao.querySelector(".cg-lista-de-registros")).toBeNull();
    expect(secao.querySelector(".cg-carta")).toBeNull();
  });

  it("nenhuma tela pública rotaciona conteúdo (RF-03-13)", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    comLeituras({
      guerreiros: [guerreiro("primeira"), guerreiro("segunda", 2)],
      ranking: [noRanking("primeira"), noRanking("segunda", 2)],
      criacoes: [noPortfolio("primeira")],
    });
    const { container } = render(<App />);

    expect(await screen.findAllByText("primeira")).not.toHaveLength(0);
    const antes = container.textContent;
    await act(async () => {
      vi.advanceTimersByTime(20000);
    });

    // Nada troca sozinho: a rotação saiu com a listagem (`RF-03-04`
    // removido), e nenhuma outra seção a reintroduziu.
    expect(container.textContent).toBe(antes);
    expect(screen.queryByRole("button", { name: /próximo card|card anterior/i })).toBeNull();
    vi.useRealTimers();
  });

  it("a consulta por nick exato leva à página individual (RF-03-11, RF-03-12)", async () => {
    comLeituras({ guerreiros: [guerreiro("guerreira-da-consulta")] });
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.type(screen.getByLabelText("Nick exato"), "guerreira-da-consulta");
    await testeDeUsuario.click(screen.getByRole("button", { name: "Procurar" }));

    expect(window.location.pathname).toBe("/guerreiros/guerreira-da-consulta");
    expect(
      await screen.findByRole("heading", { name: "guerreira-da-consulta", level: 2 }),
    ).toBeVisible();
  });

  it("a linha do ranking e o nick do portfólio apontam à página (RF-03-03)", async () => {
    comLeituras({
      guerreiros: [guerreiro("guerreira-da-linha")],
      ranking: [noRanking("guerreira-da-linha")],
      criacoes: [noPortfolio("guerreira-da-linha")],
    });
    render(<App />);

    const portas = await screen.findAllByRole("link", { name: /guerreira-da-linha/ });
    // Duas portas: a linha do ranking e o nick do autor no portfólio. As duas
    // levam ao **mesmo endereço próprio** (`RF-03-03`).
    expect(portas).toHaveLength(2);
    for (const porta of portas) {
      expect(porta).toHaveAttribute("href", "/guerreiros/guerreira-da-linha");
    }
  });

  it("o endereço direto resolve a página (RF-03-03)", async () => {
    comLeituras({ guerreiros: [guerreiro("guerreira-direta")] });
    window.history.pushState(null, "", "/guerreiros/guerreira-direta");
    render(<App />);

    expect(
      await screen.findByRole("heading", { name: "guerreira-direta", level: 2 }),
    ).toBeVisible();
    // A trilha aparece na carta e no portfólio da página — as duas leituras
    // vêm da mesma composição.
    expect(screen.getAllByText(/Trilha da Água/).length).toBeGreaterThan(0);
  });

  it("a página exibe só avatar, nick, badges, poderes e desempenho (RF-03-05, RF-03-06)", async () => {
    comLeituras({ guerreiros: [guerreiro("guerreira-da-pagina")] });
    window.history.pushState(null, "", "/guerreiros/guerreira-da-pagina");
    const { container } = render(<App />);

    expect(
      await screen.findByRole("heading", { name: "guerreira-da-pagina", level: 2 }),
    ).toBeVisible();
    expect(screen.getByText(/1º no ranking · 40 pontos regulares/)).toBeVisible();
    // O poder continua público **como atributo do Guerreiro(a)**, embora a
    // seção de poderes tenha saído da vitrine em 2026-10-11: é aqui que o
    // `RF-03-05` o exige, e não numa seção própria.
    expect(screen.getByText("Poder do Código", { selector: "*" })).toBeTruthy();

    expect(container.textContent).not.toMatch(/nome civil|nascimento|whatsapp|instagram/i);
    expect(container.querySelector('a[href^="mailto:"]')).toBeNull();
    expect(container.querySelector('a[href^="tel:"]')).toBeNull();
  });

  it("carta incompleta não se apresenta (documento 11 §8.2)", async () => {
    const incompleta = {
      avatar: null,
      nick: "guerreira-incompleta",
    } as unknown as GuerreiroPublico;
    comLeituras({ guerreiros: [incompleta] });
    window.history.pushState(null, "", "/guerreiros/guerreira-incompleta");
    render(<App />);

    expect(await screen.findByText(/veio incompleta/i)).toBeVisible();
    expect(document.querySelector(".cg-carta")).toBeNull();
  });
});

describe("o saldo de pontos extras nunca chega à superfície pública", () => {
  // Invariantes 8, 12 e 23: o saldo é de tela logada. A vitrine usa a **mesma**
  // carta da Área do Guerreiro(a), e a garantia é por construção — a projeção
  // pública não traz o campo, e a rota que o serve só atende o próprio
  // Guerreiro(a) em sessão (`RF-03-06`, `RF-01-21`).
  it("o adaptador da carta pública não carrega o campo do saldo", () => {
    const dados = cartaDoGuerreiro(guerreiro("zeferina"));

    expect(dados).not.toHaveProperty("saldoParaTrocar");
    expect("saldoParaTrocar" in dados).toBe(false);
  });

  it("a carta pública se apresenta em três colunas, sem a do saldo", () => {
    const dados = cartaDoGuerreiro(guerreiro("zeferina"));
    // E a falta do saldo não a torna incompleta: a decisão de apresentar carta
    // segue sendo a do documento 11 §8.2, sem o saldo entre o que ela exige.
    expect(cartaEstaCompleta(dados)).toBe(true);

    const { container } = render(<CartaDoPersonagem dados={dados} />);

    expect(container.querySelectorAll(".cg-carta__coluna")).toHaveLength(3);
    expect(container.textContent).not.toContain("Para trocar");
    expect(container.textContent).not.toContain("pontos extras");
  });
});

describe("o acervo na carta e na página do Guerreiro(a)", () => {
  // Fatia 13 do PRD-03 (`RF-03-86`, `RF-03-87`, `RN-03-43`, decisão do
  // fundador, 2026-11-07): a coluna da carta é o resumo do acervo, e o
  // portfólio abaixo dela usa a linha da vitrine, que abre a produção.
  function comprovacao(nick: string, titulo: string, validada_em: string): CriacaoPublica {
    return {
      id: `p-${titulo}`,
      fonte: "comprovacao_do_pratico",
      titulo,
      tipo: "texto",
      trilha_id: "t-2",
      trilha: "Trilha do Território",
      validada_em,
      producao: `Comprovação de ${titulo}.`,
      autores: [{ avatar: "avatar-de-teste", nick }],
    };
  }

  function customizacao(nick: string, descricao: string, validada_em: string): CriacaoPublica {
    return {
      id: `k-${descricao}`,
      fonte: "customizacao_do_kit",
      titulo: descricao,
      tipo: "imagem",
      trilha_id: "t-3",
      trilha: "Trilha dos Robôs",
      validada_em,
      producao: null,
      autores: [{ avatar: "avatar-de-teste", nick }],
    };
  }

  function comAcervo(nick: string, criacoes: CriacaoPublica[]) {
    comLeituras({ guerreiros: [{ ...guerreiro(nick), criacoes }] });
    window.history.pushState(null, "", `/guerreiros/${nick}`);
    return render(<App />);
  }

  function colunaDaCarta() {
    const coluna = document.querySelector(".cg-carta__criacoes");
    return [...(coluna?.querySelectorAll("li") ?? [])].map((item) => item.textContent);
  }

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("só comprovações aprovadas preenchem a coluna, pelo título e pela data (RF-03-86)", async () => {
    const { container } = comAcervo("so-pratico", [
      comprovacao("so-pratico", "Mapa da rua", "2026-10-02T10:00:00Z"),
    ]);

    await screen.findByRole("heading", { name: "so-pratico", level: 2 });
    expect(colunaDaCarta()).toEqual(["Mapa da rua — 02/10/2026"]);
    expect(container.textContent).not.toContain("Nenhuma criação original validada ainda.");
  });

  it("a criação da culminância aparece pelo nome da trilha (RN-03-43)", async () => {
    comAcervo("culminante", [noPortfolio("culminante")]);

    await screen.findByRole("heading", { name: "culminante", level: 2 });
    expect(colunaDaCarta()).toEqual(["Trilha da Água — 01/08/2026"]);
  });

  it("a coluna e o portfólio abrem pelo mais recente (RF-03-86, RF-03-87)", async () => {
    comAcervo("em-ordem", [
      comprovacao("em-ordem", "Mapa da rua", "2026-10-02T10:00:00Z"),
      noPortfolio("em-ordem"),
    ]);

    await screen.findByRole("heading", { name: "em-ordem", level: 2 });
    expect(colunaDaCarta()).toEqual([
      "Mapa da rua — 02/10/2026",
      "Trilha da Água — 01/08/2026",
    ]);
    const portfolio = screen.getByRole("list", { name: "Portfólio de em-ordem" });
    const titulos = [
      ...portfolio.querySelectorAll(".cg-lista-de-registros__identificacao"),
    ].map((celula) => celula.textContent);
    expect(titulos).toEqual(["Mapa da rua", "Trilha da Água"]);
  });

  it("sem acervo público, a coluna diz em uma frase que não há", async () => {
    comAcervo("sem-acervo", []);

    await screen.findByRole("heading", { name: "sem-acervo", level: 2 });
    const carta = document.querySelector(".cg-carta") as HTMLElement;
    expect(within(carta).getByText("Nenhuma criação original validada ainda.")).toBeVisible();
  });

  it("a linha do portfólio da página é a da vitrine e abre a produção (RF-03-87, RF-03-85)", async () => {
    const usuario = userEvent.setup();
    comAcervo("abre-producao", [
      comprovacao("abre-producao", "Mapa da rua", "2026-10-02T10:00:00Z"),
    ]);

    const portfolio = await screen.findByRole("list", { name: "Portfólio de abre-producao" });
    // A trilha sai ao lado da data na comprovação, e a autoria por nick abre
    // a página do autor — a linha do portfólio da vitrine.
    expect(portfolio.textContent).toContain("Trilha do Território");
    expect(portfolio.querySelector('a[href*="abre-producao"]')).not.toBeNull();

    await usuario.click(screen.getByRole("button", { name: "Ler a produção" }));
    expect(await screen.findByText("Comprovação de Mapa da rua.")).toBeVisible();
  });

  it("a customização aprovada aparece na carta pela descrição e pela data (RF-03-86, RF-03-88)", async () => {
    comAcervo("customizou", [
      customizacao("customizou", "Robô com braço de garrafa", "2026-11-12T10:00:00Z"),
    ]);

    await screen.findByRole("heading", { name: "customizou", level: 2 });
    expect(colunaDaCarta()).toEqual(["Robô com braço de garrafa — 12/11/2026"]);
  });

  it("o portfólio da página traz a customização, com a trilha do kit, e abre a mídia (RF-03-87, RF-03-88)", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:producao-do-acervo"),
      revokeObjectURL: vi.fn(),
    });
    const buscar = vi
      .spyOn(leituras, "lerArquivoDoAcervo")
      .mockResolvedValue(new Blob([new Uint8Array([1])], { type: "image/png" }));
    const usuario = userEvent.setup();
    comAcervo("mostra-kit", [
      customizacao("mostra-kit", "Robô com braço de garrafa", "2026-11-12T10:00:00Z"),
    ]);

    const portfolio = await screen.findByRole("list", { name: "Portfólio de mostra-kit" });
    expect(portfolio.textContent).toContain("Robô com braço de garrafa");
    expect(portfolio.textContent).toContain("Trilha dos Robôs");

    await usuario.click(within(portfolio).getByRole("button", { name: "Ver a imagem" }));
    const imagem = await within(portfolio).findByRole("img", {
      name: "Produção de Robô com braço de garrafa",
    });
    expect(imagem).toHaveAttribute("src", "blob:producao-do-acervo");
    expect(buscar).toHaveBeenCalledWith({
      id: "k-Robô com braço de garrafa",
      fonte: "customizacao_do_kit",
    });
    vi.unstubAllGlobals();
  });
});
