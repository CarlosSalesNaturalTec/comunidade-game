import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as cartaApi from "comum/carta/api";
import * as trilhaComumApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { MinhaCarteira } from "./MinhaCarteira";

const CHAVE_DE_SESSAO = "app-05:teste-minha-carteira";

async function renderizar(divulgacaoAutorizada?: boolean) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  // A carta do próprio Guerreiro(a) vem à frente da carteira e tem teste
  // próprio em `MinhaCarta.test.tsx`; aqui basta que ela não peça rede: sem
  // comunidade não há carta, e a Área apresenta o que tem em outra forma.
  vi.spyOn(cartaApi, "listarMinhasSeriesDaCarta").mockResolvedValue({ itens: [] });
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
  vi.spyOn(cartaApi, "listarMinhasSeriesDaCarta").mockResolvedValue({ itens: [] });
  vi.spyOn(trilhaComumApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
  vi.spyOn(cartaApi, "obterProgressoDaCarta").mockResolvedValue([]);
  vi.spyOn(cartaApi, "obterPortfolioDaCarta").mockResolvedValue([]);
  vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
    acumulado: 40,
    saldo_disponivel: 10,
  });
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    divulgacao_autorizada: true,
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

    // Uma decisão por tela: a carteira é leitura, e autorizar a divulgação é
    // ato do responsável na App 07 (`RN-05-42`) — nenhum botão aqui.
    expect(screen.queryAllByRole("button")).toHaveLength(0);
  });

  it("sem foto escolhida, a tela é a cor chapada, e nenhuma imagem é pedida", async () => {
    const { container } = await renderizarRetornando();

    // `ComunidadeVirtual` ainda não tem campo de foto, e a tela não perde
    // nada por isso (documento 15 §6.3).
    expect(container.querySelector(".cg-fundo-de-comunidade")).not.toBeNull();
    expect(container.querySelector("img")).toBeNull();
  });
});
