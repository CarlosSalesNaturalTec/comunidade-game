import { render, screen } from "@testing-library/react";
import { ErroDaApi } from "comum/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { ApoiadorPublico, MestrePublico } from "../api/leituras";
import * as leituras from "../api/leituras";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12 para Mestres e Apoiadores, agora em
// **lista de registros**: a linha abre a página em endereço próprio, as duas
// seções saem em ordem alfabética, a prova sai como link com rótulo, a vitrine
// não edita, Apoiador sem aporte homologado não aparece, a seção não é pódio —
// sem posição e sem controle de ordenação — e a efetividade sai sem quem
// concluiu (`RF-03-02`, `RF-03-03`, `RF-03-83`, `RN-03-40`).

const MESTRE: MestrePublico = {
  id: "11111111-1111-4111-8111-111111111111",
  avatar: "avatar-do-mestre",
  avatar_padrao: false,
  identificacao: { valor: "mestra_ana", tipo: "nick" },
  areas_de_habilidade: ["Tecnologia"],
  artefatos: [{ endereco: "https://exemplo.org/cv", rotulo: "Currículo" }],
  trilhas_de_autoria: [
    {
      id: "aaaaaaaa-1111-4111-8111-111111111111",
      nome: "Robótica",
      area_do_conhecimento: "Tecnologia",
    },
  ],
  absorcoes: 2,
};

const APOIADOR: ApoiadorPublico = {
  id: "22222222-2222-4222-8222-222222222222",
  avatar: "logo-propria",
  avatar_padrao: false,
  identificacao: { valor: "apoia_norte", tipo: "nick" },
  total_em_moedas: "42.00",
  nivel_de_sustento: 2,
  nome_do_nivel: "Quem faz acontecer",
  selos: [{ familia: "de_aporte", nome: "Primeiro aporte" }],
  desafios_propostos: [
    {
      trilha: "Trilha da Água",
      periodo_inicio: "2026-03-01",
      periodo_fim: "2026-04-30",
      concluiram: 3,
      direcionado: false,
    },
  ],
  artefatos: [{ endereco: "https://exemplo.org/portfolio", rotulo: "Portfólio" }],
};

function comLeituras(mestres: MestrePublico[], apoiadores: ApoiadorPublico[]) {
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarMestres").mockResolvedValue({
    itens: mestres,
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarApoiadores").mockResolvedValue({
    itens: apoiadores,
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "obterMestrePorId").mockImplementation(async (id) => {
    const achado = mestres.find((item) => item.id === id);
    if (!achado)
      throw new ErroDaApi(404, {
        codigo: "nao_encontrado",
        mensagem: "Mestre não encontrado.",
      });
    return achado;
  });
  vi.spyOn(leituras, "obterApoiadorPorId").mockImplementation(async (id) => {
    const achado = apoiadores.find((item) => item.id === id);
    if (!achado)
      throw new ErroDaApi(404, {
        codigo: "nao_encontrado",
        mensagem: "Apoiador não encontrado.",
      });
    return achado;
  });
}

function secaoDe(titulo: string) {
  const cabecalho = screen.getByRole("heading", { name: titulo, level: 2 });
  const secao = cabecalho.closest("section");
  if (!secao) throw new Error(`Seção não encontrada: ${titulo}`);
  return secao;
}

