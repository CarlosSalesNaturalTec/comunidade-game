import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MarcaDeGravacao } from "./MarcaDeGravacao";

describe("MarcaDeGravacao", () => {
  it("instante nulo não apresenta marca", () => {
    const { container } = render(<MarcaDeGravacao instante={null} />);
    expect(container).toBeEmptyDOMElement();
  });

  it("instante presente apresenta o momento em texto", () => {
    render(<MarcaDeGravacao instante={new Date(2026, 8, 7, 14, 32)} />);
    expect(screen.getByText("Salvo às 14h32")).toBeInTheDocument();
  });

  it("instante novo substitui o anterior", () => {
    const { rerender } = render(<MarcaDeGravacao instante={new Date(2026, 8, 7, 14, 32)} />);
    expect(screen.getByText("Salvo às 14h32")).toBeInTheDocument();

    rerender(<MarcaDeGravacao instante={new Date(2026, 8, 7, 15, 5)} />);

    expect(screen.queryByText("Salvo às 14h32")).not.toBeInTheDocument();
    expect(screen.getByText("Salvo às 15h05")).toBeInTheDocument();
  });
});
