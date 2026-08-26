import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AvisoDeColeta } from "./AvisoDeColeta";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("aviso de coleta de dados", () => {
  it("não bloqueia a tela nem exige confirmação para continuar", () => {
    render(<AvisoDeColeta />);

    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("dá acesso à área detalhada, sem começar aberta", async () => {
    render(<AvisoDeColeta />);
    const usuario = userEvent.setup();

    expect(
      screen.queryByText(/fica guardado com o seu nome de coletor/i),
    ).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /saber mais/i }));

    expect(screen.getByText(/fica guardado com o seu nome de coletor/i)).toBeInTheDocument();
  });
});
