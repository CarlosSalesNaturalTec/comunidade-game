import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as responsaveisApi from "./api";
import { TelaDeResponsaveis } from "./TelaDeResponsaveis";

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

const GUERREIRO = { id: "guerreiro-1", nick: "guerreira-teste", avatar: "avatar-1" };

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cadastro do responsável", () => {
  it("declara que o cadastro pressupõe a apresentação presencial", () => {
    configurarSessao();
    render(<TelaDeResponsaveis />);

    expect(screen.getByText(/apresentou pessoalmente/i)).toBeInTheDocument();
  });

  it("recusa o cadastro sem nome", async () => {
    configurarSessao();
    const cadastrarEspiado = vi.spyOn(responsaveisApi, "cadastrarResponsavel");
    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));

    expect(await screen.findByText(/informe o nome/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });
});

describe("vínculo com Guerreiro(a)", () => {
  it("escolhe o Guerreiro(a) por nick e avatar, e exige o grau de parentesco", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    const criarVinculoEspiado = vi.spyOn(responsaveisApi, "criarVinculo");

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    const opcao = await screen.findByRole("option", { name: /guerreira-teste — avatar-1/i });
    expect(opcao).toBeInTheDocument();
    expect(screen.queryByRole("img")).not.toBeInTheDocument();

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));
    expect(await screen.findByText(/informe o grau de parentesco/i)).toBeInTheDocument();
    expect(criarVinculoEspiado).not.toHaveBeenCalled();
  });

  it("cria dois vínculos, cada um com o seu grau de parentesco", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO, { id: "guerreiro-2", nick: "guerreiro-dois", avatar: "avatar-2" }],
      proximo_cursor: null,
    });
    vi.spyOn(responsaveisApi, "criarVinculo")
      .mockResolvedValueOnce({
        id: "v1",
        responsavel_id: "resp-1",
        guerreiro_id: "guerreiro-1",
        grau_de_parentesco: "mãe",
        inicio: "2026-08-29T10:00:00-03:00",
      })
      .mockResolvedValueOnce({
        id: "v2",
        responsavel_id: "resp-1",
        guerreiro_id: "guerreiro-2",
        grau_de_parentesco: "tia",
        inicio: "2026-08-29T10:05:00-03:00",
      });

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "mãe");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));
    await screen.findByText("mãe");

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), "guerreiro-2");
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tia");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText("tia")).toBeInTheDocument();
    expect(screen.getByText("mãe")).toBeInTheDocument();
  });

  it("o quarto vínculo é recusado com o teto de três, sem perder o que já foi criado", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [GUERREIRO],
      proximo_cursor: null,
    });
    vi.spyOn(responsaveisApi, "criarVinculo").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este Guerreiro(a) já tem três responsáveis vigentes.",
        campo: "guerreiro_id",
      }),
    );

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    await usuario.selectOptions(screen.getByLabelText(/^guerreiro\(a\)$/i), GUERREIRO.id);
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "tio");
    await usuario.click(screen.getByRole("button", { name: /^vincular$/i }));

    expect(await screen.findByText(/três responsáveis vigentes/i)).toBeInTheDocument();
    expect(screen.getByText(/responsável cadastrado/i)).toBeInTheDocument();
  });
});

describe("credencial provisória", () => {
  it("mostra a senha provisória uma vez, sem caminho para recuperá-la", async () => {
    configurarSessao();
    vi.spyOn(responsaveisApi, "cadastrarResponsavel").mockResolvedValue({
      id: "resp-1",
      nome: "Maria",
    });
    vi.spyOn(responsaveisApi, "listarGuerreirosVinculaveis").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(responsaveisApi, "criarCredencialProvisoria").mockResolvedValue({
      id: "cred-1",
      usuario: "maria",
      senha_provisoria: "abc123",
    });

    render(<TelaDeResponsaveis />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /cadastrar responsável/i }));
    await screen.findByText(/responsável cadastrado/i);

    await usuario.type(screen.getByLabelText(/usuário \(para quem/i), "maria");
    await usuario.click(screen.getByRole("button", { name: /criar credencial provisória/i }));

    expect(await screen.findByText(/abc123/)).toBeInTheDocument();
    expect(screen.getByText(/não aparece de novo/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /criar credencial provisória/i }),
    ).not.toBeInTheDocument();
  });
});
