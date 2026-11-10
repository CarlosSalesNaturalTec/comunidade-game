import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as autenticacaoApi from "../autenticacao/api";
import { ProvedorDeSessao } from "../autenticacao/ContextoDeSessao";
import { ProvedorDeNarracao } from "../narracao/ProvedorDeNarracao";
import * as trilhaApi from "./api";
import { RETORNO_DA_SONDAGEM_MS } from "./DesafioDeDesbloqueio";
import { GuiaDaTrilha } from "./GuiaDaTrilha";
import { Sondagem } from "./Sondagem";

// A sondagem com retorno por pergunta e refazer (`RF-05-99`, `RF-05-100`,
// `RF-05-101`, `RN-05-56`, `RF-04-78`): cada resposta mostra o acerto ou o
// erro por 2 s e segue sozinha; ao fim, o total, com Refazer e Concluir. A
// resposta por voz está em `sondagemPorVoz.test.tsx`.

const CHAVE_DE_SESSAO = "comum:teste-sondagem-com-retorno";

const SONDAGEM: trilhaApi.DesafioDeDesbloqueio = {
  forma_de_comprovacao: null,
  criterio_de_aceite: null,
  titulo_curto: null,
  tipo: "quiz",
  enunciado: null,
  perguntas: [
    {
      id: "p1",
      ordem: 1,
      enunciado: "Quanto é 1 + 1?",
      alternativas: ["1", "2", "3", "4"],
      imagem_referencia: null,
      alternativa_correta: 2,
    },
    {
      id: "p2",
      ordem: 2,
      enunciado: "Quanto é 2 + 2?",
      alternativas: ["3", "4", "5", "6"],
      imagem_referencia: null,
      alternativa_correta: 2,
    },
  ],
};

function resultado(acertos: number) {
  return {
    aprovado: true,
    aguardando_mestre: false,
    acertos,
    total: 2,
    comprovacao_entregue: null,
  };
}

async function renderizar(conteudo: React.ReactNode) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  let montado!: ReturnType<typeof render>;
  await act(async () => {
    montado = render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>{conteudo}</ProvedorDeSessao>,
    );
  });
  return montado;
}

async function passarORetorno() {
  await act(async () => {
    vi.advanceTimersByTime(RETORNO_DA_SONDAGEM_MS);
  });
}

// O retorno mora numa região própria: o `Aviso` da sondagem também é
// `status`, e a busca por papel acharia os dois.
function retornoNaTela(): HTMLElement {
  const regiao = document.querySelector<HTMLElement>(".cg-trilha__retorno-da-sondagem");
  expect(regiao).not.toBeNull();
  expect(regiao).toHaveAttribute("role", "status");
  return regiao as HTMLElement;
}

let usuario: ReturnType<typeof userEvent.setup>;

beforeEach(() => {
  vi.useFakeTimers({ shouldAdvanceTime: true });
  usuario = userEvent.setup({ advanceTimers: vi.advanceTimersByTime });
});

afterEach(() => {
  vi.useRealTimers();
  vi.restoreAllMocks();
  sessionStorage.clear();
});

function sondagem(aoResponder = vi.fn()) {
  return (
    <Sondagem
      missaoId="sondagem-1"
      desafio={SONDAGEM}
      aoResponder={aoResponder}
      submissaoLigada
    />
  );
}

describe("cada resposta tem retorno por 2 s e segue sozinha (RF-05-99)", () => {
  it("acertar mostra o símbolo de acerto, trava as alternativas e avança", async () => {
    await renderizar(sondagem());

    await usuario.click(screen.getByRole("radio", { name: "2" }));

    const retorno = retornoNaTela();
    expect(retorno).toHaveTextContent("Você acertou!");
    expect(retorno.querySelector(".cg-trilha__retorno--acerto svg")).not.toBeNull();
    for (const alternativa of screen.getAllByRole("radio")) {
      expect(alternativa).toBeDisabled();
    }
    expect(screen.getByText("Quanto é 1 + 1?")).toBeInTheDocument();

    await passarORetorno();

    expect(screen.getByText("Quanto é 2 + 2?")).toBeInTheDocument();
    expect(retornoNaTela()).toHaveTextContent("");
  });

  it("errar mostra o símbolo de erro, de forma distinta do acerto", async () => {
    await renderizar(sondagem());

    await usuario.click(screen.getByRole("radio", { name: "3" }));

    const retorno = retornoNaTela();
    expect(retorno).toHaveTextContent("Não foi essa.");
    expect(retorno.querySelector(".cg-trilha__retorno--erro svg")).not.toBeNull();
  });

  it("a sondagem não volta nem tem botão de enviar", async () => {
    await renderizar(sondagem());

    expect(
      screen.queryByRole("button", { name: "Pergunta anterior" }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Próxima pergunta" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Enviar respostas" })).not.toBeInTheDocument();
  });

  it("com a narração desligada o retorno não fala", async () => {
    const falar = vi.fn();
    vi.stubGlobal("speechSynthesis", {
      speak: falar,
      cancel() {},
      getVoices: () => [],
      addEventListener() {},
      removeEventListener() {},
    });
    await renderizar(<ProvedorDeNarracao>{sondagem()}</ProvedorDeNarracao>);

    await usuario.click(screen.getByRole("radio", { name: "2" }));

    expect(retornoNaTela()).toHaveTextContent("Você acertou!");
    expect(falar).not.toHaveBeenCalled();
    vi.unstubAllGlobals();
  });
});

