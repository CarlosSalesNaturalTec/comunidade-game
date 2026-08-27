import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { DesbloqueioPendente } from "../trilhas/api";
import * as trilhasApi from "../trilhas/api";
import { TelaDeDesbloqueiosPendentes } from "./TelaDeDesbloqueiosPendentes";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

function configurarSessao() {
  vi.mocked(useSessao).mockReturnValue({
    sessao: SESSAO_DE_MESTRE,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

function pendente(sobrescreve: Partial<DesbloqueioPendente> = {}): DesbloqueioPendente {
  return {
    id: "desbloqueio-1",
    guerreiro_id: "guerreiro-1",
    guerreiro_nome: "Guerreira Ana",
    missao_id: "missao-1",
    missao_titulo: "Montar o robô",
    momento: "2026-08-27T10:00:00-03:00",
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("bancada dos desafios práticos a julgar (RF-09-26, RF-09-117)", () => {
  it("a lista traz o que espera julgamento", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText("Guerreira Ana")).toBeInTheDocument();
    expect(screen.getByText(/montar o robô/i)).toBeInTheDocument();
  });

  it("sem nenhuma declaração pendente, avisa sem erro", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([]);

    render(<TelaDeDesbloqueiosPendentes />);

    expect(await screen.findByText(/nenhum desafio prático/i)).toBeInTheDocument();
  });

  it("julgar que passou tira da lista", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);
    const julgarEspiado = vi
      .spyOn(trilhasApi, "julgarDesafioPratico")
      .mockResolvedValue({ aprovado: true });

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^passou$/i }));

    await waitFor(() =>
      expect(julgarEspiado).toHaveBeenCalledWith(
        "missao-1",
        "guerreiro-1",
        true,
        "token-do-mestre",
      ),
    );
    expect(screen.queryByText("Guerreira Ana")).not.toBeInTheDocument();
  });

  it("julgar que não passou também tira da lista, sem eliminar ninguém", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarDesbloqueiosPendentes").mockResolvedValue([pendente()]);
    vi.spyOn(trilhasApi, "julgarDesafioPratico").mockResolvedValue({ aprovado: false });

    render(<TelaDeDesbloqueiosPendentes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /não passou/i }));

    await waitFor(() => expect(screen.queryByText("Guerreira Ana")).not.toBeInTheDocument());
  });
});
