import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AtividadeDoMestre, AulaDaTurma, MinhasTurmas, OcorrenciaDeConduta } from "./api";
import * as turmasApi from "./api";
import { TelaDeMinhasTurmas } from "./TelaDeMinhasTurmas";

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
  });
}

function aula(sobrescreve: Partial<AulaDaTurma> = {}): AulaDaTurma {
  return {
    id: "aula-1",
    comunidade_virtual_id: "comunidade-1",
    ponto_de_apoio_id: "ponto-1",
    inicio_em: "2026-08-01T10:00:00-03:00",
    fim_em: "2026-08-01T12:00:00-03:00",
    situacao: "confirmada",
    cancelamento_motivo: null,
    recursos_faltantes: [],
    ...sobrescreve,
  };
}

function atividade(sobrescreve: Partial<AtividadeDoMestre> = {}): AtividadeDoMestre {
  return {
    id: "atividade-1",
    missao_id: "missao-1",
    titulo: "Montagem do robô",
    formato: "presencial",
    modalidade: "individual",
    aula_id: null,
    ...sobrescreve,
  };
}

function turmas(sobrescreve: Partial<MinhasTurmas> = {}): MinhasTurmas {
  return {
    itens: [aula()],
    proximo_cursor: null,
    atividades_presenciais: [atividade()],
    atividades_on_line: [],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("lista das turmas do Mestre (RF-09-42, RF-09-73)", () => {
  it("lista as aulas e as atividades presenciais e on-line separadas", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({
        atividades_presenciais: [atividade({ id: "presencial-1", titulo: "Oficina" })],
        atividades_on_line: [
          atividade({ id: "on-line-1", titulo: "Fórum", formato: "on_line_assincrona" }),
        ],
      }),
    );

    render(<TelaDeMinhasTurmas />);

    expect(await screen.findByText("Oficina")).toBeInTheDocument();
    expect(screen.getByText("Fórum")).toBeInTheDocument();
  });

  it("turma sem aula nem atividade mostra o estado vazio", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [], atividades_presenciais: [], atividades_on_line: [] }),
    );

    render(<TelaDeMinhasTurmas />);

    expect(await screen.findByText(/nenhuma aula agendada/i)).toBeInTheDocument();
    expect(screen.getByText(/nenhuma atividade presencial sua/i)).toBeInTheDocument();
    expect(screen.getByText(/nenhuma atividade on-line sua/i)).toBeInTheDocument();
  });
});

describe("lançamento da atividade (RF-09-43, RF-09-44, RF-09-74)", () => {
  async function abrirTelaDeLancamento() {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(turmas());

    render(<TelaDeMinhasTurmas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /presença e ocorrência/i }));
    await usuario.click(await screen.findByRole("button", { name: /^lançar$/i }));
    return usuario;
  }

  it("o Mestre lança vários participantes num só envio", async () => {
    const usuario = await abrirTelaDeLancamento();
    const lancarEspiado = vi
      .spyOn(turmasApi, "lancarResultadosDaAtividade")
      .mockResolvedValue([]);

    await usuario.click(
      await screen.findByRole("button", { name: /adicionar participante/i }),
    );

    const identificadores = screen.getAllByLabelText(/identificador do guerreiro/i);
    await usuario.type(identificadores[0], "guerreiro-1");
    await usuario.type(identificadores[1], "guerreiro-2");

    await usuario.click(screen.getByRole("button", { name: /^lançar$/i }));

    await waitFor(() => expect(lancarEspiado).toHaveBeenCalled());
    const [, , participantes] = lancarEspiado.mock.calls[0];
    expect(participantes).toHaveLength(2);
    expect(participantes.map((p) => p.guerreiro_id)).toEqual(["guerreiro-1", "guerreiro-2"]);
    expect(await screen.findByText(/lançamento registrado/i)).toBeInTheDocument();
  });

  it("a recusa do núcleo chega em linguagem simples (RN-09-16)", async () => {
    const usuario = await abrirTelaDeLancamento();
    vi.spyOn(turmasApi, "lancarResultadosDaAtividade").mockRejectedValue(
      new ErroDaApi(403, { codigo: "permissao_negada", mensagem: "Só o Mestre autor lança." }),
    );

    await usuario.click(screen.getByRole("button", { name: /^lançar$/i }));

    expect(await screen.findByText(/só o mestre autor lança/i)).toBeInTheDocument();
  });
});

