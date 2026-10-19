import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as autenticacaoApi from "../autenticacao/api";
import { ProvedorDeSessao } from "../autenticacao/ContextoDeSessao";
import { ProvedorDeNarracao, useNarracao } from "../narracao/ProvedorDeNarracao";
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
  let resultado!: ReturnType<typeof render>;
  await act(async () => {
    resultado = render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>{conteudo}</ProvedorDeSessao>,
    );
  });
  return {
    ...resultado,
    // Remonta sob o **mesmo** provedor de sessão: é assim que se observa a
    // troca de missão sem recriar a sessão, que zeraria tudo por tabela.
    rerenderizar: async (novo: React.ReactNode) => {
      await act(async () => {
        resultado.rerender(
          <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>{novo}</ProvedorDeSessao>,
        );
      });
    },
  };
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
  bibliografia: trilhaApi.BibliografiaDaMissaoPublica[] = [],
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
        bibliografia,
      },
    ],
  };
}

// A `Missao` recebe o dado público por `prop` — quem busca a trilha
// publicada é o `GuiaDaTrilha` (fatia 27 do PRD-04).
function missaoDe(trilha: ReturnType<typeof trilhaPublica>) {
  return trilha.missoes[0];
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

    expect(screen.getByText("Quanto é 1 + 1?")).toBeInTheDocument();
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
    const publica = missaoDe(trilhaPublica(ATIVIDADES));

    await renderizar(
      <Missao
        missao={MISSAO_ABERTA}
        missaoPublica={publica}
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
    const publica = missaoDe(trilhaPublica(ATIVIDADES));

    await renderizar(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    expect(
      await screen.findByRole("heading", { name: "Primeira Missão" }),
    ).toBeInTheDocument();
    expect(screen.queryByText(/entrega/i)).not.toBeInTheDocument();
  });

  it("os dois atos são independentes: o desbloqueio liga sem a entrega", async () => {
    const publica = missaoDe(trilhaPublica(ATIVIDADES));

    await renderizar(
      <Missao
        missao={{
          ...MISSAO_ABERTA,
          desbloqueada: false,
          e_proxima: true,
          desafio_de_desbloqueio: QUIZ,
        }}
        missaoPublica={publica}
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

describe("o conteúdo da missão sai um por vez", () => {
  it("o primeiro conteúdo aparece sozinho, e avançar leva ao segundo", async () => {
    const publica = missaoDe(
      trilhaPublica(
        [],
        [
          conteudoDeTexto("conteudo-2", 2, "Segundo parágrafo."),
          conteudoDeTexto("conteudo-1", 1, "Primeiro parágrafo."),
        ],
      ),
    );

    await renderizar(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    // A ordem é a do autor, não a da resposta do núcleo.
    expect(await screen.findByText("Primeiro parágrafo.")).toBeInTheDocument();
    expect(screen.queryByText("Segundo parágrafo.")).not.toBeInTheDocument();
    // A posição na sequência não é declarada (decisão do fundador de
    // 2026-10-16).
    expect(screen.queryByText(/de 2/)).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));

    expect(screen.getByText("Segundo parágrafo.")).toBeInTheDocument();
    expect(screen.queryByText("Primeiro parágrafo.")).not.toBeInTheDocument();
    // No último não há para onde avançar.
    expect(screen.queryByRole("button", { name: "Próximo conteúdo" })).not.toBeInTheDocument();
  });

  it("conteúdo único não pagina", async () => {
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Próximo conteúdo" })).not.toBeInTheDocument();
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

    expect(screen.getByText("Quanto é 1 + 1?")).toBeInTheDocument();
    expect(screen.queryByText("Quanto é 2 + 2?")).not.toBeInTheDocument();
    expect(screen.queryByText(/de 3/)).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    expect(screen.getByText("Quanto é 2 + 2?")).toBeInTheDocument();
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

  // O envio impedido antes do toque substitui o salto até a pendente: o
  // inválido não se explica depois, não acontece (decisão do fundador de
  // 2026-10-16, que aposentou o aviso de falta e o salto).
  it("com pergunta sem resposta, enviar fica indisponível e nada é submetido", async () => {
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

    expect(screen.getByRole("button", { name: /enviar respostas/i })).toBeDisabled();

    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "1" }));

    // Duas das três respondidas: segue indisponível, e o aviso de falta não
    // existe mais.
    expect(screen.getByRole("button", { name: /enviar respostas/i })).toBeDisabled();
    expect(screen.queryByText(/falta responder/i)).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));
    expect(submeter).not.toHaveBeenCalled();
  });

  it("respondidas todas, enviar fica disponível, ao lado de avançar e voltar", async () => {
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
    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    expect(screen.getByRole("button", { name: /enviar respostas/i })).toBeDisabled();

    await usuario.click(screen.getByRole("radio", { name: "1" }));

    const enviar = screen.getByRole("button", { name: /enviar respostas/i });
    expect(enviar).toBeEnabled();
    // Na mesma linha de avançar e voltar, que é onde ele passou a morar.
    const controles = enviar.closest(".cg-sequencia__controles");
    expect(controles).not.toBeNull();
    expect(controles).toContainElement(
      screen.getByRole("button", { name: "Pergunta anterior" }),
    );
  });

  it("quiz de uma pergunta não pagina, mas oferece enviar", async () => {
    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );

    expect(screen.queryByRole("button", { name: "Próxima pergunta" })).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /enviar respostas/i })).toBeInTheDocument();
  });

  it("o desafio por declaração não espera resposta e segue disponível", async () => {
    const submeter = vi
      .spyOn(trilhaApi, "submeterDesafioDeDesbloqueio")
      .mockResolvedValue({ aprovado: null, aguardando_mestre: true, acertos: 0, total: 0 });

    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={{ tipo: "pratico", enunciado: "Monte o robô.", perguntas: null }}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );
    const usuario = userEvent.setup();

    const declarar = screen.getByRole("button", { name: /já cumpri/i });
    expect(declarar).toBeEnabled();
    expect(screen.queryByRole("radio")).not.toBeInTheDocument();

    await usuario.click(declarar);
    expect(submeter).toHaveBeenCalledTimes(1);
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

// ---------------------------------------------------------------------------
// Ouvir o conteúdo da missão (documento 15 §5.1, documento 03 §4)
// ---------------------------------------------------------------------------

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

function instalarMotorDeFalaFalso() {
  const motor = new MotorDeFalaFalso();
  vi.stubGlobal("speechSynthesis", motor);
  vi.stubGlobal("SpeechSynthesisUtterance", EnunciadoFalso);
  return motor;
}

function conteudoDeLink(id: string, ordem: number, endereco: string) {
  return {
    id,
    ordem,
    tipo: "link_externo" as const,
    corpo: null,
    endereco,
    referencia: null,
    autoria: "propria" as const,
    fonte: null,
  };
}

async function renderizarComNarracao(conteudo: React.ReactNode) {
  await renderizar(<ProvedorDeNarracao>{conteudo}</ProvedorDeNarracao>);
}

describe("o conteúdo em texto oferece ouvi-lo, e nunca fala sozinho", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
    localStorage.clear();
  });

  it("o controle aparece no conteúdo em texto, e o conteúdo não é falado sozinho", async () => {
    const motor = instalarMotorDeFalaFalso();
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizarComNarracao(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    expect(
      await screen.findByRole("button", { name: "Ouvir este texto" }),
    ).toBeInTheDocument();
    expect(motor.ditos).toHaveLength(0);
  });

  it("acioná-lo fala o corpo daquele texto", async () => {
    const motor = instalarMotorDeFalaFalso();
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizarComNarracao(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: "Ouvir este texto" }));

    // O enunciado vazio é o armar, que o próprio toque dispara: o controle não
    // depende do liga e desliga das telas, então é ele que arma o que fala.
    expect(motor.ditos.map((dito) => dito.text)).toEqual(["", "Parágrafo único."]);
  });

  it("conteúdo que não é texto não oferece o controle", async () => {
    instalarMotorDeFalaFalso();
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeLink("conteudo-1", 1, "https://exemplo.org")]),
    );

    await renderizarComNarracao(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    expect(await screen.findByRole("link")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Ouvir este texto" })).not.toBeInTheDocument();
  });

  it("sem o provedor montado — a App 05 de hoje — o controle não aparece", async () => {
    instalarMotorDeFalaFalso();
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Ouvir este texto" })).not.toBeInTheDocument();
  });

  it("com a narração desligada o controle continua lá, e acioná-lo lê o texto", async () => {
    const motor = instalarMotorDeFalaFalso();
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    // A narração nasce desligada, e é assim que esta tela monta: o controle
    // não depende dela (decisão do fundador de 2026-10-14).
    await renderizarComNarracao(
      <Missao missao={MISSAO_ABERTA} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Ouvir este texto" }));

    expect(motor.ditos.map((dito) => dito.text)).toEqual(["", "Parágrafo único."]);
  });
});

