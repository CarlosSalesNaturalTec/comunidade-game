import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { createRef } from "react";
import { describe, expect, it } from "vitest";
import { Visor } from "./Visor";

const ESTILOS = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "estilos.css"),
  "utf-8",
);

/** O corpo da regra que abre com o seletor pedido, sem as regras seguintes. */
function corpoDaRegra(seletor: string): string {
  const inicio = ESTILOS.indexOf(`${seletor} {`);
  expect(inicio).toBeGreaterThan(-1);
  const abre = ESTILOS.indexOf("{", inicio);
  return ESTILOS.slice(abre + 1, ESTILOS.indexOf("}", abre));
}

describe("Visor", () => {
  it("empresta um lugar e nunca recebe a imagem", () => {
    // O contrato do `RN-05-53`: a tela empresta um lugar, e é o módulo de
    // biometria que anexa o vídeo lá dentro. Nem `MediaStream`, nem quadro,
    // nem pixel passam pelo componente — ele não tem por onde recebê-los.
    const lugar = createRef<HTMLDivElement>();
    const { container } = render(<Visor lugar={lugar} />);

    expect(lugar.current).toHaveClass("cg-visor-lugar");
    expect(lugar.current?.childElementCount).toBe(0);
    expect(container.querySelector("video")).toBeNull();

    // O módulo de biometria anexa o vídeo por fora, e o visor segue de pé sem
    // ter sabido de nada.
    lugar.current?.replaceChildren(document.createElement("video"));
    expect(lugar.current?.childElementCount).toBe(1);
  });

  it("o visor vazio não ocupa a tela", () => {
    // O lugar fica sempre montado, para existir no DOM antes de o preparo
    // terminar; é o CSS que o esconde enquanto está vazio, e por isso não há
    // corrida entre a renderização e o acoplamento do espelho.
    const lugar = createRef<HTMLDivElement>();
    render(<Visor lugar={lugar} />);

    expect(lugar.current).toBeInTheDocument();
    expect(corpoDaRegra(".cg-visor-lugar:empty")).toContain("display: none");
  });

  it("espelha a imagem na horizontal", () => {
    // Quem se move para a direita se vê ir para a direita, como num espelho
    // de verdade.
    expect(corpoDaRegra(".cg-visor")).toContain("transform: scaleX(-1)");
  });

  it("não deixa o vídeo impor a própria dimensão à tela", () => {
    // O celular modesto do documento 03 §3.2 é o aparelho de referência: um
    // vídeo com a dimensão intrínseca dele empurraria o resto da tela para
    // fora.
    const regra = corpoDaRegra(".cg-visor");
    expect(regra).toContain("width: 100%");
    expect(regra).toContain("max-height");
    expect(regra).toContain("object-fit: cover");
  });

  it("apresenta a frase que quem o usa declarou", () => {
    const lugar = createRef<HTMLDivElement>();
    render(<Visor lugar={lugar} frase="Achei você! Fique assim um pouquinho…" />);

    expect(screen.getByText("Achei você! Fique assim um pouquinho…")).toBeInTheDocument();
  });

  it("duas telas, duas redações para o mesmo estado do laço", () => {
    // A redação é de quem usa o visor, porque o público de cada tela é outro:
    // a tela que um Mestre opera fala com quem opera, e a entrada da App 05
    // fala com uma criança de 6 anos (`RF-05-95`, PRD-05 §10). O mesmo visor
    // serve as duas.
    const daBancada = createRef<HTMLDivElement>();
    const { unmount } = render(
      <Visor lugar={daBancada} frase="Rosto encontrado. Confirmando que há uma pessoa…" />,
    );
    expect(
      screen.getByText("Rosto encontrado. Confirmando que há uma pessoa…"),
    ).toBeInTheDocument();
    unmount();

    const daCrianca = createRef<HTMLDivElement>();
    render(<Visor lugar={daCrianca} frase="Achei você! Fique assim um pouquinho…" />);
    expect(screen.getByText("Achei você! Fique assim um pouquinho…")).toBeInTheDocument();
    expect(screen.queryByText(/Confirmando que há uma pessoa/)).toBeNull();
  });

  it("sem frase, não apresenta parágrafo algum", () => {
    const lugar = createRef<HTMLDivElement>();
    const { container } = render(<Visor lugar={lugar} />);

    expect(container.querySelector(".cg-visor-estado")).toBeNull();
  });
});
