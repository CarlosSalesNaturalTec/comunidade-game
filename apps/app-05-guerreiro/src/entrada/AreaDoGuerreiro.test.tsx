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
  // O bloco da coleta carrega as próprias séries quando é aberto — isolado
  // aqui, sem série nenhuma, porque este arquivo testa só o encerramento por
  // inatividade (coberto em `../coleta/*.test.tsx`).
  vi.spyOn(coletaApi, "listarMinhasSeries").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  // O cartão da trilha lê as trilhas do Guerreiro(a) — isolado aqui, sem
  // trilha nenhuma, porque este bloco de provas testa só o encerramento por
  // inatividade.
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

// O menu dos caminhos e as telas de conteúdo: o que a área mostra ao abrir, a
// ordem dos cartões, o Voltar, a saída e a próxima missão no cartão da trilha
// (`RF-05-05`, `RF-05-08`, `RF-05-17`, `RF-05-71`).
describe("o menu da Área do Guerreiro(a) (RF-05-08, RF-05-17)", () => {
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
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([]);
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

  /** Aciona um cartão do menu e espera o conteúdo do bloco assentar. */
  async function acionar(nome: RegExp | string) {
    await act(async () => {
      screen.getByRole("button", { name: nome }).click();
    });
  }

  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("abre no menu, sem conteúdo de bloco algum na tela", async () => {
    await abrirArea();

    // Até 2026-10-31 a área abria direto no bloco da trilha. Agora o guia só
    // aparece depois do toque, e o menu é o que a sessão encontra.
    screen.getByRole("heading", { name: /minha área/i });
    expect(screen.queryByRole("button", { name: /^Guia$/ })).toBeNull();
    expect(screen.queryByText(/não foi possível carregar as suas trilhas/i)).toBeNull();
  });

  it("apresenta os cinco caminhos em cartão, na ordem decidida", async () => {
    await abrirArea();

    const rotulos = Array.from(document.querySelectorAll(".cg-caminho")).map((cartao) =>
      cartao.querySelector(".cg-caminho__rotulo")?.textContent?.trim(),
    );

    expect(rotulos).toEqual([
      "Trilha — o seu percurso e a próxima missão",
      "Minha carteira — seus pontos, badges e conquistas",
      "Desafios e equipes — o que está em aberto e com quem você joga",
      "Coleta do território — medir e registrar o que você vê na sua rua",
      "Sair",
    ]);
  });

  it("dispõe os cartões um por linha, com o glifo ao lado do rótulo", async () => {
    await abrirArea();

    // Sem marco de navegação: aqui os caminhos **são** a tela, e o cartão de
    // sair é ação, não destino (design — decisão 4).
    expect(screen.queryByRole("navigation")).toBeNull();
    const lista = document.querySelector(".cg-caminhos");
    expect(lista).not.toBeNull();
    expect(lista?.className).toBe("cg-caminhos");
    for (const cartao of document.querySelectorAll(".cg-caminho")) {
      expect(cartao.firstElementChild).toHaveClass("cg-icone");
    }
  });

  it("nenhum cartão é anunciado como o atual", async () => {
    await abrirArea();

    // O caminho corrente saiu com a grade: menu e conteúdo são telas
    // separadas, e não há bloco aberto enquanto os cartões estão na tela.
    expect(document.querySelectorAll("[aria-current]")).toHaveLength(0);
  });

  it("acionado um caminho, o conteúdo ocupa a tela e os cartões somem", async () => {
    await abrirArea();

    await acionar(/^Minha carteira/);

    screen.getByRole("heading", { name: "Minha carteira" });
    expect(document.querySelectorAll(".cg-caminho")).toHaveLength(0);
    expect(screen.queryByRole("heading", { name: /minha área/i })).toBeNull();
  });

  it("o Voltar salta ao menu de qualquer profundidade do bloco", async () => {
    await abrirArea();

    await acionar(/^Trilha —/);
    // Desce um nível dentro do bloco: o guia dá lugar ao progresso.
    await acionar(/^Progresso$/);

    await acionar("Voltar");

    // Volta ao menu, e não ao guia: o estado interno do bloco é desmontado
    // junto com ele (design — decisão 2).
    screen.getByRole("heading", { name: /minha área/i });
    expect(document.querySelectorAll(".cg-caminho")).toHaveLength(5);
    expect(screen.queryByRole("button", { name: /^Progresso$/ })).toBeNull();
  });

  it("trocar de bloco passa pelo menu", async () => {
    await abrirArea();

    await acionar(/^Trilha —/);
    await acionar("Voltar");
    await acionar(/^Coleta do território/);

    screen.getByRole("heading", { name: "Coleta do território" });
  });

  it("a saída é o último cartão do menu, e encerra a sessão", async () => {
    const encerrarSessaoDoGuerreiro = vi
      .spyOn(autenticacaoApi, "encerrarSessao")
      .mockResolvedValue(undefined);
    await abrirArea();

    const cartoes = Array.from(document.querySelectorAll(".cg-caminho"));
    expect(cartoes.at(-1)?.textContent?.trim()).toBe("Sair");
    // Cartão igual aos demais, sem agrupamento próprio: na App 05 quem sai é
    // a própria criança, não um adulto que opera o aparelho.
    expect(screen.queryByRole("group")).toBeNull();

    await acionar("Sair");
    expect(encerrarSessaoDoGuerreiro).toHaveBeenCalledWith("token-do-guerreiro");
  });

  it("a tela de conteúdo oferece Voltar e nenhuma saída de sessão", async () => {
    await abrirArea();

    await acionar(/^Desafios e equipes/);

    screen.getByRole("button", { name: "Voltar" });
    expect(screen.queryByRole("button", { name: "Sair" })).toBeNull();
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

  it("falhando a leitura das trilhas, o cartão recua ao rótulo e o menu não mostra erro", async () => {
    await abrirArea(new Error("rede fora"));

    const cartao = screen.getByRole("button", { name: /^Trilha —/ });
    expect(cartao.querySelector(".cg-caminho__extra")).toBeNull();
    // O cartão é silencioso, e o menu não carrega o bloco: o erro da trilha
    // só aparece quando a criança abre a trilha.
    expect(screen.queryByText(/não foi possível carregar as suas trilhas/i)).toBeNull();
  });

  it("o aviso de inatividade aparece dentro de um bloco, e Continuar não tira dali", async () => {
    vi.useFakeTimers();
    try {
      vi.spyOn(autenticacaoApi, "encerrarSessao").mockResolvedValue(undefined);
      await abrirArea();
      await acionar(/^Minha carteira/);

      await act(async () => {
        await vi.advanceTimersByTimeAsync(DURACAO_EM_MS - UM_MINUTO_EM_MS);
      });

      expect(screen.getByText(/sessão vai fechar/i)).toBeInTheDocument();
      await act(async () => {
        screen.getByRole("button", { name: /continuar/i }).click();
      });

      // Segue na mesma tela, e a sessão não fechou.
      screen.getByRole("heading", { name: "Minha carteira" });
      expect(screen.queryByText(/sessão vai fechar/i)).toBeNull();
    } finally {
      vi.useRealTimers();
    }
  });
});
