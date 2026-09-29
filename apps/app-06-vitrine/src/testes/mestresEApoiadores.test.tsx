import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { ApoiadorPublico, MestrePublico } from "../api/leituras";
import * as leituras from "../api/leituras";

// Critérios de aceite do PRD-03 §12 para a fatia 7: card abre a página em
// endereço próprio, a prova sai como link com rótulo, a vitrine não edita,
// Apoiador sem aporte homologado não aparece, a seção não é pódio e a
// efetividade sai sem quem concluiu.

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
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);
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

describe("as seções e páginas de Mestres e Apoiadores", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("o card do Mestre abre a página em endereço próprio (RF-03-03)", async () => {
    comLeituras([MESTRE], [APOIADOR]);
    render(<App />);

    await userEvent.click(
      await screen.findByRole("button", { name: /Abrir a página de mestra_ana/ }),
    );

    expect(window.location.pathname).toBe(`/mestres/${MESTRE.id}`);
    expect(await screen.findByRole("heading", { name: "mestra_ana" })).toBeVisible();
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

  it("a seção de Apoiadores não é pódio: sem posição e sem ordem por valor (RN-14-38)", async () => {
    const modesto = {
      ...APOIADOR,
      id: "33333333-3333-4333-8333-333333333333",
      total_em_moedas: "2.00",
      identificacao: { valor: "apoia_pouco", tipo: "nick" as const },
    };
    comLeituras([MESTRE], [modesto, APOIADOR]);
    const { container } = render(<App />);

    await screen.findByText("apoia_pouco");
    // A asserção é sobre os cards de Apoiador, não sobre a página inteira:
    // a seção de Ranking tem a palavra "posição" por direito próprio.
    const cartas = Array.from(container.querySelectorAll('[data-variante="apoiador"]'));
    expect(cartas).toHaveLength(2);
    for (const carta of cartas) {
      expect(carta.textContent).not.toMatch(/\dº|posição|pódio/i);
    }
    // A ordem apresentada é a que o núcleo devolveu, não a do valor.
    const nicks = cartas.map((carta) => carta.querySelector(".cg-carta__nick")?.textContent);
    expect(nicks).toEqual(["apoia_pouco", "apoia_norte"]);
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
    const { container } = render(<App />);

    await screen.findByText("apoia_norte");
    const carta = container.querySelector('[data-variante="apoiador"]');
    expect(carta?.getAttribute("data-avatar-padrao")).toBe("sim");
    expect(screen.getByText("5.00 moedas")).toBeVisible();
  });

  it("o adulto sem nick aparece pelo nome, declarado como nome (RF-03-79)", async () => {
    const semNick: MestrePublico = {
      ...MESTRE,
      identificacao: { valor: "Ana Clara Ribeiro", tipo: "nome" },
    };
    comLeituras([semNick], [APOIADOR]);
    const { container } = render(<App />);

    await screen.findByText("Ana Clara Ribeiro");
    const identificacao = container.querySelector('[data-variante="mestre"] .cg-carta__nick');
    expect(identificacao?.getAttribute("data-tipo")).toBe("nome");
  });
});
