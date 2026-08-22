import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PoderDaLista } from "./api";
import * as poderesApi from "./api";
import { FormularioDePoder } from "./FormularioDePoder";
import { TelaDePoderes } from "./TelaDePoderes";

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
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
    ...sobrescreve,
  });
}

function poder(sobrescreve: Partial<PoderDaLista> = {}): PoderDaLista {
  return {
    id: "poder-1",
    nome: "Poder da Rima",
    descricao: "Expressão artística: rima, rap, batalhas de rima.",
    natureza: "de_guerreiro",
    vigencia: "vigente",
    papel: null,
    ativo: true,
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("catálogo de Poderes", () => {
  it("a lista mostra o poder desativado marcado como inativo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [poder({ ativo: false })],
      proximo_cursor: null,
    });

    render(<TelaDePoderes />);

    expect(await screen.findByText("Inativo")).toBeInTheDocument();
  });

  it("o cadastro envia natureza, vigência e papel ao núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "cadastrarPoder").mockResolvedValue(
      poder({ natureza: "derivado_do_aporte", vigencia: "ciclo_futuro", papel: "territorio" }),
    );

    render(<FormularioDePoder onSalvo={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Poder do Território");
    await usuario.type(screen.getByLabelText(/descrição/i), "Registro do território.");
    await usuario.selectOptions(screen.getByLabelText(/natureza/i), "derivado_do_aporte");
    await usuario.selectOptions(screen.getByLabelText(/vigência/i), "ciclo_futuro");
    await usuario.selectOptions(screen.getByLabelText(/^papel$/i), "territorio");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() =>
      expect(poderesApi.cadastrarPoder).toHaveBeenCalledWith(
        {
          nome: "Poder do Território",
          descricao: "Registro do território.",
          natureza: "derivado_do_aporte",
          vigencia: "ciclo_futuro",
          papel: "territorio",
        },
        "token-do-admin",
      ),
    );
  });

  it("nome em falta é apontado no campo, sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const cadastrarEspiado = vi.spyOn(poderesApi, "cadastrarPoder");

    render(<FormularioDePoder onSalvo={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(await screen.findByText(/informe o nome do poder/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("recusa por papel é explicada em linguagem simples", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(poderesApi, "cadastrarPoder").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "permissao_negada",
        mensagem: "O papel desta persona não autoriza esta operação.",
      }),
    );

    render(<FormularioDePoder onSalvo={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Poder da Rima");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(
      await screen.findByText(/só o admin cadastra, altera ou desativa poder do catálogo/i),
    ).toBeInTheDocument();
  });

  it("o segundo papel do Território é recusado com a mensagem do núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "cadastrarPoder").mockRejectedValue(
      new ErroDaApi(409, {
        codigo: "papel_do_poder_territorio_ja_declarado",
        mensagem: "Já existe um poder com o papel do Território declarado no catálogo.",
      }),
    );

    render(<FormularioDePoder onSalvo={vi.fn()} onCancelar={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^nome$/i), "Poder do Território (duplicado)");
    await usuario.selectOptions(screen.getByLabelText(/^papel$/i), "territorio");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(
      await screen.findByText(/já existe um poder com o papel do território declarado/i),
    ).toBeInTheDocument();
  });

  it("a desativação atualiza a linha do poder", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes")
      .mockResolvedValueOnce({ itens: [poder()], proximo_cursor: null })
      .mockResolvedValueOnce({ itens: [poder({ ativo: false })], proximo_cursor: null });
    vi.spyOn(poderesApi, "desativarPoder").mockResolvedValue(poder({ ativo: false }));

    render(<TelaDePoderes />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^desativar$/i }));
    await usuario.click(screen.getByRole("button", { name: /^confirmar desativação$/i }));

    await waitFor(() =>
      expect(poderesApi.desativarPoder).toHaveBeenCalledWith("poder-1", "token-do-admin"),
    );
    expect(await screen.findByText("Inativo")).toBeInTheDocument();
  });
});
