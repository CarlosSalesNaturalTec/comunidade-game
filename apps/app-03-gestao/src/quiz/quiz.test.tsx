import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { EquipeDaAula, EstadoDaPartida, MinhasTurmas, PerguntaDeQuiz } from "./api";
import * as quizApi from "./api";
import { TelaDeQuiz } from "./TelaDeQuiz";

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

const SESSAO_DE_GUERREIRO: SessaoAberta = {
  token: "token-do-guerreiro",
  papel: "guerreiro",
  permissoes: {},
  persona_id: "guerreiro-1",
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

function minhasTurmas(sobrescreve: Partial<MinhasTurmas> = {}): MinhasTurmas {
  return {
    itens: [
      {
        id: "aula-1",
        comunidade_virtual_id: "comunidade-1",
        ponto_de_apoio_id: "ponto-1",
        inicio_em: "2026-08-25T14:00:00-03:00",
        fim_em: "2026-08-25T16:00:00-03:00",
        situacao: "confirmada",
      },
    ],
    proximo_cursor: null,
    atividades_presenciais: [
      {
        id: "atividade-1",
        missao_id: "missao-1",
        titulo: "Quiz da trilha",
        formato: "presencial",
        modalidade: "em_equipe",
        natureza: "competição ao vivo",
      },
    ],
    atividades_on_line: [],
    ...sobrescreve,
  };
}

function equipe(id: string, nick: string): EquipeDaAula {
  return { id, aula_id: "aula-1", integrantes: [{ avatar: null, nick, papel: null }] };
}

function pergunta(sobrescreve: Partial<PerguntaDeQuiz> = {}): PerguntaDeQuiz {
  return {
    id: "pergunta-1",
    enunciado: "Qual é a primeira capital do Brasil?",
    alternativas: ["Salvador", "Recife", "Cachoeira", "Ilhéus"],
    alternativa_correta: 1,
    missao_id: "missao-1",
    trilha_id: "trilha-1",
    registrado_em: "2026-08-20T10:00:00-03:00",
    ...sobrescreve,
  };
}

// `delay: null` evita que o clique interno espere um `setTimeout` real —
// necessário para conviver com `vi.useFakeTimers()` na sondagem sem travar.
function configurarUsuario() {
  return userEvent.setup({ delay: null });
}

function estado(sobrescreve: Partial<EstadoDaPartida> = {}): EstadoDaPartida {
  return {
    id: "partida-1",
    aula_id: "aula-1",
    atividade_id: "atividade-1",
    situacao: "aberta",
    equipes_disputantes: ["equipe-a", "equipe-b"],
    pergunta_no_ar: null,
    equipes_que_responderam: [],
    ...sobrescreve,
  };
}

async function abrirAPartida() {
  vi.spyOn(quizApi, "listarMinhasTurmas").mockResolvedValue(minhasTurmas());
  vi.spyOn(quizApi, "listarEquipesDaAula").mockResolvedValue({
    itens: [equipe("equipe-a", "Susy"), equipe("equipe-b", "Otávio")],
    proximo_cursor: null,
  });
  vi.spyOn(quizApi, "abrirPartida").mockResolvedValue({
    id: "partida-1",
    aula_id: "aula-1",
    atividade_id: "atividade-1",
    situacao: "aberta",
    equipes_disputantes: ["equipe-a", "equipe-b"],
    encerrada_em: null,
    registrado_em: "2026-08-25T14:05:00-03:00",
  });
  vi.spyOn(quizApi, "lerEstadoDaPartida").mockResolvedValue(estado());
  vi.spyOn(quizApi, "listarPerguntasDaMissao").mockResolvedValue({
    itens: [pergunta()],
    proximo_cursor: null,
  });

  const usuario = configurarUsuario();
  render(<TelaDeQuiz />);

  await screen.findByLabelText("Aula");
  await usuario.selectOptions(screen.getByLabelText("Aula"), "aula-1");
  await usuario.selectOptions(
    await screen.findByLabelText("Atividade de Quiz ao Vivo"),
    "atividade-1",
  );
  await screen.findByText("Susy");
  await usuario.click(screen.getByRole("button", { name: "Abrir partida" }));
  await screen.findByLabelText("Próxima pergunta");

  return usuario;
}

describe("TelaDeQuiz", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it("recusa quem não é Mestre nem Admin", () => {
    configurarSessao(SESSAO_DE_GUERREIRO);

    render(<TelaDeQuiz />);

    expect(screen.getByText(/Esta área é do Mestre e do Admin/)).toBeInTheDocument();
    expect(screen.queryByLabelText("Aula")).not.toBeInTheDocument();
  });

  it("avisa quando a aula não tem equipe formada", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(quizApi, "listarMinhasTurmas").mockResolvedValue(minhasTurmas());
    vi.spyOn(quizApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    const usuario = configurarUsuario();
    render(<TelaDeQuiz />);
    await usuario.selectOptions(await screen.findByLabelText("Aula"), "aula-1");

    expect(await screen.findByText(/Nenhuma equipe formada nesta aula/)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Abrir partida" })).not.toBeInTheDocument();
  });

  it("abre a partida e conduz uma pergunta até liberar o resultado", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    await abrirAPartida();

    await configurarUsuario().selectOptions(
      screen.getByLabelText("Próxima pergunta"),
      "pergunta-1",
    );
    vi.spyOn(quizApi, "porPerguntaNoAr").mockResolvedValue(
      estado({
        pergunta_no_ar: {
          id: "no-ar-1",
          pergunta_id: "pergunta-1",
          enunciado: pergunta().enunciado,
          alternativas: pergunta().alternativas,
          ordem: 1,
          entrou_em: "2026-08-25T14:10:00-03:00",
          resultado_liberado: false,
          alternativa_correta: null,
          equipes_que_acertaram: null,
          primeira_equipe_a_acertar: null,
        },
      }),
    );
    await configurarUsuario().click(
      screen.getByRole("button", { name: "Pôr pergunta no ar" }),
    );

    expect(
      await screen.findByRole("heading", { name: pergunta().enunciado }),
    ).toBeInTheDocument();
    expect(screen.getByText("0 de 2 equipes já responderam.")).toBeInTheDocument();

    vi.spyOn(quizApi, "liberarResultado").mockResolvedValue(
      estado({
        pergunta_no_ar: {
          id: "no-ar-1",
          pergunta_id: "pergunta-1",
          enunciado: pergunta().enunciado,
          alternativas: pergunta().alternativas,
          ordem: 1,
          entrou_em: "2026-08-25T14:10:00-03:00",
          resultado_liberado: true,
          alternativa_correta: 1,
          equipes_que_acertaram: ["equipe-a"],
          primeira_equipe_a_acertar: "equipe-a",
        },
      }),
    );
    await configurarUsuario().click(screen.getByRole("button", { name: "Liberar resultado" }));

    expect(await screen.findByText(/A alternativa correta é a 1/)).toBeInTheDocument();
  });

  it("encerra a partida e mostra o aviso do lançamento", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    await abrirAPartida();

    vi.spyOn(quizApi, "encerrarPartida").mockResolvedValue({
      id: "partida-1",
      aula_id: "aula-1",
      atividade_id: "atividade-1",
      situacao: "encerrada",
      equipes_disputantes: ["equipe-a", "equipe-b"],
      encerrada_em: "2026-08-25T14:30:00-03:00",
      registrado_em: "2026-08-25T14:05:00-03:00",
    });
    vi.spyOn(quizApi, "lerEstadoDaPartida").mockResolvedValue(
      estado({ situacao: "encerrada" }),
    );
    await configurarUsuario().click(screen.getByRole("button", { name: "Encerrar partida" }));

    expect(
      await screen.findByText(/Partida encerrada\. A pontuação foi lançada/),
    ).toBeInTheDocument();
  });

  it("avisa da perda de contato sem apagar o estado, e retoma na sondagem seguinte", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    configurarSessao(SESSAO_DE_MESTRE);
    await abrirAPartida();

    vi.spyOn(quizApi, "lerEstadoDaPartida").mockRejectedValueOnce(
      new ErroDaApi(0, {
        codigo: "erro_de_rede",
        mensagem: "Não foi possível falar com o núcleo.",
      }),
    );

    await vi.advanceTimersByTimeAsync(2000);

    expect(await screen.findByText(/Perdemos contato com o núcleo/)).toBeInTheDocument();
    expect(screen.getByLabelText("Próxima pergunta")).toBeInTheDocument();

    vi.spyOn(quizApi, "lerEstadoDaPartida").mockResolvedValue(estado());
    await vi.advanceTimersByTimeAsync(2000);

    await waitFor(() =>
      expect(screen.queryByText(/Perdemos contato com o núcleo/)).not.toBeInTheDocument(),
    );
  });
});
