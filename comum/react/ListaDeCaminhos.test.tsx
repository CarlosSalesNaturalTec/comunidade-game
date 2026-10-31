import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { type CaminhoDaTela, ListaDeCaminhos } from "./ListaDeCaminhos";

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

function caminhos(aoAcionar = vi.fn()): CaminhoDaTela[] {
  return [
    {
      chave: "carteira",
      rotulo: "Minha carteira — seus pontos e conquistas",
      glifo: "carteira",
      aoAcionar,
    },
    { chave: "trilha", rotulo: "Trilha — sua próxima missão", glifo: "trilhas", aoAcionar },
  ];
}

describe("ListaDeCaminhos", () => {
  it("dispõe os cartões um por linha, com o glifo ao lado do rótulo", () => {
    const { container } = render(<ListaDeCaminhos caminhos={caminhos()} />);

    expect(container.querySelectorAll(".cg-caminho")).toHaveLength(2);
    // Há **uma** disposição: a lista não tem modificador a escolher, e a
    // folha de estilo empilha os cartões em coluna, com o glifo em linha com
    // o texto (documento 15 §6.5).
    expect(corpoDaRegra(".cg-caminhos")).toContain("flex-direction: column");
    expect(corpoDaRegra(".cg-caminho")).toContain("flex-direction: row");
    for (const cartao of container.querySelectorAll(".cg-caminho")) {
      expect(cartao.firstElementChild).toHaveClass("cg-icone");
    }
  });

  it("não traz disposição em grade nem marca de caminho corrente", () => {
    // As duas saíram com a decisão do fundador de 2026-10-31: a grade existia
    // para a tela que misturava menu e conteúdo, e o caminho corrente só tinha
    // objeto ali. Item corrente de navegação persistente é o `NavegacaoDeAreas`.
    const { container } = render(<ListaDeCaminhos caminhos={caminhos()} />);

    expect(ESTILOS).not.toContain("cg-caminhos--grade");
    expect(ESTILOS).not.toContain(".cg-caminho[aria-current]");
    expect(container.querySelectorAll("[aria-current]")).toHaveLength(0);
  });

  it("o cartão alcança o alvo de toque e a separação do vizinho", () => {
    // O piso da camada comum é `48` px de alvo e `8` px de separação. O cartão
    // fica bem acima dos dois: `6rem` de altura mínima e o intervalo de `16`
    // px da lista.
    expect(corpoDaRegra(".cg-caminho")).toContain("min-height: 6rem");
    expect(corpoDaRegra(".cg-caminhos")).toContain("gap: var(--espaco-16)");
  });

  it("entrega cada caminho como botão cujo nome acessível é o rótulo em frase", async () => {
    const usuario = userEvent.setup();
    const aoAcionar = vi.fn();
    render(<ListaDeCaminhos caminhos={caminhos(aoAcionar)} />);

    // O glifo é decorativo: o nome do botão é a frase, nunca o desenho
    // (documento 15 §5).
    const cartao = screen.getByRole("button", {
      name: "Minha carteira — seus pontos e conquistas",
    });
    await usuario.click(cartao);
    expect(aoAcionar).toHaveBeenCalledOnce();
  });

  it("apresenta o conteúdo extra abaixo do rótulo, sem tirar o rótulo do nome", () => {
    render(
      <ListaDeCaminhos
        caminhos={[
          {
            chave: "trilha",
            rotulo: "Trilha",
            glifo: "trilhas",
            conteudoExtra: "Missão 3 — O rio da minha rua",
            aoAcionar: vi.fn(),
          },
        ]}
      />,
    );

    screen.getByRole("button", { name: "Trilha Missão 3 — O rio da minha rua" });
    expect(screen.getByText("Missão 3 — O rio da minha rua")).toHaveClass("cg-caminho__extra");
  });

  it("desabilita o cartão que o pede, sem removê-lo da tela", () => {
    render(
      <ListaDeCaminhos
        caminhos={[
          {
            chave: "troca",
            rotulo: "Abrindo…",
            glifo: "troca",
            desabilitado: true,
            aoAcionar: vi.fn(),
          },
        ]}
      />,
    );

    expect(screen.getByRole("button", { name: "Abrindo…" })).toBeDisabled();
  });

  it("declara marco de navegação só quando recebe rótulo", () => {
    const { unmount } = render(
      <ListaDeCaminhos rotulo="Caminhos de uma área" caminhos={caminhos()} />,
    );
    screen.getByRole("navigation", { name: "Caminhos de uma área" });
    unmount();

    render(<ListaDeCaminhos caminhos={caminhos()} />);
    expect(screen.queryByRole("navigation")).toBeNull();
  });

  it("acrescenta ao fim o grupo próprio que a tela monta", () => {
    render(
      <ListaDeCaminhos caminhos={caminhos()}>
        <fieldset className="cg-caminhos__operacao">
          <legend>Para quem opera o aparelho</legend>
        </fieldset>
      </ListaDeCaminhos>,
    );

    screen.getByRole("group", { name: "Para quem opera o aparelho" });
  });
});
