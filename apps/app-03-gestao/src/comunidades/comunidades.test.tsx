import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as comunidadesApi from "./api";
import { FormularioDeComunidade } from "./FormularioDeComunidade";
import { TelaDeComunidades } from "./TelaDeComunidades";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

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

function configurarSessao(
  sessao: SessaoAberta | null,
  sobrescreve: Record<string, unknown> = {},
) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
    ...sobrescreve,
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cadastro de Comunidade Virtual", () => {
  it("Admin cria a comunidade com os três campos e ela aparece entre as existentes", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades")
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null, ciclo_rotulo: "2026" })
      .mockResolvedValueOnce({
        itens: [
          {
            id: "1",
            nome: "Comunidade Nova",
            localizacao: "Bairro Novo",
            series_abertas: null,
            series_ativas: null,
            registros_validos: null,
            continuidade: null,
          },
        ],
        proximo_cursor: null,
        ciclo_rotulo: "2026",
      });
    vi.spyOn(comunidadesApi, "criarComunidade").mockResolvedValue({
      id: "1",
      nome: "Comunidade Nova",
      localizacao: "Bairro Novo",
      granularidade_maxima: "bairro",
    });

    render(<TelaDeComunidades />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova comunidade/i }));
    await usuario.type(screen.getByLabelText(/^nome$/i), "Comunidade Nova");
    await usuario.type(screen.getByLabelText(/localização/i), "Bairro Novo");
    await usuario.type(screen.getByLabelText(/granularidade máxima/i), "bairro");
    await usuario.click(screen.getByRole("button", { name: /^criar$/i }));

    await waitFor(() =>
      expect(comunidadesApi.criarComunidade).toHaveBeenCalledWith(
        {
          nome: "Comunidade Nova",
          localizacao: "Bairro Novo",
          granularidade_maxima: "bairro",
        },
        "token-do-admin",
      ),
    );

    expect(await screen.findByText("Comunidade Nova")).toBeInTheDocument();
  });

  it("comunidade recém-criada aparece listada sem indicadores do território", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [
        {
          id: "1",
          nome: "Comunidade Nova",
          localizacao: "Bairro Novo",
          series_abertas: null,
          series_ativas: null,
          registros_validos: null,
          continuidade: null,
        },
      ],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });

    render(<TelaDeComunidades />);

    expect(
      await screen.findByText(/ainda sem indicadores do território/i),
    ).toBeInTheDocument();
  });

  it("a ausência de indicadores é informação, nunca aviso de erro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [
        {
          id: "1",
          nome: "Comunidade Nova",
          localizacao: "Bairro Novo",
          series_abertas: null,
          series_ativas: null,
          registros_validos: null,
          continuidade: null,
        },
      ],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });

    render(<TelaDeComunidades />);

    const indicadoresAusentes = await screen.findByText(
      /ainda sem indicadores do território/i,
    );
    expect(indicadoresAusentes).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("campo obrigatório em falta é apontado no campo, sem criar nada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const criarComunidadeEspiado = vi.spyOn(comunidadesApi, "criarComunidade");

    render(<FormularioDeComunidade onCriada={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Comunidade Nova");
    await usuario.click(screen.getByRole("button", { name: /^criar$/i }));

    expect(await screen.findByText(/informe a localização/i)).toBeInTheDocument();
    expect(criarComunidadeEspiado).not.toHaveBeenCalled();
  });

  it("erro de campo é anunciado no próprio campo, alcançado depois que surgiu", async () => {
    configurarSessao(SESSAO_DE_ADMIN);

    render(<FormularioDeComunidade onCriada={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Comunidade Nova");
    await usuario.click(screen.getByRole("button", { name: /^criar$/i }));
    await screen.findByText(/informe a localização/i);

    const campoDeLocalizacao = screen.getByLabelText(/localização/i);
    expect(campoDeLocalizacao).toHaveAccessibleDescription(/informe a localização/i);
    expect(campoDeLocalizacao).toHaveAttribute("aria-invalid", "true");
  });

  it("recusa por papel é explicada em linguagem simples", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "criarComunidade").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "permissao_negada",
        mensagem: "O papel desta persona não autoriza esta operação.",
      }),
    );

    render(<FormularioDeComunidade onCriada={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Comunidade Nova");
    await usuario.type(screen.getByLabelText(/localização/i), "Bairro Novo");
    await usuario.type(screen.getByLabelText(/granularidade máxima/i), "bairro");
    await usuario.click(screen.getByRole("button", { name: /^criar$/i }));

    expect(await screen.findByText(/só o admin cria comunidade virtual/i)).toBeInTheDocument();
  });

  it("o caminho de criação não é oferecido a quem não é Admin", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });

    render(<TelaDeComunidades />);

    await screen.findByText(/nenhuma comunidade virtual cadastrada/i);
    expect(screen.queryByRole("button", { name: /nova comunidade/i })).not.toBeInTheDocument();
  });

  it("todo elemento acionável recebe foco visível na travessia pelo teclado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });

    render(<TelaDeComunidades />);
    const usuario = userEvent.setup();
    await screen.findByText(/nenhuma comunidade virtual cadastrada/i);

    await usuario.tab();
    expect(screen.getByRole("button", { name: /sair/i })).toHaveFocus();

    await usuario.tab();
    expect(screen.getByRole("button", { name: /nova comunidade/i })).toHaveFocus();
  });
});