// --- Fatia 27: a tela da missão em quatro grupos, separados por linha muda
// (`RF-04-72`, `RF-04-73`, `RF-05-08`, `RF-05-10` a `RF-05-12`,
// documento 15 §6, decisão do fundador de 2026-10-15)

describe("a tela da missão se divide em quatro grupos", () => {
  const TRILHA: trilhaApi.TrilhaComProximaMissao = {
    id: "trilha-1",
    nome: "Robô Educa",
    poder_id: "poder-1",
    proxima_missao_id: "missao-1",
    proxima_missao_titulo: "Primeira Missão",
    proxima_missao_posicao: 1,
  };

  const TRILHA_CONCLUIDA: trilhaApi.TrilhaComProximaMissao = {
    ...TRILHA,
    proxima_missao_id: null,
    proxima_missao_titulo: null,
    proxima_missao_posicao: null,
  };

  const BIBLIOGRAFIA: trilhaApi.BibliografiaDaMissaoPublica[] = [
    {
      id: "bib-1",
      titulo: "Livro X",
      capitulo: "Capítulo 1",
      disponivel: null,
      apoiador_nome: null,
    },
  ];

  // A missão de agora tem um desafio por responder, e a seguinte está
  // trancada: é o caso em que os quatro grupos existem ao mesmo tempo.
  function montarPercurso() {
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, posicao) =>
      Promise.resolve(
        posicao === 1
          ? {
              ...MISSAO_ABERTA,
              desbloqueada: false,
              e_proxima: true,
              desafio_de_desbloqueio: QUIZ,
            }
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
  }

  function grupos() {
    const guia = screen.getByRole("region", { name: /Guia de Robô Educa/ });
    return Array.from(guia.querySelectorAll<HTMLElement>(":scope > .cg-trilha__grupo"));
  }

  it("os quatro grupos saem na ordem decidida, com o ato junto do conteúdo", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")], BIBLIOGRAFIA),
    );

    await renderizar(
      <GuiaDaTrilha
        trilha={TRILHA}
        aoAtualizarTrilhas={vi.fn()}
        submissaoDoDesbloqueioLigada
        atividadesDoEncontro={<h2>Atividades do encontro</h2>}
        aoEscolherOutroPoder={vi.fn()}
      />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    const [conteudo, leDepois, encontro, rodape] = grupos();
    expect(grupos()).toHaveLength(4);

    // Grupo 1: o conteúdo e o ato da missão, acima da primeira linha.
    expect(conteudo).toContainElement(screen.getByText("Parágrafo único."));
    expect(conteudo).toContainElement(
      screen.getByRole("button", { name: /enviar respostas/i }),
    );

    // Grupo 2: os dois recolhidos, e nada do ato.
    expect(leDepois).toContainElement(screen.getByText("Próxima missão"));
    expect(leDepois).toContainElement(screen.getByText("Bibliografia"));

    // Grupo 3: as atividades do encontro, que vieram por slot.
    expect(encontro).toContainElement(screen.getByText("Atividades do encontro"));

    // Grupo 4: o rodapé — o caminho ao catálogo e o crédito da obra.
    expect(rodape).toContainElement(
      screen.getByRole("button", { name: "Escolher outro poder" }),
    );
    expect(rodape).toContainElement(screen.getByText("Crédito e licença"));
  });

  it("a linha é muda: não há separador anunciado nem rótulo nela", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")], BIBLIOGRAFIA),
    );

    await renderizar(
      <GuiaDaTrilha
        trilha={TRILHA}
        aoAtualizarTrilhas={vi.fn()}
        atividadesDoEncontro={<h2>Atividades do encontro</h2>}
        aoEscolherOutroPoder={vi.fn()}
      />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    const guia = screen.getByRole("region", { name: /Guia de Robô Educa/ });

    // A linha é `border-top` do grupo de baixo, nunca elemento próprio: `<hr>`
    // carrega `role="separator"` implícito e é anunciado por parte dos
    // leitores de tela, e o fundador pediu linha muda em 2026-10-15.
    expect(screen.queryAllByRole("separator")).toHaveLength(0);
    expect(guia.querySelectorAll("hr")).toHaveLength(0);
    // Os quatro grupos estão lá — a ausência de separador não é tela vazia.
    expect(grupos()).toHaveLength(4);
  });

  it("a bibliografia nasce fechada e abre com título e capítulo", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [], BIBLIOGRAFIA),
    );

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);
    const usuario = userEvent.setup();

    // Fechada, a linha nomeia sem entregar o conteúdo (documento 15 §6.1).
    expect(await screen.findByText("Bibliografia")).toBeInTheDocument();
    expect(screen.getByText("Onde ler mais sobre esta missão.")).toBeInTheDocument();
    expect(screen.queryByText(/Livro X/)).not.toBeVisible();

    await usuario.click(screen.getByText("Bibliografia"));

    expect(screen.getByText(/Livro X/)).toBeVisible();
    expect(screen.getByText(/Capítulo 1/)).toBeVisible();
    // Sem vínculo com exemplar, a disponibilidade não é afirmada nem negada.
    expect(screen.queryByText(/disponível no seu ponto de apoio/)).not.toBeInTheDocument();
  });

  it("missão sem bibliografia não apresenta o bloco", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica());

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Próxima missão")).toBeInTheDocument();
    expect(screen.queryByText("Bibliografia")).not.toBeInTheDocument();
  });

  it("grupo sem conteúdo não aparece, e leva a sua linha embora", async () => {
    // Última missão da trilha — não há seguinte — e sem bibliografia: o
    // grupo do meio não tem o que apresentar.
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, posicao) =>
      posicao === 1
        ? Promise.resolve(MISSAO_ABERTA)
        : Promise.reject({ codigo: "nao_encontrado" }),
    );
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(
      <GuiaDaTrilha
        trilha={TRILHA}
        aoAtualizarTrilhas={vi.fn()}
        atividadesDoEncontro={<h2>Atividades do encontro</h2>}
      />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    expect(screen.queryByText("Próxima missão")).not.toBeInTheDocument();
    expect(screen.queryByText("Bibliografia")).not.toBeInTheDocument();
    // Restam o conteúdo, as atividades e o rodapé — nunca um grupo vazio
    // entre duas linhas.
    expect(grupos()).toHaveLength(3);
  });

  it("sem o slot das atividades, o grupo do encontro não existe", async () => {
    // É o caso da App 05, que não tem encontro algum a apresentar.
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [], BIBLIOGRAFIA),
    );

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Bibliografia")).toBeInTheDocument();
    expect(screen.queryByText("Atividades do encontro")).not.toBeInTheDocument();
    // Conteúdo, o que se lê depois e o rodapé com o crédito.
    expect(grupos()).toHaveLength(3);
  });

  it("o caminho ao catálogo só aparece quando quem monta a tela o passa", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica());

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Crédito e licença")).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Escolher outro poder" }),
    ).not.toBeInTheDocument();
  });

  it("o crédito fica no rodapé, fechado, e abre ao ser acionado", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);
    const usuario = userEvent.setup();

    // Fechado, a linha nomeia o que guarda sem repetir o conteúdo.
    expect(await screen.findByText("Crédito e licença")).toBeInTheDocument();
    expect(screen.queryByText(/Mestre Ana/)).not.toBeVisible();

    await usuario.click(screen.getByText("Crédito e licença"));

    expect(screen.getByText(/Mestre Ana/)).toBeVisible();
    expect(screen.getByText(/CC BY-SA/)).toBeVisible();

    // E está no último grupo, não sob o conteúdo.
    const todos = grupos();
    expect(todos[todos.length - 1]).toContainElement(screen.getByText("Crédito e licença"));
  });

  it("a trilha concluída mantém os grupos, e credita a autoria", async () => {
    // O caminho da culminância, em que o guia saía cedo e levava consigo as
    // atividades do encontro e o crédito (invariante 5 do documento 99).
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica());

    await renderizar(
      <GuiaDaTrilha
        trilha={TRILHA_CONCLUIDA}
        aoAtualizarTrilhas={vi.fn()}
        atividadesDoEncontro={<h2>Atividades do encontro</h2>}
      />,
    );

    expect(await screen.findByText(/hora da culminância/i)).toBeInTheDocument();
    expect(screen.getByText("Atividades do encontro")).toBeInTheDocument();
    expect(screen.getByText("Crédito e licença")).toBeInTheDocument();
    expect(screen.queryByText("Próxima missão")).not.toBeInTheDocument();
    expect(grupos()).toHaveLength(3);
  });
});

