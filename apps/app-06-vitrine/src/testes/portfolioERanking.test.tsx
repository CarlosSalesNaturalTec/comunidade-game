import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12: o portfólio e o ranking saem em **lista
// de registros**, o ranking é de ponto regular, o portfólio abre pelo item
// aprovado mais recentemente, cada nick de autor abre a página dele, a
// produção **abre na própria linha**, e, depois de navegar e recarregar, nada
// da visita ficou no aparelho (`RF-03-02`, `RF-03-03`, `RF-03-08`,
// `RF-03-09`, `RF-03-83`, `RF-03-84`, `RF-03-85`).

/** A criação da culminância: o **título é o nome da trilha**, e por isso a
 * linha não a repete (`RN-03-43`). */
const CULMINANCIA: leituras.CriacaoPublica = {
  id: "c-1",
  fonte: "criacao_original",
  titulo: "Trilha da Água",
  tipo: "texto",
  trilha_id: "t-1",
  trilha: "Trilha da Água",
  validada_em: "2026-08-01T10:00:00Z",
  producao: "Produção de teste.",
  autores: [{ avatar: "avatar-de-teste", nick: "autora-da-obra" }],
};

/** A comprovação aprovada do desafio prático: título curto do Mestre, e a
 * trilha ao lado da data (`RF-03-84`). */
const COMPROVACAO: leituras.CriacaoPublica = {
  id: "d-1",
  fonte: "comprovacao_do_pratico",
  titulo: "Horta na laje",
  tipo: "imagem",
  trilha_id: "t-2",
  trilha: "Trilha do Vento",
  validada_em: "2026-03-01T10:00:00Z",
  producao: null,
  autores: [{ avatar: null, nick: "autor-antigo" }],
};

