import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { CampoDeDataHora } from "./CampoDeDataHora";

function CampoControlado() {
  const [valor, definirValor] = useState("");
  return <CampoDeDataHora rotulo="Início" valor={valor} aoAlterar={definirValor} />;
}

describe("CampoDeDataHora", () => {
  it("o valor devolvido sempre carrega fuso explícito", () => {
    const aoAlterar = vi.fn();
    render(<CampoDeDataHora rotulo="Início" valor="" aoAlterar={aoAlterar} />);

    const campo = screen.getByLabelText("Início");
    fireEvent.change(campo, { target: { value: "2026-08-10T10:00" } });

    expect(aoAlterar).toHaveBeenCalledTimes(1);
    const valorDevolvido = aoAlterar.mock.calls[0][0] as string;
    expect(valorDevolvido).toMatch(/^2026-08-10T10:00:00(Z|[+-]\d{2}:\d{2})$/);
  });

  it("o valor devolvido é aceito de volta e reexibido no campo", () => {
    render(<CampoControlado />);

    const campo = screen.getByLabelText("Início");
    fireEvent.change(campo, { target: { value: "2026-08-10T10:00" } });

    expect(campo).toHaveValue("2026-08-10T10:00");
  });

  it("campo vazio nunca produz horário sem fuso", () => {
    const aoAlterar = vi.fn();
    render(
      <CampoDeDataHora rotulo="Início" valor="2026-08-10T10:00:00Z" aoAlterar={aoAlterar} />,
    );

    const campo = screen.getByLabelText("Início");
    fireEvent.change(campo, { target: { value: "" } });

    expect(aoAlterar).toHaveBeenCalledWith("");
  });

  it("valor inválido aponta o erro no próprio campo", () => {
    render(
      <CampoDeDataHora
        rotulo="Início"
        valor=""
        aoAlterar={vi.fn()}
        erro="Horário final precisa ser posterior ao inicial."
      />,
    );

    const campo = screen.getByLabelText("Início");
    expect(campo).toHaveAttribute("aria-invalid", "true");
    expect(campo).toHaveAccessibleDescription(
      "Horário final precisa ser posterior ao inicial.",
    );
    expect(screen.getByRole("alert")).toHaveTextContent(
      "Horário final precisa ser posterior ao inicial.",
    );
  });

  it("sem erro, o campo não é anunciado como inválido", () => {
    render(<CampoDeDataHora rotulo="Início" valor="" aoAlterar={vi.fn()} erro={null} />);

    const campo = screen.getByLabelText("Início");
    expect(campo).not.toHaveAttribute("aria-invalid");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("é um input nativo alcançável pelo teclado, na ordem de tabulação", async () => {
    const usuario = userEvent.setup();
    render(<CampoControlado />);

    await usuario.tab();
    const campo = screen.getByLabelText("Início");
    expect(campo.tagName).toBe("INPUT");
    expect(campo).toHaveAttribute("type", "datetime-local");
    expect(campo).toHaveFocus();
  });
});
