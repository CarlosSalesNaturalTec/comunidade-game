import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MarcaDoProjeto } from "./MarcaDoProjeto";

// Os cenários do delta de `camada-visual-comum` desta change: o cabeçalho
// apresenta o símbolo servido pelo próprio domínio, o nome sobrevive à
// ausência da imagem, o nome não aparece em dobro e o escuro recebe a
// monocromática.

const PASTA_DA_MARCA = join(dirname(fileURLToPath(import.meta.url)), "..", "marca");
const ESTILOS = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "estilos.css"),
  "utf-8",
);

describe("MarcaDoProjeto — o símbolo e o nome no topo da aplicação", () => {
  it("apresenta o símbolo embutido no documento, e não buscado de fora", () => {
    const { container } = render(<MarcaDoProjeto />);

    const simbolos = container.querySelectorAll(".cg-marca__simbolo svg");
    expect(simbolos).toHaveLength(2);
    // Embutido: nenhum `<img>` e nenhum endereço de terceiro.
    expect(container.querySelector("img")).toBeNull();
    expect(container.innerHTML).not.toMatch(/https?:\/\/(?!www\.w3\.org)/);
  });

  it("o nome é texto, e continua legível quando o símbolo não aparece", () => {
    render(<MarcaDoProjeto />);

    const nome = screen.getByText("Comunidade Game");
    expect(nome).toBeInTheDocument();
    // O símbolo é decorativo: quem lê por voz ouve o nome, nunca o desenho.
    expect(nome.closest(".cg-marca__simbolo")).toBeNull();
  });

  it("o nome não aparece em dobro: o símbolo não carrega o nome em curvas", () => {
    render(<MarcaDoProjeto />);

    expect(screen.getAllByText("Comunidade Game")).toHaveLength(1);
    // A peça apresentada é o símbolo — a marca horizontal traria o nome de novo.
    const simbolo = readFileSync(join(PASTA_DA_MARCA, "simbolo.svg"), "utf-8");
    const horizontal = readFileSync(join(PASTA_DA_MARCA, "marca-horizontal.svg"), "utf-8");
    expect(simbolo.length).toBeLessThan(horizontal.length / 2);
  });

  it("os dois símbolos ficam fora da leitura por voz", () => {
    const { container } = render(<MarcaDoProjeto />);

    for (const peca of container.querySelectorAll(".cg-marca__simbolo")) {
      expect(peca.getAttribute("aria-hidden")).toBe("true");
    }
  });

  it("o escuro e a foto recebem a monocromática, e o claro a colorida", () => {
    const { container } = render(<MarcaDoProjeto />);

    expect(container.querySelector(".cg-marca__simbolo--colorida")).not.toBeNull();
    expect(container.querySelector(".cg-marca__simbolo--mono")).not.toBeNull();

    // A troca é do CSS, nunca da aplicação: nenhuma pode esquecer de trocar.
    expect(ESTILOS).toMatch(
      /@media \(prefers-color-scheme: dark\) \{\s*\.cg-marca__simbolo--colorida \{\s*display: none;/,
    );
    expect(ESTILOS).toContain(".cg-fundo-de-comunidade .cg-marca__simbolo--colorida");
  });

  it("a monocromática herda a cor do texto, e a colorida traz a paleta", () => {
    const mono = readFileSync(join(PASTA_DA_MARCA, "simbolo-mono.svg"), "utf-8");
    const colorida = readFileSync(join(PASTA_DA_MARCA, "simbolo.svg"), "utf-8");

    expect(mono).toContain("currentColor");
    expect(mono).not.toMatch(/#[0-9a-fA-F]{6}/);
    expect(colorida).toContain("#F25C05");
  });

  it("leva à abertura quando recebe destino, e é só apresentação quando não", () => {
    const { container, rerender } = render(<MarcaDoProjeto />);
    expect(container.querySelector("a")).toBeNull();

    rerender(<MarcaDoProjeto href="/" />);
    expect(container.querySelector("a")?.getAttribute("href")).toBe("/");
  });
});