describe("a sondagem termina na tela do total, com Refazer e Concluir (RF-05-100)", () => {
  async function responderAsDuas(primeira: string, segunda: string) {
    await usuario.click(screen.getByRole("radio", { name: primeira }));
    await passarORetorno();
    await usuario.click(screen.getByRole("radio", { name: segunda }));
    await passarORetorno();
  }

  it("depois do último retorno submete sozinha e mostra o total do núcleo", async () => {
    const submeter = vi
      .spyOn(trilhaApi, "submeterDesafioDeDesbloqueio")
      .mockResolvedValue(resultado(1));
    const aoResponder = vi.fn();
    await renderizar(sondagem(aoResponder));

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await passarORetorno();
    await usuario.click(screen.getByRole("radio", { name: "5" }));
    expect(submeter).not.toHaveBeenCalled();
    await passarORetorno();

    expect(submeter).toHaveBeenCalledWith(
      "sondagem-1",
      [
        { pergunta_id: "p1", alternativa_escolhida: 2 },
        { pergunta_id: "p2", alternativa_escolhida: 3 },
      ],
      "token-do-guerreiro",
      {},
    );
    expect(await screen.findByText("Você acertou 1 e errou 1.")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Refazer" })).toBeInTheDocument();
    // A trilha só segue no Concluir, senão a tela final sumiria.
    expect(aoResponder).not.toHaveBeenCalled();

    await usuario.click(screen.getByRole("button", { name: "Concluir" }));
    expect(aoResponder).toHaveBeenCalledTimes(1);
  });

  it("Refazer recomeça da primeira pergunta, sem resposta, e grava de novo ao fim", async () => {
    const submeter = vi
      .spyOn(trilhaApi, "submeterDesafioDeDesbloqueio")
      .mockResolvedValueOnce(resultado(0))
      .mockResolvedValueOnce(resultado(2));
    await renderizar(sondagem());
    await responderAsDuas("3", "5");
    expect(await screen.findByText("Você acertou 0 e errou 2.")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: "Refazer" }));

    expect(screen.getByText("Quanto é 1 + 1?")).toBeInTheDocument();
    for (const alternativa of screen.getAllByRole("radio")) {
      expect(alternativa).not.toBeChecked();
    }
    await responderAsDuas("2", "4");
    expect(submeter).toHaveBeenCalledTimes(2);
    expect(await screen.findByText("Você acertou 2 e errou 0.")).toBeInTheDocument();
  });

  it("falhando o envio, diz em linguagem simples e tenta de novo sem refazer", async () => {
    const submeter = vi
      .spyOn(trilhaApi, "submeterDesafioDeDesbloqueio")
      .mockRejectedValueOnce(new Error("rede"))
      .mockResolvedValueOnce(resultado(2));
    await renderizar(sondagem());
    await responderAsDuas("2", "4");

    expect(await screen.findByText(/Não foi possível enviar agora/)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Tentar de novo" }));

    expect(submeter).toHaveBeenCalledTimes(2);
    expect(submeter.mock.calls[1][1]).toEqual(submeter.mock.calls[0][1]);
    expect(await screen.findByText("Você acertou 2 e errou 0.")).toBeInTheDocument();
  });

  it("sondagem largada no meio não grava nada", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio");
    const montado = await renderizar(sondagem());
    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await passarORetorno();
    await usuario.click(screen.getByRole("radio", { name: "4" }));

    montado.unmount();
    await passarORetorno();

    expect(submeter).not.toHaveBeenCalled();
  });
});

