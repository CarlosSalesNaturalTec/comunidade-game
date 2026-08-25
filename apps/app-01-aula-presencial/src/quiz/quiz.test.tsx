import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as presencasApi from "../api/presencas";
import type { PartidaDaAula, PerguntaParaEquipe } from "../api/quiz";
import * as quizApi from "../api/quiz";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { TelaInicial } from "../inicio/TelaInicial";
import { CHAVE_DA_PARTIDA_DE_QUIZ, TelaDaPartida } from "./TelaDaPartida";

function partida(sobrescreve: Partial<PartidaDaAula> = {}): PartidaDaAula {
  return { id: "partida-1", situacao: "aberta", equipe_id: "equipe-a", ...sobrescreve };
}

function pergunta(sobrescreve: Partial<PerguntaParaEquipe> = {}): PerguntaParaEquipe {
  return {
    id: "pergunta-1",
    enunciado: "Qual é a primeira capital do Brasil?",
    alternativas: ["Salvador", "Recife", "Cachoeira", "Ilhéus"],
    resultado_liberado: false,
    ...sobrescreve,
  };
}

const SEM_PERGUNTA_NO_AR: PerguntaParaEquipe = {
  id: null,
  enunciado: null,
  alternativas: null,
  resultado_liberado: false,
};

// `delay: null` evita que o clique interno espere um `setTimeout` real —
// necessário para conviver com `vi.useFakeTimers()` na sondagem.
function configurarUsuario() {
  return userEvent.setup({ delay: null });
}

