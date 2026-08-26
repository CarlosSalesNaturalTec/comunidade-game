import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as encerramentoApi from "./api";
import { TelaDeEncerramentoDeCiclo } from "./TelaDeEncerramentoDeCiclo";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
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

describe("encerramento do ciclo", () => {
  it("pede confirmação, enunciando os dois efeitos, antes de executar", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const encerrarEspiado = vi.spyOn(encerramentoApi, "encerrarCiclo");

    render(<TelaDeEncerramentoDeCiclo />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /encerrar ciclo/i }));

    const aviso = screen.getByText(/apaga o motivo/i);
    expect(aviso.textContent).toMatch(/ranking/i);
    expect(encerrarEspiado).not.toHaveBeenCalled();
  });

  it("desistir não executa nada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const encerrarEspiado = vi.spyOn(encerramentoApi, "encerrarCiclo");

    render(<TelaDeEncerramentoDeCiclo />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /encerrar ciclo/i }));
    await usuario.click(screen.getByRole("button", { name: /^voltar$/i }));

    expect(screen.getByRole("button", { name: /encerrar ciclo/i })).toBeInTheDocument();
    expect(encerrarEspiado).not.toHaveBeenCalled();
  });

  it("confirmado, executa o ato e exibe o resultado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(encerramentoApi, "encerrarCiclo").mockResolvedValue({
      ocorrencias_expurgadas: 3,
    });

    render(<TelaDeEncerramentoDeCiclo />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /encerrar ciclo/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar encerramento/i }));

    expect(encerramentoApi.encerrarCiclo).toHaveBeenCalledWith("token-do-admin");
    expect(await screen.findByText(/3.*ocorrências de conduta tiveram/i)).toBeInTheDocument();
  });

  it("a tela não oferece campo, opção nem etapa para declarar o ciclo seguinte", async () => {
    configurarSessao(SESSAO_DE_ADMIN);

    render(<TelaDeEncerramentoDeCiclo />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /encerrar ciclo/i }));

    // Nenhum campo de formulário existe nesta tela — o único insumo é a
    // confirmação, e o ciclo seguinte é declaração à parte na implantação.
    expect(screen.queryAllByRole("textbox")).toHaveLength(0);
    expect(screen.queryAllByRole("combobox")).toHaveLength(0);
    expect(
      screen.queryByRole("button", { name: /pr[oó]ximo ciclo|declarar ciclo/i }),
    ).not.toBeInTheDocument();
  });

  it("quem não é Admin recebe a recusa, sem alcançar a confirmação", async () => {
    configurarSessao({
      token: "token-do-mestre",
      papel: "mestre",
      permissoes: {},
      persona_id: "mestre-1",
    });

    render(<TelaDeEncerramentoDeCiclo />);

    expect(await screen.findByText(/só o admin encerra o ciclo/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /encerrar ciclo/i })).not.toBeInTheDocument();
  });

  it("recusa do núcleo é lida em linguagem simples", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(encerramentoApi, "encerrarCiclo").mockRejectedValue(
      new ErroDaApi(403, { codigo: "permissao_negada", mensagem: "Sem permissão." }),
    );

    render(<TelaDeEncerramentoDeCiclo />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /encerrar ciclo/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar encerramento/i }));

    expect(await screen.findByText(/só o admin encerra o ciclo/i)).toBeInTheDocument();
  });
});
