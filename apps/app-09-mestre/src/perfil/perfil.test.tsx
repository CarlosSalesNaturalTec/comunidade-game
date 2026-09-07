import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as perfilApi from "./api";
import { TelaDoPerfil } from "./TelaDoPerfil";

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

const IDENTIDADE_VAZIA: perfilApi.IdentidadeDoMestre = { nick: null, avatar: null };

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

describe("identidade do Mestre", () => {
  it("mostra a ausência de nick e avatar quando ainda não definidos", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);

    render(<TelaDoPerfil />);

    expect(await screen.findByLabelText(/^nick$/i)).toHaveValue("");
    expect(screen.getByLabelText(/avatar \(endereço/i)).toHaveValue("");
  });

  it("mostra o nick e o avatar já gravados", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue({
      nick: "MestreDeTal",
      avatar: "https://exemplo.org/avatar.png",
    });
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);

    render(<TelaDoPerfil />);

    expect(await screen.findByLabelText(/^nick$/i)).toHaveValue("MestreDeTal");
  });

  it("grava o nick sem sugerir nenhum", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);
    const gravarEspiado = vi.spyOn(perfilApi, "gravarIdentidade").mockResolvedValue({
      nick: "MestreNovo",
      avatar: null,
    });

    render(<TelaDoPerfil />);
    const usuario = userEvent.setup();

    expect(await screen.findByLabelText(/^nick$/i)).toHaveValue("");
    await usuario.type(screen.getByLabelText(/^nick$/i), "MestreNovo");
    await usuario.click(screen.getByRole("button", { name: /gravar nick/i }));

    expect(gravarEspiado).toHaveBeenCalledWith({ nick: "MestreNovo" }, "token-do-mestre");
    expect(await screen.findByText(/nick gravado/i)).toBeInTheDocument();
  });

  it("grava o avatar sem condicionar a moeda alguma", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);
    const gravarEspiado = vi.spyOn(perfilApi, "gravarIdentidade").mockResolvedValue({
      nick: null,
      avatar: "https://exemplo.org/avatar.png",
    });

    render(<TelaDoPerfil />);
    const usuario = userEvent.setup();

    await usuario.type(
      await screen.findByLabelText(/avatar \(endereço/i),
      "https://exemplo.org/avatar.png",
    );
    await usuario.click(screen.getByRole("button", { name: /gravar avatar/i }));

    expect(gravarEspiado).toHaveBeenCalledWith(
      { avatar: "https://exemplo.org/avatar.png" },
      "token-do-mestre",
    );
    expect(await screen.findByText(/avatar gravado/i)).toBeInTheDocument();
    expect(screen.queryByText(/moeda/i)).not.toBeInTheDocument();
  });
});

describe("publicação de artefato", () => {
  it("mostra o aviso de coleta dos artefatos comprobatórios", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);

    render(<TelaDoPerfil />);

    expect(
      await screen.findByText(/coleta os artefatos que comprovam a sua habilidade/i),
    ).toHaveAttribute("role", "status");
  });

  it("publica por endereço e rótulo, sem campo de anexo", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);
    const declararEspiado = vi.spyOn(perfilApi, "declararArtefato").mockResolvedValue({
      id: "art-1",
      endereco: "https://exemplo.org/curriculo",
      rotulo: "Currículo",
      declarado_no_cadastro: false,
    });

    render(<TelaDoPerfil />);
    const usuario = userEvent.setup();

    expect(screen.queryByLabelText(/arquivo/i)).not.toBeInTheDocument();
    await screen.findByLabelText(/^rótulo$/i);

    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Currículo");
    await usuario.type(screen.getByLabelText(/^endereço$/i), "https://exemplo.org/curriculo");
    await usuario.click(screen.getByRole("button", { name: /publicar artefato/i }));

    expect(declararEspiado).toHaveBeenCalledWith(
      "mestre-1",
      { endereco: "https://exemplo.org/curriculo", rotulo: "Currículo" },
      "token-do-mestre",
    );
  });
});

describe("artefato do cadastro", () => {
  it("aparece marcado, sem caminho de remoção", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([
      {
        id: "art-cadastro",
        endereco: "https://exemplo.org/do-cadastro",
        rotulo: "Currículo do cadastro",
        declarado_no_cadastro: true,
      },
    ]);

    render(<TelaDoPerfil />);

    await screen.findByText(/currículo do cadastro/i);
    expect(screen.getByText(/declarado no cadastro/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /remover/i })).not.toBeInTheDocument();
  });

  it("o do cadastro oferece editar", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([
      {
        id: "art-cadastro",
        endereco: "https://exemplo.org/do-cadastro",
        rotulo: "Currículo do cadastro",
        declarado_no_cadastro: true,
      },
    ]);
    const editarEspiado = vi.spyOn(perfilApi, "editarArtefato").mockResolvedValue({
      id: "art-cadastro",
      endereco: "https://exemplo.org/corrigido",
      rotulo: "Currículo do cadastro",
      declarado_no_cadastro: true,
    });

    render(<TelaDoPerfil />);
    const usuario = userEvent.setup();

    await screen.findByText(/currículo do cadastro/i);
    await usuario.click(screen.getByRole("button", { name: /editar/i }));

    const formularioDeEdicao = screen.getByRole("form", { name: /editar artefato/i });
    const campoDeEndereco = within(formularioDeEdicao).getByLabelText(/^endereço$/i);
    await usuario.clear(campoDeEndereco);
    await usuario.type(campoDeEndereco, "https://exemplo.org/corrigido");
    await usuario.click(within(formularioDeEdicao).getByRole("button", { name: /^salvar$/i }));

    expect(editarEspiado).toHaveBeenCalledWith(
      "mestre-1",
      "art-cadastro",
      { endereco: "https://exemplo.org/corrigido", rotulo: "Currículo do cadastro" },
      "token-do-mestre",
    );
  });

  it("o Mestre remove o que ele mesmo publicou", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([
      {
        id: "art-proprio",
        endereco: "https://exemplo.org/proprio",
        rotulo: "Portfólio",
        declarado_no_cadastro: false,
      },
    ]);
    const removerEspiado = vi.spyOn(perfilApi, "removerArtefato").mockResolvedValue(undefined);

    render(<TelaDoPerfil />);
    const usuario = userEvent.setup();

    await screen.findByText(/portfólio/i);
    await usuario.click(screen.getByRole("button", { name: /remover/i }));

    expect(removerEspiado).toHaveBeenCalledWith("mestre-1", "art-proprio", "token-do-mestre");
  });
});

describe("cadastro de Mestre", () => {
  it("não oferece caminho de cadastro nem edição do próprio cadastro", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "lerIdentidade").mockResolvedValue(IDENTIDADE_VAZIA);
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);

    render(<TelaDoPerfil />);

    expect(await screen.findByText(/ato exclusivo de admin/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/^nome$/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/^e-mail$/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/^papel$/i)).not.toBeInTheDocument();
  });
});
