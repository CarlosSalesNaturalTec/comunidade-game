import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as autenticacaoApi from "../autenticacao/api";
import { ProvedorDeSessao } from "../autenticacao/ContextoDeSessao";
import * as trilhaApi from "./api";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";
import { EscolhaDoPoder } from "./EscolhaDoPoder";
import { GuiaDaTrilha } from "./GuiaDaTrilha";
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

function pergunta(id: string, ordem: number, enunciado: string) {
  return {
    id,
    ordem,
    enunciado,
    alternativas: ["1", "2", "3", "4"],
    imagem_referencia: null,
  };
}

const QUIZ_DE_TRES: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  enunciado: null,
  perguntas: [
    pergunta("p1", 1, "Quanto é 1 + 1?"),
    pergunta("p2", 2, "Quanto é 2 + 2?"),
    pergunta("p3", 3, "Quanto é 3 + 3?"),
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

function conteudoDeTexto(id: string, ordem: number, corpo: string) {
  return {
    id,
    ordem,
    tipo: "texto" as const,
    corpo,
    endereco: null,
    referencia: null,
    autoria: "propria" as const,
    fonte: null,
  };
}

function trilhaPublica(
  atividades: trilhaApi.AtividadeDaMissaoPublica[] = [],
  conteudos: trilhaApi.ConteudoDaMissaoPublico[] = [],
) {
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
        conteudos,
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

// --- Fatia 22: um conteúdo por vez, e o secundário recolhido
// (`RF-05-11`, `RF-05-13`, `RN-05-45`, `RF-05-08`, `RF-05-10`,
// documento 15 §§6.1, 6.4)

describe("o conteúdo da missão sai um por vez, com o crédito recolhido", () => {
  it("o primeiro conteúdo aparece sozinho, e avançar leva ao segundo", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica(
        [],
        [
          conteudoDeTexto("conteudo-2", 2, "Segundo parágrafo."),
          conteudoDeTexto("conteudo-1", 1, "Primeiro parágrafo."),
        ],
      ),
    );

    await renderizar(
      <Missao trilhaId="trilha-1" missao={MISSAO_ABERTA} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    // A ordem é a do autor, não a da resposta do núcleo.
    expect(await screen.findByText("Primeiro parágrafo.")).toBeInTheDocument();
    expect(screen.queryByText("Segundo parágrafo.")).not.toBeInTheDocument();
    expect(screen.getByText("Conteúdo 1 de 2")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));

    expect(screen.getByText("Segundo parágrafo.")).toBeInTheDocument();
    expect(screen.queryByText("Primeiro parágrafo.")).not.toBeInTheDocument();
    // No último não há para onde avançar.
    expect(screen.queryByRole("button", { name: "Próximo conteúdo" })).not.toBeInTheDocument();
  });

  it("conteúdo único não pagina", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(
      <Missao trilhaId="trilha-1" missao={MISSAO_ABERTA} aoDesbloquear={vi.fn()} />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Próximo conteúdo" })).not.toBeInTheDocument();
  });

  it("o crédito e a licença ficam num bloco fechado, que abre ao ser acionado", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(
      <Missao trilhaId="trilha-1" missao={MISSAO_ABERTA} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    // Fechado, a linha nomeia o que guarda sem repetir o conteúdo.
    expect(await screen.findByText("Crédito e licença")).toBeInTheDocument();
    expect(screen.queryByText(/Mestre Ana/)).not.toBeVisible();

    await usuario.click(screen.getByText("Crédito e licença"));

    expect(screen.getByText(/Mestre Ana/)).toBeVisible();
    expect(screen.getByText(/CC BY-SA/)).toBeVisible();
  });
});

