import { render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as trilhaApi from "comum/trilha/api";
import { act } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as coletaApi from "../api/coleta";
import { AreaDoGuerreiro } from "./AreaDoGuerreiro";

const UM_MINUTO_EM_MS = 60_000;
// A duração do teste (design — vite.config.ts `test.env`): 5 minutos.
const DURACAO_EM_MS = 5 * UM_MINUTO_EM_MS;

async function renderizarComSessaoAberta() {
  sessionStorage.setItem("app-05:sessao-guerreiro-teste", "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  // O bloco da coleta carrega as próprias séries assim que a área abre —
  // isolado aqui, sem série nenhuma, porque este arquivo testa só o
  // encerramento por inatividade (coberto em `../coleta/*.test.tsx`).
  vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  // A área abre no bloco da trilha, que lê as trilhas do Guerreiro(a) —
  // isolado aqui, sem trilha nenhuma, porque este bloco de provas testa só o
  // encerramento por inatividade.
  vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([]);
  vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento="app-05:sessao-guerreiro-teste">
        <AreaDoGuerreiro />
      </ProvedorDeSessao>,
    );
  });
  screen.getByRole("heading", { name: /minha área/i });
}

describe("encerramento por saída e por inatividade", () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("avisa um minuto antes do encerramento por inatividade", async () => {
    await renderizarComSessaoAberta();

    expect(screen.queryByText(/sessão vai fechar/i)).toBeNull();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(DURACAO_EM_MS - UM_MINUTO_EM_MS);
    });

    expect(screen.getByText(/sessão vai fechar/i)).toBeInTheDocument();
  });

  it("sem resposta ao aviso, a sessão encerra", async () => {
    // O retorno ao pedido de nick é responsabilidade de
    // `AparelhoDaAreaDoGuerreiro` — coberto em
    // `AparelhoDaAreaDoGuerreiro.test.tsx`. Aqui, isolado, confere só que o
    // encerramento por inatividade chama a saída da sessão.
    const encerrarSessaoDoGuerreiro = vi
      .spyOn(autenticacaoApi, "encerrarSessao")
      .mockResolvedValue(undefined);
    await renderizarComSessaoAberta();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(DURACAO_EM_MS);
    });

    expect(encerrarSessaoDoGuerreiro).toHaveBeenCalledWith("token-do-guerreiro");
  });

  it("continuar recomeça a contagem, e a sessão segue aberta", async () => {
    vi.spyOn(autenticacaoApi, "encerrarSessao").mockResolvedValue(undefined);
    await renderizarComSessaoAberta();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(DURACAO_EM_MS - UM_MINUTO_EM_MS);
    });
    screen.getByRole("button", { name: /continuar/i }).click();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(UM_MINUTO_EM_MS);
    });

    expect(screen.getByRole("heading", { name: /minha área/i })).toBeInTheDocument();
    expect(screen.queryByText(/sessão vai fechar/i)).toBeNull();
  });
});

