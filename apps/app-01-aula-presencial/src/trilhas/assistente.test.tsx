import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as assistenteApi from "../api/assistente";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDoAssistente } from "./TelaDoAssistente";

class GravadorFalso {
  ondataavailable: ((evento: { data: Blob }) => void) | null = null;
  onstop: (() => void) | null = null;
  start() {}
  stop() {
    this.ondataavailable?.({ data: new Blob(["fala-fake"]) });
    this.onstop?.();
  }
}

function configurarMicrofoneFalso() {
  const pistas = [{ stop: vi.fn() }];
  const getUserMedia = vi.fn().mockResolvedValue({ getTracks: () => pistas });
  vi.stubGlobal("navigator", { ...navigator, mediaDevices: { getUserMedia } });
  vi.stubGlobal(
    "MediaRecorder",
    class {
      constructor() {
        return new GravadorFalso() as unknown as MediaRecorder;
      }
    },
  );
  return getUserMedia;
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

function renderizar(aoVoltar = vi.fn()) {
  return render(
    <ProvedorDeEstadoDeRede>
      <TelaDoAssistente equipeId="equipe-1" token="token-guerreiro" aoVoltar={aoVoltar} />
    </ProvedorDeEstadoDeRede>,
  );
}

describe("assistente de trilhas (RF-04-36 a RF-04-40, RN-04-19 a RN-04-21)", () => {
  it("as duas formas de perguntar estão em tela ao mesmo tempo", () => {
    renderizar();

    expect(screen.getByLabelText(/pergunta/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /perguntar por voz/i })).toBeInTheDocument();
  });

  it("pergunta por texto mostra a resposta na conversa", async () => {
    const consultar = vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas").mockResolvedValue({
      id: "consulta-1",
      equipe_id: "equipe-1",
      guerreiro_id: null,
      assistente: "trilhas",
      desfecho: "respondida",
      pergunta: "O que é uma variável?",
      resposta: "É um espaço na memória.",
      registrado_em: new Date().toISOString(),
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/pergunta/i), "O que é uma variável?");
    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));

    expect(await screen.findByText("É um espaço na memória.")).toBeInTheDocument();
    expect(screen.getByText("O que é uma variável?")).toBeInTheDocument();
    expect(consultar).toHaveBeenCalledWith(
      "equipe-1",
      { texto: "O que é uma variável?", arquivo: undefined },
      "token-guerreiro",
    );
  });

  it("sem toque no microfone não há captação", () => {
    const getUserMedia = configurarMicrofoneFalso();
    renderizar();

    expect(getUserMedia).not.toHaveBeenCalled();
  });

  it("o microfone abre ao toque e fecha ao fim da fala, enviando o áudio", async () => {
    configurarMicrofoneFalso();
    const consultar = vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas").mockResolvedValue({
      id: "consulta-1",
      equipe_id: "equipe-1",
      guerreiro_id: null,
      assistente: "trilhas",
      desfecho: "respondida",
      pergunta: "Transcrição da fala.",
      resposta: "Resposta ao que foi falado.",
      registrado_em: new Date().toISOString(),
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /perguntar por voz/i }));
    expect(await screen.findByRole("button", { name: /parar a gravação/i })).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /parar a gravação/i }));
    expect(await screen.findByText(/pronta para enviar/i)).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));

    await vi.waitFor(() => expect(consultar).toHaveBeenCalled());
    expect(consultar.mock.calls[0][1].texto).toBeUndefined();
    expect(consultar.mock.calls[0][1].arquivo).toBeInstanceOf(Blob);
  });

  it("a recusa explicada aparece como resposta, nunca como erro", async () => {
    vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas").mockResolvedValue({
      id: "consulta-1",
      equipe_id: "equipe-1",
      guerreiro_id: null,
      assistente: "trilhas",
      desfecho: "fora_do_corpus",
      pergunta: "Qual é a capital da Mongólia?",
      resposta: "Esse assunto ainda não está no material desta trilha. Procure um Mestre.",
      registrado_em: new Date().toISOString(),
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/pergunta/i), "Qual é a capital da Mongólia?");
    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));

    expect(await screen.findByText(/procure um mestre/i)).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("o encaminhamento à App 05 aparece como resposta", async () => {
    vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas").mockResolvedValue({
      id: "consulta-1",
      equipe_id: "equipe-1",
      guerreiro_id: null,
      assistente: "trilhas",
      desfecho: "tarefa_escolar",
      pergunta: "Preciso fazer o dever de casa",
      resposta: "Essa pergunta é de tarefa escolar — esse apoio é da App 05.",
      registrado_em: new Date().toISOString(),
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/pergunta/i), "Preciso fazer o dever de casa");
    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));

    expect(await screen.findByText(/app 05/i)).toBeInTheDocument();
  });

  it("resposta indisponível convida a perguntar de novo, sem sumir com a pergunta", async () => {
    vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas").mockRejectedValue(
      new ErroDaApi(503, {
        codigo: "consulta_ao_assistente_indisponivel",
        mensagem: "O assistente não respondeu agora.",
      }),
    );

    renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/pergunta/i), "Uma pergunta qualquer");
    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));

    expect(await screen.findByText(/pergunte de novo/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/pergunta/i)).toHaveValue("Uma pergunta qualquer");
  });

  it("sem rede o assistente fica indisponível e nada é enviado", async () => {
    const consultar = vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas");
    renderizar();
    window.dispatchEvent(new Event("offline"));

    expect(
      await screen.findByText(/sem rede, o assistente de trilhas fica indisponível/i),
    ).toBeInTheDocument();
    expect(screen.queryByLabelText(/pergunta/i)).not.toBeInTheDocument();
    expect(consultar).not.toHaveBeenCalled();
  });

  it("a conversa não sobrevive ao fim do atendimento", async () => {
    vi.spyOn(assistenteApi, "consultarAssistenteDeTrilhas").mockResolvedValue({
      id: "consulta-1",
      equipe_id: "equipe-1",
      guerreiro_id: null,
      assistente: "trilhas",
      desfecho: "respondida",
      pergunta: "O que é uma variável?",
      resposta: "É um espaço na memória.",
      registrado_em: new Date().toISOString(),
    });

    const { unmount } = renderizar();
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/pergunta/i), "O que é uma variável?");
    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));
    expect(await screen.findByText("É um espaço na memória.")).toBeInTheDocument();

    unmount();
    renderizar();

    expect(screen.queryByText("É um espaço na memória.")).not.toBeInTheDocument();
    expect(localStorage.length).toBe(0);
  });
});
