import { afterEach, describe, expect, it, vi } from "vitest";
import {
  cancelar,
  enunciarFala,
  existeSinteseDeFala,
  type Fala,
  falar,
  vozPreferida,
} from "./narracao";

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

function voz(lang: string, localService: boolean, name = lang): SpeechSynthesisVoice {
  return { lang, localService, name, default: false, voiceURI: name } as SpeechSynthesisVoice;
}

// O jsdom não tem síntese de fala: o motor falso é instalado por
// `vi.stubGlobal`, no padrão de `comum/fala/fala.test.ts` (design — Risks).
function instalarMotorFalso(vozes: SpeechSynthesisVoice[] = [voz("pt-BR", true)]) {
  const motor = new MotorFalso(vozes);
  vi.stubGlobal("speechSynthesis", motor);
  vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
  return motor;
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("existeSinteseDeFala", () => {
  it("é falso sem a API do navegador", () => {
    expect(existeSinteseDeFala()).toBe(false);
  });

  it("é verdadeiro com a API do navegador", () => {
    instalarMotorFalso();
    expect(existeSinteseDeFala()).toBe(true);
  });
});

describe("vozPreferida (documento 15 §5.1, design — decisão 5)", () => {
  it("prefere a voz local entre as pt-BR, porque ela funciona sem rede", () => {
    instalarMotorFalso([voz("pt-BR", false, "rede"), voz("pt-BR", true, "local")]);
    expect(vozPreferida()?.name).toBe("local");
  });

  it("aceita `pt_BR`, como alguns aparelhos Android a escrevem", () => {
    instalarMotorFalso([voz("pt_BR", false, "android")]);
    expect(vozPreferida()?.name).toBe("android");
  });

  it("não havendo voz pt-BR alguma, não há voz — a camada cala", () => {
    instalarMotorFalso([voz("pt-PT", true), voz("en-US", true)]);
    expect(vozPreferida()).toBeNull();
  });

  it("sem a API do navegador, não há voz", () => {
    expect(vozPreferida()).toBeNull();
  });
});

describe("a fronteira do dado (documento 03 §§1.12, 12, design — decisão 2)", () => {
  it("fala o texto declarado pela tela", () => {
    const motor = instalarMotorFalso();
    falar({ texto: "Comunidade Game — Aula" }, voz("pt-BR", true));
    expect(motor.ditos.map((dito) => dito.text)).toEqual(["Comunidade Game — Aula"]);
  });

  it("substitui `{nick}` pelo nick do Guerreiro(a)", () => {
    expect(enunciarFala({ texto: "Oi, {nick}! Bora?", nick: "zeferina" })).toBe(
      "Oi, zeferina! Bora?",
    );
  });

  it("sem nick, o marcador some e a frase segue legível", () => {
    expect(enunciarFala({ texto: "Oi, {nick}! Bora?" })).toBe("Oi, ! Bora?");
  });

  it("nenhum outro dado pessoal alcança a síntese, ainda que a tela o entregue", () => {
    const motor = instalarMotorFalso();
    // O tipo `Fala` não tem campo para nome — entregá-lo exige burlar o
    // compilador, e nem assim ele é falado: a camada lê `texto` e `nick`.
    const comNome = {
      texto: "Oi, {nick}!",
      nick: "zeferina",
      nome: "Maria Zeferina da Silva",
      nascimento: "2019-04-02",
    } as Fala;
    falar(comNome, voz("pt-BR", true));
    expect(motor.ditos[0].text).toBe("Oi, zeferina!");
    expect(motor.ditos[0].text).not.toContain("Maria");
    expect(motor.ditos[0].text).not.toContain("2019");
  });

  it("o tipo recusa o nome no ponto de chamada", () => {
    const motor = instalarMotorFalso();
    // @ts-expect-error `Fala` admite só `texto` e `nick` — é o compilador
    // que impede o nome de chegar à narração (design — decisão 2).
    falar({ texto: "Oi!", nome: "Maria Zeferina da Silva" }, voz("pt-BR", true));
    expect(motor.ditos[0].text).toBe("Oi!");
  });
});

describe("falar", () => {
  it("fala em pt-BR, pela voz escolhida", () => {
    const motor = instalarMotorFalso();
    const escolhida = voz("pt-BR", true, "local");
    falar({ texto: "Quiz ao Vivo" }, escolhida);
    expect(motor.ditos[0].lang).toBe("pt-BR");
    expect(motor.ditos[0].voice).toBe(escolhida);
  });

  it("cancela a fala em curso antes de iniciar a seguinte", () => {
    const motor = instalarMotorFalso();
    falar({ texto: "Tela anterior" }, voz("pt-BR", true));
    falar({ texto: "Tela seguinte" }, voz("pt-BR", true));
    expect(motor.cancelamentos).toBe(2);
    expect(motor.ditos.map((dito) => dito.text)).toEqual(["Tela anterior", "Tela seguinte"]);
  });

  it("enunciado vazio não vira fala", () => {
    const motor = instalarMotorFalso();
    falar({ texto: "   " }, voz("pt-BR", true));
    expect(motor.ditos).toHaveLength(0);
  });

  it("sem a API do navegador, fica em silêncio e não lança", () => {
    expect(() => falar({ texto: "Oi" }, voz("pt-BR", true))).not.toThrow();
  });
});

describe("cancelar", () => {
  it("interrompe a fala em curso", () => {
    const motor = instalarMotorFalso();
    falar({ texto: "Tela anterior" }, voz("pt-BR", true));
    cancelar();
    expect(motor.cancelamentos).toBe(2);
  });

  it("sem a API do navegador, não lança", () => {
    expect(() => cancelar()).not.toThrow();
  });
});
