import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { SessaoAberta } from "../autenticacao/ContextoDeSessao";
import * as comunidadesApi from "../comunidades/api";
import * as pontosDeApoioApi from "./api";
import { FormularioDePontoDeApoio } from "./FormularioDePontoDeApoio";
import { TelaDePontosDeApoio } from "./TelaDePontosDeApoio";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
};

const COMUNIDADE = {
  id: "comunidade-1",
  nome: "Comunidade de Teste",
  localizacao: "Bairro de teste",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

vi.mock("../autenticacao/ContextoDeSessao", async () => {
  const real = await vi.importActual<typeof import("../autenticacao/ContextoDeSessao")>(
    "../autenticacao/ContextoDeSessao",
  );
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "../autenticacao/ContextoDeSessao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cadastro de ponto de apoio", () => {
  it("Admin cadastra o ponto de apoio e ele aparece entre os existentes", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio")
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [
          {
            id: "ponto-1",
            nome: "Sede",
            comunidade_virtual_id: COMUNIDADE.id,
            responsavel_id: null,
            ativo: true,
          },
        ],
        proximo_cursor: null,
      });
    vi.spyOn(pontosDeApoioApi, "cadastrarPontoDeApoio").mockResolvedValue({
      id: "ponto-1",
      nome: "Sede",
      comunidade_virtual_id: COMUNIDADE.id,
      responsavel_id: null,
      ativo: true,
    });

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /novo ponto de apoio/i }));
    await usuario.type(screen.getByLabelText(/^nome$/i), "Sede");

    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() =>
      expect(pontosDeApoioApi.cadastrarPontoDeApoio).toHaveBeenCalledWith(
        { nome: "Sede", comunidade_id: COMUNIDADE.id },
        "token-do-admin",
      ),
    );

    expect(await screen.findByText("Sede")).toBeInTheDocument();
  });

  it("campo obrigatório em falta é apontado no campo, sem cadastrar nada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const cadastrarEspiado = vi.spyOn(pontosDeApoioApi, "cadastrarPontoDeApoio");

    render(
      <FormularioDePontoDeApoio
        comunidades={[COMUNIDADE]}
        onCriado={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(await screen.findByText(/informe o nome do ponto de apoio/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("ponto de apoio sem responsável é apresentado como informação, não como erro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [
        {
          id: "ponto-1",
          nome: "Sede",
          comunidade_virtual_id: COMUNIDADE.id,
          responsavel_id: null,
          ativo: true,
        },
      ],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    const semResponsavel = await screen.findByText(/sem responsável designado/i);
    expect(semResponsavel).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("Mestre não recebe o caminho de cadastro", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    await screen.findByText(/nenhum ponto de apoio cadastrado/i);
    expect(
      screen.queryByRole("button", { name: /novo ponto de apoio/i }),
    ).not.toBeInTheDocument();
  });
});
