import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as cartaApi from "comum/carta/api";
import * as trilhaComumApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { MinhaCarteira } from "./MinhaCarteira";

vi.mock("comum/pontuacao", async () => {
  const real = await vi.importActual<typeof import("comum/pontuacao")>("comum/pontuacao");
  return { ...real, lerMeuHistoricoDePontuacao: vi.fn() };
});

import { lerMeuHistoricoDePontuacao } from "comum/pontuacao";

const CHAVE_DE_SESSAO = "app-05:teste-minha-carteira";

async function renderizar(divulgacaoAutorizada?: boolean) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  // A carta do próprio Guerreiro(a) vem à frente da carteira e tem teste
  // próprio em `MinhaCarta.test.tsx`; aqui basta que ela não peça rede: sem
  // comunidade não há carta, e a Área apresenta o que tem em outra forma.
  vi.spyOn(cartaApi, "obterMinhaPosicaoNoRanking").mockResolvedValue({
    minha_posicao: { posicao: 1, pontos_regulares: 0 },
  });
  vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
  vi.spyOn(cartaApi, "obterProgressoDaCarta").mockResolvedValue([]);
  vi.spyOn(cartaApi, "obterPortfolioDaCarta").mockResolvedValue([]);
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    divulgacao_autorizada: divulgacaoAutorizada,
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <MinhaCarteira />
      </ProvedorDeSessao>,
    );
  });
}

/** Como `renderizar`, devolvendo o container para as asserções de composição. */
async function renderizarRetornando() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(cartaApi, "obterMinhaPosicaoNoRanking").mockResolvedValue({
    minha_posicao: { posicao: 1, pontos_regulares: 0 },
  });
  vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
  vi.spyOn(cartaApi, "obterProgressoDaCarta").mockResolvedValue([]);
  vi.spyOn(cartaApi, "obterPortfolioDaCarta").mockResolvedValue([]);
  vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
    acumulado: 40,
    saldo_disponivel: 10,
  });
  vi.spyOn(cartaApi, "obterSaldoParaTrocar").mockResolvedValue({ saldo_disponivel: 10 });
  // Com nick e avatar a variante do documento 11 §8.2 fecha, e a carta se
  // apresenta de fato no palco — sem eles, o que ocupa o primeiro plano é o
  // aviso de carta incompleta, e nenhuma asserção sobre a carta valeria.
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    divulgacao_autorizada: true,
    nick: "Zeferina",
    avatar: '{"v":1,"tom":"t3"}',
  });
  let renderizado!: ReturnType<typeof render>;
  await act(async () => {
    renderizado = render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <MinhaCarteira />
      </ProvedorDeSessao>,
    );
  });
  return renderizado;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("carteira de pontos extras", () => {
  it("mostra o acumulado e o saldo disponível separados, sem soma", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 30,
      saldo_disponivel: 18,
    });

    await renderizar(true);

    expect(await screen.findByText(/30 pontos extras/i)).toBeInTheDocument();
    expect(screen.getByText(/18 pontos extras/i)).toBeInTheDocument();
    expect(screen.queryByText(/48 pontos extras/i)).not.toBeInTheDocument();
    // `RN-01-64`: o acumulado só cai pelo estorno da presença anulada, e a
    // tela não promete que ele "só cresce" — promete o que vale, que a troca
    // não o diminui.
    expect(screen.getByText(/trocar não diminui o acumulado/i)).toBeInTheDocument();
    expect(screen.queryByText(/só cresce/i)).not.toBeInTheDocument();
  });

  it("diz que a divulgação está autorizada quando o responsável concedeu", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 0,
      saldo_disponivel: 0,
    });

    await renderizar(true);

    expect(await screen.findByText(/autorizou mostrar seu avatar/i)).toBeInTheDocument();
  });

  it("diz que o perfil ainda não aparece quando não há autorização, sem ação de decidir", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 0,
      saldo_disponivel: 0,
    });

    await renderizar(false);

    expect(await screen.findByText(/ainda não aparece/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /autorizar/i })).not.toBeInTheDocument();
  });
});

describe("a carta domina a tela da Arena (documento 15 §6)", () => {
  it("a carta é o elemento maior, e as contas e o perfil ficam no apoio", async () => {
    const { container } = await renderizarRetornando();

    // A carta ocupa o primeiro plano do palco; nada mais disputa com ela.
    const palco = container.querySelector(".cg-palco");
    expect(palco).not.toBeNull();
    expect(palco?.querySelector(".cg-palco__personagem")).not.toBeNull();

    // Acumulado, saldo e perfil público seguem na tela — inteiros —, mas no
    // apoio, abaixo e menores que a apresentação.
    const apoio = palco?.querySelector(".cg-palco__apoio");
    expect(apoio?.textContent).toMatch(/Acumulado/);
    expect(apoio?.textContent).toMatch(/Meu perfil público/);

    // Uma decisão por tela: a única é mudar o próprio avatar (`RF-05-51`), e
    // autorizar a divulgação segue sendo ato do responsável na App 07
    // (`RN-05-42`) — nenhuma ação dele aqui. "Como cheguei aqui" só abre a
    // leitura do próprio histórico (`RF-05-104`): é caminho, não decisão.
    expect(screen.queryAllByRole("button").map((botao) => botao.textContent)).toEqual([
      "Como cheguei aqui",
      "Mudar o meu avatar",
    ]);
  });

  it("sem foto escolhida, a tela é a cor chapada, e nenhuma imagem é pedida", async () => {
    const { container } = await renderizarRetornando();

    // `ComunidadeVirtual` ainda não tem campo de foto, e a tela não perde
    // nada por isso (documento 15 §6.3).
    expect(container.querySelector(".cg-fundo-de-comunidade")).not.toBeNull();
    expect(container.querySelector("img")).toBeNull();
  });
});

