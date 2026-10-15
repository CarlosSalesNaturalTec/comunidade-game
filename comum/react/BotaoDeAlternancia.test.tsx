import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { BotaoDeAlternancia } from "./BotaoDeAlternancia";
import { Cabecalho } from "./Cabecalho";

function renderizar(ligado: boolean, onClick = vi.fn()) {
  render(
    <BotaoDeAlternancia
      rotulo={ligado ? "Desligar o som" : "Ligar o som"}
      ligado={ligado}
      glifoLigado="som"
      glifoDesligado="som-desligado"
      onClick={onClick}
    />,
  );
  return onClick;
}

describe("BotaoDeAlternancia — o rótulo alcança o leitor de tela (documento 15 §5)", () => {
  it("o nome acessível é o rótulo declarado, e não a descrição do desenho", () => {
    renderizar(true);
    const botao = screen.getByRole("button", { name: "Desligar o som" });
    // O glifo está lá e é decorativo: não concorre com o rótulo.
    const svg = botao.querySelector("svg");
    expect(svg).not.toBeNull();
    expect(svg?.getAttribute("aria-hidden")).toBe("true");
    expect(botao.textContent).toBe("");
  });

  it("o rótulo diz o que o toque vai fazer, e muda com o estado", () => {
    const { unmount } = render(
      <BotaoDeAlternancia
        rotulo="Ligar o som"
        ligado={false}
        glifoLigado="som"
        glifoDesligado="som-desligado"
        onClick={vi.fn()}
      />,
    );
    expect(screen.getByRole("button", { name: "Ligar o som" })).toBeInTheDocument();
    unmount();

    renderizar(true);
    expect(screen.getByRole("button", { name: "Desligar o som" })).toBeInTheDocument();
  });
});

describe("BotaoDeAlternancia — o estado não se comunica por cor (documento 15 §5)", () => {
  it("anuncia o estado por aria-pressed", () => {
    const { unmount } = render(
      <BotaoDeAlternancia
        rotulo="Ligar o som"
        ligado={false}
        glifoLigado="som"
        glifoDesligado="som-desligado"
        onClick={vi.fn()}
      />,
    );
    expect(screen.getByRole("button")).toHaveAttribute("aria-pressed", "false");
    unmount();

    renderizar(true);
    expect(screen.getByRole("button")).toHaveAttribute("aria-pressed", "true");
  });

  it("o glifo muda de desenho com o estado, não de cor", () => {
    const { unmount, container } = render(
      <BotaoDeAlternancia
        rotulo="Ligar o som"
        ligado={false}
        glifoLigado="som"
        glifoDesligado="som-desligado"
        onClick={vi.fn()}
      />,
    );
    const desligado = container.querySelector("svg")?.innerHTML;
    unmount();

    const { container: aceso } = render(
      <BotaoDeAlternancia
        rotulo="Desligar o som"
        ligado={true}
        glifoLigado="som"
        glifoDesligado="som-desligado"
        onClick={vi.fn()}
      />,
    );
    const ligado = aceso.querySelector("svg")?.innerHTML;

    expect(desligado).not.toBe(ligado);
    // Nenhum dos dois declara cor: o traço é `currentColor` do `Icone`.
    expect(desligado).not.toContain("#");
    expect(ligado).not.toContain("#");
  });
});

describe("BotaoDeAlternancia — cumpre o alvo de toque e aciona (documento 15 §5)", () => {
  it("leva a classe do botão comum, que é onde o alvo de toque e o foco moram", () => {
    renderizar(false);
    const botao = screen.getByRole("button");
    expect(botao.className).toContain("cg-botao");
    expect(botao.className).toContain("cg-botao--icone");
  });

  it("o toque chama quem o montou, e desabilitado não chama", async () => {
    const usuario = userEvent.setup();
    const aoAcionar = renderizar(false);

    await usuario.click(screen.getByRole("button"));
    expect(aoAcionar).toHaveBeenCalledTimes(1);

    render(
      <BotaoDeAlternancia
        rotulo="Ligar o som"
        ligado={false}
        glifoLigado="som"
        glifoDesligado="som-desligado"
        onClick={aoAcionar}
        desabilitado
      />,
    );
    const todos = screen.getAllByRole("button");
    expect(todos[todos.length - 1]).toBeDisabled();
  });
});

describe("Cabecalho — o canto acolhe o controle que a tela passa", () => {
  it("apresenta o controle do canto ao lado da ação", () => {
    render(
      <Cabecalho
        titulo="Comunidade Game — Aula"
        acao={{ rotulo: "Voltar ao início", aoAcionar: vi.fn() }}
        canto={
          <BotaoDeAlternancia
            rotulo="Ligar o som"
            ligado={false}
            glifoLigado="som"
            glifoDesligado="som-desligado"
            onClick={vi.fn()}
          />
        }
      />,
    );
    expect(screen.getByRole("button", { name: "Ligar o som" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Voltar ao início" })).toBeInTheDocument();
  });

  it("a tela que não passa canto algum fica como estava", () => {
    render(
      <Cabecalho
        titulo="Comunidade Game — Aula"
        acao={{ rotulo: "Voltar ao início", aoAcionar: vi.fn() }}
      />,
    );
    expect(screen.getAllByRole("button")).toHaveLength(1);
  });

  it("o canto sozinho, sem ação, também é apresentado", () => {
    render(
      <Cabecalho
        titulo="Comunidade Game — Aula"
        canto={
          <BotaoDeAlternancia
            rotulo="Ligar o som"
            ligado={false}
            glifoLigado="som"
            glifoDesligado="som-desligado"
            onClick={vi.fn()}
          />
        }
      />,
    );
    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(screen.getByRole("button", { name: "Ligar o som" })).toBeInTheDocument();
  });
});
