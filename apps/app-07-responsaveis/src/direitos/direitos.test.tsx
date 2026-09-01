import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AvisoDeColeta } from "./AvisoDeColeta";
import { ProvedorDeDireitos } from "./ContextoDeDireitos";

afterEach(() => {
  vi.restoreAllMocks();
});

describe("aviso de coleta", () => {
  it("não bloqueia a tela nem exige confirmação para continuar", () => {
    render(
      <ProvedorDeDireitos irParaTransparencia={vi.fn()}>
        <AvisoDeColeta dado="a decisão da autorização" />
      </ProvedorDeDireitos>,
    );

    expect(screen.getByText(/coleta a decisão da autorização/i)).toHaveAttribute(
      "role",
      "status",
    );
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("nomeia o dado da própria tela, e não o de outra", () => {
    render(
      <ProvedorDeDireitos irParaTransparencia={vi.fn()}>
        <AvisoDeColeta dado="o texto da sua proposta de evolução da plataforma" />
      </ProvedorDeDireitos>,
    );

    expect(screen.getByText(/coleta o texto da sua proposta/i)).toBeInTheDocument();
    expect(screen.queryByText(/decisão da autorização/i)).not.toBeInTheDocument();
  });

  it("o acesso a partir do aviso chega na transparência", async () => {
    const irParaTransparencia = vi.fn();
    render(
      <ProvedorDeDireitos irParaTransparencia={irParaTransparencia}>
        <AvisoDeColeta dado="a decisão da autorização" />
      </ProvedorDeDireitos>,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /ver na transparência/i }));

    expect(irParaTransparencia).toHaveBeenCalledTimes(1);
  });
});
