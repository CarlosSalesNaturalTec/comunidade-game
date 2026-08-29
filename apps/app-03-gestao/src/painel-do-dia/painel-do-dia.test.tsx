import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PainelDoDia } from "./api";
import * as painelApi from "./api";
import { TelaDoPainelDoDia } from "./TelaDoPainelDoDia";

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

function painelVazio(): PainelDoDia {
  return {
    aula_id: null,
    comunidade_virtual_id: null,
    ponto_de_apoio_id: null,
    presencas: [],
    aguardando_aparelho: [],
    equipes: [],
    atividades_previstas: [],
    recursos_providos: [],
    saldo_do_ponto_de_apoio: [],
    pendencias: [],
  };
}

function painelDoEncontro(sobrescreve: Partial<PainelDoDia> = {}): PainelDoDia {
  return {
    aula_id: "aula-1",
    comunidade_virtual_id: "comunidade-1",
    ponto_de_apoio_id: "ponto-1",
    presencas: [
      {
        id: "presenca-1",
        guerreiro_id: "guerreiro-1",
        avatar: null,
        nick: "zeferina",
        modo: "reconhecimento",
        confirmador_id: null,
      },
    ],
    aguardando_aparelho: [{ guerreiro_id: "guerreiro-2", avatar: null, nick: "tais" }],
    equipes: [
      {
        id: "equipe-1",
        integrantes: [{ avatar: null, nick: "zeferina" }],
        missao_id: "missao-1",
        missao_titulo: "Montagem do robô",
      },
    ],
    atividades_previstas: [
      {
        id: "atividade-1",
        titulo: "Montagem",
        missao_id: "missao-1",
        missao_titulo: "Montagem do robô",
      },
    ],
    recursos_providos: [{ tipo_de_recurso_id: "tipo-1", quantidade: "2.00" }],
    saldo_do_ponto_de_apoio: [{ tipo_de_recurso_id: "tipo-1", saldo: "5.00" }],
    pendencias: [
      {
        tipo: "lancamento_da_atividade_realizada",
        guerreiro_id: null,
        nick: null,
        consentimento_id: null,
      },
    ],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.useRealTimers();
});

