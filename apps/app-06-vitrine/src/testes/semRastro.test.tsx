import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as leituras from "../api/leituras";
import { lerDoNucleo } from "../api/nucleo";
import { esquecerConteudoInstitucional } from "../institucional/useConteudoInstitucional";
import { esquecerNecessidades } from "../necessidades/useNecessidades";
import App from "./TelaDaVitrine";

// A chave e o endereço do núcleo entram como a produção os entrega — por
// `../api/configuracao` —, e **não** por uma chamada de configuração feita no
// próprio teste: era ela que fornecia o que a produção não fornecia, e por isso
// este arquivo passava enquanto toda seção da vitrine falhava no navegador
// (design — decisão 5).
vi.mock("../api/configuracao", async () => {
  const real =
    await vi.importActual<typeof import("../api/configuracao")>("../api/configuracao");
  return {
    ...real,
    CHAVE_DE_APLICACAO: "chave-da-vitrine",
    URL_DO_NUCLEO: "https://nucleo.example.org",
  };
});

describe("a vitrine não deixa rastro no aparelho", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    localStorage.clear();
    sessionStorage.clear();
  });
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("uma visita inteira não guarda nada (RF-03-51, RF-03-60, RN-03-22)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Gestores públicos" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Apoiador" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: /fechar/i }));

    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });

  it("acompanhar, escolher modalidade e recusar não guardam favorito nenhum (RF-03-38, RN-03-15, RN-03-16)", async () => {
    esquecerConteudoInstitucional();
    esquecerNecessidades();
    vi.spyOn(leituras, "listarNecessidades").mockResolvedValue([]);
    vi.spyOn(leituras, "lerConteudoInstitucional").mockResolvedValue([
      { secao: "quem-somos", texto: "Somos o projeto.", video_url: null },
      { secao: "contatos", texto: null, video_url: null },
      { secao: "como-apoiar", texto: "Chave PIX: uma-chave", video_url: null },
    ]);
    vi.spyOn(leituras, "obterGuerreiroPorNick").mockResolvedValue({
      avatar: "avatar-de-teste",
      nick: "ZeBita",
      badges: [],
      poderes: [],
      pontos_regulares: 10,
      posicao_no_ranking: 1,
      criacoes: [],
    });
    window.history.pushState(null, "", "/guerreiros/ZeBita");
    const tela = render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: "Quero acompanhar" }),
    );
    await testeDeUsuario.click(await screen.findByRole("button", { name: "Divulgação" }));
    await testeDeUsuario.click(
      screen.getByRole("button", { name: "Não quero agora, voltar à vitrine" }),
    );

    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");

    // Recarregada, a vitrine está idêntica à primeira visita: nenhuma pessoa
    // acompanhada, nenhuma modalidade lembrada.
    tela.unmount();
    esquecerConteudoInstitucional();
    esquecerNecessidades();
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    expect(await screen.findByRole("button", { name: "Dinheiro" })).toBeVisible();
    expect(screen.queryByText("ZeBita")).not.toBeInTheDocument();
    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
  });
});

describe("a chamada ao núcleo leva a chave e nenhuma credencial de persona", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("o cabeçalho de sessão nunca é enviado (RN-03-33)", async () => {
    const buscar = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify([]), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await lerDoNucleo("/v1/vitrine/guerreiros");

    const [, opcoes] = buscar.mock.calls[0];
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-da-vitrine");
    expect(cabecalhos.Authorization).toBeUndefined();
  });
});
