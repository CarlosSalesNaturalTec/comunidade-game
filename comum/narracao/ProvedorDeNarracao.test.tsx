import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ProvedorDeNarracao, useNarracao, useNarrarAoEntrar } from "./ProvedorDeNarracao";

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

// A tela de teste: declara a narração dela e expõe os dois controles que a
// aplicação real tem — o alternador da tela inicial e o de ouvir o texto
// longo, que **não** depende do alternador.
function TelaDeTeste({ texto = "Tela de teste" }: { texto?: string | null }) {
  const { ligada, disponivel, alternarNarracao, ouvir } = useNarracao();
  useNarrarAoEntrar(texto ?? null);
  return (
    <>
      <button type="button" onClick={alternarNarracao}>
        {ligada ? "Desligar a narração" : "Ligar a narração"}
      </button>
      {disponivel && (
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
  it("nasce desligada, e nenhuma tela é falada sozinha", () => {
    const motor = instalarMotorFalso();
    renderizarComProvedor();

    expect(screen.getByRole("button", { name: "Ligar a narração" })).toBeInTheDocument();
    expect(motor.ditos).toHaveLength(0);
  });

  it("ligar já arma, e a tela seguinte fala — sem segundo controle", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    const { rerender } = renderizarComProvedor("Tela de teste");

    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));

    // O enunciado vazio é o armar, falado dentro do próprio gesto de ligar; e
    // a tela que já está montada passa a ser falada no mesmo ato, porque ligar
    // reavalia a narração dela.
    expect(motor.ditos.map((dito) => dito.text)).toEqual(["", "Tela de teste"]);

    rerender(
      <ProvedorDeNarracao>
        <TelaDeTeste texto="Quiz ao Vivo" />
      </ProvedorDeNarracao>,
    );

    expect(motor.ditos.map((dito) => dito.text)).toContain("Quiz ao Vivo");
    expect(screen.getByRole("button", { name: "Desligar a narração" })).toBeInTheDocument();
  });

  it("a escolha não é gravada em lugar algum", async () => {
    instalarMotorFalso();
    const usuario = userEvent.setup();
    renderizarComProvedor();

    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));

    expect(localStorage.length).toBe(0);
  });

  it("a recarga devolve a narração ao desligado", async () => {
    instalarMotorFalso();
    const usuario = userEvent.setup();
    const { unmount } = renderizarComProvedor();

    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));
    expect(screen.getByRole("button", { name: "Desligar a narração" })).toBeInTheDocument();

    // Recarregar a aplicação monta o provedor de novo, sem nada guardado de
    // onde ler a escolha anterior.
    unmount();
    renderizarComProvedor();

    expect(screen.getByRole("button", { name: "Ligar a narração" })).toBeInTheDocument();
  });

  it("desligada, nada fala sozinho, e nenhum alarme aparece", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    const { rerender } = renderizarComProvedor("Tela de teste");

    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));
    await usuario.click(screen.getByRole("button", { name: "Desligar a narração" }));

    rerender(
      <ProvedorDeNarracao>
        <TelaDeTeste texto="Quiz ao Vivo" />
      </ProvedorDeNarracao>,
    );

    expect(motor.ditos.map((dito) => dito.text)).not.toContain("Quiz ao Vivo");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("`localStorage` que lança não tem como derrubar a camada", () => {
    instalarMotorFalso();
    vi.spyOn(Storage.prototype, "getItem").mockImplementation(() => {
      throw new Error("dado de site bloqueado");
    });
    vi.spyOn(Storage.prototype, "setItem").mockImplementation(() => {
      throw new Error("dado de site bloqueado");
    });

    expect(() => renderizarComProvedor()).not.toThrow();
    expect(screen.getByRole("button", { name: "Ligar a narração" })).toBeInTheDocument();
  });
});

describe("o texto longo não depende do liga e desliga (documento 15 §5.1)", () => {
  it("o toque fala o conteúdo com a narração desligada", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    renderizarComProvedor(null);

    expect(screen.getByRole("button", { name: "Ligar a narração" })).toBeInTheDocument();
    expect(motor.ditos).toHaveLength(0);

    await usuario.click(screen.getByRole("button", { name: "Ouvir este texto" }));

    // O enunciado vazio é o armar, que o próprio toque dispara.
    expect(motor.ditos.map((dito) => dito.text)).toEqual(["", "O conteúdo longo da missão"]);
  });

  it("as telas continuam caladas depois de ouvir o texto longo", async () => {
    const motor = instalarMotorFalso();
    const usuario = userEvent.setup();
    const { rerender } = renderizarComProvedor(null);

    await usuario.click(screen.getByRole("button", { name: "Ouvir este texto" }));

    rerender(
      <ProvedorDeNarracao>
        <TelaDeTeste texto="Quiz ao Vivo" />
      </ProvedorDeNarracao>,
    );

    expect(motor.ditos.map((dito) => dito.text)).not.toContain("Quiz ao Vivo");
  });

  it("sem síntese no navegador o controle de ouvir não é oferecido, e nada lança", () => {
    expect(() => renderizarComProvedor()).not.toThrow();
    expect(screen.queryByRole("button", { name: "Ouvir este texto" })).not.toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
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

    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));
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
  });
});
