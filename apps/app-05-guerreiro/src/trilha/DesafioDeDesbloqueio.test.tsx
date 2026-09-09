import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";

const CHAVE_DE_SESSAO = "app-05:teste-desafio-de-desbloqueio";

function pergunta(id: string, enunciado: string): trilhaApi.PerguntaDoDesbloqueio {
  return { id, ordem: 1, enunciado, alternativas: ["1", "2", "3", "4"] };
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
