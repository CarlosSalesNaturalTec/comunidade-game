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

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
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

describe("aviso de coleta", () => {
  it("não bloqueia a tela nem exige confirmação para continuar", () => {
    render(
      <ProvedorDeDireitos irParaDireitos={vi.fn()}>
        <AvisoDeColeta dado="a presença do Guerreiro(a) na atividade" />
      </ProvedorDeDireitos>,
    );

    expect(screen.getByText(/coleta a presença do guerreiro/i)).toHaveAttribute(
      "role",
      "status",
    );
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("o acesso a partir do aviso chega na área Direitos e dados", async () => {
    const irParaDireitos = vi.fn();
    render(
      <ProvedorDeDireitos irParaDireitos={irParaDireitos}>
        <AvisoDeColeta dado="a presença do Guerreiro(a) na atividade" />
      </ProvedorDeDireitos>,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /ver em direitos e dados/i }));

    expect(irParaDireitos).toHaveBeenCalledTimes(1);
  });
});

describe("área Direitos e dados", () => {
  it("apresenta o destino de cada dado da tabela do PRD-09 §11", () => {
    configurarSessao(SESSAO_DE_MESTRE);
    render(<TelaDeDireitos />);

    const linha = screen.getByRole("row", { name: /artefatos comprobatórios do mestre/i });
    expect(linha).toHaveTextContent("Provar habilidade");
    expect(linha).toHaveTextContent("Consentimento");
    expect(linha).toHaveTextContent("Gestão e visitante");

    expect(
      screen.getByRole("row", { name: /conteúdo autoral do mestre/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /presença e resultado de atividade/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /pontuação negativa e motivo/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /criação original do guerreiro/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("row", { name: /contato do responsável/i })).toBeInTheDocument();
  });

  it("declara os pontos que a §11 traz em prosa", () => {
    configurarSessao(SESSAO_DE_MESTRE);
    render(<TelaDeDireitos />);

    expect(screen.getByText(/não vê a imagem real do guerreiro/i)).toBeInTheDocument();
    expect(
      screen.getByText(/criação original validada só vai à vitrine com autorização/i),
    ).toBeInTheDocument();
    expect(
      screen.getByText(/pontuação negativa fica restrita à gestão e ao responsável/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/chega pela app 07 e é tratado pela gestão/i)).toBeInTheDocument();
  });

  it("é uma área de leitura, sem escrita, exclusão ou exportação", () => {
    configurarSessao(SESSAO_DE_MESTRE);
    render(<TelaDeDireitos />);

    expect(
      screen.queryByRole("button", { name: /excluir|exportar|editar|salvar/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });
});
