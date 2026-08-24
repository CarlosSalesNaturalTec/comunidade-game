import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ChaveDeAplicacao } from "./api";
import * as chavesApi from "./api";
import { TelaDeChaves } from "./TelaDeChaves";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

function chaveDeAplicacao(parcial: Partial<ChaveDeAplicacao> = {}): ChaveDeAplicacao {
  return {
    id: "chave-1",
    aplicacao: "Desenvolvedora de Tal",
    natureza: "de_terceiro",
    ambiente: "producao",
    prazo_de_apresentacao: "2026-09-01T00:00:00-03:00",
    url_apresentada: null,
    situacao: "vigente",
    ...parcial,
  };
}

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("painel de chaves", () => {
  it("mostra prazo, URL apresentada e situação de cada chave", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(chavesApi, "listarChaves").mockResolvedValue({
      itens: [
        chaveDeAplicacao({
          url_apresentada: "https://exemplo.org/painel",
          prazo_de_apresentacao: null,
        }),
      ],
      proximo_cursor: null,
    });

    render(<TelaDeChaves />);

    expect(await screen.findByText("Desenvolvedora de Tal")).toBeInTheDocument();
    expect(screen.getByText("Vigente")).toBeInTheDocument();
    expect(screen.getByText(/https:\/\/exemplo\.org\/painel/)).toBeInTheDocument();
  });

  it("prazo a vencer vem por rótulo legível, sem depender de cor", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(chavesApi, "listarChaves").mockResolvedValue({
      itens: [chaveDeAplicacao({ url_apresentada: null })],
      proximo_cursor: null,
    });

    render(<TelaDeChaves />);

    const rotulo = await screen.findByText("Prazo a vencer");
    expect(rotulo.tagName).toBe("SPAN");
  });

  it("revogada por prazo vencido vem por rótulo legível, sem depender de cor", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(chavesApi, "listarChaves").mockResolvedValue({
      itens: [
        chaveDeAplicacao({
          situacao: "revogada",
          url_apresentada: null,
          prazo_de_apresentacao: "2020-01-01T00:00:00-03:00",
        }),
      ],
      proximo_cursor: null,
    });

    render(<TelaDeChaves />);

    const rotulo = await screen.findByText("Revogada por prazo vencido");
    expect(rotulo.tagName).toBe("SPAN");
  });

  it("revogar sem motivo é apontado no campo sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(chavesApi, "listarChaves").mockResolvedValue({
      itens: [chaveDeAplicacao()],
      proximo_cursor: null,
    });
    const revogarEspiado = vi.spyOn(chavesApi, "revogarChave");

    render(<TelaDeChaves />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^revogar$/i }));
    await usuario.click(screen.getByRole("button", { name: /^confirmar revogação$/i }));

    expect(await screen.findByText(/informe o motivo da revogação/i)).toBeInTheDocument();
    expect(revogarEspiado).not.toHaveBeenCalled();
  });

  it("revogar com motivo chama o núcleo e recarrega a lista", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(chavesApi, "listarChaves").mockResolvedValue({
      itens: [chaveDeAplicacao()],
      proximo_cursor: null,
    });
    vi.spyOn(chavesApi, "revogarChave").mockResolvedValue(undefined);

    render(<TelaDeChaves />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^revogar$/i }));
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Uso indevido detectado.");
    await usuario.click(screen.getByRole("button", { name: /^confirmar revogação$/i }));

    await waitFor(() =>
      expect(chavesApi.revogarChave).toHaveBeenCalledWith(
        "chave-1",
        "Uso indevido detectado.",
        "token-do-admin",
      ),
    );
    await waitFor(() => expect(chavesApi.listarChaves).toHaveBeenCalledTimes(2));
  });

  it("o painel nunca mostra o segredo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(chavesApi, "listarChaves").mockResolvedValue({
      itens: [chaveDeAplicacao()],
      proximo_cursor: null,
    });

    render(<TelaDeChaves />);

    await screen.findByText("Desenvolvedora de Tal");
    expect(document.body.textContent?.toLowerCase()).not.toContain("segredo");
  });

  it("Mestre lê a recusa em linguagem simples, não um erro cru", async () => {
    configurarSessao({
      token: "token-do-mestre",
      papel: "mestre",
      permissoes: {},
      persona_id: "mestre-1",
    });
    const listarEspiado = vi.spyOn(chavesApi, "listarChaves");

    render(<TelaDeChaves />);

    expect(await screen.findByText(/esta área é do admin/i)).toBeInTheDocument();
    expect(listarEspiado).not.toHaveBeenCalled();
  });
});