describe("as seções e páginas de Mestres e Apoiadores", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("cada Mestre sai em linha, e a linha abre a página dele (RF-03-02, RF-03-03)", async () => {
    comLeituras([MESTRE], [APOIADOR]);
    render(<App />);

    const porta = await screen.findByRole("link", { name: "mestra_ana" });
    expect(porta).toHaveAttribute("href", `/mestres/${MESTRE.id}`);

    const linha = porta.closest(".cg-lista-de-registros__linha");
    // A linha traz o avatar e as áreas de habilidade; o resto da carta mora
    // na página (documento 11 §8.2).
    expect(linha?.querySelector(".cg-lista-de-registros__avatar")).not.toBeNull();
    expect(linha?.textContent).toContain("Tecnologia");
    // A seção não é tabela: nenhum cabeçalho de coluna, nenhuma grade.
    expect(secaoDe("Mestres").querySelector("table")).toBeNull();
  });

  it("Mestres e Apoiadores saem na ordem alfabética que o núcleo devolveu (RF-03-83)", async () => {
    const mestreA: MestrePublico = {
      ...MESTRE,
      id: "44444444-4444-4444-8444-444444444444",
      identificacao: { valor: "Ávila Nogueira", tipo: "nome" },
    };
    const mestreZ: MestrePublico = {
      ...MESTRE,
      id: "55555555-5555-4555-8555-555555555555",
      identificacao: { valor: "zelia_mestra", tipo: "nick" },
    };
    const apoiadorA: ApoiadorPublico = {
      ...APOIADOR,
      id: "66666666-6666-4666-8666-666666666666",
      identificacao: { valor: "ana_apoia", tipo: "nick" },
      total_em_moedas: "2.00",
    };
    comLeituras([mestreA, MESTRE, mestreZ], [apoiadorA, APOIADOR]);
    render(<App />);

    await screen.findByRole("link", { name: "mestra_ana" });
    const identificacoes = (secao: HTMLElement) =>
      [...secao.querySelectorAll(".cg-lista-de-registros__identificacao")].map(
        (celula) => celula.textContent,
      );

    // A ordem é a do núcleo — a tela a apresenta, não a refaz.
    expect(identificacoes(secaoDe("Mestres"))).toEqual([
      "Ávila Nogueira",
      "mestra_ana",
      "zelia_mestra",
    ]);
    expect(identificacoes(secaoDe("Apoiadores"))).toEqual(["ana_apoia", "apoia_norte"]);
  });

  it("o mesmo endereço, aberto direto, leva à mesma página (RF-03-03)", async () => {
    comLeituras([MESTRE], [APOIADOR]);
    window.history.pushState(null, "", `/mestres/${MESTRE.id}`);
    render(<App />);

    expect(await screen.findByRole("heading", { name: "mestra_ana" })).toBeVisible();
    // A trilha aparece duas vezes por desenho: a carta é o resumo e a página
    // é o detalhe (documento 11 §8.2).
    expect(screen.getAllByText("Robótica").length).toBeGreaterThan(0);
  });

  it("a prova pública sai como link com rótulo, nunca como anexo (RF-03-07)", async () => {
    comLeituras([MESTRE], [APOIADOR]);
    window.history.pushState(null, "", `/mestres/${MESTRE.id}`);
    render(<App />);

    const links = await screen.findAllByRole("link", { name: "Currículo" });
    expect(links[0]).toHaveAttribute("href", "https://exemplo.org/cv");
  });

  it("a vitrine não oferece edição da página do Mestre (PRD-03 §4)", async () => {
    comLeituras([MESTRE], [APOIADOR]);
    window.history.pushState(null, "", `/mestres/${MESTRE.id}`);
    render(<App />);
    await screen.findByRole("heading", { name: "mestra_ana" });

    for (const rotulo of [/editar/i, /acrescentar/i, /remover/i, /salvar/i]) {
      expect(screen.queryByRole("button", { name: rotulo })).toBeNull();
    }
  });

  it("Apoiador sem aporte homologado não aparece, e a página dele é 'não encontrado' (RF-03-57)", async () => {
    comLeituras([MESTRE], []);
    render(<App />);

    expect(
      await screen.findByText("Nenhum Apoiador com aporte homologado por enquanto."),
    ).toBeVisible();

    window.history.pushState(null, "", `/apoiadores/${APOIADOR.id}`);
    render(<App />);
    expect(await screen.findAllByText("Não encontrado.")).not.toHaveLength(0);
  });

  it("a linha do Apoiador leva o total em moedas, sem posição (RF-03-10, RN-03-40)", async () => {
    const modesto = {
      ...APOIADOR,
      id: "33333333-3333-4333-8333-333333333333",
      total_em_moedas: "2.00",
      identificacao: { valor: "apoia_pouco", tipo: "nick" as const },
    };
    comLeituras([MESTRE], [modesto, APOIADOR]);
    render(<App />);

    await screen.findByRole("link", { name: "apoia_pouco" });
    // A asserção é sobre a seção de Apoiadores, não sobre a tela inteira: a
    // de Ranking tem posição por direito próprio.
    const secao = secaoDe("Apoiadores");
    const linhas = [...secao.querySelectorAll(".cg-lista-de-registros__linha")];
    expect(linhas).toHaveLength(2);
    for (const linha of linhas) {
      expect(linha.textContent).toContain("moedas");
      expect(linha.textContent).not.toMatch(/\dº|posição|pódio|R\$/i);
    }
    // Nenhum controle oferece ordenar — nem por valor, nem por nada.
    expect(secao.textContent).not.toMatch(/ordenar|classificar/i);
    for (const botao of secao.querySelectorAll("button")) {
      expect(botao.textContent).toMatch(/^(Próxima página|Página anterior)$/);
    }
  });

  it("a página do Apoiador traz a efetividade sem quem concluiu (RF-03-80)", async () => {
    comLeituras([MESTRE], [APOIADOR]);
    window.history.pushState(null, "", `/apoiadores/${APOIADOR.id}`);
    const { container } = render(<App />);

    await screen.findByRole("heading", { name: "apoia_norte" });
    expect(container.textContent).toContain("Trilha da Água");
    expect(container.textContent).toContain("3 concluíram");
    expect(container.textContent).toContain("42.00 moedas");
    expect(container.textContent).not.toContain("R$");
  });

  it("o Apoiador abaixo do piso aparece com o avatar padrão (RF-03-66)", async () => {
    const abaixoDoPiso: ApoiadorPublico = {
      ...APOIADOR,
      avatar: null,
      avatar_padrao: true,
      total_em_moedas: "5.00",
    };
    comLeituras([MESTRE], [abaixoDoPiso]);
    // O piso se lê na **carta**, e a carta mora na página individual: a linha
    // apresenta o avatar, não o motivo dele.
    window.history.pushState(null, "", `/apoiadores/${APOIADOR.id}`);
    const { container } = render(<App />);

    await screen.findByRole("heading", { name: "apoia_norte" });
    const carta = container.querySelector('[data-variante="apoiador"]');
    expect(carta?.getAttribute("data-avatar-padrao")).toBe("sim");
    expect(screen.getAllByText("5.00 moedas").length).toBeGreaterThan(0);
  });

  it("o adulto sem nick aparece pelo nome, declarado como nome (RF-03-79)", async () => {
    const semNick: MestrePublico = {
      ...MESTRE,
      identificacao: { valor: "Ana Clara Ribeiro", tipo: "nome" },
    };
    comLeituras([semNick], [APOIADOR]);
    render(<App />);

    // Na linha, o nome ocupa a célula que identifica e abre a página.
    expect(await screen.findByRole("link", { name: "Ana Clara Ribeiro" })).toHaveAttribute(
      "href",
      `/mestres/${MESTRE.id}`,
    );

    // O **tipo** da identificação é declarado na carta, na página individual.
    window.history.pushState(null, "", `/mestres/${MESTRE.id}`);
    const { container } = render(<App />);
    await screen.findAllByRole("heading", { name: "Ana Clara Ribeiro" });
    const identificacao = container.querySelector('[data-variante="mestre"] .cg-carta__nick');
    expect(identificacao?.getAttribute("data-tipo")).toBe("nome");
  });
});
