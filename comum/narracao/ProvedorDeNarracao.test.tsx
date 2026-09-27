import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  CHAVE_DA_NARRACAO_NO_APARELHO,
  ProvedorDeNarracao,
  useNarracao,
  useNarrarAoEntrar,
} from "./ProvedorDeNarracao";

class EnunciadoFalso {
  lang = "";
  voice: SpeechSynthesisVoice | null = null;
  text: string;

  constructor(text: string) {
    this.text = text;
  }
}

class MotorFalso {
  ditos: EnunciadoFalso[] = [];
  cancelamentos = 0;

  vozes: SpeechSynthesisVoice[];

  constructor(vozes: SpeechSynthesisVoice[]) {
    this.vozes = vozes;
  }

  getVoices() {
    return this.vozes;
  }

  speak(dito: EnunciadoFalso) {
    this.ditos.push(dito);
  }

  cancel() {
    this.cancelamentos += 1;
  }

  addEventListener() {}

  removeEventListener() {}
}

function vozPtBr(): SpeechSynthesisVoice {
  return {
    lang: "pt-BR",
    localService: true,
    name: "local",
    default: true,
    voiceURI: "local",
  } as SpeechSynthesisVoice;
}

function instalarMotorFalso(vozes: SpeechSynthesisVoice[] = [vozPtBr()]) {
  const motor = new MotorFalso(vozes);
  vi.stubGlobal("speechSynthesis", motor);
  vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
  return motor;
}

// A tela de teste: declara a narração dela e expõe os controles que a
// aplicação real põe na tela inicial e na primeira interação.
function TelaDeTeste({ texto = "Tela de teste" }: { texto?: string | null }) {
  const { ligada, armada, disponivel, alternarNarracao, armarNarracao, ouvir } = useNarracao();
  useNarrarAoEntrar(texto ?? null);
  return (
    <>
      <button type="button" onClick={alternarNarracao}>
        {ligada ? "Desligar a narração" : "Ligar a narração"}
      </button>
      {ligada && !armada && disponivel && (
        <button type="button" onClick={armarNarracao}>
          Iniciar a narração
        </button>
      )}
      {ligada && (
        <button type="button" onClick={() => ouvir({ texto: "O conteúdo longo da missão" })}>
          Ouvir este texto
        </button>
      )}
    </>
  );
}

function renderizarComProvedor(texto?: string | null) {
  return render(
    <ProvedorDeNarracao>
      <TelaDeTeste texto={texto} />
    </ProvedorDeNarracao>,
  );
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
  localStorage.clear();
});

describe("o liga e desliga do aparelho (documento 15 §5.1)", () => {
  it("nasce ligada no aparelho onde ninguém escolheu", () => {
    instalarMotorFalso();
    renderizarComProvedor();
    expect(screen.getByRole("button", { name: "Desligar a narração" })).toBeInTheDocument();
  });

  it("a escolha de desligar fica guardada no aparelho", async () => {
    instalarMotorFalso();
    const usuario = userEvent.setup();
    renderizarComProvedor();

    await usuario.click(screen.getByRole("button", { name: "Desligar a narração" }));

    expect(localStorage.getItem(CHAVE_DA_NARRACAO_NO_APARELHO)).toBe("desligada");
    expect(screen.getByRole("button", { name: "Ligar a narração" })).toBeInTheDocument();
  });

  it("abre desligada onde o aparelho guardou a escolha de desligar", () => {
    instalarMotorFalso();
    localStorage.setItem(CHAVE_DA_NARRACAO_NO_APARELHO, "desligada");
    renderizarComProvedor();
    expect(screen.getByRole("button", { name: "Ligar a narração" })).toBeInTheDocument();
  });

  it("`localStorage` que lança não derruba a camada — e ela nasce ligada", () => {
    instalarMotorFalso();
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("dado de site bloqueado");
    });
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("dado de site bloqueado");
    });

    expect(() => renderizarComProvedor()).not.toThrow();
    expect(screen.getByRole("button", { name: "Desligar a narração" })).toBeInTheDocument();
  });
});

describe("o gesto que arma a narração (design — decisão 6)", () => {
  it("carregada e sem gesto, nada fala, e o iniciar é oferecido", () => {
    const motor = instalarMotorFalso();
    renderizarComProvedor();

    expect(motor.ditos).toHaveLength(0);
    expect(screen.getByRole("button", { name: "Iniciar a narração" })).toBeInTheDocument();
  });

  it("acionado o iniciar, a tela seguinte fala o que declarou", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    const { rerender } = renderizarComProvedor("Tela de teste");

    await usuario.click(screen.getByRole("button", { name: "Iniciar a narração" }));

    rerender(
      <ProvedorDeNarracao>
        <TelaDeTeste texto="Quiz ao Vivo" />
      </ProvedorDeNarracao>,
    );

    expect(motor.ditos.map((dito) => dito.text)).toContain("Quiz ao Vivo");
    expect(
      screen.queryByRole("button", { name: "Iniciar a narração" }),
    ).not.toBeInTheDocument();
  });

  it("desligada, não há o que iniciar nem o que ouvir, e nada fala", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    renderizarComProvedor();

    await usuario.click(screen.getByRole("button", { name: "Desligar a narração" }));

    expect(
      screen.queryByRole("button", { name: "Iniciar a narração" }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Ouvir este texto" })).not.toBeInTheDocument();
    expect(motor.ditos).toHaveLength(0);
  });

  it("sem síntese no navegador, o iniciar não é oferecido e nada lança", () => {
    expect(() => renderizarComProvedor()).not.toThrow();
    expect(
      screen.queryByRole("button", { name: "Iniciar a narração" }),
    ).not.toBeInTheDocument();
  });
});

describe("o texto longo espera o toque (documento 15 §5.1)", () => {
  it("o toque fala o conteúdo e arma a narração de vez", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    renderizarComProvedor(null);

    expect(motor.ditos).toHaveLength(0);

    await usuario.click(screen.getByRole("button", { name: "Ouvir este texto" }));

    expect(motor.ditos.map((dito) => dito.text)).toEqual(["O conteúdo longo da missão"]);
    expect(
      screen.queryByRole("button", { name: "Iniciar a narração" }),
    ).not.toBeInTheDocument();
  });
});

describe("sem voz pt-BR, a camada cala sem alarme (design — decisão 5)", () => {
  it("nada é falado e nenhuma mensagem de erro aparece", async () => {
    const motor = instalarMotorFalso([
      {
        lang: "en-US",
        localService: true,
        name: "en",
        default: true,
        voiceURI: "en",
      } as SpeechSynthesisVoice,
    ]);
    const usuario = userEvent.setup();
    renderizarComProvedor();

    await usuario.click(screen.getByRole("button", { name: "Iniciar a narração" }));
    await usuario.click(screen.getByRole("button", { name: "Ouvir este texto" }));

    // Só o enunciado vazio do armar — nenhuma fala, e nenhum aviso na tela.
    expect(motor.ditos.map((dito) => dito.text)).toEqual([""]);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("sem provedor montado a camada é inerte (design — decisão 3)", () => {
  it("nada fala, e nenhum controle de ouvir é oferecido", () => {
    const motor = instalarMotorFalso();
    render(<TelaDeTeste />);

    expect(motor.ditos).toHaveLength(0);
    expect(screen.queryByRole("button", { name: "Ouvir este texto" })).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Iniciar a narração" }),
    ).not.toBeInTheDocument();
  });
});
