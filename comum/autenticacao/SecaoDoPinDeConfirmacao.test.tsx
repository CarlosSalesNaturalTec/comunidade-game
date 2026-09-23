import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as api from "./api";
import { SecaoDoPinDeConfirmacao } from "./SecaoDoPinDeConfirmacao";

function renderizar(temPin: boolean) {
  vi.spyOn(api, "eu").mockResolvedValue({
    persona_id: "mestre-1",
    papel: "mestre",
    permissoes: {},
    tem_pin_de_confirmacao: temPin,
  });
  render(<SecaoDoPinDeConfirmacao token="token-do-mestre" aoRecusarSessao={vi.fn()} />);
}

describe("PIN de confirmação do adulto (RF-09-121, RF-02-110)", () => {
  beforeEach(() => sessionStorage.clear());
  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("cadastra o PIN digitado duas vezes e diz que está cadastrado, sem mostrá-lo", async () => {
    renderizar(false);
    const cadastrar = vi.spyOn(api, "cadastrarPinDeConfirmacao").mockResolvedValue(undefined);
    const usuario = userEvent.setup();

    expect(await screen.findByText(/ainda não tem pin cadastrado/i)).toBeInTheDocument();
    await usuario.type(screen.getByLabelText(/^pin \(4 dígitos\)/i), "4821");
    await usuario.type(screen.getByLabelText(/repita o pin/i), "4821");
    await usuario.click(screen.getByRole("button", { name: /cadastrar pin/i }));

    await waitFor(() => expect(cadastrar).toHaveBeenCalledWith("token-do-mestre", "4821"));
    expect(await screen.findByText(/^pin cadastrado\.$/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^pin \(4 dígitos\)/i)).toHaveAttribute("type", "password");
    expect(screen.getByLabelText(/^pin \(4 dígitos\)/i)).toHaveValue("");
    expect(document.body.textContent).not.toContain("4821");
  });

  it("digitações diferentes não saem da tela", async () => {
    renderizar(false);
    const cadastrar = vi.spyOn(api, "cadastrarPinDeConfirmacao");
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^pin \(4 dígitos\)/i), "4821");
    await usuario.type(screen.getByLabelText(/repita o pin/i), "4822");
    await usuario.click(screen.getByRole("button", { name: /cadastrar pin/i }));

    expect(await screen.findByText(/não são iguais/i)).toBeInTheDocument();
    expect(cadastrar).not.toHaveBeenCalled();
  });

  it("PIN fora do formato não sai da tela", async () => {
    renderizar(false);
    const cadastrar = vi.spyOn(api, "cadastrarPinDeConfirmacao");
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^pin \(4 dígitos\)/i), "48a");
    await usuario.type(screen.getByLabelText(/repita o pin/i), "48");
    await usuario.click(screen.getByRole("button", { name: /cadastrar pin/i }));

    expect(await screen.findByText(/4 dígitos, só números/i)).toBeInTheDocument();
    expect(cadastrar).not.toHaveBeenCalled();
  });

  it("com PIN já cadastrado, diz isso e oferece a troca", async () => {
    renderizar(true);

    expect(await screen.findByText(/já tem pin cadastrado/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /trocar pin/i })).toBeInTheDocument();
  });
});
