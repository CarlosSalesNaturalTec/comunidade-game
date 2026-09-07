import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "./App";

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
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

// A saída fica só na navegação — nenhuma tela de área a monta de novo
// (documento 15 §6, design — decisão 4).
describe("saída da sessão única (documento 15 §6)", () => {
  it("existe exatamente uma saída, sempre no mesmo lugar, ao trocar de área", async () => {
    configurarSessao();
    const usuario = userEvent.setup();
    render(<App />);

    for (const rotulo of ["Minhas turmas", "Direitos e dados", "Minhas trilhas"]) {
      await usuario.click(screen.getByRole("button", { name: rotulo }));
      expect(screen.getAllByRole("button", { name: "Sair" })).toHaveLength(1);
    }
  });

  it("aciona a saída da sessão pela navegação", async () => {
    const aoSair = vi.fn();
    vi.mocked(useSessao).mockReturnValue({
      sessao: SESSAO_DE_MESTRE,
      restaurando: false,
      entrando: false,
      erroDeEntrada: null,
      entrarComGoogle: vi.fn(),
      entrarComToken: vi.fn(),
      sair: aoSair,
      tratarRecusaDeSessao: vi.fn(),
      entrarComCredencial: vi.fn(),
      trocaDeSenhaPendente: false,
      trocandoSenha: false,
      erroDeTrocaDeSenha: null,
      trocarSenhaProvisoria: vi.fn(),
    });
    const usuario = userEvent.setup();
    render(<App />);

    await usuario.click(screen.getByRole("button", { name: "Sair" }));

    expect(aoSair).toHaveBeenCalledOnce();
  });
});
