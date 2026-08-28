import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AvisoDeColeta } from "./AvisoDeColeta";
import { ProvedorDeDireitos } from "./ContextoDeDireitos";
import { TelaDeDireitos } from "./TelaDeDireitos";

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

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("aviso de coleta", () => {
  it("não bloqueia a tela nem exige confirmação para continuar", () => {
    render(
      <ProvedorDeDireitos irParaDireitos={vi.fn()}>
        <AvisoDeColeta dado="o nome do Guerreiro(a)" />
      </ProvedorDeDireitos>,
    );

    expect(screen.getByText(/coleta o nome do guerreiro/i)).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("o acesso a partir do aviso chega na área Direitos e dados", async () => {
    const irParaDireitos = vi.fn();
    render(
      <ProvedorDeDireitos irParaDireitos={irParaDireitos}>
        <AvisoDeColeta dado="o nome do Guerreiro(a)" />
      </ProvedorDeDireitos>,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /ver em direitos e dados/i }));

    expect(irParaDireitos).toHaveBeenCalledTimes(1);
  });
});

describe("área Direitos e dados", () => {
  it("apresenta o destino de cada dado da tabela do PRD-02 §11", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    render(<TelaDeDireitos />);

    const linha = screen.getByRole("row", { name: /cadastro do guerreiro/i });
    expect(linha).toHaveTextContent("Identificação e operação");
    expect(linha).toHaveTextContent("Consentimento");
    expect(linha).toHaveTextContent("Gestão e responsável");

    expect(
      screen.getByRole("row", { name: /infração e pontuação negativa/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /solicitação de participação/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("row", { name: /solicitação de dados/i })).toBeInTheDocument();
  });

  it("declara que o dado do território é despersonalizado, não apagado", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    render(<TelaDeDireitos />);

    expect(screen.getByText(/despersonalizado quando revogado/i)).toBeInTheDocument();
    expect(screen.getByText(/não vê a imagem do guerreiro/i)).toBeInTheDocument();
    expect(screen.getByText(/exerce os direitos.*pela app 07/i)).toBeInTheDocument();
    expect(
      screen.getByText(/infração fica restrito à gestão e ao responsável/i),
    ).toBeInTheDocument();
  });

  it("é uma área de leitura, sem escrita, exclusão ou exportação", () => {
    configurarSessao(SESSAO_DE_ADMIN);
    render(<TelaDeDireitos />);

    expect(
      screen.queryByRole("button", { name: /excluir|exportar|editar|salvar/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });
});