describe("o desafio de desbloqueio sai uma pergunta por vez", () => {
  it("uma pergunta por vez, e voltar preserva e troca a resposta", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 3,
      total: 3,
    });

    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ_DE_TRES}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );
    const usuario = userEvent.setup();

    expect(screen.getByText("1. Quanto é 1 + 1?")).toBeInTheDocument();
    expect(screen.queryByText("2. Quanto é 2 + 2?")).not.toBeInTheDocument();
    expect(screen.getByText("Pergunta 1 de 3")).toBeInTheDocument();

    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    expect(screen.getByText("2. Quanto é 2 + 2?")).toBeInTheDocument();
    await usuario.click(screen.getByRole("radio", { name: "2" }));

    // Voltar traz a resposta já dada, e ela pode ser trocada.
    await usuario.click(screen.getByRole("button", { name: "Pergunta anterior" }));
    expect(screen.getByRole("radio", { name: "1" })).toBeChecked();
    await usuario.click(screen.getByRole("radio", { name: "3" }));
    expect(screen.getByRole("radio", { name: "3" })).toBeChecked();

    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "4" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    // O que protege o `RN-05-45`: uma submissão só, com todas as respostas.
    expect(submeter).toHaveBeenCalledTimes(1);
    expect(submeter.mock.calls[0][1]).toEqual([
      { pergunta_id: "p1", alternativa_escolhida: 3 },
      { pergunta_id: "p2", alternativa_escolhida: 2 },
      { pergunta_id: "p3", alternativa_escolhida: 4 },
    ]);
  });

  it("concluir com pendência leva até ela e não envia", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio");

    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ_DE_TRES}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    // A tela não conta quantas faltam e deixa procurar: leva até a primeira.
    expect(await screen.findByText(/falta responder 1 pergunta/i)).toBeInTheDocument();
    expect(screen.getByText("2. Quanto é 2 + 2?")).toBeInTheDocument();
    expect(screen.getByText("Pergunta 2 de 3")).toBeInTheDocument();
    expect(submeter).not.toHaveBeenCalled();
  });
});

describe("a missão seguinte fica recolhida no guia da trilha", () => {
  const TRILHA: trilhaApi.TrilhaComProximaMissao = {
    id: "trilha-1",
    nome: "Robô Educa",
    poder_id: "poder-1",
    proxima_missao_id: "missao-1",
    proxima_missao_titulo: "Primeira Missão",
    proxima_missao_posicao: 1,
  };

  it("a seguinte abre num bloco fechado de resumo neutro, com o motivo dentro", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica());
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, posicao) =>
      Promise.resolve(
        posicao === 1
          ? { ...MISSAO_ABERTA, desbloqueada: false, e_proxima: true }
          : {
              ...MISSAO_ABERTA,
              id: "missao-2",
              titulo: "Segunda Missão",
              posicao: 2,
              desbloqueada: false,
              e_proxima: false,
              motivo_do_bloqueio: 'Desbloqueie "Primeira Missão" primeiro.',
            },
      ),
    );

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);
    const usuario = userEvent.setup();

    // Fechado, o resumo nomeia sem entregar o título nem o motivo.
    expect(await screen.findByText("Próxima missão")).toBeInTheDocument();
    expect(screen.queryByText("Segunda Missão")).not.toBeVisible();

    await usuario.click(screen.getByText("Próxima missão"));

    expect(screen.getByText("Segunda Missão")).toBeVisible();
    expect(screen.getByText(/Desbloqueie "Primeira Missão" primeiro\./)).toBeVisible();
  });

  it("abrir uma missão trancada segue mostrando o motivo direto, sem recolher", async () => {
    await renderizar(
      <Missao
        trilhaId="trilha-1"
        missao={{
          ...MISSAO_ABERTA,
          desbloqueada: false,
          e_proxima: false,
          motivo_do_bloqueio: 'Desbloqueie "Primeira Missão" primeiro.',
        }}
        aoDesbloquear={vi.fn()}
      />,
    );

    expect(screen.getByText(/ainda está trancada/i)).toBeVisible();
    expect(screen.queryByText("Próxima missão")).not.toBeInTheDocument();
  });
});
