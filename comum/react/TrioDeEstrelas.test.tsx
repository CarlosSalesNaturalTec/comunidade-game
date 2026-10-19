import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TrioDeEstrelas } from "./TrioDeEstrelas";

const PASTA = dirname(fileURLToPath(import.meta.url));
const COMPONENTE = readFileSync(join(PASTA, "TrioDeEstrelas.tsx"), "utf-8");
const ESTILOS = readFileSync(join(PASTA, "estilos.css"), "utf-8");

describe("TrioDeEstrelas", () => {
  it("apresenta três estrelas, que é o que o diferencia do ponto", () => {
    // `RF-05-45`: ponto regular é **uma** estrela (documento 15 §9), e a
    // recompensa de marco são três — é a contagem que separa as duas.
    const { container } = render(<TrioDeEstrelas />);

    expect(container.querySelectorAll("svg")).toHaveLength(3);
    expect(container.querySelectorAll("path")).toHaveLength(3);
  });

  it("tira a cor dos tokens da família ponto, e não do arquivo", () => {
    // A peça é preenchida — exceção do documento 15 §11.1 —, mas a exceção é
    // ao traço, nunca à regra de que o tema troca o ícone junto.
    expect(ESTILOS).toContain("fill: var(--cor-ponto)");
    expect(ESTILOS).toContain("stroke: var(--cor-ponto-contorno)");
  });

  it("não guarda valor de cor algum no componente", () => {
    // Nem hexadecimal, nem `rgb(`, nem a palavra `black` que o pedido
    // original trazia: contorno preto literal não acompanharia o tema escuro.
    expect(COMPONENTE).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    expect(COMPONENTE).not.toMatch(/\brgb\(/);
    expect(COMPONENTE).not.toMatch(/\b(black|yellow|gold)\b/i);
  });

  it("fica escondido de leitor de tela, porque o texto é a via primeira", () => {
    // Documento 15 §5: quem navega por voz alcança o texto da recompensa, e
    // nunca a contagem nem a descrição das estrelas.
    const { container } = render(<TrioDeEstrelas />);
    const trio = container.querySelector(".cg-trio-de-estrelas");

    expect(trio).not.toBeNull();
    expect(trio?.getAttribute("aria-hidden")).toBe("true");
  });

  it("desenha na grade de 24 px do sistema de ícone", () => {
    const { container } = render(<TrioDeEstrelas />);

    for (const svg of container.querySelectorAll("svg")) {
      expect(svg.getAttribute("viewBox")).toBe("0 0 24 24");
      expect(svg.getAttribute("focusable")).toBe("false");
    }
  });
});
