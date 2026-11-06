import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { DesafioDeDesbloqueio } from "comum/trilha";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";

const CHAVE_DE_SESSAO = "app-05:teste-desafio-de-desbloqueio";

function pergunta(
  id: string,
  enunciado: string,
  imagem_referencia: string | null = null,
  ordem = 1,
): trilhaApi.PerguntaDoDesbloqueio {
  return { id, ordem, enunciado, alternativas: ["1", "2", "3", "4"], imagem_referencia };
}

const QUIZ_DE_DUAS: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  forma_de_comprovacao: null,
  criterio_de_aceite: null,
  titulo_curto: null,
  enunciado: null,
  perguntas: [pergunta("p1", "Quanto é 1 + 1?"), pergunta("p2", "Quanto é 2 + 2?", null, 2)],
};

async function renderizar(desafio: trilhaApi.DesafioDeDesbloqueio, aoDesbloquear = vi.fn()) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <DesafioDeDesbloqueio
          missaoId="missao-1"
          desafio={desafio}
          aoDesbloquear={aoDesbloquear}
          submissaoLigada
        />
      </ProvedorDeSessao>,
    );
  });
  return aoDesbloquear;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("desafio de desbloqueio", () => {
  it("uma pergunta por vez, e todas vão numa submissão só (RF-05-89, RN-05-45)", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 2,
      total: 2,
      comprovacao_entregue: null,
    });
    const aoDesbloquear = await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "4" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledTimes(1);
    expect(submeter.mock.calls[0][1]).toEqual([
      { pergunta_id: "p1", alternativa_escolhida: 2 },
      { pergunta_id: "p2", alternativa_escolhida: 4 },
    ]);
    expect(aoDesbloquear).toHaveBeenCalled();
  });

  it("pergunta sem resposta deixa o envio indisponível (RF-05-89)", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio");
    await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    // O inválido se impede antes do toque: o aviso de falta e o salto até a
    // pendente foram aposentados (decisão do fundador de 2026-10-16).
    const enviar = screen.getByRole("button", { name: /enviar respostas/i });
    expect(enviar).toBeDisabled();
    expect(screen.queryByText(/falta responder/i)).not.toBeInTheDocument();

    await usuario.click(enviar);
    expect(submeter).not.toHaveBeenCalled();
  });

  it("não passar diz quantas acertou e convida a tentar de novo, sem punição", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: false,
      aguardando_mestre: false,
      acertos: 1,
      total: 2,
      comprovacao_entregue: null,
    });
    await renderizar(QUIZ_DE_DUAS);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));
    await usuario.click(screen.getByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(await screen.findByText(/não foi dessa vez/i)).toBeInTheDocument();
    expect(screen.getByText(/acertou 1 de 2/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /enviar respostas/i })).not.toBeDisabled();
  });

  it("prático declarado fica aguardando o Mestre", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: null,
      aguardando_mestre: true,
      acertos: 0,
      total: 0,
      comprovacao_entregue: null,
    });
    await renderizar({
      tipo: "pratico",
      forma_de_comprovacao: null,
      criterio_de_aceite: null,
      titulo_curto: null,
      enunciado: "Monte o robô e mostre ao Mestre.",
      perguntas: null,
    });

    await act(async () => {
      screen.getByRole("button", { name: /já cumpri/i }).click();
    });

    expect(await screen.findByText(/aguardando|esperar o mestre/i)).toBeInTheDocument();
  });
});

