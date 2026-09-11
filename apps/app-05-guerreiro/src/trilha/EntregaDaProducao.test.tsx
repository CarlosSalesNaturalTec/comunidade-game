import { act, fireEvent, render, screen } from "@testing-library/react";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { EntregaDaProducao } from "./EntregaDaProducao";

const CHAVE_DE_SESSAO = "app-05:teste-entrega-da-producao";

const ATIVIDADES: trilhaApi.AtividadeDaMissaoPublica[] = [
  { id: "atividade-1", titulo: "Atividade Única", producao_esperada: "Um texto." },
];

// Duplo da Web Speech API do navegador, no mesmo padrão de
// `comum/fala/fala.test.ts` e do teste da tela do assistente da App 01: aqui
// se verifica que a tela usa `comum/fala` corretamente e que nenhum áudio é
// enviado (`RF-05-76`, `RN-05-32`).
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

function falar(transcricao: string) {
  reconhecimentoAtual?.onresult?.({ results: { 0: { 0: { transcript: transcricao } } } });
  reconhecimentoAtual?.onend?.();
}

function producaoGravada(
  sobrescreve: Partial<trilhaApi.ProducaoDaMissao> = {},
): trilhaApi.ProducaoDaMissao {
  return {
    id: "producao-1",
    equipe_id: null,
    guerreiro_id: "guerreiro-1",
    missao_id: "missao-1",
    atividade_id: "atividade-1",
    forma: "texto",
    transcricao: "Minha produção.",
    devolutiva: "Você foi bem em X, tente Y a seguir.",
    registrado_em: "2026-01-01T00:00:00Z",
    ...sobrescreve,
  };
}

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  let retorno: ReturnType<typeof render> | undefined;
  await act(async () => {
    retorno = render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <EntregaDaProducao missaoId="missao-1" atividades={ATIVIDADES} />
      </ProvedorDeSessao>,
    );
  });
  return retorno as ReturnType<typeof render>;
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
  sessionStorage.clear();
});

describe("entrega da produção", () => {
  it("as três formas aparecem lado a lado com o caminho do encontro", async () => {
    instalarReconhecimentoFalso();
    await renderizar();

    expect(screen.getByRole("button", { name: "Escrever" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Falar" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Fotografar" })).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Entregar ao Mestre no encontro" }),
    ).toBeInTheDocument();
  });

  it("avisa o descarte da foto antes de enviar", async () => {
    instalarReconhecimentoFalso();
    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Fotografar" }));

    expect(screen.getByText(/é usada só para ler/i)).toBeInTheDocument();
    expect(screen.getByText(/depois é descartada/i)).toBeInTheDocument();
  });

  it("avisa que a gravação não sai do aparelho antes de falar", async () => {
    instalarReconhecimentoFalso();
    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Falar" }));

    expect(screen.getByText(/não sai deste aparelho/i)).toBeInTheDocument();
  });

  it("a fala vira texto no campo e segue transcrita, com a forma áudio", async () => {
    instalarReconhecimentoFalso();
    const entregar = vi
      .spyOn(trilhaApi, "entregarProducaoIndividual")
      .mockResolvedValue(producaoGravada({ forma: "audio" }));

    await renderizar();
    fireEvent.click(screen.getByRole("button", { name: "Falar" }));
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /falar a produção/i }));
    });
    act(() => falar("o que eu falei"));

    expect(screen.getByLabelText(/sua produção/i)).toHaveValue("o que eu falei");

    // A transcrição é editável antes do envio, e é o texto corrigido que
    // segue ao núcleo (documento 09 §1, decisão de 2026-09-10).
    fireEvent.change(screen.getByLabelText(/sua produção/i), {
      target: { value: "o que eu falei, corrigido" },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(entregar).toHaveBeenCalledWith(
      "missao-1",
      {
        atividadeId: "atividade-1",
        forma: "audio",
        texto: "o que eu falei, corrigido",
        arquivo: undefined,
      },
      "token-do-guerreiro",
    );
  });

  it("quando a fala não é entendida, avisa sem apagar o que já estava escrito", async () => {
    instalarReconhecimentoFalso();
    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Falar" }));
    fireEvent.change(screen.getByLabelText(/sua produção/i), {
      target: { value: "texto que não deve sumir" },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /falar a produção/i }));
    });
    act(() => {
      reconhecimentoAtual?.onerror?.({ error: "no-speech" });
      reconhecimentoAtual?.onend?.();
    });

    expect(await screen.findByText(/não consegui entender a sua fala/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/sua produção/i)).toHaveValue("texto que não deve sumir");
  });

  it("o microfone fecha se a tela sair enquanto ainda ouve", async () => {
    instalarReconhecimentoFalso();
    const { unmount } = await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Falar" }));
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /falar a produção/i }));
    });
    unmount();

    expect(reconhecimentoAtual?.parado).toBe(true);
  });

  it("sem transcrição no aparelho, a fala não é oferecida e a tela o diz", async () => {
    await renderizar();

    expect(screen.queryByRole("button", { name: "Falar" })).not.toBeInTheDocument();
    expect(screen.getByText(/não transforma a sua fala em texto/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Escrever" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Fotografar" })).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Entregar ao Mestre no encontro" }),
    ).toBeInTheDocument();
  });

  it("quem escolhe o encontro não perde a missão e não vê formulário", async () => {
    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Entregar ao Mestre no encontro" }));

    expect(screen.getByText(/você não perde a missão/i)).toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });

  it("entrega em texto envia a atividade declarada e mostra a devolutiva sem ponto", async () => {
    const entregar = vi
      .spyOn(trilhaApi, "entregarProducaoIndividual")
      .mockResolvedValue(producaoGravada());

    await renderizar();

    fireEvent.change(screen.getByLabelText(/sua produção/i), {
      target: { value: "Minha produção." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(entregar).toHaveBeenCalledWith(
      "missao-1",
      {
        atividadeId: "atividade-1",
        forma: "texto",
        texto: "Minha produção.",
        arquivo: undefined,
      },
      "token-do-guerreiro",
    );
    expect(screen.getByText(/você foi bem em x/i)).toBeInTheDocument();
    expect(screen.getByText(/não vale ponto/i)).toBeInTheDocument();
    expect(screen.queryByText(/nível|badge/i)).not.toBeInTheDocument();
  });

  it("devolutiva que não vem confirma que a produção foi guardada", async () => {
    vi.spyOn(trilhaApi, "entregarProducaoIndividual").mockResolvedValue(
      producaoGravada({ devolutiva: null }),
    );

    await renderizar();

    fireEvent.change(screen.getByLabelText(/sua produção/i), {
      target: { value: "Minha produção." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(screen.getByText(/foi guardada/i)).toBeInTheDocument();
    expect(screen.getByText(/retorno não veio agora/i)).toBeInTheDocument();
  });

  it("leitura da foto indisponível mostra mensagem para tentar de novo", async () => {
    vi.spyOn(trilhaApi, "entregarProducaoIndividual").mockRejectedValue(
      new ErroDaApi(503, {
        codigo: "leitura_da_producao_indisponivel",
        mensagem: "A leitura da produção não veio agora.",
      }),
    );

    await renderizar();

    fireEvent.click(screen.getByRole("button", { name: "Fotografar" }));
    const arquivo = new File(["foto"], "foto.jpg", { type: "image/jpeg" });
    fireEvent.change(screen.getByLabelText(/^foto$/i), { target: { files: [arquivo] } });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Entregar" }));
    });

    expect(screen.getByText(/tente enviar de novo/i)).toBeInTheDocument();
  });
});
