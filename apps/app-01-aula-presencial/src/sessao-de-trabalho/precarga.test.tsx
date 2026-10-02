import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import * as biometria from "comum/biometria";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App, { CHAVE_DE_SESSAO_DE_TRABALHO } from "../App";
import * as aulasApi from "../api/aulas";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: ({
      aoReceberIdToken,
    }: {
      aoReceberIdToken: (t: string) => void;
    }) => (
      <button type="button" onClick={() => aoReceberIdToken("id-token-de-teste")}>
        Entrar com Google
      </button>
    ),
  };
});

/** Uma promessa que o teste resolve quando quiser: é assim que se observa a
 * tela **durante** a pré-carga, e não só depois dela. */
function promessaControlada<T>() {
  let resolver!: (valor: T) => void;
  const promessa = new Promise<T>((cumprir) => {
    resolver = cumprir;
  });
  return { promessa, resolver };
}

function darMestreComAula() {
  vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
    token: "token-do-mestre",
    expira_em: new Date().toISOString(),
    papel: "mestre",
  });
  vi.spyOn(sessaoApi, "eu").mockResolvedValue({
    persona_id: "mestre-1",
    papel: "mestre",
    permissoes: {},
  });
  vi.spyOn(aulasApi, "listarAulasVigentes").mockResolvedValue({
    itens: [
      {
        id: "aula-1",
        comunidade_virtual_id: "comunidade-1",
        inicio_em: "2026-08-24T10:00:00-03:00",
        fim_em: "2026-08-24T12:00:00-03:00",
      },
    ],
    proximo_cursor: null,
  });
}

async function entrarComoMestre() {
  const usuario = userEvent.setup();
  await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));
}

beforeEach(() => {
  limparToken(CHAVE_DE_SESSAO_DE_TRABALHO);
  limparToken("app-01:sessao-guerreiro");
  sessionStorage.removeItem("app-01:sessao-trabalho:aula");
  darMestreComAula();
});

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
  sessionStorage.clear();
  localStorage.clear();
});

describe("pré-carga dos modelos de biometria", () => {
  it("começa ao abrir a sessão de trabalho, havendo rede", async () => {
    render(<App />);
    await entrarComoMestre();

    await waitFor(() => expect(biometria.precarregarModelos).toHaveBeenCalled());
  });

  it("não começa sem rede, e a aplicação segue operando", async () => {
    render(<App />);
    window.dispatchEvent(new Event("offline"));
    await entrarComoMestre();

    expect(await screen.findByText(/operando sem conexão/i)).toBeInTheDocument();
    expect(biometria.precarregarModelos).not.toHaveBeenCalled();
  });

  // O caso que impede o indicador de virar portão numa mudança futura: o
  // pedido original era exatamente isto — menu só depois do download —, e
  // contraria o documento 03 §3.4 (`RF-04-75`).
  it("a tela inicial aparece e opera com a pré-carga em andamento", async () => {
    const { promessa } = promessaControlada<boolean>();
    vi.spyOn(biometria, "precarregarModelos").mockReturnValue(promessa);

    render(<App />);
    await entrarComoMestre();

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
  });

  it("o andamento é dito por modelo carregado, e não em percentual", async () => {
    const { promessa, resolver } = promessaControlada<boolean>();
    vi.spyOn(biometria, "precarregarModelos").mockReturnValue(promessa);
    vi.spyOn(biometria, "andamentoDosModelos").mockReturnValue({ carregados: 2, total: 5 });

    render(<App />);
    await entrarComoMestre();

    const andamento = await screen.findByText(/carregando modelos de reconhecimento facial/i);
    expect(andamento).toHaveTextContent("2 de 5");
    expect(andamento.textContent).not.toMatch(/%/);
    // Informação, nunca erro: o aviso de andamento é `role="status"`.
    expect(andamento.closest('[role="status"]')).not.toBeNull();

    resolver(true);
    await waitFor(() =>
      expect(
        screen.queryByText(/carregando modelos de reconhecimento facial/i),
      ).not.toBeInTheDocument(),
    );
  });

  // A falha é dita, e **não interrompe**: por isso não usa o `Aviso` em
  // vermelho, cujos dois tipos são `role="alert"` (decisão do fundador de
  // 2026-10-02).
  it("a falha é dita em região de status, nunca em alerta", async () => {
    vi.spyOn(biometria, "precarregarModelos").mockResolvedValue(false);

    render(<App />);
    await entrarComoMestre();

    const falha = await screen.findByText(/não foi possível carregar os modelos/i);
    expect(falha.closest('[role="status"]')).not.toBeNull();
    expect(falha.closest('[role="alert"]')).toBeNull();
  });

  // A falha não vem do `Aviso`, que narra por omissão: ela pede a fala à mão.
  // Este caso é o que impede a narração de se perder numa refatoração
  // (documento 15 §5.1).
  it("a narração fala a falha quando está ativada", async () => {
    class EnunciadoFalso {
      lang = "";
      voice: SpeechSynthesisVoice | null = null;
      text: string;
      constructor(text: string) {
        this.text = text;
      }
    }
    class MotorDeFalaFalso {
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
    const motor = new MotorDeFalaFalso();
    vi.stubGlobal("speechSynthesis", motor);
    vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
    vi.spyOn(biometria, "precarregarModelos").mockResolvedValue(false);

    render(<App />);
    // O navegador não fala antes de um gesto: este é o gesto.
    await userEvent
      .setup()
      .click(await screen.findByRole("button", { name: "Iniciar a narração das telas" }));
    await entrarComoMestre();

    await screen.findByText(/não foi possível carregar os modelos/i);
    await waitFor(() =>
      expect(motor.ditos.map((dito) => dito.text)).toContain(
        "Não foi possível carregar os modelos de reconhecimento facial.",
      ),
    );
  });

  it("a falha não impede a tela inicial nem os caminhos dela", async () => {
    vi.spyOn(biometria, "precarregarModelos").mockResolvedValue(false);

    render(<App />);
    await entrarComoMestre();

    expect(
      await screen.findByText(/não foi possível carregar os modelos/i),
    ).toBeInTheDocument();
    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
  });
});