// ---------------------------------------------------------------------------
// A pergunta do quiz fala, e a mídia que carrega trava a troca de pergunta
// (documento 15 §5.1 e §6.4, decisão do fundador de 2026-10-16)
// ---------------------------------------------------------------------------

// A narração nasce desligada, e o alternador mora na tela inicial da App 01 —
// fora de `comum/`. Este controle é o gesto que a liga, para o teste alcançar
// o que uma tela com narração ativada fala.
function LigarNarracao() {
  const { alternarNarracao } = useNarracao();
  return (
    <button type="button" onClick={alternarNarracao}>
      Ligar a narração
    </button>
  );
}

const QUIZ_COM_IMAGEM: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  enunciado: null,
  perguntas: [
    { ...pergunta("p1", 1, "Quanto é 1 + 1?"), imagem_referencia: "imagem-1" },
    { ...pergunta("p2", 2, "Quanto é 2 + 2?"), imagem_referencia: "imagem-2" },
  ],
};

describe("a pergunta do quiz é falada ao ser alcançada", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("fala o enunciado e as alternativas, avançando e voltando", async () => {
    const motor = instalarMotorDeFalaFalso();

    await renderizarComNarracao(
      <>
        <LigarNarracao />
        <DesafioDeDesbloqueio
          missaoId="missao-1"
          desafio={QUIZ_DE_TRES}
          aoDesbloquear={vi.fn()}
          submissaoLigada
        />
      </>,
    );
    const usuario = userEvent.setup();

    // Desligada, nada fala sozinho.
    expect(motor.ditos).toHaveLength(0);

    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));
    // O primeiro enunciado é o armar, disparado pelo próprio gesto que liga.
    const faladas = () => motor.ditos.map((dito) => dito.text).filter((texto) => texto !== "");

    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    expect(faladas()).toContain("Quanto é 2 + 2?. 1. 2. 3. 4");

    await usuario.click(screen.getByRole("button", { name: "Pergunta anterior" }));
    // Retornar fala de novo a pergunta alcançada.
    expect(faladas().at(-1)).toBe("Quanto é 1 + 1?. 1. 2. 3. 4");
  });

  it("escolher alternativa não refaz a fala da mesma pergunta", async () => {
    const motor = instalarMotorDeFalaFalso();

    await renderizarComNarracao(
      <>
        <LigarNarracao />
        <DesafioDeDesbloqueio
          missaoId="missao-1"
          desafio={QUIZ_DE_TRES}
          aoDesbloquear={vi.fn()}
          submissaoLigada
        />
      </>,
    );
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: "Ligar a narração" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    const quantas = motor.ditos.length;

    // Render novo da mesma pergunta: a fala é por identidade do item, nunca
    // por reapresentação — senão a tela falaria em laço.
    await usuario.click(screen.getByRole("radio", { name: "3" }));

    expect(motor.ditos).toHaveLength(quantas);
  });

  it("com a narração desligada a pergunta não fala, e segue legível", async () => {
    const motor = instalarMotorDeFalaFalso();

    await renderizarComNarracao(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ_DE_TRES}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    expect(motor.ditos).toHaveLength(0);
    expect(screen.getByText("Quanto é 2 + 2?")).toBeInTheDocument();
  });
});

