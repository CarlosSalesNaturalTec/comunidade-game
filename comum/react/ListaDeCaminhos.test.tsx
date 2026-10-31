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
  it("na grade, dispõe os cartões em duas colunas e põe o glifo acima do rótulo", () => {
    const { container } = render(<ListaDeCaminhos caminhos={caminhos()} disposicao="grade" />);

    const lista = container.querySelector(".cg-caminhos");
    expect(lista).toHaveClass("cg-caminhos--grade");
    // O lugar do glifo decorre da disposição: a folha de estilo vira o cartão
    // em coluna só dentro de `--grade`, e é a presença do modificador que o
    // teste pode afirmar sem depender de CSS computado.
    expect(container.querySelectorAll(".cg-caminhos--grade .cg-caminho")).toHaveLength(2);
    for (const cartao of container.querySelectorAll(".cg-caminho")) {
      expect(cartao.firstElementChild).toHaveClass("cg-icone");
    }
  });

  it("o cartão alcança o alvo de toque e a separação do vizinho", () => {
    // O piso da camada comum é `48` px de alvo e `8` px de separação. O cartão
    // fica bem acima dos dois: `6rem` de altura mínima e o intervalo de `16`
    // px da lista, nas duas disposições.
    expect(corpoDaRegra(".cg-caminho")).toContain("min-height: 6rem");
    expect(corpoDaRegra(".cg-caminhos")).toContain("gap: var(--espaco-16)");
  });

  it("a grade dobra em quatro colunas a partir do marco de 768 px", () => {
    // O marco não entra em `@media`, que não lê `var()`: a literal é o que o
    // repositório já faz, no idioma da carta em colunas.
    expect(corpoDaRegra(".cg-caminhos--grade")).toContain(
      "grid-template-columns: repeat(2, minmax(0, 1fr))",
    );
    const marco = ESTILOS.indexOf(
      "@media (min-width: 768px)",
      ESTILOS.indexOf(".cg-caminhos--grade"),
    );
    expect(marco).toBeGreaterThan(-1);
    expect(ESTILOS.slice(marco, marco + 300)).toContain("grid-auto-flow: column");
  });

  it("na coluna, mantém o glifo ao lado do rótulo e não aplica a grade", () => {
    const { container } = render(<ListaDeCaminhos caminhos={caminhos()} />);

    expect(container.querySelector(".cg-caminhos")).not.toHaveClass("cg-caminhos--grade");
    expect(container.querySelectorAll(".cg-caminho")).toHaveLength(2);
  });

  it("entrega cada caminho como botão cujo nome acessível é o rótulo em frase", async () => {
    const usuario = userEvent.setup();
    const aoAcionar = vi.fn();
    render(<ListaDeCaminhos caminhos={caminhos(aoAcionar)} disposicao="grade" />);

    // O glifo é decorativo: o nome do botão é a frase, nunca o desenho
    // (documento 15 §5).
    const cartao = screen.getByRole("button", {
      name: "Minha carteira — seus pontos e conquistas",
    });
    await usuario.click(cartao);
    expect(aoAcionar).toHaveBeenCalledOnce();
  });

  it("anuncia o caminho corrente como o atual e o distingue por peso de fonte", () => {
    const { container } = render(
      <ListaDeCaminhos caminhos={caminhos()} disposicao="grade" caminhoAtual="trilha" />,
    );

    screen.getByRole("button", { name: "Trilha — sua próxima missão", current: true });
    expect(
      screen.getByRole("button", { name: "Minha carteira — seus pontos e conquistas" }),
    ).not.toHaveAttribute("aria-current");
    // O sinal além da cor mora na folha de estilo, atrelado ao próprio
    // `aria-current` — não há segunda classe a manter em sincronia.
    expect(container.querySelectorAll(".cg-caminho[aria-current]")).toHaveLength(1);
  });

  it("sem caminho corrente declarado, nenhum cartão é o atual", () => {
    const { container } = render(<ListaDeCaminhos caminhos={caminhos()} />);

    expect(container.querySelectorAll(".cg-caminho[aria-current]")).toHaveLength(0);
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
        disposicao="grade"
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
      <ListaDeCaminhos
        rotulo="Área do Guerreiro(a)"
        caminhos={caminhos()}
        disposicao="grade"
      />,
    );
    screen.getByRole("navigation", { name: "Área do Guerreiro(a)" });
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
