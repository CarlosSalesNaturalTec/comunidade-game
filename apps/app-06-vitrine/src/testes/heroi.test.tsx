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
    const acao = within(heroi()).getByRole("link", { name: "Quero participar" });
    expect(acao).toBeVisible();
    expect(acao).toHaveAttribute("href", "/quero-participar");
  });

  it("não oferece ação que a vitrine não tenha, e não repete o Entrar (RF-03-58)", () => {
    render(<App />);

    // A única ação do herói é "Quero participar", que leva à mesma porta que o
    // resto da vitrine já oferece.
    expect(within(heroi()).getAllByRole("link")).toHaveLength(1);
    expect(within(heroi()).queryAllByRole("button")).toHaveLength(0);
    // O "Entrar" continua sendo um só, o do cabeçalho (decisão do fundador de
    // 2026-10-09).
    expect(screen.getAllByRole("button", { name: "Entrar" })).toHaveLength(1);
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
