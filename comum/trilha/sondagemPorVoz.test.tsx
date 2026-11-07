import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as autenticacaoApi from "../autenticacao/api";
import { ProvedorDeSessao } from "../autenticacao/ContextoDeSessao";
import * as fala from "../fala/fala";
import { ProvedorDeNarracao, useNarracao } from "../narracao/ProvedorDeNarracao";
import * as trilhaApi from "./api";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";
import { JanelaDeEscuta } from "./JanelaDeEscuta";
import { Sondagem } from "./Sondagem";

// A sondagem respondida por voz (`RF-05-97`, `RF-05-98`, `RN-05-54`): a
// fala da pergunta termina, a janela de 5 s abre, e a resposta segue sozinha.
// O reconhecimento do navegador é substituído por `escutarPorJanela` falso:
// o teste entrega o parcial e o fim quando quer.

const CHAVE_DE_SESSAO = "comum:teste-sondagem-por-voz";

function pergunta(id: string, enunciado: string, alternativas: string[]) {
  return { id, ordem: Number(id.slice(1)), enunciado, alternativas, imagem_referencia: null };
}

const SONDAGEM: trilhaApi.DesafioDeDesbloqueio = {
  forma_de_comprovacao: null,
  criterio_de_aceite: null,
  titulo_curto: null,
  tipo: "quiz",
  enunciado: null,
  perguntas: [
    pergunta("p1", "O que as plantas fazem com a luz?", [
      "Fotossíntese",
      "Respiração",
      "Evaporação",
      "Chuva ácida",
    ]),
    pergunta("p2", "Quanto é 2 + 2?", ["3", "4", "5", "6"]),
  ],
};

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

class MotorDeFalaFalso {
  ditos: EnunciadoFalso[] = [];

  getVoices() {
    return [
      { lang: "pt-BR", localService: true, name: "local", default: true, voiceURI: "local" },
    ] as SpeechSynthesisVoice[];
  }

  speak(dito: EnunciadoFalso) {
    this.ditos.push(dito);
  }

  cancel() {}

  addEventListener() {}

  removeEventListener() {}
}

interface JanelaFalsa {
  aoParcial: (transcricao: string) => void;
  aoEncerrar: (transcricao: string) => void;
  encerrar: ReturnType<typeof vi.fn>;
}

let motor: MotorDeFalaFalso;
let janelas: JanelaFalsa[];

function LigarNarracao() {
  const { alternarNarracao } = useNarracao();
  return (
    <button type="button" onClick={alternarNarracao}>
      Ligar a narração
    </button>
  );
}

async function renderizar(conteudo: React.ReactNode) {
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
          {conteudo}
        </ProvedorDeNarracao>
      </ProvedorDeSessao>,
    );
  });
}

function sondagem(props: Partial<React.ComponentProps<typeof DesafioDeDesbloqueio>> = {}) {
  return (
    <DesafioDeDesbloqueio
      missaoId="sondagem-1"
      desafio={SONDAGEM}
      aoDesbloquear={vi.fn()}
      submissaoLigada
      respostaPorVoz
      {...props}
    />
  );
}

// O fim da fala que a narração pediu por último — o que abre a janela.
async function terminarAFala() {
  const dito = motor.ditos.at(-1);
  await act(async () => {
    dito?.onend?.();
  });
}

async function ligarOAudio(usuario: ReturnType<typeof userEvent.setup>) {
  await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));
  // A permissão do microfone chega depois do toque; a pergunta no ar é
  // falada de novo, agora com a janela.
  await act(async () => {});
}

