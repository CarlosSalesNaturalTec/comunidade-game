import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { TrilhaDaLista } from "./api";
import * as trilhasApi from "./api";
import { DuplicarTrilha } from "./DuplicarTrilha";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

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
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

function copiaDaTrilha(): TrilhaDaLista {
  return {
    id: "trilha-copia",
    nome: "Robô Educa (cópia)",
    objetivo: "Construir o próprio robô.",
    area_do_conhecimento: "Programação e Robótica",
    poder_id: "poder-1",
    situacao: "rascunho",
    motivo_da_situacao: null,
    etiquetas_ods: [],
    cobertura_ods: { objetivos: [], ciclo: "Ciclo 01" },
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Duplicar trilha", () => {
  it("avisa o que a cópia traz e o que não traz antes de duplicar", async () => {
    configurarSessao();

    render(<DuplicarTrilha idDaTrilha="trilha-1" onDuplicada={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^duplicar$/i }));

    expect(screen.getByText(/nasce em rascunho/i)).toBeInTheDocument();
    expect(screen.getByText(/missões e as atividades da origem/i)).toBeInTheDocument();
    expect(screen.getByText(/não traz inscrição, desbloqueio/i)).toBeInTheDocument();
  });

  it("confirma a duplicação e leva a cópia em rascunho ao Mestre", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "duplicarTrilha").mockResolvedValue(copiaDaTrilha());
    const aoDuplicar = vi.fn();

    render(<DuplicarTrilha idDaTrilha="trilha-1" onDuplicada={aoDuplicar} />);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^duplicar$/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar duplicação/i }));

    await waitFor(() =>
      expect(trilhasApi.duplicarTrilha).toHaveBeenCalledWith("trilha-1", "token-do-mestre"),
    );
    expect(aoDuplicar).toHaveBeenCalledWith(
      expect.objectContaining({ id: "trilha-copia", situacao: "rascunho" }),
    );
  });
});