describe("a imagem que carrega trava a troca de pergunta", () => {
  it("trava avançar enquanto carrega e libera quando a imagem chega", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:imagem"),
      revokeObjectURL: vi.fn(),
    });
    let liberar: (bytes: Blob) => void = () => {};
    vi.spyOn(trilhaApi, "lerImagemDaPergunta").mockImplementation(
      () =>
        new Promise<Blob>((resolver) => {
          liberar = resolver;
        }),
    );

    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ_COM_IMAGEM}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );

    expect(await screen.findByText("Carregando…")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Próxima pergunta" })).toBeDisabled();

    await act(async () => {
      liberar(new Blob(["bytes"], { type: "image/png" }));
    });

    expect(screen.getByRole("button", { name: "Próxima pergunta" })).toBeEnabled();
  });

  it("imagem que não abre libera a navegação", async () => {
    vi.spyOn(trilhaApi, "lerImagemDaPergunta").mockRejectedValue(new Error("falhou"));

    await renderizar(
      <DesafioDeDesbloqueio
        missaoId="missao-1"
        desafio={QUIZ_COM_IMAGEM}
        aoDesbloquear={vi.fn()}
        submissaoLigada
      />,
    );

    expect(
      await screen.findByText("A imagem desta pergunta não abriu, mas pode responder."),
    ).toBeInTheDocument();
    // A válvula de escape: mídia que não abriu nunca prende quem percorre.
    expect(screen.getByRole("button", { name: "Próxima pergunta" })).toBeEnabled();
  });
});

