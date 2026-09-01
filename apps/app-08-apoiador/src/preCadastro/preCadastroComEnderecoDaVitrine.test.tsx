import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as preCadastroApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

// Só este arquivo declara o endereço do formulário da vitrine, para isolar o
// caso do endereço configurado do caso, mais comum no Ciclo 01, sem endereço
// (`RF-14-07`, RN-14-05`, design — decisão 7).
vi.mock("../api/configuracao", async () => {
  const real =
    await vi.importActual<typeof import("../api/configuracao")>("../api/configuracao");
  return { ...real, URL_DO_FORMULARIO_DA_VITRINE: "https://vitrine.example.org/participar" };
});

describe("encaminhamento à vitrine com endereço configurado", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(preCadastroApi, "listarNecessidadesEmAberto").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("com endereço configurado, a porta oferece o link do formulário da vitrine", async () => {
    render(<App />);
    await screen.findByRole("heading", { name: /comunidade game — área do apoiador/i });
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByLabelText(/sem transferir dinheiro/i));

    const link = await screen.findByRole("link", {
      name: /formulário de solicitação da vitrine/i,
    });
    expect(link).toHaveAttribute("href", "https://vitrine.example.org/participar");
  });
});
