import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { TipoDeRecurso } from "../recursos/api";
import * as recursosApi from "../recursos/api";
import type { PendenciaDeEntrega } from "./api";
import * as recompensasApi from "./api";
import { FilaDeEntregasPendentes } from "./FilaDeEntregasPendentes";

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

function pendencia(sobrescreve: Partial<PendenciaDeEntrega> = {}): PendenciaDeEntrega {
  return {
    guerreiro_id: "guerreiro-1",
    guerreiro_nick: "Guerreira10",
    guerreiro_avatar: "avatar-3",
    trilha_id: "trilha-1",
    trilha_nome: "Robô Educa",
    missao_id: "missao-1",
    missao_titulo: "Missão marco",
    recompensa_de_marco_id: "recompensa-1",
    tipo_de_recurso_id: "tipo-1",
    quantidade: "1",
    ...sobrescreve,
  };
}

function tipoDeRecurso(): TipoDeRecurso {
  return {
    id: "tipo-1",
    nome: "Camisa",
    natureza: "duravel",
    unidade: "unidade",
    exige_comprovante: false,
    finalidade: "recompensa" as const,
    ativo: true,
    valor_em_moedas: "10.00",
    vigencia_inicio: "2026-01-01",
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Fila de entregas pendentes", () => {
  it("mostra quem conquistou e ainda não recebeu, sem valor em moedas ou reais", async () => {
    configurarSessao();
    vi.spyOn(recompensasApi, "listarEntregasPendentes").mockResolvedValue([pendencia()]);
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([tipoDeRecurso()]);

    render(<FilaDeEntregasPendentes />);

    expect(await screen.findByText("Guerreira10", { exact: false })).toBeInTheDocument();
    expect(screen.getByText(/robô educa/i)).toBeInTheDocument();
    expect(screen.getByText(/1 camisa/i)).toBeInTheDocument();
    expect(screen.queryByText(/moeda/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/real/i)).not.toBeInTheDocument();
  });

  it("desenha o avatar ao lado do nick, sem o texto do campo (RF-09-75, RN-09-18)", async () => {
    configurarSessao();
    const avatarEmTexto = JSON.stringify({
      formaDeTratamento: "guerreira",
      avatar: { v: 1, fundo: "acao-100", tom: "t5", cabelo: "black-power" },
    });
    vi.spyOn(recompensasApi, "listarEntregasPendentes").mockResolvedValue([
      pendencia({ guerreiro_avatar: avatarEmTexto }),
    ]);
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([tipoDeRecurso()]);

    const { container } = render(<FilaDeEntregasPendentes />);

    expect(await screen.findByText("Guerreira10")).toBeInTheDocument();
    expect(container.textContent).not.toMatch(/formaDeTratamento|black-power/);
    expect(container.querySelector("svg")).not.toBeNull();
  });

  it("a entrega confirmada sai da fila", async () => {
    configurarSessao();
    vi.spyOn(recompensasApi, "listarEntregasPendentes").mockResolvedValue([pendencia()]);
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([tipoDeRecurso()]);
    vi.spyOn(recompensasApi, "registrarEntrega").mockResolvedValue({
      id: "entrega-1",
      recompensa_de_marco_id: "recompensa-1",
      missao_id: "missao-1",
      trilha_id: "trilha-1",
      tipo_de_recurso_id: "tipo-1",
      quantidade: "1",
      guerreiro_id: "guerreiro-1",
      ponto_de_apoio_id: "ponto-1",
      lancamento_id: "lancamento-1",
      autor_id: "mestre-1",
      registrado_em: "2026-08-29T10:00:00-03:00",
    });

    render(<FilaDeEntregasPendentes />);
    const usuario = userEvent.setup();

    await screen.findByText("Guerreira10", { exact: false });
    await usuario.click(screen.getByRole("button", { name: /confirmar entrega/i }));

    await waitFor(() =>
      expect(recompensasApi.registrarEntrega).toHaveBeenCalledWith(
        "recompensa-1",
        { guerreiro_id: "guerreiro-1" },
        "token-do-mestre",
      ),
    );
    await waitFor(() =>
      expect(screen.queryByText("Guerreira10", { exact: false })).not.toBeInTheDocument(),
    );
  });

  it("a confirmação não pede o ponto de apoio", async () => {
    // O núcleo tira o recurso da aula imediatamente anterior da comunidade
    // (`RF-09-76`, `RF-07-13`).
    configurarSessao();
    vi.spyOn(recompensasApi, "listarEntregasPendentes").mockResolvedValue([pendencia()]);
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([tipoDeRecurso()]);

    render(<FilaDeEntregasPendentes />);

    await screen.findByText("Guerreira10", { exact: false });
    expect(screen.queryByLabelText(/ponto de apoio/i)).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /confirmar entrega/i })).toBeInTheDocument();
  });

  it("a recusa da entrega é traduzida em linguagem simples", async () => {
    configurarSessao();
    vi.spyOn(recompensasApi, "listarEntregasPendentes").mockResolvedValue([pendencia()]);
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([tipoDeRecurso()]);
    vi.spyOn(recompensasApi, "registrarEntrega").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Lastro insuficiente no ponto de apoio informado para esta entrega.",
      }),
    );

    render(<FilaDeEntregasPendentes />);
    const usuario = userEvent.setup();

    await screen.findByText("Guerreira10", { exact: false });
    await usuario.click(screen.getByRole("button", { name: /confirmar entrega/i }));

    expect(await screen.findByText(/lastro insuficiente/i)).toBeInTheDocument();
  });
});