describe("o saldo na carta não dispensa a carteira (`RF-05-82`)", () => {
  it("o saldo aparece nas duas, com rótulo próprio em cada uma", async () => {
    // Decisão expressa do fundador de 2026-10-30, depois de a duplicação ser
    // levantada: a carta diz o que dá para trocar, e o apoio mantém as duas
    // contas com o aviso que explica a diferença.
    const { container } = await renderizarRetornando();

    const carta = container.querySelector(".cg-palco__personagem");
    expect(carta?.textContent).toContain("Para trocar");

    const apoio = container.querySelector(".cg-palco__apoio");
    expect(apoio?.textContent).toMatch(/Acumulado/);
    expect(apoio?.textContent).toMatch(/Saldo disponível/);
  });

  it("o acumulado continua só no apoio, nunca na carta", async () => {
    const { container } = await renderizarRetornando();

    const carta = container.querySelector(".cg-palco__personagem");
    expect(carta?.textContent).not.toMatch(/Acumulado/i);
  });
});

describe("mudar o próprio avatar a partir da carteira (`RF-05-51`, `RF-05-50`)", () => {
  it("abre a montagem, salva e volta com a carta relendo a sessão", async () => {
    await renderizarRetornando();
    const alterar = vi
      .spyOn(carteiraApi, "alterarMeuAvatar")
      .mockResolvedValue({ avatar: "gravado" });
    const usuario = userEvent.setup();
    const leiturasAntes = vi.mocked(autenticacaoApi.eu).mock.calls.length;

    await usuario.click(screen.getByRole("button", { name: "Mudar o meu avatar" }));
    expect(await screen.findByRole("region", { name: "Meu avatar" })).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Salvar o meu avatar" }));

    expect(alterar).toHaveBeenCalledTimes(1);
    expect(await screen.findByRole("region", { name: "Minha carteira" })).toBeInTheDocument();
    // Uma leitura da montagem e outra da carta remontada.
    expect(vi.mocked(autenticacaoApi.eu).mock.calls.length).toBeGreaterThanOrEqual(
      leiturasAntes + 2,
    );
  });

  it("voltar sem salvar devolve à carteira sem gravar", async () => {
    await renderizarRetornando();
    const alterar = vi.spyOn(carteiraApi, "alterarMeuAvatar");
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: "Mudar o meu avatar" }));
    await usuario.click(await screen.findByRole("button", { name: "Voltar sem salvar" }));

    expect(alterar).not.toHaveBeenCalled();
    expect(screen.getByRole("region", { name: "Minha carteira" })).toBeInTheDocument();
  });
});

describe("histórico de pontuação do próprio Guerreiro(a) (RF-05-104)", () => {
  it("abre pela carteira, com a conduta e o motivo e a linha de saldo anterior", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 0,
      saldo_disponivel: 0,
    });
    vi.mocked(lerMeuHistoricoDePontuacao).mockResolvedValue({
      saldos: {
        regular: [{ trilha_id: "t1", poder_id: null, nome: "Robótica", total: 15 }],
        extra: { acumulado: 0, saldo_disponivel: 0 },
      },
      itens: [
        {
          id: "l2",
          registrado_em: "2026-11-12T13:00:00Z",
          conta: "regular",
          origem: "ocorrencia_de_conduta",
          valor: -5,
          valor_no_acumulado: null,
          trilha_id: "t1",
          poder_id: null,
          nome_da_trilha_ou_poder: "Robótica",
          detalhe: null,
          motivo: "Desrespeitou um colega.",
        },
        {
          id: "l1",
          registrado_em: "2026-11-01T13:00:00Z",
          conta: "regular",
          origem: "saldo_anterior",
          valor: 20,
          valor_no_acumulado: null,
          trilha_id: "t1",
          poder_id: null,
          nome_da_trilha_ou_poder: "Robótica",
          detalhe: null,
          motivo: null,
        },
      ],
      proximo_cursor: null,
    });

    await renderizar(true);
    await userEvent.click(await screen.findByRole("button", { name: "Como cheguei aqui" }));

    expect(await screen.findByText("Motivo: Desrespeitou um colega.")).toBeInTheDocument();
    expect(screen.getByText("Saldo anterior ao histórico")).toBeInTheDocument();
    expect(lerMeuHistoricoDePontuacao).toHaveBeenCalledWith("token-do-guerreiro", null);
  });

  it("avisa quando ainda não há lançamento", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 0,
      saldo_disponivel: 0,
    });
    vi.mocked(lerMeuHistoricoDePontuacao).mockResolvedValue({
      saldos: { regular: [], extra: { acumulado: 0, saldo_disponivel: 0 } },
      itens: [],
      proximo_cursor: null,
    });

    await renderizar(true);
    await userEvent.click(await screen.findByRole("button", { name: "Como cheguei aqui" }));

    expect(
      await screen.findByText("Ainda não há lançamento de pontuação."),
    ).toBeInTheDocument();
  });
});
