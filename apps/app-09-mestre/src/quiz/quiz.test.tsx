import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { TrilhaDoMestre } from "../trilhas/api";
import * as trilhasApi from "../trilhas/api";
import type { PerguntaDeQuiz } from "./api";
import * as quizApi from "./api";
import { TelaDoBancoDeQuiz } from "./TelaDoBancoDeQuiz";

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
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

function trilha(sobrescreve: Partial<TrilhaDoMestre> = {}): TrilhaDoMestre {
  return {
    id: "trilha-1",
    nome: "Robô Educa",
    objetivo: "Construir o próprio robô.",
    area_do_conhecimento: "Programação e Robótica",
    poder_id: "poder-guerreiro",
    situacao: "publicada",
    motivo_da_situacao: null,
    etiquetas_ods: [],
    cobertura_ods: { objetivos: [], ciclo: "Ciclo 01" },
    missoes: [
      {
        id: "missao-1",
        trilha_id: "trilha-1",
        titulo: "Primeira missão",
        posicao: 1,
        nivel_de_dificuldade: 1,
        obrigatoria: true,
        e_sondagem: false,
        etapa_do_ciclo: "abertura",
        cadencia_de_retomada: null,
        atividades: [],
        etiquetas_ods: [],
      },
    ],
    ...sobrescreve,
  };
}

function pergunta(sobrescreve: Partial<PerguntaDeQuiz> = {}): PerguntaDeQuiz {
  return {
    id: "pergunta-1",
    enunciado: "Qual é a primeira capital do Brasil?",
    alternativas: ["Salvador", "Recife", "Cachoeira", "Ilhéus"],
    alternativa_correta: 1,
    missao_id: "missao-1",
    trilha_id: "trilha-1",
    registrado_em: "2026-08-23T10:00:00-03:00",
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("cadastro de pergunta (RF-09-36, RF-09-37, RF-09-39)", () => {
  it("Mestre cadastra a pergunta com as quatro alternativas, a correta e a missão", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(quizApi, "listarBancoDeQuiz").mockResolvedValueOnce({
      itens: [],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi
      .spyOn(quizApi, "cadastrarPergunta")
      .mockResolvedValue(pergunta());
    vi.spyOn(quizApi, "listarBancoDeQuiz").mockResolvedValueOnce({
      itens: [pergunta()],
      proximo_cursor: null,
    });

    render(<TelaDoBancoDeQuiz />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova pergunta/i }));
    await usuario.type(
      screen.getByLabelText(/enunciado/i),
      "Qual é a primeira capital do Brasil?",
    );
    await usuario.selectOptions(screen.getByLabelText(/^trilha$/i), "trilha-1");
    await usuario.selectOptions(screen.getByLabelText(/^missão$/i), "missao-1");
    await usuario.type(screen.getByLabelText(/alternativa 1/i), "Salvador");
    await usuario.type(screen.getByLabelText(/alternativa 2/i), "Recife");
    await usuario.type(screen.getByLabelText(/alternativa 3/i), "Cachoeira");
    await usuario.type(screen.getByLabelText(/alternativa 4/i), "Ilhéus");
    await usuario.selectOptions(screen.getByLabelText(/alternativa correta/i), "1");
    await usuario.click(screen.getByRole("button", { name: /cadastrar pergunta/i }));

    await waitFor(() =>
      expect(cadastrarEspiado).toHaveBeenCalledWith(
        {
          enunciado: "Qual é a primeira capital do Brasil?",
          alternativas: ["Salvador", "Recife", "Cachoeira", "Ilhéus"],
          alternativa_correta: 1,
          missao_id: "missao-1",
        },
        "token-do-mestre",
      ),
    );
    expect(
      await screen.findByText("Qual é a primeira capital do Brasil?"),
    ).toBeInTheDocument();
  });

  it("envio incompleto é recusado no próprio campo, sem chamar o núcleo", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(quizApi, "listarBancoDeQuiz").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(quizApi, "cadastrarPergunta");

    render(<TelaDoBancoDeQuiz />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova pergunta/i }));
    await usuario.click(screen.getByRole("button", { name: /cadastrar pergunta/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/enunciado/i);
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });
});

describe("filtro do banco (RF-09-40)", () => {
  it("filtra a lista por trilha e por missão", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    const listarBancoEspiado = vi
      .spyOn(quizApi, "listarBancoDeQuiz")
      .mockResolvedValue({ itens: [pergunta()], proximo_cursor: null });

    render(<TelaDoBancoDeQuiz />);
    const usuario = userEvent.setup();

    await waitFor(() =>
      expect(listarBancoEspiado).toHaveBeenCalledWith(
        { trilhaId: "", missaoId: "" },
        "token-do-mestre",
      ),
    );

    await usuario.selectOptions(screen.getByLabelText(/filtrar por trilha/i), "trilha-1");
    await waitFor(() =>
      expect(listarBancoEspiado).toHaveBeenCalledWith(
        { trilhaId: "trilha-1", missaoId: "" },
        "token-do-mestre",
      ),
    );

    await usuario.selectOptions(screen.getByLabelText(/filtrar por missão/i), "missao-1");
    await waitFor(() =>
      expect(listarBancoEspiado).toHaveBeenCalledWith(
        { trilhaId: "trilha-1", missaoId: "missao-1" },
        "token-do-mestre",
      ),
    );
  });
});
