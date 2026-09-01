import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { DocumentoDoApoiador } from "./api";
import * as documentosApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

async function entrarNosComprobatorios() {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-apoiador",
    expira_em: new Date().toISOString(),
    papel: "apoiador",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: "algum-id",
    papel: "apoiador",
    permissoes: {},
  });

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "apoiadora");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.click(
    await screen.findByRole("button", { name: /documentos comprobatórios/i }),
  );
  await screen.findByRole("heading", { name: /documentos comprobatórios/i });
  return testeDeUsuario;
}

describe("documentos comprobatórios do Apoiador", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(documentosApi, "listarMeusDocumentos").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a tela pede endereço e rótulo, e não oferece anexo de arquivo", async () => {
    await entrarNosComprobatorios();

    expect(screen.getByLabelText(/endereço \(link\)/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^rótulo$/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/anexo|arquivo/i)).not.toBeInTheDocument();
    expect(document.querySelector('input[type="file"]')).not.toBeInTheDocument();
  });

  it("a declaração de que só o Admin publica aparece antes do envio", async () => {
    await entrarNosComprobatorios();

    expect(
      screen.getByText(/só aparece na sua página pública quando um admin o anexar/i),
    ).toBeInTheDocument();
  });

  it("o documento enviado aparece como pendente", async () => {
    const testeDeUsuario = await entrarNosComprobatorios();
    const declarado: DocumentoDoApoiador = {
      id: "doc-1",
      endereco: "https://exemplo.org/curriculo",
      rotulo: "Currículo",
      publicado: false,
    };
    vi.spyOn(documentosApi, "declararDocumento").mockResolvedValue(declarado);
    vi.spyOn(documentosApi, "listarMeusDocumentos").mockResolvedValue([declarado]);

    await testeDeUsuario.type(
      screen.getByLabelText(/endereço \(link\)/i),
      "https://exemplo.org/curriculo",
    );
    await testeDeUsuario.type(screen.getByLabelText(/^rótulo$/i), "Currículo");
    await testeDeUsuario.click(screen.getByRole("button", { name: /enviar documento/i }));

    expect(await screen.findByText(/documento enviado como pendente/i)).toBeInTheDocument();
    const secaoPendentes = screen.getByRole("heading", { name: /pendentes/i })
      .parentElement as HTMLElement;
    expect(secaoPendentes).toHaveTextContent(/currículo/i);
  });

  it("a lista separa o que já está publicado do que está pendente", async () => {
    vi.spyOn(documentosApi, "listarMeusDocumentos").mockResolvedValue([
      {
        id: "doc-publicado",
        endereco: "https://exemplo.org/portfolio",
        rotulo: "Portfólio",
        publicado: true,
      },
      {
        id: "doc-pendente",
        endereco: "https://exemplo.org/curriculo",
        rotulo: "Currículo",
        publicado: false,
      },
    ]);

    await entrarNosComprobatorios();

    const secaoPublicados = await screen.findByRole("heading", { name: /^publicados$/i });
    const secaoPendentes = screen.getByRole("heading", { name: /^pendentes$/i });
    expect(secaoPublicados.parentElement).toHaveTextContent(/portfólio/i);
    expect(secaoPublicados.parentElement).not.toHaveTextContent(/currículo/i);
    expect(secaoPendentes.parentElement).toHaveTextContent(/currículo/i);
    expect(secaoPendentes.parentElement).not.toHaveTextContent(/portfólio/i);
  });
});
