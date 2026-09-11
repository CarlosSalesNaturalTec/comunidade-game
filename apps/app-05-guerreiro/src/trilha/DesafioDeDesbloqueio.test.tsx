import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";

const CHAVE_DE_SESSAO = "app-05:teste-desafio-de-desbloqueio";

function pergunta(
  id: string,
  enunciado: string,
  imagem_referencia: string | null = null,
): trilhaApi.PerguntaDoDesbloqueio {
  return { id, ordem: 1, enunciado, alternativas: ["1", "2", "3", "4"], imagem_referencia };
}

const QUIZ_DE_DUAS: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  enunciado: null,
  perguntas: [pergunta("p1", "Quanto é 1 + 1?"), pergunta("p2", "Quanto é 2 + 2?")],
};

async function renderizar(desafio: trilhaApi.DesafioDeDesbloqueio, aoDesbloquear = vi.fn()) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <DesafioDeDesbloqueio
          missaoId="missao-1"
          desafio={desafio}
          aoDesbloquear={aoDesbloquear}
        />
      </ProvedorDeSessao>,
    );
  });
  return aoDesbloquear;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("desafio de desbloqueio", () => {
  it("todas as perguntas vão numa submissão só (RF-05-89)", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 2,
      total: 2,
    });
    const aoDesbloquear = await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getAllByRole("radio", { name: "2" })[0]);
    await usuario.click(screen.getAllByRole("radio", { name: "4" })[1]);
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledTimes(1);
    expect(submeter.mock.calls[0][1]).toEqual([
      { pergunta_id: "p1", alternativa_escolhida: 2 },
      { pergunta_id: "p2", alternativa_escolhida: 4 },
    ]);
    expect(aoDesbloquear).toHaveBeenCalled();
  });

  it("pergunta sem resposta é sinalizada e nada é enviado (RF-05-89)", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio");
    await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getAllByRole("radio", { name: "2" })[0]);
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(await screen.findByText(/falta responder 1 pergunta/i)).toBeInTheDocument();
    expect(submeter).not.toHaveBeenCalled();
  });

  it("não passar diz quantas acertou e convida a tentar de novo, sem punição", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: false,
      aguardando_mestre: false,
      acertos: 1,
      total: 2,
    });
    await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getAllByRole("radio", { name: "1" })[0]);
    await usuario.click(screen.getAllByRole("radio", { name: "1" })[1]);
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(await screen.findByText(/não foi dessa vez/i)).toBeInTheDocument();
    expect(screen.getByText(/acertou 1 de 2/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /enviar respostas/i })).not.toBeDisabled();
  });

  it("prático declarado fica aguardando o Mestre", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: null,
      aguardando_mestre: true,
      acertos: 0,
      total: 0,
    });
    await renderizar({
      tipo: "pratico",
      enunciado: "Monte o robô e mostre ao Mestre.",
      perguntas: null,
    });

    await act(async () => {
      screen.getByRole("button", { name: /já cumpri/i }).click();
    });

    expect(await screen.findByText(/aguardando|esperar o mestre/i)).toBeInTheDocument();
  });
});

describe("a imagem da pergunta (RF-09-119, RF-05-89)", () => {
  const QUIZ_COM_IMAGEM: trilhaApi.DesafioDeDesbloqueio = {
    tipo: "quiz",
    enunciado: null,
    perguntas: [
      pergunta("p1", "Quanto é 1 + 1?"),
      pergunta("p2", "O que o gráfico mostra?", "perguntas-do-desbloqueio/p2/imagem"),
    ],
  };

  it("a pergunta com imagem a exibe com o enunciado, antes das alternativas", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:imagem-da-p2"),
      revokeObjectURL: vi.fn(),
    });
    const ler = vi
      .spyOn(trilhaApi, "lerImagemDaPergunta")
      .mockResolvedValue(new Blob(["bytes"], { type: "image/png" }));

    await renderizar(QUIZ_COM_IMAGEM);

    // Só a pergunta que tem imagem a busca.
    expect(ler).toHaveBeenCalledTimes(1);
    expect(ler.mock.calls[0][0]).toBe("p2");
    const imagem = await screen.findByRole("img", {
      name: /imagem da pergunta: o que o gráfico mostra\?/i,
    });
    expect(imagem).toBeInTheDocument();
    // Antes das alternativas daquela pergunta, dentro do mesmo bloco.
    const bloco = imagem.closest("fieldset");
    expect(bloco?.textContent).toContain("O que o gráfico mostra?");
    expect(
      bloco?.querySelector(".cg-trilha__alternativas")?.compareDocumentPosition(imagem),
    ).toBe(Node.DOCUMENT_POSITION_PRECEDING);
    vi.unstubAllGlobals();
  });

  it("imagem que não carrega avisa e não tranca a pergunta", async () => {
    vi.spyOn(trilhaApi, "lerImagemDaPergunta").mockRejectedValue(new Error("caiu a rede"));
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 2,
      total: 2,
    });

    await renderizar(QUIZ_COM_IMAGEM);
    const usuario = userEvent.setup();

    expect(await screen.findByText(/a imagem desta pergunta não abriu/i)).toBeInTheDocument();
    await usuario.click(screen.getAllByRole("radio", { name: "2" })[0]);
    await usuario.click(screen.getAllByRole("radio", { name: "2" })[1]);
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledTimes(1);
  });
});
