import { afterEach, describe, expect, it, vi } from "vitest";
import { existeTranscricaoDeFala, iniciarTranscricao } from "./fala";

class ReconhecimentoFalso {
  lang = "";
  continuous = true;
  interimResults = true;
  // biome-ignore lint/suspicious/noExplicitAny: espelha os eventos mínimos que fala.ts consome
  onresult: ((evento: any) => void) | null = null;
  // biome-ignore lint/suspicious/noExplicitAny: espelha os eventos mínimos que fala.ts consome
  onerror: ((evento: any) => void) | null = null;
  onend: (() => void) | null = null;
  parado = false;

  start() {}

  stop() {
    this.parado = true;
  }
}

let ultimoReconhecimento: ReconhecimentoFalso | null = null;

function instalarReconhecimentoFalso() {
  ultimoReconhecimento = null;
  class Construtor extends ReconhecimentoFalso {
    constructor() {
      super();
      ultimoReconhecimento = this;
    }
  }
  vi.stubGlobal("SpeechRecognition", Construtor);
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("existeTranscricaoDeFala (RF-04-39, RF-04-40)", () => {
  it("é falso sem a API do navegador", () => {
    expect(existeTranscricaoDeFala()).toBe(false);
  });

  it("é verdadeiro com a API do navegador", () => {
    instalarReconhecimentoFalso();
    expect(existeTranscricaoDeFala()).toBe(true);
  });
});

describe("iniciarTranscricao", () => {
  it("lança quando o navegador não oferece a API", () => {
    expect(() =>
      iniciarTranscricao({ aoTranscrever: vi.fn(), aoFalhar: vi.fn(), aoEncerrar: vi.fn() }),
    ).toThrow();
  });

  it("abre uma fala por vez, em pt-BR, sem resultado parcial", () => {
    instalarReconhecimentoFalso();
    iniciarTranscricao({ aoTranscrever: vi.fn(), aoFalhar: vi.fn(), aoEncerrar: vi.fn() });

    expect(ultimoReconhecimento?.lang).toBe("pt-BR");
    expect(ultimoReconhecimento?.continuous).toBe(false);
    expect(ultimoReconhecimento?.interimResults).toBe(false);
  });

  it("entrega a transcrição do resultado", () => {
    instalarReconhecimentoFalso();
    const aoTranscrever = vi.fn();
    iniciarTranscricao({ aoTranscrever, aoFalhar: vi.fn(), aoEncerrar: vi.fn() });

    ultimoReconhecimento?.onresult?.({
      results: { 0: { 0: { transcript: "o que é uma variável" }, length: 1 }, length: 1 },
    });

    expect(aoTranscrever).toHaveBeenCalledWith("o que é uma variável");
  });

  it("avisa a falha sem lançar exceção", () => {
    instalarReconhecimentoFalso();
    const aoFalhar = vi.fn();
    iniciarTranscricao({ aoTranscrever: vi.fn(), aoFalhar, aoEncerrar: vi.fn() });

    ultimoReconhecimento?.onerror?.({ error: "no-speech" });

    expect(aoFalhar).toHaveBeenCalledWith("no-speech");
  });

  it("chama aoEncerrar quando a fala termina sozinha", () => {
    instalarReconhecimentoFalso();
    const aoEncerrar = vi.fn();
    iniciarTranscricao({ aoTranscrever: vi.fn(), aoFalhar: vi.fn(), aoEncerrar });

    ultimoReconhecimento?.onend?.();

    expect(aoEncerrar).toHaveBeenCalled();
  });

  it("o encerrador fecha o microfone antes do fim natural da fala", () => {
    instalarReconhecimentoFalso();
    const encerrar = iniciarTranscricao({
      aoTranscrever: vi.fn(),
      aoFalhar: vi.fn(),
      aoEncerrar: vi.fn(),
    });

    encerrar();

    expect(ultimoReconhecimento?.parado).toBe(true);
  });

  it("o encerrador não faz nada depois que a fala já terminou sozinha", () => {
    instalarReconhecimentoFalso();
    const encerrar = iniciarTranscricao({
      aoTranscrever: vi.fn(),
      aoFalhar: vi.fn(),
      aoEncerrar: vi.fn(),
    });

    ultimoReconhecimento?.onend?.();
    encerrar();

    expect(ultimoReconhecimento?.parado).toBe(false);
  });
});
