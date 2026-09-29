import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type {
  ApoiadorPublico,
  ComunidadePublica,
  GuerreiroPublico,
  MestrePublico,
  SeriePublica,
} from "../api/leituras";
import * as leituras from "../api/leituras";
import { esquecerConteudoInstitucional } from "../institucional/useConteudoInstitucional";
import { esquecerNecessidades } from "../necessidades/useNecessidades";

// Critérios de aceite do PRD-03 §12 para o convite: toda página individual traz
// a chamada "Quero participar"; clicando nela, a tela seguinte não cita a pessoa
// que estava sendo vista e leva ao pré-cadastro da App 08; pedir para favoritar
// chega à mesma porta; e recusar devolve à navegação sem gravar nada.

const NICK = "ZeBita";
const ID_DA_COMUNIDADE = "11111111-1111-1111-1111-111111111111";
const NOME_DA_COMUNIDADE = "Guerreira Zeferina";
const COMO_APOIAR = "Doações por PIX.\n\nChave PIX (CNPJ): 51.730.395/0001-19";

function guerreiro(): GuerreiroPublico {
  return {
    avatar: "avatar-de-teste",
    nick: NICK,
    badges: [{ familia: "de_nivel", poder: "Poder do Código" }],
    poderes: [{ poder: "Poder do Código", nivel: 3 }],
    pontos_regulares: 40,
    posicao_no_ranking: 1,
    criacoes: [],
  };
}

const ID_DO_MESTRE = "11111111-1111-4111-8111-111111111111";
const ID_DO_APOIADOR = "22222222-2222-4222-8222-222222222222";

const MESTRE: MestrePublico = {
  id: ID_DO_MESTRE,
  avatar: null,
  avatar_padrao: true,
  identificacao: { valor: "mestra_ana", tipo: "nick" },
  areas_de_habilidade: [],
  artefatos: [],
  trilhas_de_autoria: [],
  absorcoes: 0,
};

const APOIADOR: ApoiadorPublico = {
  id: ID_DO_APOIADOR,
  avatar: null,
  avatar_padrao: true,
  identificacao: { valor: "apoia_norte", tipo: "nick" },
  total_em_moedas: "12.00",
  nivel_de_sustento: 1,
  nome_do_nivel: "Quem começou",
  selos: [],
  desafios_propostos: [],
  artefatos: [],
};

function comLeituras() {
  const ficha: ComunidadePublica = {
    id: ID_DA_COMUNIDADE,
    nome: NOME_DA_COMUNIDADE,
    locais: [{ id: "raiz", nivel: "comunidade", rotulo: "Comunidade", local_pai_id: null }],
    tipos_de_coleta: [],
    guerreiros_vinculados: 23,
  };
  const serie: SeriePublica = { itens: [], proximo_cursor: null, recortes: [] };
  vi.spyOn(leituras, "listarGuerreiros").mockResolvedValue({
    itens: [guerreiro()],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "obterGuerreiroPorNick").mockResolvedValue(guerreiro());
  vi.spyOn(leituras, "listarCriacoes").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarRanking").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarPoderes").mockResolvedValue([]);
  vi.spyOn(leituras, "listarMestres").mockResolvedValue({ itens: [], proximo_cursor: null });
  vi.spyOn(leituras, "listarApoiadores").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(leituras, "obterMestrePorId").mockResolvedValue(MESTRE);
  vi.spyOn(leituras, "obterApoiadorPorId").mockResolvedValue(APOIADOR);
  vi.spyOn(leituras, "listarComunidades").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
    ciclo_rotulo: "Ciclo 01",
  });
  vi.spyOn(leituras, "obterComunidade").mockResolvedValue(ficha);
  vi.spyOn(leituras, "lerSerieDaComunidade").mockResolvedValue(serie);
  vi.spyOn(leituras, "lerCoberturaDeOds").mockResolvedValue([]);
  vi.spyOn(leituras, "listarNecessidades").mockResolvedValue([]);
  vi.spyOn(leituras, "lerConteudoInstitucional").mockResolvedValue([
    { secao: "quem-somos", texto: "Somos o projeto.", video_url: null },
    { secao: "contatos", texto: null, video_url: null },
    { secao: "como-apoiar", texto: COMO_APOIAR, video_url: null },
  ]);
}