describe("a imagem da pergunta (RF-09-119, RF-05-89)", () => {
  const QUIZ_COM_IMAGEM: trilhaApi.DesafioDeDesbloqueio = {
    tipo: "quiz",
    forma_de_comprovacao: null,
    criterio_de_aceite: null,
    titulo_curto: null,
    enunciado: null,
    perguntas: [
      pergunta("p1", "Quanto é 1 + 1?"),
      pergunta("p2", "O que o gráfico mostra?", "perguntas-do-desbloqueio/p2/imagem", 2),
    ],
  };

  it("a pergunta com imagem a exibe com o enunciado, antes das alternativas", async () => {
    vi.stubGlobal("URL", {
      ...URL,
      createObjectURL: vi.fn(() => "blob:imagem-da-p2"),
      revokeObjectURL: vi.fn(),
    });
    const ler = vi
      .spyOn(trilhaApi, "lerImagemDaPergunta")
      .mockResolvedValue(new Blob(["bytes"], { type: "image/png" }));

    await renderizar(QUIZ_COM_IMAGEM);
    const usuario = userEvent.setup();

    // A primeira pergunta não tem imagem, e nada é buscado por ela.
    expect(ler).not.toHaveBeenCalled();
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    // Só a pergunta que tem imagem a busca.
    expect(ler).toHaveBeenCalledTimes(1);
    expect(ler.mock.calls[0][0]).toBe("p2");
    const imagem = await screen.findByRole("img", {
      name: /imagem da pergunta: o que o gráfico mostra\?/i,
    });
    expect(imagem).toBeInTheDocument();
    // Antes das alternativas daquela pergunta, dentro do mesmo bloco.
    const bloco = imagem.closest("fieldset");
    expect(bloco?.textContent).toContain("O que o gráfico mostra?");
    expect(
      bloco?.querySelector(".cg-trilha__alternativas")?.compareDocumentPosition(imagem),
    ).toBe(Node.DOCUMENT_POSITION_PRECEDING);
    // A mesma moldura de tamanho fixo do conteúdo da missão (decisão do
    // fundador de 2026-09-17).
    expect(imagem.closest(".cg-midia-do-nucleo")).not.toBeNull();
    vi.unstubAllGlobals();
  });

  it("imagem que não carrega avisa e não tranca a pergunta", async () => {
    vi.spyOn(trilhaApi, "lerImagemDaPergunta").mockRejectedValue(new Error("caiu a rede"));
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 2,
      total: 2,
      comprovacao_entregue: null,
    });

    await renderizar(QUIZ_COM_IMAGEM);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: "Próxima pergunta" }));

    expect(await screen.findByText(/a imagem desta pergunta não abriu/i)).toBeInTheDocument();
    await usuario.click(screen.getByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledTimes(1);
  });
});

// A App 05 entrega a comprovação pela tela da trilha, pelo componente comum e
// sem reimplementação própria (`RF-05-91`, `RF-05-92`, `RN-05-51`).
describe("a entrega da comprovação do prático na App 05", () => {
  const PRATICO_EM_VIDEO: trilhaApi.DesafioDeDesbloqueio = {
    tipo: "pratico",
    enunciado: "Monte o robô e grave um vídeo.",
    perguntas: null,
    forma_de_comprovacao: "video",
    criterio_de_aceite: "Não deve aparecer o rosto da criança, só a produção.",
    titulo_curto: "Robô de sucata",
  };

  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("apresenta o critério, o aviso da mídia guardada e a alternativa presencial", async () => {
    await renderizar(PRATICO_EM_VIDEO);

    expect(
      screen.getByText("Não deve aparecer o rosto da criança, só a produção."),
    ).toBeInTheDocument();
    expect(screen.getByText(/fica guardado/i)).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /entregar ao mestre no encontro/i }),
    ).toBeInTheDocument();
  });

  it("não declara que cumpriu antes de a comprovação estar escolhida", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio");
    await renderizar(PRATICO_EM_VIDEO);

    expect(screen.getByRole("button", { name: /já cumpri/i })).toBeDisabled();
    expect(submeter).not.toHaveBeenCalled();
  });

  it("a entrega no encontro segue pela mesma rota, sem mídia", async () => {
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: null,
      aguardando_mestre: true,
      acertos: 0,
      total: 0,
      comprovacao_entregue: {
        forma: "video",
        comprovacao: null,
        entrega_presencial: true,
        tem_arquivo: false,
      },
    });
    await renderizar(PRATICO_EM_VIDEO);
    const usuario = userEvent.setup();

    await usuario.click(
      screen.getByRole("button", { name: /entregar ao mestre no encontro/i }),
    );

    expect(submeter).toHaveBeenCalledWith("missao-1", null, "token-do-guerreiro", {
      entrega_presencial: true,
    });
  });
});

