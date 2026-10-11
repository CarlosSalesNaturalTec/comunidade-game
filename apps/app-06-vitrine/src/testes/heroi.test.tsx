import { render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it } from "vitest";
import App from "./TelaDaVitrine";

// Os cenários do delta de `aplicacao-da-vitrine`: a abertura ganha herói, com
// a ilustração do elenco em primeiro plano, a frase que diz o que o projeto é
// e a ação que a vitrine já oferece (documento 15 §6; `RF-03-01`, `RF-03-51`,
// `RF-03-58`).
describe("a abertura tem herói", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  function heroi() {
    return screen.getByRole("region", { name: "O que é o Comunidade Game" });
  }

  /** Os nomes de arquivo das figuras, na ordem em que saem no documento. */
  function ordemDasFiguras() {
    return [...heroi().querySelectorAll("img")].map(
      (figura) => figura.getAttribute("src")?.replace(/^\/elenco\/|\.webp$/g, "") ?? "",
    );
  }

  it("o herói vem antes da primeira seção (RF-03-01)", () => {
    const { container } = render(<App />);

    const regiao = heroi();
    const primeiraSecao = screen.getByRole("heading", { name: "Quem somos", level: 2 });
    // `DOCUMENT_POSITION_FOLLOWING`: o título da primeira seção vem **depois**
    // do herói no documento.
    expect(regiao.compareDocumentPosition(primeiraSecao)).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING,
    );
    expect(container.querySelector(".cg-vitrine")?.firstElementChild).toBe(regiao);
  });

  it("traz a frase que diz o que o projeto é (documento 01 §1)", () => {
    render(<App />);

    expect(heroi()).toHaveTextContent(/plataforma educacional gamificada, de código aberto/i);
    expect(heroi()).toHaveTextContent(/comunidades periféricas/i);
  });

  it("traz a ilustração do elenco, com um rótulo só para as quatro (documento 15 §13.6)", () => {
    render(<App />);

    const elenco = within(heroi()).getByRole("img", { name: /elenco do Comunidade Game/i });
    const figuras = elenco.querySelectorAll("img");
    expect(figuras).toHaveLength(4);
    for (const figura of figuras) {
      // `alt` vazio: o rótulo do grupo já diz o que elas são, e quatro nomes
      // soltos seriam ruído em leitor de tela.
      expect(figura).toHaveAttribute("alt", "");
    }
  });

  it("a composição põe o professor ao lado da criatura que ele indica", () => {
    render(<App />);

    // A ordem é decisão do fundador de 2026-10-10 e tem razão: os dois
    // estudantes nas extremidades, e ao centro o professor ao lado do Robô
    // Educa, para onde a mão dele aponta. Separar os dois quebra o gesto.
    expect(ordemDasFiguras()).toEqual(["susy", "robo-educa", "trenell", "otavio"]);

    const ordem = ordemDasFiguras();
    expect(ordem.indexOf("trenell")).toBe(ordem.indexOf("robo-educa") + 1);
    expect([ordem.at(0), ordem.at(-1)].sort()).toEqual(["otavio", "susy"]);
  });

  it("o rótulo único nomeia as quatro na ordem em que elas aparecem", () => {
    render(<App />);

    const rotulo =
      within(heroi())
        .getByRole("img", { name: /elenco do Comunidade Game/i })
        .getAttribute("aria-label") ?? "";

    // Um rótulo só, já conferido acima; aqui o que importa é ele não contar
    // uma ordem diferente da que os olhos veem.
    const NOME: Record<string, string> = {
      susy: "Susy",
      "robo-educa": "Robô Educa",
      trenell: "Carlos Trenell",
      otavio: "Otávio",
    };
    const posicoes = ordemDasFiguras().map((arquivo) => rotulo.indexOf(NOME[arquivo]));

    expect(posicoes).not.toContain(-1);
    expect(posicoes).toEqual([...posicoes].sort((a, b) => a - b));
  });

  it("a ilustração fica fora do caminho crítico e reserva o próprio lugar", () => {
    render(<App />);

    for (const figura of heroi().querySelectorAll("img")) {
      expect(figura).toHaveAttribute("loading", "lazy");
      expect(figura).toHaveAttribute("decoding", "async");
      // Largura e altura declaradas: a tela não pula quando a imagem chega
      // (documento 15 §1, princípio 4).
      expect(Number(figura.getAttribute("width"))).toBeGreaterThan(0);
      expect(Number(figura.getAttribute("height"))).toBeGreaterThan(0);
    }
  });

  it("a frase e a ação continuam de pé sem a ilustração (RF-03-01)", () => {
    render(<App />);

    // Tirar as figuras é o que acontece quando a rede cai ou o aparelho não
    // as busca: o que o herói comunica não pode depender delas.
    for (const figura of heroi().querySelectorAll("picture")) figura.remove();

    expect(heroi()).toHaveTextContent(/plataforma educacional gamificada/i);
    const acao = within(heroi()).getByRole("link", { name: "Quero apoiar" });
    expect(acao).toBeVisible();
    expect(acao).toHaveAttribute("href", "/quero-participar");
  });

  it("não oferece ação que a vitrine não tenha, e o Entrar é um só (RF-03-58)", () => {
    render(<App />);

    // As duas ações do herói levam a portas que o resto da vitrine já oferece:
    // "Quero apoiar" é link, "Entrar" abre a pergunta de persona.
    expect(within(heroi()).getAllByRole("link")).toHaveLength(1);
    expect(within(heroi()).getAllByRole("button", { name: "Entrar" })).toHaveLength(1);
    // Um só na tela: o do herói. O cabeçalho da abertura não traz o seu
    // (decisão do fundador de 2026-10-10).
    expect(screen.getAllByRole("button", { name: "Entrar" })).toHaveLength(1);
  });

  it("apresenta as duas ações como um par de iguais (RF-03-58)", () => {
    render(<App />);

    const participar = within(heroi()).getByRole("link", { name: "Quero apoiar" });
    const entrar = within(heroi()).getByRole("button", { name: "Entrar" });

    // No mesmo par, lado a lado, e com a mesma forma de botão da camada
    // comum: o que distingue as duas é a cor **e** o rótulo, nunca a cor
    // sozinha (documento 15 §5). A asserção é de **conter**, e não de pai
    // direto: no build o Astro embrulha a ilha num `<astro-island>`.
    const acoes = heroi().querySelector(".cg-heroi__acoes");
    expect(acoes).toContainElement(participar);
    expect(acoes).toContainElement(entrar);
    expect(participar).toHaveClass("cg-botao");
    expect(entrar).toHaveClass("cg-botao");
    expect(participar.className).not.toBe(entrar.className);

    // Cada ação é de uma família de cor, e a variante do "Entrar" tem nome de
    // **papel**, não de família: a cor do par já mudou de laranja para verde
    // uma vez (decisão do fundador de 2026-10-11), e um nome de família
    // mentiria na próxima.
    expect(entrar).toHaveClass("cg-botao--entrada");
    expect(entrar).not.toHaveClass("cg-botao--marca");

    // E o rótulo sozinho já distingue as duas: quem não enxerga a cor lê
    // "Entrar" e "Quero apoiar" (documento 15 §5).
    expect(entrar).toHaveAccessibleName("Entrar");
    expect(participar).toHaveAccessibleName("Quero apoiar");
  });

  it("o endereço da porta não mudou com o rótulo (RF-03-42)", () => {
    render(<App />);

    // O rótulo virou "Quero apoiar" em 2026-10-11; o caminho é público e
    // compartilhável, está no sitemap, e por isso **não** acompanhou.
    const acao = within(heroi()).getByRole("link", { name: "Quero apoiar" });
    expect(acao).toHaveAttribute("href", "/quero-participar");
  });

  it("sem a ilustração, as duas ações continuam acionáveis (RF-03-01)", () => {
    render(<App />);

    for (const figura of heroi().querySelectorAll("picture")) figura.remove();

    expect(within(heroi()).getByRole("link", { name: "Quero apoiar" })).toBeVisible();
    expect(within(heroi()).getByRole("button", { name: "Entrar" })).toBeVisible();
  });

  it("não busca recurso de domínio de terceiro (RF-03-51)", () => {
    render(<App />);

    for (const no of heroi().querySelectorAll("img, source")) {
      const endereco = no.getAttribute("src") ?? no.getAttribute("srcset") ?? "";
      expect(endereco).toMatch(/^\/elenco\//);
    }
  });

  it("o herói é da abertura, e não dos outros recortes (RF-03-25)", () => {
    window.history.pushState(null, "", "/pesquisadores");
    render(<App />);

    expect(
      screen.queryByRole("region", { name: "O que é o Comunidade Game" }),
    ).not.toBeInTheDocument();
  });
});
