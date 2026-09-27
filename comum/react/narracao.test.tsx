import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { ProvedorDeNarracao, useNarracao } from "../narracao/ProvedorDeNarracao";
import { Aviso } from "./Aviso";
import { Cabecalho } from "./Cabecalho";

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

  getVoices() {
    return [
      {
        lang: "pt-BR",
        localService: true,
        name: "local",
        default: true,
        voiceURI: "local",
      } as SpeechSynthesisVoice,
    ];
  }

  speak(dito: EnunciadoFalso) {
    this.ditos.push(dito);
  }

  cancel() {}

  addEventListener() {}

  removeEventListener() {}
}

function instalarMotorFalso() {
  const motor = new MotorFalso();
  vi.stubGlobal("speechSynthesis", motor);
  vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
  return motor;
}

// A narração só fala depois do gesto que a arma: o botão está aqui para que
// cada teste passe por ele antes de montar a tela que fala.
function Armador() {
  const { armarNarracao } = useNarracao();
  return (
    <button type="button" onClick={armarNarracao}>
      Iniciar a narração
    </button>
  );
}

function renderizarArmada(tela: React.ReactNode) {
  const resultado = render(
    <ProvedorDeNarracao>
      <Armador />
    </ProvedorDeNarracao>,
  );
  screen.getByRole("button", { name: "Iniciar a narração" }).click();
  resultado.rerender(
    <ProvedorDeNarracao>
      <Armador />
      {tela}
    </ProvedorDeNarracao>,
  );
  return resultado;
}

// O enunciado vazio do armar não é fala: sai da conta.
function ditos(motor: MotorFalso): string[] {
  return motor.ditos.map((dito) => dito.text).filter((texto) => texto !== "");
}

afterEach(() => {
  vi.unstubAllGlobals();
  localStorage.clear();
});

describe("Cabecalho (documento 15 §5.1, design — decisão 4)", () => {
  it("fala o título da tela ao entrar nela", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(<Cabecalho titulo="Quiz ao Vivo" />);
    expect(ditos(motor)).toEqual(["Quiz ao Vivo"]);
  });

  it("o subtítulo não é narrado — é onde mora a interpolação", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(
      <Cabecalho titulo="Comunidade Game — Aula" subtitulo="O que você quer fazer?" />,
    );
    expect(ditos(motor)).toEqual(["Comunidade Game — Aula"]);
  });

  it("a narração declarada substitui o que se ouve, sem mudar o que está escrito", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(
      <Cabecalho
        titulo="Medição do limiar"
        narracao={{ texto: "Oi, {nick}!", nick: "zeferina" }}
      />,
    );
    expect(ditos(motor)).toEqual(["Oi, zeferina!"]);
    expect(screen.getByRole("heading", { name: "Medição do limiar" })).toBeInTheDocument();
  });

  it("o cabeçalho calado aparece na tela e não é narrado", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(<Cabecalho titulo="Quiz ao Vivo" narracao={null} />);
    expect(ditos(motor)).toEqual([]);
    expect(screen.getByRole("heading", { name: "Quiz ao Vivo" })).toBeInTheDocument();
  });

  it("o título escrito não é escondido do leitor de tela (design — decisão 8)", () => {
    instalarMotorFalso();
    renderizarArmada(<Cabecalho titulo="Quiz ao Vivo" />);
    expect(screen.getByRole("heading", { name: "Quiz ao Vivo" })).not.toHaveAttribute(
      "aria-hidden",
    );
  });
});

describe("Aviso", () => {
  it("fala o rótulo e o texto do aviso ao entrar na tela", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(<Aviso tipo="atencao">Não há aula agendada para agora.</Aviso>);
    expect(ditos(motor)).toEqual(["Atenção: Não há aula agendada para agora."]);
  });

  it("o aviso calado aparece na tela e não é narrado", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(
      <Aviso tipo="erro" narracao={null}>
        Esse arquivo não abriu agora.
      </Aviso>,
    );
    expect(ditos(motor)).toEqual([]);
    expect(screen.getByRole("alert")).toBeInTheDocument();
  });

  it("conteúdo que não é texto simples só fala com narração declarada", () => {
    const motor = instalarMotorFalso();
    renderizarArmada(
      <Aviso tipo="andamento">
        Veja <button type="button">o que a gente coleta</button>.
      </Aviso>,
    );
    expect(ditos(motor)).toEqual([]);
  });
});

describe("sem provedor montado, nada fala (design — decisão 3)", () => {
  it("o cabeçalho e o aviso da App 05 seguem como estavam", () => {
    const motor = instalarMotorFalso();
    render(
      <>
        <Cabecalho titulo="Minha trilha" />
        <Aviso tipo="andamento">Essa missão é opcional.</Aviso>
      </>,
    );
    expect(ditos(motor)).toEqual([]);
  });
});
