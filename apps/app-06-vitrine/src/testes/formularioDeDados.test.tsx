import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as solicitacoes from "../api/solicitacoes";

const REGISTRO = { id: "protocolo-456", prazo: "2026-10-06T12:00:00Z" };

describe("formulário de dados", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/solicitar-dados");
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("declara as condições da entrega (RF-03-33)", () => {
    render(<App />);
    const aviso = screen.getByText(/A entrega é gratuita/);
    expect(aviso).toHaveTextContent(/anonimizada/);
    expect(aviso).toHaveTextContent(/CC BY-SA/);
    expect(aviso).toHaveTextContent(/aprovação de um Admin/);
    expect(aviso).toHaveTextContent(/7 dias/);
  });

  it("aponta o campo em falta (RF-03-32)", async () => {
    const enviar = vi.spyOn(solicitacoes, "enviarSolicitacaoDeDados");
    render(<App />);
    await userEvent.click(screen.getByRole("button", { name: "Enviar pedido" }));
    expect(screen.getAllByText("Preencha este campo.")).toHaveLength(5);
    expect(enviar).not.toHaveBeenCalled();
  });

  it("confirma sem arquivo nem link de download (RF-03-34, RN-03-13)", async () => {
    vi.spyOn(solicitacoes, "enviarSolicitacaoDeDados").mockResolvedValue(REGISTRO);
    render(<App />);
    const u = userEvent.setup();
    await u.type(screen.getByLabelText("Solicitante"), "Ana");
    await u.type(screen.getByLabelText("Instituição"), "Prefeitura");
    await u.type(screen.getByLabelText("E-mail"), "ana@exemplo.org");
    await u.type(screen.getByLabelText("Finalidade declarada"), "Política pública");
    await u.type(screen.getByLabelText(/Recorte pedido/), "Todas as comunidades");
    await u.click(screen.getByRole("button", { name: "Enviar pedido" }));

    expect(await screen.findByText(/protocolo-456/)).toBeInTheDocument();
    expect(screen.getByText(/depende de aprovação de um Admin/)).toBeInTheDocument();
    expect(screen.queryByRole("link")).not.toBeInTheDocument();
  });

  it("a seção do recorte de pesquisadores leva ao formulário", async () => {
    window.history.pushState(null, "", "/pesquisadores");
    render(<App />);
    await userEvent.click(screen.getByRole("button", { name: "Pedir o conjunto de dados" }));
    expect(window.location.pathname).toBe("/solicitar-dados");
  });
});
