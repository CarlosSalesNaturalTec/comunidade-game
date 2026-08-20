import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { describe, expect, it, vi } from "vitest";
import { Campo } from "./Campo";

function CampoControlado({ erroInicial }: { erroInicial: string | null }) {
  const [valor, definirValor] = useState("");
  const [erro, definirErro] = useState(erroInicial);
  return (
    <Campo
      rotulo="Nome"
      valor={valor}
      aoAlterar={(novoValor) => {
        definirValor(novoValor);
        definirErro(null);
      }}
      erro={erro}
    />
  );
}

describe("Campo", () => {
  it("amarra rótulo, mensagem de erro e estado inválido ao campo", () => {
    render(<Campo rotulo="Nome" valor="" aoAlterar={vi.fn()} erro="Informe o nome." />);

    const campo = screen.getByLabelText("Nome");
    expect(campo).toHaveAttribute("aria-invalid", "true");
    expect(campo).toHaveAccessibleDescription("Informe o nome.");
    expect(screen.getByRole("alert")).toHaveTextContent("Informe o nome.");
  });

  it("sem erro, o campo não é anunciado como inválido nem descrito por mensagem alguma", () => {
    render(<Campo rotulo="Nome" valor="" aoAlterar={vi.fn()} erro={null} />);

    const campo = screen.getByLabelText("Nome");
    expect(campo).not.toHaveAttribute("aria-invalid");
    expect(campo).toHaveAccessibleDescription("");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("corrigido o valor, o campo deixa de ser anunciado como inválido", async () => {
    const usuario = userEvent.setup();
    render(<CampoControlado erroInicial="Informe o nome." />);

    const campo = screen.getByLabelText("Nome");
    expect(campo).toHaveAttribute("aria-invalid", "true");

    await usuario.type(campo, "a");

    expect(campo).not.toHaveAttribute("aria-invalid");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});
