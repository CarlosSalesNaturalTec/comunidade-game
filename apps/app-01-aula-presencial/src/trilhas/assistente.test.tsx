import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as assistenteApi from "../api/assistente";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDoAssistente } from "./TelaDoAssistente";

// Duplo da Web Speech API do navegador — o mesmo padrão de teste de
// `comum/fala/fala.test.ts`, aqui verificando que a tela usa `comum/fala`
// corretamente (`RF-04-39`, `RF-04-40`).
class ReconhecimentoFalso {
  lang = "";
  continuous = true;
  interimResults = true;
  // biome-ignore lint/suspicious/noExplicitAny: espelha os eventos mínimos que comum/fala consome
  onresult: ((evento: any) => void) | null = null;
  // biome-ignore lint/suspicious/noExplicitAny: espelha os eventos mínimos que comum/fala consome
  onerror: ((evento: any) => void) | null = null;
  onend: (() => void) | null = null;
  parado = false;

  start() {}

  stop() {
    this.parado = true;
    this.onend?.();
  }
}

let reconhecimentoAtual: ReconhecimentoFalso | null = null;

function instalarReconhecimentoFalso() {
  reconhecimentoAtual = null;
  class Construtor extends ReconhecimentoFalso {
    constructor() {
      super();
      reconhecimentoAtual = this;
    }
  }
  vi.stubGlobal("SpeechRecognition", Construtor);
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
  it("o campo de texto está sempre em tela, com o botão de falar ao lado", () => {
    instalarReconhecimentoFalso();
    renderizar();

    expect(screen.getByLabelText(/pergunta/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /perguntar por voz/i })).toBeInTheDocument();
  });

  it("pergunta por texto mostra a resposta na conversa", async () => {
    const consultar = vi
      .spyOn(assistenteApi, "consultarAssistenteDeTrilhas")
      .mockResolvedValue({
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
      "O que é uma variável?",
      "token-guerreiro",
    );
  });

  it("sem toque no microfone não há captação", () => {
    instalarReconhecimentoFalso();
    renderizar();

    expect(reconhecimentoAtual).toBeNull();
  });

  it("o microfone abre ao toque e a transcrição final entra no campo da pergunta", async () => {
    instalarReconhecimentoFalso();
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /perguntar por voz/i }));
    expect(await screen.findByText(/ouvindo/i)).toBeInTheDocument();

    reconhecimentoAtual?.onresult?.({
      results: { 0: { 0: { transcript: "o que é uma variável" }, length: 1 }, length: 1 },
    });
    reconhecimentoAtual?.onend?.();

    expect(await screen.findByLabelText(/pergunta/i)).toHaveValue("o que é uma variável");
    expect(screen.queryByText(/ouvindo/i)).not.toBeInTheDocument();
  });

  it("a transcrição é editável antes do envio, e o texto corrigido é o que segue ao núcleo", async () => {
    instalarReconhecimentoFalso();
    const consultar = vi
      .spyOn(assistenteApi, "consultarAssistenteDeTrilhas")
      .mockResolvedValue({
        id: "consulta-1",
        equipe_id: "equipe-1",
        guerreiro_id: null,
        assistente: "trilhas",
        desfecho: "respondida",
        pergunta: "pergunta corrigida",
        resposta: "Resposta.",
        registrado_em: new Date().toISOString(),
      });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /perguntar por voz/i }));
    reconhecimentoAtual?.onresult?.({
      results: { 0: { 0: { transcript: "transcricao com erro" }, length: 1 }, length: 1 },
    });
    reconhecimentoAtual?.onend?.();
    expect(await screen.findByLabelText(/pergunta/i)).toHaveValue("transcricao com erro");

    await usuario.clear(screen.getByLabelText(/pergunta/i));
    await usuario.type(screen.getByLabelText(/pergunta/i), "pergunta corrigida");
    await usuario.click(screen.getByRole("button", { name: /^perguntar$/i }));

    await vi.waitFor(() => expect(consultar).toHaveBeenCalled());
    expect(consultar).toHaveBeenCalledWith(
      "equipe-1",
      "pergunta corrigida",
      "token-guerreiro",
    );
  });

  it("quando a transcrição falha, avisa sem apagar o que já estava escrito", async () => {
    instalarReconhecimentoFalso();
    renderizar();
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/pergunta/i), "texto que não deve sumir");
    await usuario.click(screen.getByRole("button", { name: /perguntar por voz/i }));

    reconhecimentoAtual?.onerror?.({ error: "no-speech" });
    reconhecimentoAtual?.onend?.();

    expect(await screen.findByText(/não foi possível entender a fala/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/pergunta/i)).toHaveValue("texto que não deve sumir");
  });

  it("o microfone fecha se a tela sair enquanto ainda ouve", async () => {
    instalarReconhecimentoFalso();
    const { unmount } = renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /perguntar por voz/i }));

    unmount();

    expect(reconhecimentoAtual?.parado).toBe(true);
  });

  it("sem a API de fala do aparelho, a tela avisa e mantém só a pergunta por texto", () => {
    renderizar();

    expect(
      screen.queryByRole("button", { name: /perguntar por voz/i }),
    ).not.toBeInTheDocument();
    expect(screen.getByText(/não transcreve fala/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/pergunta/i)).toBeInTheDocument();
  });

  it("a recusa explicada aparece como resposta, nunca como erro", async () => {
    instalarReconhecimentoFalso();
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