// --- Fatia 29: o ato da missão só depois de todos os conteúdos
// (`RF-04-73`, `RF-05-11`, `RF-05-13`, `RF-05-14`, `RF-05-89`, `RN-05-45`,
// decisão do fundador de 2026-10-16)

describe("o ato da missão só aparece depois do último conteúdo", () => {
  const MISSAO_COM_DESAFIO: trilhaApi.MissaoNoPercurso = {
    ...MISSAO_ABERTA,
    desbloqueada: false,
    e_proxima: true,
    desafio_de_desbloqueio: QUIZ,
  };

  function oDesafioEstaEmTela() {
    return screen.queryByRole("heading", { name: "Desafio de desbloqueio" }) !== null;
  }

  it("o desafio fica oculto no primeiro conteúdo e aparece no último", async () => {
    const publica = missaoDe(
      trilhaPublica(
        [],
        [
          conteudoDeTexto("conteudo-1", 1, "Primeiro parágrafo."),
          conteudoDeTexto("conteudo-2", 2, "Segundo parágrafo."),
          conteudoDeTexto("conteudo-3", 3, "Terceiro parágrafo."),
        ],
      ),
    );

    await renderizar(
      <Missao missao={MISSAO_COM_DESAFIO} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    expect(await screen.findByText("Primeiro parágrafo.")).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(false);

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));
    expect(screen.getByText("Segundo parágrafo.")).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(false);

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));
    expect(screen.getByText("Terceiro parágrafo.")).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(true);
  });

  it("missão sem conteúdo algum apresenta o ato de imediato", async () => {
    const publica = missaoDe(trilhaPublica([], []));

    await renderizar(
      <Missao missao={MISSAO_COM_DESAFIO} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    // Sem isto a sondagem — que costuma não ter conteúdo — travaria a trilha.
    expect(
      await screen.findByRole("heading", { name: "Desafio de desbloqueio" }),
    ).toBeInTheDocument();
  });

  it("missão de um conteúdo só apresenta o ato junto dele", async () => {
    const publica = missaoDe(
      trilhaPublica([], [conteudoDeTexto("conteudo-1", 1, "Parágrafo único.")]),
    );

    await renderizar(
      <Missao missao={MISSAO_COM_DESAFIO} missaoPublica={publica} aoDesbloquear={vi.fn()} />,
    );

    expect(await screen.findByText("Parágrafo único.")).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(true);
  });

  it("a sondagem segue a mesma regra do desafio", async () => {
    const publica = missaoDe(
      trilhaPublica(
        [],
        [
          conteudoDeTexto("conteudo-1", 1, "Primeiro parágrafo."),
          conteudoDeTexto("conteudo-2", 2, "Segundo parágrafo."),
        ],
      ),
    );

    await renderizar(
      <Missao
        missao={{ ...MISSAO_COM_DESAFIO, e_sondagem: true }}
        missaoPublica={publica}
        aoDesbloquear={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    expect(await screen.findByText("Primeiro parágrafo.")).toBeInTheDocument();
    expect(screen.queryByRole("region", { name: "Sondagem" })).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Próximo conteúdo" }));

    expect(screen.getByRole("region", { name: "Sondagem" })).toBeInTheDocument();
  });

  // O risco central do desenho: a `Missao` NÃO remonta quando a missão
  // avança, e índice guardado nela abriria a missão nova no índice da
  // anterior, com o ato liberado de cara (design — decisão 1).
  it("a missão seguinte recomeça no primeiro conteúdo, com o ato oculto", async () => {
    const primeira = missaoDe(
      trilhaPublica(
        [],
        [
          conteudoDeTexto("conteudo-1", 1, "Primeiro parágrafo."),
          conteudoDeTexto("conteudo-2", 2, "Segundo parágrafo."),
        ],
      ),
    );
    const segunda = {
      ...missaoDe(
        trilhaPublica(
          [],
          [
            conteudoDeTexto("conteudo-3", 1, "Parágrafo da segunda."),
            conteudoDeTexto("conteudo-4", 2, "Outro da segunda."),
          ],
        ),
      ),
      id: "missao-2",
      titulo: "Segunda Missão",
    };

    const { rerenderizar } = await renderizar(
      <Missao missao={MISSAO_COM_DESAFIO} missaoPublica={primeira} aoDesbloquear={vi.fn()} />,
    );
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: "Próximo conteúdo" }));
    expect(oDesafioEstaEmTela()).toBe(true);

    await rerenderizar(
      <Missao
        missao={{ ...MISSAO_COM_DESAFIO, id: "missao-2", titulo: "Segunda Missão" }}
        missaoPublica={segunda}
        aoDesbloquear={vi.fn()}
      />,
    );

    expect(screen.getByText("Parágrafo da segunda.")).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(false);
  });

  it("o conteúdo que falha libera o ato, e o que carrega o mantém oculto", async () => {
    // Carregando: o ato não aparece para sumir quando a lista chegar.
    const { rerenderizar } = await renderizar(
      <Missao missao={MISSAO_COM_DESAFIO} missaoPublica={undefined} aoDesbloquear={vi.fn()} />,
    );

    expect(await screen.findByText("Carregando o conteúdo da missão…")).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(false);

    // Falhou: o gate não tem o que guardar, e fechado deixaria a missão sem
    // saída — o ato é o caminho adiante.
    await rerenderizar(
      <Missao
        missao={MISSAO_COM_DESAFIO}
        missaoPublica={undefined}
        erroDoConteudo="Não foi possível carregar o conteúdo agora. Tente de novo em instantes."
        aoDesbloquear={vi.fn()}
      />,
    );

    expect(
      screen.getByText(
        "Não foi possível carregar o conteúdo agora. Tente de novo em instantes.",
      ),
    ).toBeInTheDocument();
    expect(oDesafioEstaEmTela()).toBe(true);
  });

  it("a entrega da produção não depende do percurso do conteúdo", async () => {
    const publica = missaoDe(
      trilhaPublica(
        [],
        [
          conteudoDeTexto("conteudo-1", 1, "Primeiro parágrafo."),
          conteudoDeTexto("conteudo-2", 2, "Segundo parágrafo."),
        ],
      ),
    );

    await renderizar(
      <Missao
        missao={MISSAO_ABERTA}
        missaoPublica={publica}
        aoDesbloquear={vi.fn()}
        entregaDaProducao={() => <p>Entrega da produção</p>}
      />,
    );

    // Missão já desbloqueada: outro estado, fora do gate.
    expect(await screen.findByText("Primeiro parágrafo.")).toBeInTheDocument();
    expect(screen.getByText("Entrega da produção")).toBeInTheDocument();
  });
});
// A tela da recompensa de desbloqueio — fatia 10 do PRD-05, decisão do
// fundador de 2026-10-19, que quita o `RF-05-45` e cria a `RN-05-50`.
describe("a recompensa conquistada entra antes da próxima missão", () => {
  const TRILHA: trilhaApi.TrilhaComProximaMissao = {
    id: "trilha-1",
    nome: "Robô Educa",
    poder_id: "poder-1",
    proxima_missao_id: "missao-1",
    proxima_missao_titulo: "Primeira Missão",
    proxima_missao_posicao: 1,
  };

  function recompensa(
    sobrepor: Partial<trilhaApi.RecompensaConquistada> = {},
  ): trilhaApi.RecompensaConquistada {
    return {
      recompensa_de_marco_id: "recompensa-1",
      trilha_id: "trilha-1",
      missao_id: "missao-1",
      tipo_de_recurso_id: "tipo-1",
      tipo_de_recurso_nome: "Camisa do Comunidade Game",
      tipo_de_recurso_unidade: "unidade",
      quantidade: 1,
      entregue: false,
      entregue_em: null,
      ciente: false,
      ...sobrepor,
    };
  }

  function montarPercurso() {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublica());
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, posicao) =>
      Promise.resolve(
        posicao === 1
          ? { ...MISSAO_ABERTA, desbloqueada: false, e_proxima: true }
          : { ...MISSAO_ABERTA, id: "missao-2", titulo: "Segunda Missão", posicao: 2 },
      ),
    );
  }

  it("apresenta o trio, o nome do recurso e o aviso de que o Mestre entrega", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([recompensa()]);

    const { container } = await renderizar(
      <GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />,
    );

    expect(await screen.findByLabelText("Recompensa conquistada")).toBeInTheDocument();
    // Três estrelas, que é o que separa a recompensa da grandeza ponto.
    expect(container.querySelectorAll(".cg-trio-de-estrelas svg")).toHaveLength(3);
    expect(screen.getByText("1 Camisa do Comunidade Game")).toBeInTheDocument();
    // `RF-05-45`/§5.6.1: o aviso da entrega pelo Mestre é obrigatório.
    expect(screen.getByText(/confirma a entrega/)).toBeInTheDocument();
    // A missão fica para depois do avançar.
    expect(screen.queryByText("Primeira Missão")).not.toBeInTheDocument();
  });

  it("avançar grava a ciência e leva à missão", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([recompensa()]);
    const ciencia = vi.spyOn(trilhaApi, "darCienciaDaRecompensa").mockResolvedValue({
      recompensa_de_marco_id: "recompensa-1",
      guerreiro_id: "guerreiro-1",
      registrado_em: "2026-10-19T10:00:00Z",
    });

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: "Avançar" }));

    expect(ciencia).toHaveBeenCalledWith("recompensa-1", expect.any(String));
    expect(await screen.findByText("Primeira Missão")).toBeInTheDocument();
    expect(screen.queryByLabelText("Recompensa conquistada")).not.toBeInTheDocument();
  });

  it("recompensa com ciência não interrompe o percurso", async () => {
    // `RN-05-50`: a tela aparece **uma vez**; voltar à trilha não a traz de
    // novo, ainda que a entrega siga aguardando o Mestre.
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([
      recompensa({ ciente: true }),
    ]);

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Primeira Missão")).toBeInTheDocument();
    expect(screen.queryByLabelText("Recompensa conquistada")).not.toBeInTheDocument();
  });

  it("marco sem recompensa não interrompe o percurso", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([]);

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Primeira Missão")).toBeInTheDocument();
    expect(screen.queryByLabelText("Recompensa conquistada")).not.toBeInTheDocument();
  });

  it("recompensa de outra trilha nunca interrompe esta", async () => {
    // Design — decisão 3: a leitura traz todas as trilhas, e a tela filtra.
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([
      recompensa({ trilha_id: "trilha-2", recompensa_de_marco_id: "recompensa-de-outra" }),
    ]);

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Primeira Missão")).toBeInTheDocument();
    expect(screen.queryByLabelText("Recompensa conquistada")).not.toBeInTheDocument();
  });

  it("duas recompensas saem uma por tela, na ordem da posição da missão", async () => {
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
      ...trilhaPublica(),
      missoes: [
        { ...missaoDe(trilhaPublica()), id: "missao-1", posicao: 1 },
        { ...missaoDe(trilhaPublica()), id: "missao-2", titulo: "Segunda", posicao: 2 },
      ],
    });
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, posicao) =>
      Promise.resolve(
        posicao === 1
          ? { ...MISSAO_ABERTA, desbloqueada: false, e_proxima: true }
          : { ...MISSAO_ABERTA, id: "missao-2", titulo: "Segunda Missão", posicao: 2 },
      ),
    );
    // Devolvidas fora de ordem de propósito: quem ordena é a tela.
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([
      recompensa({
        recompensa_de_marco_id: "recompensa-2",
        missao_id: "missao-2",
        tipo_de_recurso_nome: "Kit em MDF",
      }),
      recompensa({ recompensa_de_marco_id: "recompensa-1", missao_id: "missao-1" }),
    ]);
    const ciencia = vi.spyOn(trilhaApi, "darCienciaDaRecompensa").mockImplementation((id) =>
      Promise.resolve({
        recompensa_de_marco_id: id,
        guerreiro_id: "guerreiro-1",
        registrado_em: "2026-10-19T10:00:00Z",
      }),
    );

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);
    const usuario = userEvent.setup();

    // A da missão 1 vem primeiro, embora tenha chegado por último.
    expect(await screen.findByText("1 Camisa do Comunidade Game")).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Avançar" }));

    // A segunda ocupa a tela, e só então a missão.
    expect(await screen.findByText("1 Kit em MDF")).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Avançar" }));

    expect(await screen.findByText("Primeira Missão")).toBeInTheDocument();
    expect(ciencia).toHaveBeenCalledTimes(2);
  });

  it("a tela não oferece compra nem mostra valor em moedas ou reais", async () => {
    // `RF-05-46`, invariantes 16 e 23.
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([recompensa()]);

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    const tela = await screen.findByLabelText("Recompensa conquistada");
    expect(tela.textContent).not.toMatch(/moeda|real|reais|R\$|ponto/i);
    expect(screen.queryByRole("button", { name: /trocar|comprar|resgatar/i })).toBeNull();
  });

  it("a ciência que falha deixa a recompensa na tela, para o aviso não se perder", async () => {
    montarPercurso();
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([recompensa()]);
    vi.spyOn(trilhaApi, "darCienciaDaRecompensa").mockRejectedValue(new Error("rede"));

    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: "Avançar" }));

    expect(screen.getByLabelText("Recompensa conquistada")).toBeInTheDocument();
  });
});
