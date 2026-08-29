import { render, screen } from "@testing-library/react";
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

describe("publicação de artefato", () => {
  it("mostra o aviso de coleta dos artefatos comprobatórios", async () => {
    configurarSessao();
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);

    render(<TelaDoPerfil />);

    expect(
      await screen.findByText(/coleta os artefatos que comprovam a sua habilidade/i),
    ).toHaveAttribute("role", "status");
  });

  it("publica por endereço e rótulo, sem campo de anexo", async () => {
    configurarSessao();
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
    await screen.findByLabelText(/rótulo/i);

    await usuario.type(screen.getByLabelText(/rótulo/i), "Currículo");
    await usuario.type(screen.getByLabelText(/endereço/i), "https://exemplo.org/curriculo");
    await usuario.click(screen.getByRole("button", { name: /publicar artefato/i }));

    expect(declararEspiado).toHaveBeenCalledWith(
      "mestre-1",
      { endereco: "https://exemplo.org/curriculo", rotulo: "Currículo" },
      "token-do-mestre",
    );
  });
});

describe("artefato do cadastro", () => {
  it("aparece marcado e sem caminho de remoção", async () => {
    configurarSessao();
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

  it("o Mestre remove o que ele mesmo publicou", async () => {
    configurarSessao();
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
    vi.spyOn(perfilApi, "listarArtefatos").mockResolvedValue([]);

    render(<TelaDoPerfil />);

    expect(await screen.findByText(/ato exclusivo de admin/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/^nome$/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/^e-mail$/i)).not.toBeInTheDocument();
  });
});