describe("a sondagem respondida se refaz pelo rodapé da trilha (RF-05-101)", () => {
  const TRILHA: trilhaApi.TrilhaComProximaMissao = {
    id: "trilha-1",
    nome: "Robô Educa",
    poder_id: "poder-1",
    proxima_missao_id: "missao-2",
    proxima_missao_titulo: "Primeira Missão",
    proxima_missao_posicao: 2,
  };

  const MISSAO_SONDAGEM: trilhaApi.MissaoNoPercurso = {
    id: "sondagem-1",
    titulo: "Sondagem",
    posicao: 1,
    obrigatoria: true,
    e_sondagem: true,
    desbloqueada: true,
    e_proxima: false,
    aguardando_mestre: false,
    motivo_do_bloqueio: null,
    desafio_de_desbloqueio: SONDAGEM,
    comprovacao_entregue: null,
    julgamento: null,
  };

  const MISSAO_ATUAL: trilhaApi.MissaoNoPercurso = {
    ...MISSAO_SONDAGEM,
    id: "missao-2",
    titulo: "Primeira Missão",
    posicao: 2,
    e_sondagem: false,
    desbloqueada: false,
    e_proxima: true,
    desafio_de_desbloqueio: null,
  };

  function missaoPublica(id: string, posicao: number, titulo: string, e_sondagem: boolean) {
    return {
      id,
      titulo,
      posicao,
      obrigatoria: true,
      e_sondagem,
      atividades: [],
      conteudos: [],
      bibliografia: [],
    };
  }

  function montar(sondagemDaTrilha: trilhaApi.MissaoNoPercurso = MISSAO_SONDAGEM) {
    vi.spyOn(trilhaApi, "listarMinhasRecompensas").mockResolvedValue([]);
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
      id: "trilha-1",
      nome: "Robô Educa",
      licenca: "CC BY-SA",
      autor_nome: "Mestre Ana",
      culminancia: null,
      missoes: [
        missaoPublica("sondagem-1", 1, "Sondagem", true),
        missaoPublica("missao-2", 2, "Primeira Missão", false),
      ],
    });
    return vi
      .spyOn(trilhaApi, "obterMissaoNoPercurso")
      .mockImplementation((_id, posicao) =>
        Promise.resolve(
          posicao === 1 ? sondagemDaTrilha : posicao === 2 ? MISSAO_ATUAL : MISSAO_ATUAL,
        ),
      );
  }

  it("o rodapé oferece refazer, e concluir volta à missão do percurso", async () => {
    const percurso = montar();
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue(resultado(2));
    await renderizar(
      <GuiaDaTrilha
        trilha={TRILHA}
        aoAtualizarTrilhas={vi.fn()}
        submissaoDoDesbloqueioLigada
      />,
    );

    await usuario.click(await screen.findByRole("button", { name: "Refazer a sondagem" }));

    expect(screen.getByRole("region", { name: "Sondagem" })).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: "Refazer a sondagem" }),
    ).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await passarORetorno();
    await usuario.click(screen.getByRole("radio", { name: "4" }));
    await passarORetorno();
    const leiturasAntes = percurso.mock.calls.length;
    await usuario.click(screen.getByRole("button", { name: "Concluir" }));

    expect(screen.queryByRole("region", { name: "Sondagem" })).not.toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Primeira Missão" })).toBeInTheDocument();
    expect(percurso.mock.calls.length).toBeGreaterThan(leiturasAntes);
  });

  it("com a sondagem ainda por responder, o rodapé não oferece refazer", async () => {
    montar({ ...MISSAO_SONDAGEM, desbloqueada: false, e_proxima: true });
    await renderizar(
      <GuiaDaTrilha
        trilha={TRILHA}
        aoAtualizarTrilhas={vi.fn()}
        submissaoDoDesbloqueioLigada
      />,
    );

    expect(await screen.findByText("Crédito e licença")).toBeInTheDocument();
    // A leitura da sondagem no percurso parte depois da trilha publicada.
    await act(async () => {});
    expect(
      screen.queryByRole("button", { name: "Refazer a sondagem" }),
    ).not.toBeInTheDocument();
  });

  it("sem submissão ligada, o caminho não aparece", async () => {
    montar();
    await renderizar(<GuiaDaTrilha trilha={TRILHA} aoAtualizarTrilhas={vi.fn()} />);

    expect(await screen.findByText("Crédito e licença")).toBeInTheDocument();
    // A leitura da sondagem no percurso parte depois da trilha publicada.
    await act(async () => {});
    expect(
      screen.queryByRole("button", { name: "Refazer a sondagem" }),
    ).not.toBeInTheDocument();
  });
});