function comConteudo(itens: leituras.CriacaoPublica[] = [CULMINANCIA, COMPROVACAO]) {
  // O núcleo devolve o acervo **do mais recente para o mais antigo**
  // (`RF-03-83`): a tela apresenta essa ordem, não a refaz.
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({
    itens,
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({
    itens: [
      { avatar: null, nick: "primeira-colocada", pontos_regulares: 40, posicao: 1 },
      { avatar: null, nick: "segunda-colocada", pontos_regulares: 20, posicao: 2 },
    ],
    proximo_cursor: null,
  });
}

/** jsdom não implementa a URL de objeto, e a produção em mídia nasce dela.
 * Fica **dentro** do teste que precisa, nunca no `beforeEach`: trocar o `URL`
 * global por objeto simples derruba quem usa `new URL()` — `document.cookie`,
 * entre outros (mesmo padrão da App 09). */
function comUrlDeObjeto() {
  vi.stubGlobal("URL", {
    ...URL,
    createObjectURL: vi.fn(() => "blob:producao-do-acervo"),
    revokeObjectURL: vi.fn(),
  });
}

function secaoDe(titulo: string) {
  const cabecalho = screen.getByRole("heading", { name: titulo, level: 2 });
  const secao = cabecalho.closest("section");
  if (!secao) throw new Error(`Seção não encontrada: ${titulo}`);
  return within(secao);
}

describe("portfólio e ranking", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    comConteudo();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
    window.localStorage.clear();
    window.sessionStorage.clear();
  });

  it("a linha sai com título, data e autoria por nick (RF-03-08)", async () => {
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    expect(await portfolio.findByText("Trilha da Água")).toBeVisible();
    expect(portfolio.getByText(/01\/08\/2026/)).toBeVisible();
    expect(portfolio.getByText(/autora-da-obra/)).toBeVisible();
  });

  it("a comprovação aprovada traz o título curto e a trilha (RF-03-84)", async () => {
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    expect(await portfolio.findByText("Horta na laje")).toBeVisible();
    const linha = portfolio.getByText("Horta na laje").closest("li") as HTMLElement;
    expect(linha.textContent).toMatch(/Trilha do Vento/);
    expect(linha.textContent).toMatch(/01\/03\/2026/);
  });

  it("a criação da culminância não repete a trilha (RN-03-43)", async () => {
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Trilha da Água");
    const linha = portfolio.getByText("Trilha da Água").closest("li") as HTMLElement;
    // O título já **é** o nome da trilha: ele aparece uma vez, e não duas.
    expect(linha.textContent?.match(/Trilha da Água/g)).toHaveLength(1);
  });

  it("o portfólio abre pelo item aprovado mais recentemente (RF-03-83)", async () => {
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Trilha da Água");
    const trilhas = portfolio
      .getAllByRole("listitem")
      .map(
        (linha) => linha.querySelector(".cg-lista-de-registros__identificacao")?.textContent,
      );
    expect(trilhas).toEqual(["Trilha da Água", "Horta na laje"]);
  });

  it("no portfólio é o nick do autor que abre a página dele (RF-03-03)", async () => {
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    const porta = await portfolio.findByRole("link", { name: /autora-da-obra/ });
    expect(porta).toHaveAttribute("href", "/guerreiros/autora-da-obra");
    // A criação original não tem página individual: a linha dela não é
    // acionável, só os nicks são. A produção abre **na própria linha**, por
    // botão, nunca por endereço (`RF-03-85`).
    const linha = porta.closest("li") as HTMLElement;
    expect(linha.querySelectorAll("a")).toHaveLength(1);
  });

  it("o ranking é de ponto regular, em linha, em ordem (RF-03-09)", async () => {
    render(<App />);

    const ranking = secaoDe("Ranking");
    expect(await ranking.findByText(/primeira-colocada/)).toBeVisible();
    const posicoes = ranking.getAllByRole("listitem").map((item) => item.textContent);
    expect(posicoes[0]).toMatch(/primeira-colocada.*1º.*40 pontos regulares/);
    expect(posicoes[1]).toMatch(/segunda-colocada.*2º.*20 pontos regulares/);
    expect(ranking.queryByText(/ponto extra|moeda|R\$/i)).toBeNull();
    // A linha abre a página individual daquele Guerreiro(a) (`RF-03-03`).
    expect(ranking.getByRole("link", { name: "primeira-colocada" })).toHaveAttribute(
      "href",
      "/guerreiros/primeira-colocada",
    );
  });

  it("a abertura não traz seção de poderes (RF-03-02)", async () => {
    render(<App />);

    // A seção saiu em 2026-10-11: ela prometia uma página individual de poder
    // que nunca existiu. O poder segue público como atributo do Guerreiro(a).
    expect(await screen.findByRole("heading", { name: "Ranking", level: 2 })).toBeVisible();
    expect(screen.queryByRole("heading", { name: "Poderes", level: 2 })).toBeNull();
    expect(screen.queryByText(/Mestres responsáveis/)).toBeNull();
  });

  it("a abertura abre pelo que o projeto produziu, e fecha no institucional", async () => {
    render(<App />);

    await screen.findByText(/primeira-colocada/);

    // A ordem é decisão do fundador de 2026-10-11, e mora na página do
    // recorte — nenhum `RF` a fixa. "Como apoiar" não tem tela pública.
    const titulos = screen
      .getAllByRole("heading", { level: 2 })
      .map((cabecalho) => cabecalho.textContent);
    expect(titulos).toEqual([
      "Ranking",
      "Portfólio de criações originais",
      "Guerreiros e Guerreiras",
      "Apoiadores",
      "Mestres",
      "Comunidades Virtuais",
      "Construir sobre a API",
      "Quem somos",
      "Contatos",
    ]);
  });

  it("o texto abre na própria linha, e o fechar recolhe (RF-03-85)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Trilha da Água");

    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Ler a produção" }));
    expect(portfolio.getByText("Produção de teste.")).toBeVisible();

    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Fechar a produção" }));
    expect(portfolio.queryByText("Produção de teste.")).toBeNull();
    expect(portfolio.getByRole("button", { name: "Ler a produção" })).toBeVisible();
  });

  it("a imagem abre na linha, pelos bytes do núcleo (RF-03-85)", async () => {
    comUrlDeObjeto();
    const buscar = vi
      .spyOn(leituras, "lerArquivoDoAcervo")
      .mockResolvedValue(new Blob([new Uint8Array([1, 2, 3])], { type: "image/png" }));
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Horta na laje");
    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Ver a imagem" }));

    const imagem = await portfolio.findByRole("img", { name: "Produção de Horta na laje" });
    expect(imagem).toHaveAttribute("src", "blob:producao-do-acervo");
    // A chave da aplicação vai em cabeçalho: nenhuma rota sob `/v1` aceita
    // `<img src>` direto, e por isso a busca é em bytes.
    expect(buscar).toHaveBeenCalledWith({ id: "d-1", fonte: "comprovacao_do_pratico" });
  });

  it("o áudio e o vídeo abrem com controles, sem tocar sozinhos (RF-03-85)", async () => {
    comUrlDeObjeto();
    vi.spyOn(leituras, "lerArquivoDoAcervo").mockResolvedValue(
      new Blob([new Uint8Array([1])]),
    );
    comConteudo([
      { ...COMPROVACAO, id: "d-2", titulo: "Fala da horta", tipo: "audio" },
      { ...COMPROVACAO, id: "d-3", titulo: "Horta em movimento", tipo: "video" },
    ]);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Fala da horta");
    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Ouvir o áudio" }));
    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Ver o vídeo" }));

    const linhas = portfolio.getAllByRole("listitem");
    const audio = linhas[0].querySelector("audio") as HTMLAudioElement;
    const video = linhas[1].querySelector("video") as HTMLVideoElement;
    expect(audio).toHaveAttribute("controls");
    expect(video).toHaveAttribute("controls");
    expect(audio.autoplay).toBe(false);
    expect(video.autoplay).toBe(false);
  });

  it("o link externo sai como link de saída, sem embutir terceiro (RF-03-85)", async () => {
    comConteudo([
      {
        ...COMPROVACAO,
        titulo: "Mapa da horta",
        tipo: "link_externo",
        producao: "https://exemplo.org/mapa",
      },
    ]);
    render(<App />);

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Mapa da horta");
    const saida = portfolio.getByRole("link", { name: "Abrir a produção em outro site" });
    expect(saida).toHaveAttribute("href", "https://exemplo.org/mapa");
    expect(portfolio.queryByTitle(/iframe|embed/i)).toBeNull();
  });

  it("o arquivo sai como transferência, sem tentar exibi-lo (RF-03-85)", async () => {
    comUrlDeObjeto();
    vi.spyOn(leituras, "lerArquivoDoAcervo").mockResolvedValue(
      new Blob([new Uint8Array([1])]),
    );
    comConteudo([{ ...COMPROVACAO, titulo: "Caderno da horta", tipo: "arquivo" }]);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Caderno da horta");
    await testeDeUsuario.click(
      portfolio.getByRole("button", { name: "Preparar a produção para salvar" }),
    );

    const salvar = await portfolio.findByRole("link", { name: "Salvar a produção" });
    expect(salvar).toHaveAttribute("download", "Caderno da horta");
    expect(portfolio.queryByRole("img")).toBeNull();
  });

  it("a produção que o núcleo não serve é dita em linguagem simples (RN-03-02)", async () => {
    vi.spyOn(leituras, "lerArquivoDoAcervo").mockRejectedValue(new Error("404"));
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Horta na laje");
    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Ver a imagem" }));

    expect(await portfolio.findByText("A produção não está disponível agora.")).toBeVisible();
    // A linha segue de pé, com título, data, trilha e autoria.
    const linha = portfolio.getByText("Horta na laje").closest("li") as HTMLElement;
    expect(linha.textContent).toMatch(/Trilha do Vento/);
    expect(linha.textContent).toMatch(/autor-antigo/);
    // Nunca o motivo da recusa: nem a autorização, nem o veredito do Mestre.
    expect(linha.textContent).not.toMatch(/autoriza|publicáv|revogad/i);
  });

  it("o que foi aberto não é gravado no aparelho (RN-03-22)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    const portfolio = secaoDe("Portfólio de criações originais");
    await portfolio.findByText("Trilha da Água");
    await testeDeUsuario.click(portfolio.getByRole("button", { name: "Ler a produção" }));
    expect(portfolio.getByText("Produção de teste.")).toBeVisible();

    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");

    // Recarregar devolve todas as linhas recolhidas: o aberto é estado em
    // memória, e não sobrevive à recarga.
    cleanup();
    render(<App />);
    const depois = secaoDe("Portfólio de criações originais");
    expect(await depois.findByRole("button", { name: "Ler a produção" })).toBeVisible();
    expect(depois.queryByText("Produção de teste.")).toBeNull();
  });

  it("nada da visita fica no aparelho (RF-03-14, RN-03-22)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    expect(await screen.findByText(/primeira-colocada/)).toBeVisible();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Início" }));

    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });
});
