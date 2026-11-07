import { act, fireEvent, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { ProvedorDeNarracao, useNarracao } from "comum/narracao";
import { Sondagem } from "comum/trilha";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";

const CHAVE_DE_SESSAO = "app-05:teste-sondagem";

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("sondagem", () => {
  it("diz que serve para o Mestre ajustar e não muda o nível", async () => {
    sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });

    await act(async () => {
      render(
        <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
          <Sondagem
            missaoId="sondagem-1"
            desafio={{
              tipo: "quiz",
              forma_de_comprovacao: null,
              criterio_de_aceite: null,
              titulo_curto: null,
              enunciado: null,
              perguntas: [
                {
                  id: "p1",
                  ordem: 1,
                  enunciado: "Pergunta",
                  alternativas: ["a", "b", "c", "d"],
                  imagem_referencia: null,
                },
              ],
            }}
            aoResponder={vi.fn()}
            submissaoLigada
          />
        </ProvedorDeSessao>,
      );
    });

    expect(screen.getByText(/ajuda o mestre/i)).toBeInTheDocument();
    expect(screen.getByText(/não muda o seu nível/i)).toBeInTheDocument();
    expect(screen.queryByText(/prova/i)).not.toBeInTheDocument();
  });

  it("responder chama aoResponder", async () => {
    sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 0,
      total: 1,
      comprovacao_entregue: null,
    });
    const aoResponder = vi.fn();

    await act(async () => {
      render(
        <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
          <Sondagem
            missaoId="sondagem-1"
            desafio={{
              tipo: "quiz",
              forma_de_comprovacao: null,
              criterio_de_aceite: null,
              titulo_curto: null,
              enunciado: null,
              perguntas: [
                {
                  id: "p1",
                  ordem: 1,
                  enunciado: "Pergunta",
                  alternativas: ["a", "b", "c", "d"],
                  imagem_referencia: null,
                },
              ],
            }}
            aoResponder={aoResponder}
            submissaoLigada
          />
        </ProvedorDeSessao>,
      );
    });

    // Errar tudo na sondagem abre a trilha do mesmo jeito: quem afere é o
    // núcleo, e ele não aplica o corte de 60% aqui (`RN-05-46`).
    await act(async () => {
      screen.getByRole("radio", { name: "a" }).click();
    });
    await act(async () => {
      screen.getByRole("button", { name: /enviar respostas/i }).click();
    });

    expect(aoResponder).toHaveBeenCalled();
    expect(screen.queryByText(/não foi dessa vez/i)).not.toBeInTheDocument();
  });
});

// A sondagem respondida por voz na Área do Guerreiro(a) (`RF-05-97`,
// `RF-05-98`, `RN-05-54`). Fala, permissão e reconhecimento são do navegador:
// aqui entram os falsos dele, e o relógio falso conta os 5 s da janela.
class EnunciadoFalso {
  lang = "";
  voice: SpeechSynthesisVoice | null = null;
  text: string;
  onend: (() => void) | null = null;
  onerror: (() => void) | null = null;

  constructor(text: string) {
    this.text = text;
  }
}

class ReconhecimentoFalso {
  lang = "";
  continuous = false;
  interimResults = false;
  onresult: ((evento: { results: { transcript: string }[][] }) => void) | null = null;
  onerror: (() => void) | null = null;
  onend: (() => void) | null = null;
  start() {
    reconhecimentos.push(this);
  }
  stop() {}
}

let reconhecimentos: ReconhecimentoFalso[] = [];
let ditos: EnunciadoFalso[] = [];

function instalarNavegadorFalso() {
  reconhecimentos = [];
  ditos = [];
  vi.stubGlobal("speechSynthesis", {
    getVoices: () => [{ lang: "pt-BR", localService: true, name: "local" }],
    speak: (dito: EnunciadoFalso) => ditos.push(dito),
    cancel: () => {},
    addEventListener: () => {},
    removeEventListener: () => {},
  });
  vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
  vi.stubGlobal("SpeechRecognition", ReconhecimentoFalso);
  Object.defineProperty(navigator, "mediaDevices", {
    configurable: true,
    value: { getUserMedia: vi.fn().mockResolvedValue({ getTracks: () => [] }) },
  });
}

function LigarNarracao() {
  const { alternarNarracao } = useNarracao();
  return (
    <button type="button" onClick={alternarNarracao}>
      Ligar a narração
    </button>
  );
}

const DUAS_PERGUNTAS = {
  tipo: "quiz" as const,
  forma_de_comprovacao: null,
  criterio_de_aceite: null,
  titulo_curto: null,
  enunciado: null,
  perguntas: [
    {
      id: "p1",
      ordem: 1,
      enunciado: "Qual a cor do céu?",
      alternativas: ["Azul", "Verde", "Roxo", "Preto"],
      imagem_referencia: null,
    },
    {
      id: "p2",
      ordem: 2,
      enunciado: "Quanto é 2 + 2?",
      alternativas: ["3", "4", "5", "6"],
      imagem_referencia: null,
    },
  ],
};

async function renderizarSondagemComNarracao() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <ProvedorDeNarracao>
          <LigarNarracao />
          <Sondagem
            missaoId="sondagem-1"
            desafio={DUAS_PERGUNTAS}
            aoResponder={vi.fn()}
            submissaoLigada
          />
        </ProvedorDeNarracao>
      </ProvedorDeSessao>,
    );
  });
}

describe("sondagem respondida por voz (RF-05-97, RF-05-98, RN-05-54)", () => {
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    Reflect.deleteProperty(navigator, "mediaDevices");
  });

  it("com o áudio ligado, fala, escuta 5 s com a transcrição à vista e avança", async () => {
    instalarNavegadorFalso();
    await renderizarSondagemComNarracao();
    vi.useFakeTimers();

    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: "Ligar a narração" }));
    });
    await act(async () => {
      ditos.at(-1)?.onend?.();
    });

    expect(
      screen.getByRole("progressbar", { name: "Tempo para responder" }),
    ).toBeInTheDocument();
    await act(async () => {
      reconhecimentos[0].onresult?.({ results: [[{ transcript: "azul" }]] });
    });
    expect(screen.getByText("Você disse: azul")).toBeInTheDocument();

    await act(async () => {
      vi.advanceTimersByTime(5000);
    });

    expect(screen.getByText("Quanto é 2 + 2?")).toBeInTheDocument();
    expect(ditos.at(-1)?.text).toContain("Quanto é 2 + 2?");
  });

  it("com o áudio desligado nada escuta e a sondagem segue por toque", async () => {
    instalarNavegadorFalso();
    await renderizarSondagemComNarracao();

    expect(reconhecimentos).toHaveLength(0);
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument();
    expect(navigator.mediaDevices.getUserMedia).not.toHaveBeenCalled();
    expect(screen.getByRole("radio", { name: "Azul" })).toBeEnabled();
  });
});