describe("presença e ocorrência de conduta (RF-09-45, RF-09-46)", () => {
  async function abrirTelaDaAula() {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(turmas());

    render(<TelaDeMinhasTurmas />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /presença e ocorrência/i }));
    return usuario;
  }

  it("o Mestre confirma a presença que faltou", async () => {
    const usuario = await abrirTelaDaAula();
    const confirmarEspiado = vi.spyOn(turmasApi, "confirmarPresenca").mockResolvedValue({
      id: "presenca-1",
      aula_id: "aula-1",
      guerreiro_id: "guerreiro-1",
      modo: "confirmacao",
      confirmador_id: "mestre-1",
      momento_do_fato: "2026-08-01T10:00:00-03:00",
    });

    const identificadores = screen.getAllByLabelText(/identificador do guerreiro/i);
    await usuario.type(identificadores[0], "guerreiro-1");
    const campoDeData = screen.getByLabelText(/momento em que esteve presente/i);
    await usuario.type(campoDeData, "2026-08-01T10:00");

    await usuario.click(screen.getByRole("button", { name: /^confirmar presença$/i }));

    await waitFor(() => expect(confirmarEspiado).toHaveBeenCalled());
    expect(await screen.findByText(/presença confirmada/i)).toBeInTheDocument();
  });

  it("a ocorrência exige o motivo", async () => {
    const usuario = await abrirTelaDaAula();
    const lancarEspiado = vi.spyOn(turmasApi, "lancarOcorrenciaDeConduta");

    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    expect(await screen.findByText(/motivo é obrigatório/i)).toBeInTheDocument();
    expect(lancarEspiado).not.toHaveBeenCalled();
  });

  it("o Mestre lança a ocorrência sem informar valor algum", async () => {
    const usuario = await abrirTelaDaAula();
    const ocorrencia: OcorrenciaDeConduta = {
      id: "ocorrencia-1",
      guerreiro_id: "guerreiro-1",
      aula_id: "aula-1",
      atividade_id: "atividade-1",
      valor: 5,
      motivo: "Desrespeitou um colega.",
      momento_do_fato: "2026-08-01T10:00:00-03:00",
    };
    const lancarEspiado = vi
      .spyOn(turmasApi, "lancarOcorrenciaDeConduta")
      .mockResolvedValue(ocorrencia);

    await usuario.selectOptions(screen.getByLabelText(/^atividade$/i), "atividade-1");
    const identificadores = screen.getAllByLabelText(/identificador do guerreiro/i);
    await usuario.type(identificadores[identificadores.length - 1], "guerreiro-1");
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Desrespeitou um colega.");

    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    await waitFor(() => expect(lancarEspiado).toHaveBeenCalled());
    const chamada = lancarEspiado.mock.calls[0];
    expect(chamada[0]).toBe("guerreiro-1");
    expect(chamada[3]).toBe("Desrespeitou um colega.");
    expect(await screen.findByText(/ocorrência registrada/i)).toBeInTheDocument();
  });

  it("o teto da aula é explicado em linguagem simples (RN-09-16)", async () => {
    const usuario = await abrirTelaDaAula();
    vi.spyOn(turmasApi, "lancarOcorrenciaDeConduta").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O teto da aula foi alcançado.",
      }),
    );

    const identificadores = screen.getAllByLabelText(/identificador do guerreiro/i);
    await usuario.type(identificadores[identificadores.length - 1], "guerreiro-1");
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Desrespeitou um colega.");
    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    expect(await screen.findByText(/teto da aula foi alcançado/i)).toBeInTheDocument();
  });
});