function renderizar() {
  return render(
    <TelaDaPartida aulaId="aula-1" tokenDoGuerreiro="token-guerreiro-a" aoVoltar={vi.fn()} />,
  );
}

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("TelaDaPartida", () => {
  it("a equipe nunca é escolhida em tela — vem derivada do núcleo", async () => {
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
    vi.spyOn(quizApi, "lerPerguntaDaPartida").mockResolvedValue(SEM_PERGUNTA_NO_AR);

    renderizar();

    await screen.findByText(/próxima pergunta ainda não entrou no ar/i);
    expect(screen.queryByRole("combobox")).not.toBeInTheDocument();
    expect(screen.queryByText(/escolha a equipe/i)).not.toBeInTheDocument();
  });

  it("sem partida ou sem equipe disputante, a tela explica e oferece voltar", async () => {
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([]);

    renderizar();

    expect(await screen.findByText(/não há partida de quiz ao vivo/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /voltar ao início/i })).toBeInTheDocument();
  });

  it("Guerreiro(a) que não disputa nenhuma equipe recebe a mesma explicação", async () => {
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([
      partida({ equipe_id: null }),
    ]);

    renderizar();

    expect(await screen.findByText(/não há partida de quiz ao vivo/i)).toBeInTheDocument();
  });

  it("a pergunta aparece por sondagem, sem recarga", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
    const lerPergunta = vi
      .spyOn(quizApi, "lerPerguntaDaPartida")
      .mockResolvedValue(SEM_PERGUNTA_NO_AR);

    renderizar();
    await vi.waitFor(() =>
      expect(screen.getByText(/próxima pergunta ainda não entrou no ar/i)).toBeInTheDocument(),
    );

    lerPergunta.mockResolvedValue(pergunta());
    await vi.advanceTimersByTimeAsync(2000);

    expect(
      await screen.findByRole("heading", { name: pergunta().enunciado ?? "" }),
    ).toBeInTheDocument();
  });

  it("rede caída no meio da pergunta avisa, mas não tira a equipe da partida", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
    const lerPergunta = vi
      .spyOn(quizApi, "lerPerguntaDaPartida")
      .mockResolvedValue(pergunta());

    renderizar();
    await screen.findByRole("heading", { name: pergunta().enunciado ?? "" });

    lerPergunta.mockRejectedValueOnce(new TypeError("fetch failed"));
    await vi.advanceTimersByTimeAsync(2000);

    expect(await screen.findByText(/perdemos contato com o núcleo/i)).toBeInTheDocument();
    // A pergunta e a equipe seguem em tela — não volta para "sem partida".
    expect(
      screen.getByRole("heading", { name: pergunta().enunciado ?? "" }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/não há partida de quiz ao vivo/i)).not.toBeInTheDocument();

    lerPergunta.mockResolvedValue(pergunta());
    await vi.advanceTimersByTimeAsync(2000);

    await waitFor(() =>
      expect(screen.queryByText(/perdemos contato com o núcleo/i)).not.toBeInTheDocument(),
    );
  });

  describe("resposta e resultado", () => {
    it("a alternativa escolhida permanece em tela até a pergunta seguinte", async () => {
      vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
      vi.spyOn(quizApi, "lerPerguntaDaPartida").mockResolvedValue(pergunta());
      vi.spyOn(quizApi, "enviarResposta").mockResolvedValue({
        id: "resposta-1",
        equipe_id: "equipe-a",
        pergunta_id: "pergunta-1",
        alternativa_escolhida: 1,
        momento_de_chegada: "2026-08-25T14:10:00-03:00",
      });

      renderizar();
      const usuario = configurarUsuario();
      await screen.findByRole("heading", { name: pergunta().enunciado ?? "" });

      await usuario.click(screen.getByRole("button", { name: /1\. salvador/i }));

      expect(quizApi.enviarResposta).toHaveBeenCalledWith(
        "partida-1",
        "pergunta-1",
        "equipe-a",
        1,
        "token-guerreiro-a",
      );
      // A alternativa escolhida segue visível e destacada em tela, só
      // bloqueada para novo envio — não some nem vira tela de erro.
      const botaoEscolhido = await screen.findByRole("button", { name: /1\. salvador/i });
      await waitFor(() => expect(botaoEscolhido).toBeDisabled());
      expect(botaoEscolhido).toBeInTheDocument();
    });

    it("a segunda tentativa é recusada antes de enviar", async () => {
      vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
      vi.spyOn(quizApi, "lerPerguntaDaPartida").mockResolvedValue(pergunta());
      const enviarResposta = vi.spyOn(quizApi, "enviarResposta").mockResolvedValue({
        id: "resposta-1",
        equipe_id: "equipe-a",
        pergunta_id: "pergunta-1",
        alternativa_escolhida: 1,
        momento_de_chegada: "2026-08-25T14:10:00-03:00",
      });

      renderizar();
      const usuario = configurarUsuario();
      await screen.findByRole("heading", { name: pergunta().enunciado ?? "" });

      await usuario.click(screen.getByRole("button", { name: /1\. salvador/i }));
      await waitFor(() => expect(enviarResposta).toHaveBeenCalledTimes(1));
      await usuario.click(screen.getByRole("button", { name: /2\. recife/i }));

      expect(enviarResposta).toHaveBeenCalledTimes(1);
    });

    it("a recusa do núcleo por outro aparelho da equipe é tratada como 'já respondeu'", async () => {
      vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
      vi.spyOn(quizApi, "lerPerguntaDaPartida").mockResolvedValue(pergunta());
      vi.spyOn(quizApi, "enviarResposta").mockRejectedValue(
        new ErroDaApi(422, {
          codigo: "erro_de_validacao",
          mensagem: "Esta equipe já respondeu a esta pergunta.",
        }),
      );

      renderizar();
      const usuario = configurarUsuario();
      await screen.findByRole("heading", { name: pergunta().enunciado ?? "" });
      await usuario.click(screen.getByRole("button", { name: /1\. salvador/i }));

      const aviso = await screen.findByRole("alert");
      expect(aviso).toHaveTextContent(/esta equipe já respondeu/i);
    });

    it("o resultado fica oculto antes da liberação e completo depois, sem pontuação em tela", async () => {
      vi.useFakeTimers({ shouldAdvanceTime: true });
      vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
      const lerPergunta = vi
        .spyOn(quizApi, "lerPerguntaDaPartida")
        .mockResolvedValue(pergunta());

      renderizar();
      await screen.findByRole("heading", { name: pergunta().enunciado ?? "" });

      expect(screen.queryByText(/a alternativa correta/i)).not.toBeInTheDocument();

      lerPergunta.mockResolvedValue(
        pergunta({
          resultado_liberado: true,
          alternativa_correta: 1,
          acertou: true,
          primeira_equipe_a_acertar: "equipe-a",
        }),
      );
      await vi.advanceTimersByTimeAsync(2000);

      expect(await screen.findByText(/a alternativa correta é a 1/i)).toBeInTheDocument();
      expect(screen.getByText(/sua equipe chegou primeiro/i)).toBeInTheDocument();
      expect(screen.queryByText(/\bpontos?\b/i)).not.toBeInTheDocument();
      expect(screen.queryByText(/pontuação/i)).not.toBeInTheDocument();
    });

    it("sem rede a resposta fica indisponível, e nada é enviado", async () => {
      vi.useFakeTimers({ shouldAdvanceTime: true });
      vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([partida()]);
      const lerPergunta = vi
        .spyOn(quizApi, "lerPerguntaDaPartida")
        .mockResolvedValue(pergunta());
      const enviarResposta = vi.spyOn(quizApi, "enviarResposta");

      renderizar();
      const usuario = configurarUsuario();
      await screen.findByRole("heading", { name: pergunta().enunciado ?? "" });

      lerPergunta.mockRejectedValueOnce(new TypeError("fetch failed"));
      await vi.advanceTimersByTimeAsync(2000);
      await screen.findByText(/resposta está indisponível sem rede/i);

      await usuario.click(screen.getByRole("button", { name: /1\. salvador/i }));

      expect(enviarResposta).not.toHaveBeenCalled();
    });
  });

  it("relê a chave de sessionStorage a cada abertura, sem confiar no que já estava lá", async () => {
    sessionStorage.setItem(
      CHAVE_DA_PARTIDA_DE_QUIZ,
      JSON.stringify({ partidaId: "partida-velha", equipeId: "equipe-velha" }),
    );
    const listarPartidas = vi
      .spyOn(quizApi, "listarPartidasDaAula")
      .mockResolvedValue([partida()]);
    vi.spyOn(quizApi, "lerPerguntaDaPartida").mockResolvedValue(SEM_PERGUNTA_NO_AR);

    renderizar();

    await waitFor(() =>
      expect(listarPartidas).toHaveBeenCalledWith("aula-1", "token-guerreiro-a"),
    );
    expect(JSON.parse(sessionStorage.getItem(CHAVE_DA_PARTIDA_DE_QUIZ) ?? "{}")).toEqual({
      partidaId: "partida-1",
      equipeId: "equipe-a",
    });
  });
});

