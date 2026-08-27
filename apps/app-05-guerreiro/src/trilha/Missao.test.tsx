import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { Missao } from "./Missao";

const CHAVE_DE_SESSAO = "app-05:teste-missao";

async function renderizar(missao: trilhaApi.MissaoNoPercurso, aoDesbloquear = vi.fn()) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <Missao trilhaId="trilha-1" missao={missao} aoDesbloquear={aoDesbloquear} />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("missão no percurso", () => {
  it("bloqueada mostra o motivo, nunca cadeado mudo", async () => {
    await renderizar({
      id: "missao-2",
      titulo: "Segunda Missão",
      posicao: 2,
      obrigatoria: true,
      e_sondagem: false,
      desbloqueada: false,
      e_proxima: false,
      aguardando_mestre: false,
      motivo_do_bloqueio: 'Desbloqueie "Primeira Missão" primeiro.',
      desafio_de_desbloqueio: null,
    });

    expect(screen.getByText(/Desbloqueie "Primeira Missão" primeiro\./)).toBeInTheDocument();
  });

  it("mostra o conteúdo na ordem do autor com crédito e licença", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
      id: "trilha-1",
      nome: "Robô Educa",
      licenca: "CC BY-SA",
      autor_nome: "Mestre Ana",
      missoes: [
        {
          id: "missao-1",
          titulo: "Primeira Missão",
          posicao: 1,
          obrigatoria: true,
          e_sondagem: false,
          conteudos: [
            {
              id: "conteudo-2",
              ordem: 2,
              tipo: "texto",
              corpo: "Segundo parágrafo.",
              endereco: null,
              referencia: null,
              autoria: "propria",
              fonte: null,
            },
            {
              id: "conteudo-1",
              ordem: 1,
              tipo: "texto",
              corpo: "Primeiro parágrafo.",
              endereco: null,
              referencia: null,
              autoria: "propria",
              fonte: null,
            },
          ],
          bibliografia: [
            {
              id: "bib-1",
              titulo: "Livro X",
              capitulo: "Capítulo 1",
              disponivel: null,
              apoiador_nome: null,
            },
          ],
        },
      ],
    });

    await renderizar({
      id: "missao-1",
      titulo: "Primeira Missão",
      posicao: 1,
      obrigatoria: true,
      e_sondagem: false,
      desbloqueada: false,
      e_proxima: true,
      aguardando_mestre: false,
      motivo_do_bloqueio: null,
      desafio_de_desbloqueio: {
        tipo: "quiz",
        enunciado: "Pergunta da missão.",
        alternativas: ["a", "b", "c", "d"],
      },
    });

    const paragrafos = await screen.findAllByText(/parágrafo/);
    expect(paragrafos[0]).toHaveTextContent("Primeiro parágrafo.");
    expect(paragrafos[1]).toHaveTextContent("Segundo parágrafo.");
    expect(screen.getByText(/Mestre Ana/)).toBeInTheDocument();
    expect(screen.getByText(/CC BY-SA/)).toBeInTheDocument();
    expect(screen.getByText(/Livro X/)).toBeInTheDocument();
    expect(screen.queryByText(/disponível/)).not.toBeInTheDocument();
    expect(screen.getByText(/Pergunta da missão\./)).toBeInTheDocument();
  });

  it("opcional aparece marcada e fora da conta", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
      id: "trilha-1",
      nome: "Robô Educa",
      licenca: "CC BY-SA",
      autor_nome: "Mestre Ana",
      missoes: [
        {
          id: "missao-1",
          titulo: "Missão Opcional",
          posicao: 1,
          obrigatoria: false,
          e_sondagem: false,
          conteudos: [],
          bibliografia: [],
        },
      ],
    });

    await renderizar({
      id: "missao-1",
      titulo: "Missão Opcional",
      posicao: 1,
      obrigatoria: false,
      e_sondagem: false,
      desbloqueada: false,
      e_proxima: true,
      aguardando_mestre: false,
      motivo_do_bloqueio: null,
      desafio_de_desbloqueio: null,
    });

    expect(await screen.findByText(/não conta no que falta/i)).toBeInTheDocument();
  });
});