// O veredito do Mestre, dito ao Guerreiro(a): nada do julgamento fica gravado
// sem ser lido por ele (`RF-05-94`, `RN-05-20`, `RN-09-54`).
describe("o veredito do Mestre na tela do prático", () => {
  const PRATICO_EM_TEXTO: trilhaApi.DesafioDeDesbloqueio = {
    tipo: "pratico",
    enunciado: "Monte o robô e conte como fez.",
    perguntas: null,
    forma_de_comprovacao: "texto",
    criterio_de_aceite: "Conte como montou, sem citar nome de colega.",
    titulo_curto: "Robô de sucata",
  };

  const ENTREGUE: trilhaApi.ComprovacaoEntregue = {
    forma: "texto",
    comprovacao: "Montei com sucata do pátio.",
    entrega_presencial: false,
    tem_arquivo: false,
  };

  async function renderizarJulgado(
    julgamento: trilhaApi.JulgamentoDoPratico | null,
    entregue: trilhaApi.ComprovacaoEntregue | null = ENTREGUE,
  ) {
    sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    await act(async () => {
      render(
        <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
          <DesafioDeDesbloqueio
            missaoId="missao-1"
            desafio={PRATICO_EM_TEXTO}
            aoDesbloquear={vi.fn()}
            submissaoLigada
            comprovacaoEntregue={entregue}
            julgamento={julgamento}
          />
        </ProvedorDeSessao>,
      );
    });
  }

  afterEach(() => {
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("cumprido e publicável, a tela diz as duas coisas", async () => {
    await renderizarJulgado({
      cumpriu: true,
      publicavel: true,
      motivo: null,
      julgado_em: "2026-11-04T10:00:00-03:00",
    });

    expect(screen.getByText(/você cumpriu o desafio/i)).toBeInTheDocument();
    expect(screen.getByText(/pode aparecer na vitrine/i)).toBeInTheDocument();
  });

  it("cumprido e não publicável, a tela diz o motivo como o Mestre o escreveu", async () => {
    await renderizarJulgado({
      cumpriu: true,
      publicavel: false,
      motivo: "Ficou ótimo, mas aparece o rosto de um colega.",
      julgado_em: "2026-11-04T10:00:00-03:00",
    });

    expect(screen.getByText(/você cumpriu o desafio/i)).toBeInTheDocument();
    expect(screen.getByText(/não vai para a vitrine/i)).toBeInTheDocument();
    expect(
      screen.getByText("Ficou ótimo, mas aparece o rosto de um colega."),
    ).toBeInTheDocument();
  });

  it("não cumprido, traz o motivo na íntegra e o convite a entregar de novo", async () => {
    await renderizarJulgado({
      cumpriu: false,
      publicavel: false,
      motivo: "Faltou mostrar a peça montada.",
      julgado_em: "2026-11-04T10:00:00-03:00",
    });

    expect(screen.getByText(/pediu para você fazer mais uma vez/i)).toBeInTheDocument();
    expect(screen.getByText("Faltou mostrar a peça montada.")).toBeInTheDocument();
    // A entrega reabre: o campo volta, com o que ele mandou antes à vista.
    expect(screen.getByText(/o que você entregou antes/i)).toBeInTheDocument();
    expect(screen.getByText("Montei com sucata do pátio.")).toBeInTheDocument();
    expect(screen.getByLabelText(/conte o que você fez/i)).toBeInTheDocument();
  });

  it("o veredito não vira nota, contagem de tentativas nem comparação", async () => {
    await renderizarJulgado({
      cumpriu: false,
      publicavel: false,
      motivo: "Faltou mostrar a peça montada.",
      julgado_em: "2026-11-04T10:00:00-03:00",
    });

    expect(screen.queryByText(/nota|tentativa|pontos?\b|colegas/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/reprovad|eliminad|falhou/i)).not.toBeInTheDocument();
  });

  it("antes do julgamento, a tela segue dizendo que aguarda o Mestre", async () => {
    await renderizarJulgado(null);

    expect(screen.getByText(/esperar o Mestre conferir/i)).toBeInTheDocument();
    expect(screen.queryByText(/vitrine/i)).not.toBeInTheDocument();
  });

  it("cumprido, a tela não oferece entregar de novo", async () => {
    await renderizarJulgado({
      cumpriu: true,
      publicavel: true,
      motivo: null,
      julgado_em: "2026-11-04T10:00:00-03:00",
    });

    expect(screen.getByText(/o que você entregou/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/conte o que você fez/i)).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /declarar que cumpri/i }),
    ).not.toBeInTheDocument();
  });
});
