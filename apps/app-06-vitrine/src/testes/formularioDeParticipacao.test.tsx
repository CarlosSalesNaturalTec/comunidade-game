import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as solicitacoes from "../api/solicitacoes";
import App from "./TelaDaVitrine";

// Critérios de aceite do PRD-03 §12: formulário de participação com os cinco
// campos obrigatórios, avisos antes do envio e confirmação com o prazo.

const REGISTRO = { id: "protocolo-123", prazo: "2026-10-06T12:00:00Z" };

async function preencher(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.type(screen.getByLabelText("Nome"), "Maria Souza");
  await testeDeUsuario.type(screen.getByLabelText("E-mail"), "maria@exemplo.org");
  await testeDeUsuario.type(screen.getByLabelText("WhatsApp"), "11999990000");
  await testeDeUsuario.selectOptions(screen.getByLabelText("Quero ser"), "mestre");
  await testeDeUsuario.type(screen.getByLabelText("Apresentação"), "Sou educadora.");
}

describe("formulário de participação", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/participar");
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("declara os avisos antes de qualquer envio (RF-03-29, RF-03-30)", () => {
    render(<App />);
    expect(screen.getByText(/não cria cadastro nem acesso/i)).toBeInTheDocument();
    expect(screen.getByText(/Admin, em até 7 dias/)).toBeInTheDocument();
  });

  it("aponta o campo em falta e não chama o núcleo (RF-03-27)", async () => {
    const enviar = vi.spyOn(solicitacoes, "enviarParticipacao");
    render(<App />);
    await userEvent.click(screen.getByRole("button", { name: "Enviar pedido" }));

    expect(screen.getAllByText("Preencha este campo.")).toHaveLength(5);
    expect(enviar).not.toHaveBeenCalled();
  });

  it("envia sem os opcionais e confirma protocolo e prazo (RF-03-28, RF-03-31)", async () => {
    const enviar = vi.spyOn(solicitacoes, "enviarParticipacao").mockResolvedValue(REGISTRO);
    render(<App />);
    const testeDeUsuario = userEvent.setup();
    await preencher(testeDeUsuario);
    await testeDeUsuario.click(screen.getByRole("button", { name: "Enviar pedido" }));

    expect(enviar).toHaveBeenCalledWith(
      expect.objectContaining({
        pretensao: "mestre",
        instituicao: undefined,
        links: undefined,
      }),
    );
    expect(await screen.findByText(/protocolo-123/)).toBeInTheDocument();
    expect(screen.getByText(/não envia e-mail automático/)).toBeInTheDocument();
  });

  it("a orientação do Mestre no Entrar abre o formulário (RF-03-62)", async () => {
    window.history.pushState(null, "", "/");
    render(<App />);
    const testeDeUsuario = userEvent.setup();
    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Mestre" }));

    expect(screen.getByRole("link", { name: /formulário de participação/i })).toHaveAttribute(
      "href",
      "/participar",
    );
  });
});
