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

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

function configurarSessao() {
  vi.mocked(useSessao).mockReturnValue({
    sessao: SESSAO_DE_ADMIN,
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
  window.history.replaceState({}, "", "/");
});

// O caminho que a App 09 oferece para o painel do dia chega por parâmetro
// de URL — as duas aplicações não compartilham estado (`RF-09-50`).
describe("área inicial vinda da URL (RF-09-50)", () => {
  it("abre direto no painel do dia quando a URL declara a área", () => {
    window.history.replaceState({}, "", "/?area=painel-do-dia");
    configurarSessao();

    render(<App />);

    expect(
      screen.getByRole("button", { name: "Painel do dia", current: true }),
    ).toBeInTheDocument();
  });

  it("área desconhecida na URL cai no padrão, sem quebrar", () => {
    window.history.replaceState({}, "", "/?area=nao-existe");
    configurarSessao();

    render(<App />);

    expect(
      screen.getByRole("button", { name: "Comunidades", current: true }),
    ).toBeInTheDocument();
  });

  it("sem parâmetro na URL abre em Comunidades, como sempre", () => {
    configurarSessao();

    render(<App />);

    expect(
      screen.getByRole("button", { name: "Comunidades", current: true }),
    ).toBeInTheDocument();
  });
});

// A saída fica só na navegação — nenhuma tela de área a monta de novo
// (documento 15 §6, design — decisão 4).
describe("saída da sessão única (documento 15 §6)", () => {
  it("existe exatamente uma saída, sempre no mesmo lugar, ao trocar de área", async () => {
    configurarSessao();
    const usuario = userEvent.setup();
    render(<App />);

    for (const rotulo of ["Poderes", "Direitos e dados", "Comunidades"]) {
      await usuario.click(screen.getByRole("button", { name: rotulo }));
      expect(screen.getAllByRole("button", { name: "Sair" })).toHaveLength(1);
    }
  });

  it("aciona a saída da sessão pela navegação", async () => {
    const aoSair = vi.fn();
    vi.mocked(useSessao).mockReturnValue({
      sessao: SESSAO_DE_ADMIN,
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
