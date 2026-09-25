import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Icone, type NomeDeGlifo } from "./Icone";

const ARQUIVO = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "Icone.tsx"),
  "utf-8",
);

const GLIFOS: NomeDeGlifo[] = [
  "onboarding",
  "presenca",
  "equipes",
  "quiz",
  "medicao",
  "troca",
];

function desenhar(glifo: NomeDeGlifo): SVGSVGElement {
  const { container } = render(<Icone glifo={glifo} />);
  const svg = container.querySelector("svg");
  expect(svg).not.toBeNull();
  return svg as SVGSVGElement;
}

describe("Icone — nenhum ícone vem de fora (documento 15 §11.1, princípio 6)", () => {
  it("desenha os seis glifos embutidos, sem pedir nada a domínio algum", () => {
    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      // SVG embutido: o desenho está no próprio documento, não numa imagem
      // buscada. Nada de `<img>`, `<use>` nem `url(...)` — nenhum pedido sai.
      expect(svg.querySelector("img, image, use")).toBeNull();
      expect(svg.innerHTML).not.toContain("url(");
      expect(svg.innerHTML).not.toContain("http");
      expect(svg.querySelector("path, circle")).not.toBeNull();
    }
  });

  it("o desenho vive no pacote da aplicação, sem endereço de terceiro no arquivo", () => {
    expect(ARQUIVO).not.toMatch(/https?:\/\/(?!www\.w3\.org)/);
  });
});

describe("Icone — o ícone acompanha o tema (documento 15 §§11.1, 12)", () => {
  it("herda a cor do texto por currentColor, e não preenche", () => {
    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      expect(svg.getAttribute("stroke")).toBe("currentColor");
      expect(svg.getAttribute("fill")).toBe("none");
    }
  });

  it("nenhum arquivo de glifo guarda valor de cor", () => {
    // Nem hexadecimal, nem `rgb()`, nem nome de cor em atributo de traço ou
    // preenchimento: trocar o tema troca o ícone junto.
    expect(ARQUIVO).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    expect(ARQUIVO).not.toMatch(/\brgba?\(/);
    expect(ARQUIVO).not.toMatch(/\bhsla?\(/);

    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      for (const forma of svg.querySelectorAll("*")) {
        expect(forma.getAttribute("fill")).toBeNull();
        expect(forma.getAttribute("stroke")).toBeNull();
      }
    }
  });

  it("desenha na grade de 24 px, com traço de 2 px de ponta e junta arredondadas", () => {
    const svg = desenhar("presenca");
    expect(svg.getAttribute("viewBox")).toBe("0 0 24 24");
    expect(svg.getAttribute("stroke-width")).toBe("2");
    expect(svg.getAttribute("stroke-linecap")).toBe("round");
    expect(svg.getAttribute("stroke-linejoin")).toBe("round");
  });

  it("aceita os quatro tamanhos do documento 15 §11.1, e usa 24 por padrão", () => {
    expect(desenhar("presenca").getAttribute("width")).toBe("24");
    for (const tamanho of [16, 24, 32, 48] as const) {
      const { container } = render(<Icone glifo="presenca" tamanho={tamanho} />);
      const svg = container.querySelector("svg") as SVGSVGElement;
      expect(svg.getAttribute("width")).toBe(String(tamanho));
      expect(svg.getAttribute("height")).toBe(String(tamanho));
    }
  });
});

describe("Icone — o ícone não aparece sozinho (documento 15 §5)", () => {
  it("é decorativo: quem navega por leitor de tela alcança o rótulo, não o desenho", () => {
    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      expect(svg.getAttribute("aria-hidden")).toBe("true");
      // Sem nome acessível próprio: o ícone não concorre com o rótulo.
      expect(svg.querySelector("title")).toBeNull();
      expect(svg.getAttribute("aria-label")).toBeNull();
    }
  });

  it("o elemento acionável que o leva continua identificado pelo rótulo", () => {
    render(
      <button type="button">
        <Icone glifo="presenca" />
        Presença — registrar a presença de hoje
      </button>,
    );
    const botao = screen.getByRole("button", {
      name: "Presença — registrar a presença de hoje",
    });
    // O rótulo é o nome acessível inteiro: o glifo não acrescenta nem
    // substitui palavra alguma.
    expect(botao.querySelector("svg")).not.toBeNull();
  });
});