// A tela inicial da área: o bloco padrão, a ordem dos cartões, o caminho
// corrente e a próxima missão no cartão da trilha (`RF-05-08`, `RF-05-17`).
describe("a tela inicial da Área do Guerreiro(a) (RF-05-08, RF-05-17)", () => {
  const TRILHA_COM_MISSAO: trilhaApi.TrilhaComProximaMissao = {
    id: "trilha-1",
    nome: "Água e território",
    poder_id: "poder-do-territorio",
    proxima_missao_id: "missao-3",
    proxima_missao_titulo: "O rio da minha rua",
    proxima_missao_posicao: 3,
  };

  async function abrirArea(
    trilhas: trilhaApi.TrilhaComProximaMissao[] | Error = [TRILHA_COM_MISSAO],
  ) {
    sessionStorage.setItem("app-05:sessao-guerreiro-teste", "token-do-guerreiro");
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const listar = vi.spyOn(trilhaApi, "listarMinhasTrilhas");
    if (trilhas instanceof Error) listar.mockRejectedValue(trilhas);
    else listar.mockResolvedValue(trilhas);

    await act(async () => {
      render(
        <ProvedorDeSessao chaveDeArmazenamento="app-05:sessao-guerreiro-teste">
          <AreaDoGuerreiro />
        </ProvedorDeSessao>,
      );
    });
  }

  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("abre no bloco da trilha, sem que a criança acione caminho algum", async () => {
    await abrirArea();

    // Até 2026-10-31 a área abria na coleta do território, e a missão custava
    // uma ida ao menu — justo o que a §10 do PRD-05 proíbe.
    const atual = screen.getByRole("button", { name: /^Trilha —/, current: true });
    expect(atual).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /^Coleta do território/, current: true }),
    ).toBeNull();
  });

  it("apresenta os quatro caminhos em cartão, na ordem decidida", async () => {
    await abrirArea();

    const rotulos = Array.from(document.querySelectorAll(".cg-caminho")).map((cartao) =>
      cartao.querySelector(".cg-caminho__rotulo")?.textContent?.trim(),
    );

    expect(rotulos).toEqual([
      "Minha carteira — seus pontos, badges e conquistas",
      "Trilha — o seu percurso e a próxima missão",
      "Desafios e equipes — o que está em aberto e com quem você joga",
      "Coleta do território — medir e registrar o que você vê na sua rua",
    ]);
  });

  it("dispõe os cartões em grade, com o glifo acima do rótulo", async () => {
    await abrirArea();

    const lista = screen.getByRole("navigation", { name: "Área do Guerreiro(a)" });
    expect(lista).toHaveClass("cg-caminhos--grade");
    for (const cartao of lista.querySelectorAll(".cg-caminho")) {
      expect(cartao.firstElementChild).toHaveClass("cg-icone");
    }
  });

  it("anuncia o cartão do bloco aberto como o atual, e troca de bloco sem menu", async () => {
    await abrirArea();

    await act(async () => {
      screen.getByRole("button", { name: /^Minha carteira/ }).click();
    });

    // O bloco abre direto, e os cartões continuam na tela: não existe tela
    // intermediária de menu.
    screen.getByRole("button", { name: /^Minha carteira/, current: true });
    expect(screen.queryByRole("button", { name: /^Trilha —/, current: true })).toBeNull();
    expect(document.querySelectorAll(".cg-caminho")).toHaveLength(4);
  });

  it("nomeia a próxima missão no cartão da trilha", async () => {
    await abrirArea();

    expect(screen.getByText("Missão 3 — O rio da minha rua")).toHaveClass("cg-caminho__extra");
  });

  it("sem próxima missão, o cartão da trilha fica só com o rótulo", async () => {
    await abrirArea([
      {
        ...TRILHA_COM_MISSAO,
        proxima_missao_id: null,
        proxima_missao_titulo: null,
        proxima_missao_posicao: null,
      },
    ]);

    const cartao = screen.getByRole("button", { name: /^Trilha —/ });
    expect(cartao.querySelector(".cg-caminho__extra")).toBeNull();
    expect(cartao).toHaveAccessibleName("Trilha — o seu percurso e a próxima missão");
  });

  it("falhando a leitura das trilhas, o cartão recua ao rótulo e a tela não mostra erro", async () => {
    await abrirArea(new Error("rede fora"));

    const cartao = screen.getByRole("button", { name: /^Trilha —/ });
    expect(cartao.querySelector(".cg-caminho__extra")).toBeNull();
    // O cartão é silencioso: não acrescenta aviso algum. O erro que aparece é
    // o do próprio bloco da trilha, que já o tinha antes desta fatia — há
    // **um** aviso na tela, não dois.
    expect(screen.getByText(/não foi possível carregar as suas trilhas/i)).toBeInTheDocument();
    expect(cartao.querySelector("[role='alert']")).toBeNull();
  });

  it("mantém a saída da sessão no cabeçalho, uma única vez", async () => {
    await abrirArea();

    // A App 05 não usa o componente de navegação de áreas: o Sair segue no
    // cabeçalho, sempre no mesmo lugar (design — decisão 4).
    expect(screen.getAllByRole("button", { name: "Sair" })).toHaveLength(1);
  });
});
