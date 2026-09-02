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

const SESSAO_DE_APOIADOR: SessaoAberta = {
  token: "token-do-apoiador",
  papel: "apoiador",
  permissoes: {},
  persona_id: "apoiador-1",
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
        <AvisoDeColeta dado="o comprovante da transferência" />
      </ProvedorDeDireitos>,
    );

    expect(screen.getByText(/coleta o comprovante da transferência/i)).toHaveAttribute(
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
        <AvisoDeColeta dado="o comprovante da transferência" />
      </ProvedorDeDireitos>,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /ver em direitos e dados/i }));

    expect(irParaDireitos).toHaveBeenCalledTimes(1);
  });
});

describe("área Direitos e dados", () => {
  it("apresenta o destino e o uso de cada dado da tabela do PRD-14 §11", () => {
    configurarSessao(SESSAO_DE_APOIADOR);
    render(<TelaDeDireitos />);

    const linha = screen.getByRole("row", { name: /nome ou razão social/i });
    expect(linha).toHaveTextContent("Identificar o Apoiador e o aporte");
    expect(linha).toHaveTextContent("Consentimento");
    expect(linha).toHaveTextContent("Gestão e público (nick)");

    expect(screen.getByRole("row", { name: /^e-mail /i })).toBeInTheDocument();
    expect(screen.getByRole("row", { name: /whatsapp/i })).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /comprovante de transferência/i }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /documentos comprobatórios/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("row", { name: /avatar e nick/i })).toBeInTheDocument();
    expect(
      screen.getByRole("row", { name: /perfil pessoa física ou jurídica/i }),
    ).toBeInTheDocument();
    expect(screen.getByRole("row", { name: /justificativa do vínculo/i })).toBeInTheDocument();
    expect(screen.getByRole("row", { name: /proposta registrada/i })).toBeInTheDocument();
  });

  it("declara que os direitos correm pela gestão", () => {
    configurarSessao(SESSAO_DE_APOIADOR);
    render(<TelaDeDireitos />);

    expect(
      screen.getByText(/pedido de acesso, correção ou exclusão de dado é feito à gestão/i),
    ).toBeInTheDocument();
  });

  it("a ação de sair só aparece com sessão", () => {
    configurarSessao(null);
    render(<TelaDeDireitos />);

    expect(screen.queryByRole("button", { name: /^sair$/i })).not.toBeInTheDocument();
  });

  it("é uma área de leitura, sem escrita, exclusão ou exportação", () => {
    configurarSessao(SESSAO_DE_APOIADOR);
    render(<TelaDeDireitos />);

    expect(
      screen.queryByRole("button", { name: /excluir|exportar|editar|salvar/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });
});
