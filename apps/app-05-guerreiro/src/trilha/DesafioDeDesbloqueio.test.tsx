import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { DesafioDeDesbloqueio } from "comum/trilha";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";

const CHAVE_DE_SESSAO = "app-05:teste-desafio-de-desbloqueio";

function pergunta(
  id: string,
  enunciado: string,
  imagem_referencia: string | null = null,
  ordem = 1,
): trilhaApi.PerguntaDoDesbloqueio {
  return { id, ordem, enunciado, alternativas: ["1", "2", "3", "4"], imagem_referencia };
}

const QUIZ_DE_DUAS: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  enunciado: null,
  perguntas: [pergunta("p1", "Quanto é 1 + 1?"), pergunta("p2", "Quanto é 2 + 2?", null, 2)],
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
          submissaoLigada
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
  it("uma pergunta por vez, e todas vão numa submissão só (RF-05-89, RN-05-45)", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 2,
      total: 2,
    });
    const aoDesbloquear = await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "4" }));
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

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(await screen.findByText(/falta responder 1 pergunta/i)).toBeInTheDocument();
    // A tela leva até a pendente, em vez de só contá-la (documento 15 §6.4).
    expect(screen.getByText("2. Quanto é 2 + 2?")).toBeInTheDocument();
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

    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "1" }));
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
      pergunta("p2", "O que o gráfico mostra?", "perguntas-do-desbloqueio/p2/imagem", 2),
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
    const usuario = userEvent.setup();

    // A primeira pergunta não tem imagem, e nada é buscado por ela.
    expect(ler).not.toHaveBeenCalled();
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

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
    // A mesma moldura de tamanho fixo do conteúdo da missão (decisão do
    // fundador de 2026-09-17).
    expect(imagem.closest(".cg-midia-do-nucleo")).not.toBeNull();
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

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    expect(await screen.findByText(/a imagem desta pergunta não abriu/i)).toBeInTheDocument();
    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledTimes(1);
  });
});