beforeEach(() => {
  motor = new MotorDeFalaFalso();
  janelas = [];
  vi.stubGlobal("speechSynthesis", motor);
  vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
  vi.spyOn(fala, "existeTranscricaoDeFala").mockReturnValue(true);
  vi.spyOn(fala, "pedirPermissaoDoMicrofone").mockResolvedValue(true);
  vi.spyOn(fala, "escutarPorJanela").mockImplementation((retornos) => {
    const encerrar = vi.fn();
    janelas.push({ aoParcial: retornos.aoParcial, aoEncerrar: retornos.aoEncerrar, encerrar });
    return encerrar;
  });
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("a sondagem fala, escuta e segue sozinha (RF-05-97)", () => {
  it("terminada a fala, a janela abre com a barra do tempo e a transcrição à vista", async () => {
    const usuario = userEvent.setup();
    await renderizar(sondagem());
    await ligarOAudio(usuario);

    // Antes do fim da fala, nada escuta.
    expect(janelas).toHaveLength(0);
    await terminarAFala();

    expect(janelas).toHaveLength(1);
    expect(
      screen.getByRole("progressbar", { name: "Tempo para responder" }),
    ).toBeInTheDocument();
    await act(async () => janelas[0].aoParcial("foto"));
    expect(screen.getByText("Você disse: foto")).toBeInTheDocument();
  });

  it("ao fim da janela a resposta é marcada e a pergunta seguinte é falada", async () => {
    const usuario = userEvent.setup();
    await renderizar(sondagem());
    await ligarOAudio(usuario);
    await terminarAFala();

    await act(async () => janelas[0].aoEncerrar("foto síntese"));

    expect(screen.getByText("Quanto é 2 + 2?")).toBeInTheDocument();
    expect(motor.ditos.at(-1)?.text).toContain("Quanto é 2 + 2?");
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Pergunta anterior" }));
    expect(screen.getByRole("radio", { name: "Fotossíntese" })).toBeChecked();
  });

  it("na última pergunta a sondagem é submetida sozinha, com a forma de cada resposta", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 1,
      total: 2,
      comprovacao_entregue: null,
    });
    const aoDesbloquear = vi.fn();
    const usuario = userEvent.setup();
    await renderizar(sondagem({ aoDesbloquear }));
    await ligarOAudio(usuario);
    await terminarAFala();
    await act(async () => janelas[0].aoEncerrar("letra a"));
    await terminarAFala();

    // Fala sem correspondência segue literal (`RF-05-98`).
    await act(async () => janelas[1].aoEncerrar("não sei"));

    expect(submeter).toHaveBeenCalledWith(
      "sondagem-1",
      [
        { pergunta_id: "p1", alternativa_escolhida: 1 },
        { pergunta_id: "p2", resposta_falada: "não sei" },
      ],
      "token-do-guerreiro",
      {},
    );
    expect(aoDesbloquear).toHaveBeenCalled();
  });

  it("silêncio segue como resposta vazia, e a sondagem avança", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 0,
      total: 2,
      comprovacao_entregue: null,
    });
    const usuario = userEvent.setup();
    await renderizar(sondagem());
    await ligarOAudio(usuario);
    await terminarAFala();
    await act(async () => janelas[0].aoEncerrar(""));
    await terminarAFala();
    await act(async () => janelas[1].aoEncerrar(""));

    expect(submeter.mock.calls[0][1]).toEqual([
      { pergunta_id: "p1", resposta_falada: "" },
      { pergunta_id: "p2", resposta_falada: "" },
    ]);
  });

  it("o toque durante a janela fecha o microfone e vale a alternativa tocada", async () => {
    const usuario = userEvent.setup();
    await renderizar(sondagem());
    await ligarOAudio(usuario);
    await terminarAFala();

    await usuario.click(screen.getByRole("radio", { name: "Respiração" }));

    expect(janelas[0].encerrar).toHaveBeenCalledWith(true);
    expect(screen.getByRole("radio", { name: "Respiração" })).toBeChecked();
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument();
  });

  it("a Sondagem liga a resposta por voz no desafio que ela monta", async () => {
    const usuario = userEvent.setup();
    await renderizar(
      <Sondagem
        missaoId="sondagem-1"
        desafio={SONDAGEM}
        aoResponder={vi.fn()}
        submissaoLigada
      />,
    );
    await ligarOAudio(usuario);
    await terminarAFala();

    expect(janelas).toHaveLength(1);
  });
});

describe("fora da sondagem, ou sem áudio, nada escuta (RN-05-54)", () => {
  it("o desafio de desbloqueio não abre a janela", async () => {
    const usuario = userEvent.setup();
    await renderizar(sondagem({ respostaPorVoz: false }));
    await ligarOAudio(usuario);
    await terminarAFala();

    expect(janelas).toHaveLength(0);
    expect(screen.queryByRole("progressbar")).not.toBeInTheDocument();
  });

  it("com o áudio desligado a sondagem é por toque, como antes", async () => {
    await renderizar(sondagem());
    await terminarAFala();

    expect(janelas).toHaveLength(0);
    expect(fala.pedirPermissaoDoMicrofone).not.toHaveBeenCalled();
  });

  it("sem transcrição no navegador a sondagem é por toque", async () => {
    vi.mocked(fala.existeTranscricaoDeFala).mockReturnValue(false);
    const usuario = userEvent.setup();
    await renderizar(sondagem());
    await ligarOAudio(usuario);
    await terminarAFala();

    expect(janelas).toHaveLength(0);
  });

  it("com o microfone negado a sondagem é por toque, sem alarme", async () => {
    vi.mocked(fala.pedirPermissaoDoMicrofone).mockResolvedValue(false);
    const usuario = userEvent.setup();
    await renderizar(sondagem());
    await ligarOAudio(usuario);
    await terminarAFala();

    expect(janelas).toHaveLength(0);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("a barra mede o tempo da janela, não as perguntas (RF-05-97)", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("enche em 5 s e recomeça vazia na pergunta seguinte", () => {
    vi.useFakeTimers();
    const { rerender } = render(<JanelaDeEscuta key="p1" duracaoMs={5000} transcricao="" />);
    const barra = () => screen.getByRole("progressbar", { name: "Tempo para responder" });

    expect(barra()).toHaveAttribute("value", "0");
    act(() => {
      vi.advanceTimersByTime(2500);
    });
    expect(Number(barra().getAttribute("value"))).toBeGreaterThanOrEqual(2400);
    act(() => {
      vi.advanceTimersByTime(2500);
    });
    expect(barra()).toHaveAttribute("value", "5000");
    expect(barra()).toHaveAttribute("max", "5000");

    rerender(<JanelaDeEscuta key="p2" duracaoMs={5000} transcricao="" />);
    expect(barra()).toHaveAttribute("value", "0");
  });
});
