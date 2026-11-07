import { afterEach, describe, expect, it, vi } from "vitest";
import {
  escutarPorJanela,
  existeTranscricaoDeFala,
  iniciarTranscricao,
  pedirPermissaoDoMicrofone,
} from "./fala";

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

function resultado(...falas: string[]) {
  return { results: falas.map((fala) => [{ transcript: fala }]) };
}

describe("escutarPorJanela (RF-05-97, RF-05-98, RN-05-54)", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("escuta em pt-BR, contínuo e com parciais, e para no prazo", () => {
    vi.useFakeTimers();
    instalarReconhecimentoFalso();
    const aoEncerrar = vi.fn();
    escutarPorJanela({ duracaoMs: 5000, aoParcial: vi.fn(), aoEncerrar });
    const reconhecimento = ultimoReconhecimento as ReconhecimentoFalso;
    expect(reconhecimento.lang).toBe("pt-BR");
    expect(reconhecimento.continuous).toBe(true);
    expect(reconhecimento.interimResults).toBe(true);

    vi.advanceTimersByTime(4999);
    expect(reconhecimento.parado).toBe(false);
    vi.advanceTimersByTime(1);
    expect(reconhecimento.parado).toBe(true);
    expect(aoEncerrar).toHaveBeenCalledWith("");
  });

  it("repassa o parcial e entrega o texto acumulado uma vez só", () => {
    vi.useFakeTimers();
    instalarReconhecimentoFalso();
    const aoParcial = vi.fn();
    const aoEncerrar = vi.fn();
    escutarPorJanela({ duracaoMs: 5000, aoParcial, aoEncerrar });
    const reconhecimento = ultimoReconhecimento as ReconhecimentoFalso;

    reconhecimento.onresult?.(resultado("letra"));
    reconhecimento.onresult?.(resultado("letra", " b"));
    expect(aoParcial).toHaveBeenLastCalledWith("letra b");

    reconhecimento.onend?.();
    expect(aoEncerrar).not.toHaveBeenCalled();
    vi.advanceTimersByTime(5000);
    reconhecimento.onend?.();
    expect(aoEncerrar).toHaveBeenCalledTimes(1);
    expect(aoEncerrar).toHaveBeenCalledWith("letra b");
  });

  it("silêncio e erro entregam vazio, sem lançar", () => {
    vi.useFakeTimers();
    instalarReconhecimentoFalso();
    const aoEncerrar = vi.fn();
    escutarPorJanela({ duracaoMs: 5000, aoParcial: vi.fn(), aoEncerrar });
    ultimoReconhecimento?.onerror?.({ error: "no-speech" });
    vi.advanceTimersByTime(5000);
    expect(aoEncerrar).toHaveBeenCalledWith("");
  });

  it("o encerrador é idempotente, e descartar fecha sem entregar", () => {
    vi.useFakeTimers();
    instalarReconhecimentoFalso();
    const aoEncerrar = vi.fn();
    const encerrar = escutarPorJanela({ duracaoMs: 5000, aoParcial: vi.fn(), aoEncerrar });
    encerrar(true);
    encerrar();
    vi.advanceTimersByTime(5000);
    expect(ultimoReconhecimento?.parado).toBe(true);
    expect(aoEncerrar).not.toHaveBeenCalled();
  });
});

describe("pedirPermissaoDoMicrofone (RN-05-54)", () => {
  it("pede o microfone e para as faixas na hora", async () => {
    const parar = vi.fn();
    const getUserMedia = vi.fn().mockResolvedValue({ getTracks: () => [{ stop: parar }] });
    vi.stubGlobal("navigator", { mediaDevices: { getUserMedia } });
    await expect(pedirPermissaoDoMicrofone()).resolves.toBe(true);
    expect(getUserMedia).toHaveBeenCalledWith({ audio: true });
    expect(parar).toHaveBeenCalledTimes(1);
  });

  it("negada ou sem a API, devolve falso sem lançar", async () => {
    vi.stubGlobal("navigator", {
      mediaDevices: { getUserMedia: vi.fn().mockRejectedValue(new Error("NotAllowedError")) },
    });
    await expect(pedirPermissaoDoMicrofone()).resolves.toBe(false);
    vi.stubGlobal("navigator", {});
    await expect(pedirPermissaoDoMicrofone()).resolves.toBe(false);
  });
});
