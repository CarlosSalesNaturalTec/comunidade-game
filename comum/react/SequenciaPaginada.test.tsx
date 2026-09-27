import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { SequenciaPaginada } from "./SequenciaPaginada";

const TRES = ["Primeiro", "Segundo", "Terceiro"];

describe("SequenciaPaginada", () => {
  it("apresenta um item por vez, diz a posição e avança", async () => {
    const usuario = userEvent.setup();
    render(
      <SequenciaPaginada itens={TRES} nome="Conteúdo" rotuloDeAvancar="Próximo conteúdo">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
    );

    expect(screen.getByText("Primeiro")).toBeInTheDocument();
    expect(screen.queryByText("Segundo")).not.toBeInTheDocument();
    expect(screen.getByText("Conteúdo 1 de 3")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));

    expect(screen.getByText("Segundo")).toBeInTheDocument();
    expect(screen.queryByText("Primeiro")).not.toBeInTheDocument();
    expect(screen.getByText("Conteúdo 2 de 3")).toBeInTheDocument();
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
    expect(screen.getByText("3 de 3")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Avançar" })).not.toBeInTheDocument();
  });

  it("item único não apresenta controle de paginação", () => {
    render(
      <SequenciaPaginada itens={["Sozinho"]} nome="Conteúdo">
        {(texto) => <p>{texto}</p>}
      </SequenciaPaginada>,
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

  it("sequência vazia não apresenta nada", () => {
    const { container } = render(
      <SequenciaPaginada itens={[]}>{(texto: string) => <p>{texto}</p>}</SequenciaPaginada>,
    );

    expect(container).toBeEmptyDOMElement();
  });
});
