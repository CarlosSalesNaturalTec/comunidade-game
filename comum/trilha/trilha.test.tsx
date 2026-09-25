import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as autenticacaoApi from "../autenticacao/api";
import { ProvedorDeSessao } from "../autenticacao/ContextoDeSessao";
import * as trilhaApi from "./api";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";
import { EscolhaDoPoder } from "./EscolhaDoPoder";
import { Missao } from "./Missao";

// O contrato novo da promoção: cada ato de escrita é opcional e separado dos
// outros, de modo que a Área do Guerreiro(a) ligue os três e o aparelho do
// encontro ligue só a inscrição e o desbloqueio — sem a entrega individual da
// produção (design — decisão 3).

const CHAVE_DE_SESSAO = "comum:teste-trilha";

const QUIZ: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  enunciado: null,
  perguntas: [
    {
      id: "p1",
      ordem: 1,
      enunciado: "Quanto é 1 + 1?",
      alternativas: ["1", "2", "3", "4"],
      imagem_referencia: null,
    },
  ],
};

const MISSAO_ABERTA: trilhaApi.MissaoNoPercurso = {
  id: "missao-1",
  titulo: "Primeira Missão",
  posicao: 1,
  obrigatoria: true,
  e_sondagem: false,
  desbloqueada: true,
  e_proxima: false,
  aguardando_mestre: false,
  motivo_do_bloqueio: null,
  desafio_de_desbloqueio: null,
};

const PODER: trilhaApi.PoderPublico = {
  id: "poder-1",
  nome: "Robótica",
  descricao: "Descrição do poder.",
  trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
};

async function renderizar(conteudo: React.ReactNode) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>{conteudo}</ProvedorDeSessao>,
    );
  });
}

function trilhaPublica(atividades: trilhaApi.AtividadeDaMissaoPublica[] = []) {
  return {
    id: "trilha-1",
    nome: "Robô Educa",
    licenca: "CC BY-SA",
    autor_nome: "Mestre Ana",
    culminancia: null,
    missoes: [
      {
        id: "missao-1",
        titulo: "Primeira Missão",
        posicao: 1,
        obrigatoria: true,
        e_sondagem: false,
        atividades,
        conteudos: [],
        bibliografia: [],
      },
    ],
  };
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("a inscrição é ato opcional do catálogo de poderes", () => {
  it("ligada, o catálogo inscreve e avisa quem chamou", async () => {
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([PODER]);
    const inscrever = vi.spyOn(trilhaApi, "inscreverNaTrilha").mockResolvedValue({
      id: "inscricao-1",
      trilha_id: "trilha-1",
      momento: "2026-09-25T00:00:00-03:00",
    });
    const aoInscrever = vi.fn();

    await renderizar(<EscolhaDoPoder aoInscrever={aoInscrever} inscricaoLigada />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: "Robótica" }));
    await usuario.click(screen.getByRole("button", { name: /inscrever-se/i }));

    expect(inscrever).toHaveBeenCalledWith("trilha-1", "token-do-guerreiro");
    expect(aoInscrever).toHaveBeenCalledWith("trilha-1");
  });

  it("desligada, o catálogo é leitura e nada é enviado", async () => {
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([PODER]);
    const inscrever = vi.spyOn(trilhaApi, "inscreverNaTrilha");

    await renderizar(<EscolhaDoPoder aoInscrever={vi.fn()} />);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: "Robótica" }));

    expect(screen.getByText("Robô Educa")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /inscrever-se/i })).not.toBeInTheDocument();
    expect(inscrever).not.toHaveBeenCalled();
  });
});

describe("a submissão do desbloqueio é ato opcional do desafio", () => {
  it("ligada, o desafio envia todas as perguntas de uma vez", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 1,
      total: 1,
    });
    const aoDesbloquear = vi.fn();

    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ}
        aoDesbloquear={aoDesbloquear}
        submissaoLigada
      />,
    );
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledTimes(1);
    expect(aoDesbloquear).toHaveBeenCalled();
  });

  it("desligada, o desafio se lê e nada é enviado", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio");

    await renderizar(
      <DesafioDeDesbloqueio missaoId="missao-1" desafio={QUIZ} aoDesbloquear={vi.fn()} />,
    );

    expect(screen.getByText("1. Quanto é 1 + 1?")).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /enviar respostas/i }),
    ).not.toBeInTheDocument();
    expect(submeter).not.toHaveBeenCalled();
  });
});

describe("a entrega individual da produção é ato opcional da missão", () => {
  const ATIVIDADES = [
    { id: "atividade-1", titulo: "Atividade Única", producao_esperada: "Um texto." },
  ];

  it("ligada, a missão desbloqueada apresenta a entrega de quem a ofereceu", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica(ATIVIDADES));

    await renderizar(
      <Missao
        trilhaId="trilha-1"
        missao={MISSAO_ABERTA}
        aoDesbloquear={vi.fn()}
        entregaDaProducao={({ missaoId, atividades }) => (
          <p>
            Entrega de {missaoId} em {atividades.length} atividade(s)
          </p>
        )}
      />,
    );

    expect(
      await screen.findByText("Entrega de missao-1 em 1 atividade(s)"),
    ).toBeInTheDocument();
  });

  it("desligada, a missão desbloqueada não oferece entrega alguma", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica(ATIVIDADES));

    await renderizar(
      <Missao trilhaId="trilha-1" missao={MISSAO_ABERTA} aoDesbloquear={vi.fn()} />,
    );

    expect(
      await screen.findByRole("heading", { name: "Primeira Missão" }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/entrega/i)).not.toBeInTheDocument();
  });

  it("os dois atos são independentes: o desbloqueio liga sem a entrega", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica(ATIVIDADES));

    await renderizar(
      <Missao
        trilhaId="trilha-1"
        missao={{
          ...MISSAO_ABERTA,
          desbloqueada: false,
          e_proxima: true,
          desafio_de_desbloqueio: QUIZ,
        }}
        aoDesbloquear={vi.fn()}
        submissaoDoDesbloqueioLigada
      />,
    );

    expect(
      await screen.findByRole("button", { name: /enviar respostas/i }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/entrega/i)).not.toBeInTheDocument();
  });
});