describe("a abertura do quiz a partir da tela inicial", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  function renderizarTelaInicial() {
    return render(
      <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
        <TelaInicial
          tokenDeTrabalho="token-de-trabalho"
          personaIdDeTrabalho="mestre-de-trabalho-1"
          aulaId="aula-1"
          aoVoltarAoInicio={vi.fn()}
          podeAbrirMomentoDeTroca={false}
          momentoDeTrocaAberto={false}
          abrindoMomentoDeTroca={false}
          erroDeAberturaDaTroca={null}
          aoAbrirMomentoDeTroca={vi.fn()}
          aoFecharMomentoDeTroca={vi.fn()}
        />
      </ProvedorDeSessao>,
    );
  }

  function mockarEntradaDoGuerreiro(guerreiroId: string) {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: `token-${guerreiroId}`,
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: guerreiroId,
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(presencasApi, "registrarPresenca").mockImplementation((aulaId, entrada) =>
      Promise.resolve({
        id: `presenca-${guerreiroId}`,
        aula_id: aulaId,
        guerreiro_id: entrada.guerreiro_id,
        modo: entrada.modo,
        confirmador_id: "mestre-de-trabalho-1",
        momento_do_fato: entrada.momento_do_fato,
      }),
    );
  }

  async function entrarPeloQuiz(usuario: ReturnType<typeof userEvent.setup>, nick: string) {
    await usuario.click(screen.getByRole("button", { name: /quiz ao vivo/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), nick);
    await usuario.click(screen.getByRole("button", { name: /^entrar$/i }));
    await usuario.click(await screen.findByRole("button", { name: /confirmar identidade/i }));
  }

  it("sem sessão aberta, o caminho do quiz leva à entrada por nick e imagem", async () => {
    renderizarTelaInicial();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /quiz ao vivo/i }));

    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });

  it("o atendimento seguinte não herda a equipe do Guerreiro(a) anterior", async () => {
    mockarEntradaDoGuerreiro("guerreiro-1");
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([
      partida({ id: "partida-1", equipe_id: "equipe-a" }),
    ]);
    vi.spyOn(quizApi, "lerPerguntaDaPartida").mockResolvedValue(SEM_PERGUNTA_NO_AR);

    renderizarTelaInicial();
    const usuario = userEvent.setup();
    await entrarPeloQuiz(usuario, "zeferina");
    await screen.findByText(/próxima pergunta ainda não entrou no ar/i);
    expect(JSON.parse(sessionStorage.getItem(CHAVE_DA_PARTIDA_DE_QUIZ) ?? "{}")).toEqual({
      partidaId: "partida-1",
      equipeId: "equipe-a",
    });

    await usuario.click(screen.getByRole("button", { name: /voltar ao início/i }));
    expect(sessionStorage.getItem(CHAVE_DA_PARTIDA_DE_QUIZ)).toBeNull();

    mockarEntradaDoGuerreiro("guerreiro-2");
    vi.spyOn(quizApi, "listarPartidasDaAula").mockResolvedValue([
      partida({ id: "partida-1", equipe_id: "equipe-b" }),
    ]);

    await entrarPeloQuiz(usuario, "otavio");
    await screen.findByText(/próxima pergunta ainda não entrou no ar/i);

    expect(JSON.parse(sessionStorage.getItem(CHAVE_DA_PARTIDA_DE_QUIZ) ?? "{}")).toEqual({
      partidaId: "partida-1",
      equipeId: "equipe-b",
    });
  });
});