describe("o convite ao acompanhamento", () => {
  beforeEach(() => {
    esquecerConteudoInstitucional();
    esquecerNecessidades();
    localStorage.clear();
    sessionStorage.clear();
    window.history.pushState(null, "", "/");
    comLeituras();
  });
  afterEach(() => vi.restoreAllMocks());

  it("a página do Guerreiro(a) traz a chamada e a ação de acompanhar (RF-03-39, RF-03-40)", async () => {
    window.history.pushState(null, "", `/guerreiros/${NICK}`);
    render(<App />);

    expect(await screen.findByRole("button", { name: "Quero participar" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Quero acompanhar" })).toBeVisible();
  });

  it("a página da comunidade traz a chamada e a ação de acompanhar (RF-03-39, RF-03-40)", async () => {
    window.history.pushState(null, "", `/comunidades/${ID_DA_COMUNIDADE}`);
    render(<App />);

    expect(await screen.findByRole("button", { name: "Quero participar" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Quero acompanhar" })).toBeVisible();
  });

  it("a página do Mestre traz a chamada e a ação de acompanhar (RF-03-39, RF-03-40)", async () => {
    window.history.pushState(null, "", `/mestres/${ID_DO_MESTRE}`);
    render(<App />);

    expect(await screen.findByRole("button", { name: "Quero participar" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Quero acompanhar" })).toBeVisible();
  });

  it("a página do Apoiador traz a chamada e a ação de acompanhar (RF-03-39, RF-03-40)", async () => {
    window.history.pushState(null, "", `/apoiadores/${ID_DO_APOIADOR}`);
    render(<App />);

    expect(await screen.findByRole("button", { name: "Quero participar" })).toBeVisible();
    expect(screen.getByRole("button", { name: "Quero acompanhar" })).toBeVisible();
  });

  it("acompanhar na página do Mestre chega à mesma porta (RF-03-40, RF-14-52)", async () => {
    window.history.pushState(null, "", `/mestres/${ID_DO_MESTRE}`);
    render(<App />);

    await userEvent.click(await screen.findByRole("button", { name: "Quero acompanhar" }));

    expect(window.location.pathname).toBe("/quero-participar");
  });

  it("a chamada convida a participar do projeto, e não a apoiar quem está na tela (RF-03-41, RN-03-25)", async () => {
    window.history.pushState(null, "", `/guerreiros/${NICK}`);
    render(<App />);

    const chamada = (await screen.findByRole("button", { name: "Quero participar" }))
      .parentElement as HTMLElement;
    expect(within(chamada).getByText(/sustentar o projeto — e não uma pessoa/)).toBeVisible();
    expect(
      within(chamada).queryByText(new RegExp(`apoiar .*${NICK}`, "i")),
    ).not.toBeInTheDocument();
    expect(within(chamada).getByText(/A vitrine não guarda favoritos/)).toBeVisible();
  });

  it("a porta não cita quem estava sendo visto, e o endereço não o carrega (RF-03-41, RN-03-25)", async () => {
    window.history.pushState(null, "", `/guerreiros/${NICK}`);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: "Quero participar" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Quero participar", level: 2 }),
    ).toBeVisible();
    expect(window.location.pathname).toBe("/quero-participar");
    expect(window.location.search).toBe("");
    expect(screen.queryByText(new RegExp(NICK))).not.toBeInTheDocument();
  });

  it("acompanhar chega à mesma porta que a chamada (RF-03-40)", async () => {
    window.history.pushState(null, "", `/comunidades/${ID_DA_COMUNIDADE}`);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: "Quero acompanhar" }),
    );

    expect(
      await screen.findByRole("heading", { name: "Quero participar", level: 2 }),
    ).toBeVisible();
    expect(window.location.pathname).toBe("/quero-participar");
    expect(screen.queryByText(new RegExp(NOME_DA_COMUNIDADE))).not.toBeInTheDocument();
  });

  it("a porta explica o papel do Apoiador e declara que nada cria acesso (RF-03-42, RN-03-17)", async () => {
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    const papel = await screen.findByRole("heading", { name: "O que é ser Apoiador" });
    const secao = papel.parentElement as HTMLElement;
    expect(within(secao).getByText(/aporta/)).toBeVisible();
    expect(within(secao).getByText(/propõe desafios extras/)).toBeVisible();
    expect(within(secao).getByText(/acompanha os favoritos/)).toBeVisible();
    expect(
      screen.getByText(
        /Nada aqui cria cadastro nem acesso\. Quem cadastra Apoiador é um Admin/,
      ),
    ).toBeVisible();
    expect(screen.getByText(/em até 7 dias/)).toBeVisible();
  });

  it("a porta não pede senha, documento nem login (RN-03-17, RF-03-61)", async () => {
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    await screen.findByRole("heading", { name: "O que é ser Apoiador" });
    expect(screen.queryByLabelText(/senha/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/cpf|cnpj|documento/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /entrar com/i })).not.toBeInTheDocument();
  });

  it("a porta oferece a chave PIX publicada, sem cadastro (RF-03-43, RF-03-46)", async () => {
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);

    expect(await screen.findByText(/51\.730\.395\/0001-19/)).toBeVisible();
  });

  it("recusar devolve à página de onde o visitante veio (RF-03-44)", async () => {
    window.history.pushState(null, "", `/guerreiros/${NICK}`);
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: "Quero participar" }),
    );
    await testeDeUsuario.click(
      await screen.findByRole("button", { name: "Não quero agora, voltar à vitrine" }),
    );

    expect(await screen.findByRole("heading", { name: NICK, level: 2 })).toBeVisible();
    expect(window.location.pathname).toBe(`/guerreiros/${NICK}`);
  });

  it("recusar na porta aberta por endereço direto devolve à raiz (RF-03-44)", async () => {
    window.history.pushState(null, "", "/quero-participar");
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(
      await screen.findByRole("button", { name: "Não quero agora, voltar à vitrine" }),
    );

    expect(window.location.pathname).toBe("/");
    expect(await screen.findByRole("heading", { name: "Quem somos", level: 2 })).toBeVisible();
  });
});