describe("Painel do dia (RF-02-41 a RF-02-48, RF-02-68, RF-02-69)", () => {
  it("mostra o encontro em andamento com presenças, espera, equipes, previsto, saldo e pendências", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());

    render(<TelaDoPainelDoDia />);

    expect((await screen.findAllByText(/zeferina/)).length).toBeGreaterThan(0);
    expect(screen.getByText(/tais/)).toBeInTheDocument();
    expect(screen.getAllByText(/montagem do robô/i).length).toBeGreaterThan(0);
    expect(screen.getByText(/falta lançar a atividade realizada/i)).toBeInTheDocument();
  });

  it("fora da janela de qualquer aula, diz que não há encontro em andamento", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelVazio());

    render(<TelaDoPainelDoDia />);

    expect(await screen.findByText(/não há encontro em andamento/i)).toBeInTheDocument();
  });

  it("a tela não oferece caminho de escrita além do anexo da pendência", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());

    render(<TelaDoPainelDoDia />);
    await screen.findAllByText(/zeferina/);

    expect(
      screen.queryByRole("button", { name: /lançar|confirmar presença|editar/i }),
    ).not.toBeInTheDocument();
  });

  it("atualiza sozinha por sondagem", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    configurarSessao(SESSAO_DE_ADMIN);
    const espiado = vi
      .spyOn(painelApi, "obterPainelDoDia")
      .mockResolvedValueOnce(painelVazio())
      .mockResolvedValue(painelDoEncontro());

    render(<TelaDoPainelDoDia />);
    await waitFor(() => expect(espiado).toHaveBeenCalledTimes(1));

    await vi.advanceTimersByTimeAsync(10000);
    await waitFor(() => expect(espiado).toHaveBeenCalledTimes(2));
  });

  it("sem rede, o painel avisa e não apaga o que já carregou", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia")
      .mockResolvedValueOnce(painelDoEncontro())
      .mockRejectedValueOnce(new Error("falha de rede"));

    render(<TelaDoPainelDoDia />);
    await screen.findAllByText(/zeferina/);

    await vi.advanceTimersByTimeAsync(10000);

    expect(await screen.findByText(/perdemos contato com o núcleo/i)).toBeInTheDocument();
    expect(screen.getAllByText(/zeferina/).length).toBeGreaterThan(0);
  });

  it("o Admin anexa a digitalização a partir da pendência", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const consultar = vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(
      painelDoEncontro({
        pendencias: [
          {
            tipo: "digitalizacao_do_termo",
            guerreiro_id: "guerreiro-1",
            nick: "zeferina",
            consentimento_id: "consentimento-1",
          },
        ],
      }),
    );
    const anexar = vi.spyOn(painelApi, "anexarDigitalizacaoDoTermo").mockResolvedValue({
      id: "anexo-1",
      consentimento_id: "consentimento-1",
      registrado_em: "2026-08-25T14:00:00-03:00",
    });

    render(<TelaDoPainelDoDia />);
    await screen.findByLabelText(/anexar digitalização/i);

    const arquivo = new File(["conteudo"], "termo.pdf", { type: "application/pdf" });
    const usuario = userEvent.setup();
    await usuario.upload(screen.getByLabelText(/anexar digitalização/i), arquivo);

    await waitFor(() =>
      expect(anexar).toHaveBeenCalledWith("consentimento-1", arquivo, "token-do-admin"),
    );
    expect(await screen.findByText(/digitalização anexada/i)).toBeInTheDocument();
    expect(consultar).toHaveBeenCalled();
  });

  it("mostra o aviso de coleta da digitalização do termo, sem bloquear o anexo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(
      painelDoEncontro({
        pendencias: [
          {
            tipo: "digitalizacao_do_termo",
            guerreiro_id: "guerreiro-1",
            nick: "zeferina",
            consentimento_id: "consentimento-1",
          },
        ],
      }),
    );

    render(<TelaDoPainelDoDia />);
    await screen.findByLabelText(/anexar digitalização/i);

    expect(screen.getByText(/digitalização do termo assinado no encontro/i)).toHaveAttribute(
      "role",
      "status",
    );
  });

  it("recusa de formato é explicada em linguagem simples", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(
      painelDoEncontro({
        pendencias: [
          {
            tipo: "digitalizacao_do_termo",
            guerreiro_id: "guerreiro-1",
            nick: "zeferina",
            consentimento_id: "consentimento-1",
          },
        ],
      }),
    );
    vi.spyOn(painelApi, "anexarDigitalizacaoDoTermo").mockRejectedValue(
      new ErroDaApi(422, { codigo: "erro_de_validacao", mensagem: "Formato inválido." }),
    );

    render(<TelaDoPainelDoDia />);
    await screen.findByLabelText(/anexar digitalização/i);

    // O seletor do sistema já filtra pelo `accept` do campo; o núcleo é
    // quem confere o conteúdo de verdade e pode recusar mesmo um arquivo
    // que passou pelo seletor (`RF-02-68`) — o mock reproduz essa recusa.
    const arquivo = new File(["conteudo"], "termo.pdf", { type: "application/pdf" });
    const usuario = userEvent.setup();
    await usuario.upload(screen.getByLabelText(/anexar digitalização/i), arquivo);

    expect(
      await screen.findByText(/envie a digitalização em pdf, jpg ou png/i),
    ).toBeInTheDocument();
  });

  it("o Mestre não recebe o caminho de anexar", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(
      painelDoEncontro({
        pendencias: [
          {
            tipo: "digitalizacao_do_termo",
            guerreiro_id: "guerreiro-1",
            nick: "zeferina",
            consentimento_id: "consentimento-1",
          },
        ],
      }),
    );

    render(<TelaDoPainelDoDia />);
    await screen.findByText(/termo de biometria assinado/i);

    expect(screen.queryByLabelText(/anexar digitalização/i)).not.toBeInTheDocument();
  });
});
