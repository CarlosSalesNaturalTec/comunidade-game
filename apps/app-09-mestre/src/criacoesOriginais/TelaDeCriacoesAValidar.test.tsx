import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { CriacaoNaFila } from "./api";
import * as criacoesApi from "./api";
import { TelaDeCriacoesAValidar } from "./TelaDeCriacoesAValidar";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

vi.mock("../direitos/ContextoDeDireitos", async () => {
  const real = await vi.importActual<typeof import("../direitos/ContextoDeDireitos")>(
    "../direitos/ContextoDeDireitos",
  );
  return { ...real, useDireitos: () => ({ irParaDireitos: vi.fn() }) };
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

function criacaoNaFila(sobrescreve: Partial<CriacaoNaFila> = {}): CriacaoNaFila {
  return {
    id: "criacao-1",
    trilha_id: "trilha-1",
    trilha_nome: "Robô Educa",
    criterio_de_validacao: "Precisa funcionar de verdade.",
    tipo: "texto",
    producao: "Nosso robô de sucata.",
    referencia: null,
    autores: [
      { avatar: null, nick: "criadora", papel: "quem construiu" },
      { avatar: null, nick: "colega", papel: null },
    ],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criações originais a validar (RF-09-31 a RF-09-34)", () => {
  it("a fila traz a trilha, o critério e o papel de cada integrante", async () => {
    configurarSessao();
    vi.spyOn(criacoesApi, "listarFilaDeCriacoes").mockResolvedValue([criacaoNaFila()]);

    render(<TelaDeCriacoesAValidar />);

    expect(await screen.findByText("Robô Educa")).toBeInTheDocument();
    expect(screen.getByText(/Precisa funcionar de verdade\./)).toBeInTheDocument();
    expect(screen.getByText(/quem construiu/)).toBeInTheDocument();
    expect(screen.getByText("colega")).toBeInTheDocument();
  });

  it("sem nenhuma criação pendente, avisa sem erro", async () => {
    configurarSessao();
    vi.spyOn(criacoesApi, "listarFilaDeCriacoes").mockResolvedValue([]);

    render(<TelaDeCriacoesAValidar />);

    expect(await screen.findByText(/nenhuma criação original/i)).toBeInTheDocument();
  });

  it("validar credita a autoria, libera o badge e avisa da autorização de divulgação", async () => {
    configurarSessao();
    vi.spyOn(criacoesApi, "listarFilaDeCriacoes").mockResolvedValue([criacaoNaFila()]);
    const validarEspiado = vi.spyOn(criacoesApi, "validarCriacaoOriginal").mockResolvedValue({
      id: "criacao-1",
      trilha_id: "trilha-1",
      equipe_id: "equipe-1",
      guerreiro_id: null,
      tipo: "texto",
      producao: "Nosso robô de sucata.",
      referencia: null,
      tamanho: null,
      situacao: "validada",
      motivo_da_devolucao: null,
    });

    render(<TelaDeCriacoesAValidar />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^validar$/i }));

    await waitFor(() =>
      expect(validarEspiado).toHaveBeenCalledWith("criacao-1", "token-do-mestre"),
    );
    expect(screen.queryByText("Robô Educa")).not.toBeInTheDocument();
    expect(await screen.findByText(/autorização de divulgação vigente/i)).toBeInTheDocument();
  });

  it("devolução sem motivo é recusada, sem chamar a API", async () => {
    configurarSessao();
    vi.spyOn(criacoesApi, "listarFilaDeCriacoes").mockResolvedValue([criacaoNaFila()]);
    const devolverEspiado = vi.spyOn(criacoesApi, "devolverCriacaoOriginal");

    render(<TelaDeCriacoesAValidar />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^devolver$/i }));

    expect(await screen.findByText(/escreva o motivo/i)).toBeInTheDocument();
    expect(devolverEspiado).not.toHaveBeenCalled();
  });

  it("devolução com motivo preserva a autoria e tira da fila", async () => {
    configurarSessao();
    vi.spyOn(criacoesApi, "listarFilaDeCriacoes").mockResolvedValue([criacaoNaFila()]);
    const devolverEspiado = vi
      .spyOn(criacoesApi, "devolverCriacaoOriginal")
      .mockResolvedValue({
        id: "criacao-1",
        trilha_id: "trilha-1",
        equipe_id: "equipe-1",
        guerreiro_id: null,
        tipo: "texto",
        producao: "Nosso robô de sucata.",
        referencia: null,
        tamanho: null,
        situacao: "devolvida",
        motivo_da_devolucao: "Falta explicar como funciona.",
      });

    render(<TelaDeCriacoesAValidar />);
    const usuario = userEvent.setup();

    await usuario.type(
      await screen.findByLabelText(/motivo da devolução/i),
      "Falta explicar como funciona.",
    );
    await usuario.click(screen.getByRole("button", { name: /^devolver$/i }));

    await waitFor(() =>
      expect(devolverEspiado).toHaveBeenCalledWith(
        "criacao-1",
        "Falta explicar como funciona.",
        "token-do-mestre",
      ),
    );
    expect(screen.queryByText("Robô Educa")).not.toBeInTheDocument();
  });
});
