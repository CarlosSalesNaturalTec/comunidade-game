import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as solicitacoes from "../api/solicitacoes";

const freio = () =>
  new ErroDaApi(429, { codigo: "muitas_requisicoes", mensagem: "Espere." }, 120);

describe("o freio dos formulários é explicado, sem CAPTCHA nem cadastro", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("participação: motivo, espera e texto preservado (RF-03-35, RF-03-37)", async () => {
    window.history.pushState(null, "", "/participar");
    localStorage.clear();
    vi.spyOn(solicitacoes, "enviarParticipacao").mockRejectedValue(freio());
    render(<App />);
    const u = userEvent.setup();
    await u.type(screen.getByLabelText("Nome"), "Maria");
    await u.type(screen.getByLabelText("E-mail"), "m@e.org");
    await u.type(screen.getByLabelText("WhatsApp"), "1199");
    await u.selectOptions(screen.getByLabelText("Quero ser"), "apoiador");
    await u.type(screen.getByLabelText("Apresentação"), "Olá");
    await u.click(screen.getByRole("button", { name: "Enviar pedido" }));

    expect(await screen.findByText(/muitas vezes seguidas/)).toHaveTextContent("2 minutos");
    expect(screen.getByLabelText("Nome")).toHaveValue("Maria");
    expect(screen.queryByText(/captcha/i)).not.toBeInTheDocument();
    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });

  it("dados: motivo e espera (RF-03-35)", async () => {
    window.history.pushState(null, "", "/solicitar-dados");
    vi.spyOn(solicitacoes, "enviarSolicitacaoDeDados").mockRejectedValue(freio());
    render(<App />);
    const u = userEvent.setup();
    await u.type(screen.getByLabelText("Solicitante"), "Ana");
    await u.type(screen.getByLabelText("Instituição"), "P");
    await u.type(screen.getByLabelText("E-mail"), "a@e.org");
    await u.type(screen.getByLabelText("Finalidade declarada"), "F");
    await u.type(screen.getByLabelText(/Recorte pedido/), "R");
    await u.click(screen.getByRole("button", { name: "Enviar pedido" }));

    expect(await screen.findByText(/muitas vezes seguidas/)).toHaveTextContent("2 minutos");
    expect(screen.getByLabelText("Solicitante")).toHaveValue("Ana");
  });
});
