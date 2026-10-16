import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { SequenciaPaginada } from "./SequenciaPaginada";

const TRES = ["Primeiro", "Segundo", "Terceiro"];

describe("SequenciaPaginada", () => {
  it("apresenta um item por vez e avança, sem declarar a posição", async () => {
    const usuario = userEvent.setup();
    render(
      <SequenciaPaginada itens={TRES} rotuloDeAvancar="Próximo conteúdo">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    expect(screen.getByText("Primeiro")).toBeInTheDocument();
    expect(screen.queryByText("Segundo")).not.toBeInTheDocument();
    // A contagem saiu de vez, da tela e de quem usa leitor de tela
    // (decisão do fundador de 2026-10-16).
    expect(screen.queryByText(/de 3/)).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));

    expect(screen.getByText("Segundo")).toBeInTheDocument();
    expect(screen.queryByText("Primeiro")).not.toBeInTheDocument();
    expect(screen.queryByText(/de 3/)).not.toBeInTheDocument();
  });

  it("no último item não oferece avançar para lugar nenhum", async () => {
    const usuario = userEvent.setup();
    render(
      <SequenciaPaginada itens={TRES} rotuloDeAvancar="Avançar">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    await usuario.click(screen.getByRole("button", { name: "Avançar" }));
    await usuario.click(screen.getByRole("button", { name: "Avançar" }));

    expect(screen.getByText("Terceiro")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Avançar" })).not.toBeInTheDocument();
  });

  it("item único não apresenta controle de paginação", () => {
    render(
      <SequenciaPaginada itens={["Sozinho"]}>{(texto) => <p>{texto}</p>}</SequenciaPaginada>,
    );

    expect(screen.getByText("Sozinho")).toBeInTheDocument();
    expect(screen.queryByText(/de 1/)).not.toBeInTheDocument();
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });

  it("o retorno ao anterior só existe para quem o ligou", async () => {
    const usuario = userEvent.setup();
    const { rerender } = render(
      <SequenciaPaginada itens={TRES} rotuloDeAvancar="Avançar">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    await usuario.click(screen.getByRole("button", { name: "Avançar" }));
    expect(screen.queryByRole("button", { name: /voltar/i })).not.toBeInTheDocument();

    rerender(
      <SequenciaPaginada itens={TRES} rotuloDeAvancar="Avançar" rotuloDeVoltar="Voltar">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    await usuario.click(screen.getByRole("button", { name: "Voltar" }));
    expect(screen.getByText("Primeiro")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Voltar" })).not.toBeInTheDocument();
  });

  it("comandada de fora, quem monta manda na posição", async () => {
    const usuario = userEvent.setup();
    const irPara = vi.fn();
    render(
      <SequenciaPaginada itens={TRES} indice={2} aoIrPara={irPara} rotuloDeVoltar="Voltar">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    expect(screen.getByText("Terceiro")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Voltar" }));

    expect(irPara).toHaveBeenCalledWith(1);
    // Comandada de fora, a posição não muda sozinha: quem monta decide.
    expect(screen.getByText("Terceiro")).toBeInTheDocument();
  });

  // O encaixe de ações: o envio do quiz pertence ao conjunto, não à pergunta
  // da vez, e por isso acompanha avançar e voltar (design — decisão 4).
  it("as ações acompanham avançar e voltar na mesma linha", () => {
    const { container } = render(
      <SequenciaPaginada
        itens={TRES}
        rotuloDeAvancar="Avançar"
        acoes={<button type="button">Enviar respostas</button>}
      >
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    const controles = container.querySelector(".cg-sequencia__controles");
    expect(controles).toContainElement(
      screen.getByRole("button", { name: "Enviar respostas" }),
    );
    expect(controles).toContainElement(screen.getByRole("button", { name: "Avançar" }));
  });

  // Sem esta guarda o quiz de uma pergunta perderia o botão de enviar: a
  // linha de controles inteira não renderizava com um item só.
  it("item único não pagina, mas apresenta as ações", () => {
    render(
      <SequenciaPaginada
        itens={["Sozinho"]}
        acoes={<button type="button">Enviar respostas</button>}
      >
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    expect(screen.getByRole("button", { name: "Enviar respostas" })).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /avançar/i })).not.toBeInTheDocument();
  });

  it("travada, avançar e voltar não respondem — as ações seguem livres", async () => {
    const usuario = userEvent.setup();
    const acionar = vi.fn();
    render(
      <SequenciaPaginada
        itens={TRES}
        indice={1}
        rotuloDeAvancar="Avançar"
        rotuloDeVoltar="Voltar"
        controlesTravados
        acoes={
          <button type="button" onClick={acionar}>
            Enviar respostas
          </button>
        }
      >
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    expect(screen.getByRole("button", { name: "Avançar" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Voltar" })).toBeDisabled();

    await usuario.click(screen.getByRole("button", { name: "Enviar respostas" }));
    expect(acionar).toHaveBeenCalledTimes(1);
  });

  it("sequência vazia não apresenta nada", () => {
    const { container } = render(
      <SequenciaPaginada itens={[]}>{(texto: string) => <p>{texto}</p>}</SequenciaPaginada>,
    );

    expect(container).toBeEmptyDOMElement();
  });
});
