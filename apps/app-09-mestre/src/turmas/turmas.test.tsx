import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as responsaveisApi from "../responsaveis/api";
import type {
  AtividadeDoMestre,
  AulaDaTurma,
  MinhasTurmas,
  OcorrenciaDeConduta,
  PresencaDaAula,
  ResultadoDaAula,
  SituacaoDoPratico,
} from "./api";
import * as turmasApi from "./api";
import { TelaDeMinhasTurmas } from "./TelaDeMinhasTurmas";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

vi.mock("../api/configuracao", () => ({
  URL_DA_APP_03: "https://gestao.example.org",
}));

vi.mock("../direitos/ContextoDeDireitos", async () => {
  const real = await vi.importActual<typeof import("../direitos/ContextoDeDireitos")>(
    "../direitos/ContextoDeDireitos",
  );
  return { ...real, useDireitos: () => ({ irParaDireitos: vi.fn() }) };
});

import { useSessao } from "comum/autenticacao";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

function configurarSessao() {
  vi.mocked(useSessao).mockReturnValue({
    sessao: SESSAO_DE_MESTRE,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

function aula(sobrescreve: Partial<AulaDaTurma> = {}): AulaDaTurma {
  return {
    id: "aula-1",
    comunidade_virtual_id: "comunidade-1",
    ponto_de_apoio_id: "ponto-1",
    inicio_em: "2026-08-01T10:00:00-03:00",
    fim_em: "2026-08-01T12:00:00-03:00",
    situacao: "confirmada",
    cancelamento_motivo: null,
    recursos_faltantes: [],
    ...sobrescreve,
  };
}

function atividade(sobrescreve: Partial<AtividadeDoMestre> = {}): AtividadeDoMestre {
  return {
    id: "atividade-1",
    missao_id: "missao-1",
    titulo: "Montagem do robô",
    formato: "presencial",
    modalidade: "individual",
    aula_id: null,
    ...sobrescreve,
  };
}

function turmas(sobrescreve: Partial<MinhasTurmas> = {}): MinhasTurmas {
  return {
    itens: [aula()],
    proximo_cursor: null,
    atividades_presenciais: [atividade()],
    atividades_on_line: [],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

// Os Guerreiros e Guerreiras das comunidades do Mestre, em duas páginas, para
// a tela da aula converter o nick digitado no id (`RF-09-45`, `RF-09-46`).
function configurarGuerreiros() {
  return vi
    .spyOn(responsaveisApi, "listarGuerreirosVinculaveis")
    .mockImplementation(async (_token, cursor) =>
      cursor === "pagina-2"
        ? {
            itens: [{ id: "guerreiro-2", nick: "Dandara", avatar: "a2" }],
            proximo_cursor: null,
          }
        : {
            itens: [{ id: "guerreiro-1", nick: "Zeferina", avatar: "a1" }],
            proximo_cursor: "pagina-2",
          },
    );
}

function formulario(nome: RegExp) {
  return within(screen.getByRole("form", { name: nome }));
}

const daPresenca = () => formulario(/^confirmar presença$/i);
const daOcorrencia = () => formulario(/^lançar ocorrência de conduta$/i);
const doLancamento = () => formulario(/^lançar resultado de uma atividade$/i);

describe("lista das turmas do Mestre (RF-09-42, RF-09-73)", () => {
  it("lista as aulas e as atividades on-line, sem seção de presenciais", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({
        atividades_presenciais: [atividade({ id: "presencial-1", titulo: "Oficina" })],
        atividades_on_line: [
          atividade({ id: "on-line-1", titulo: "Fórum", formato: "on_line_assincrona" }),
        ],
      }),
    );

    render(<TelaDeMinhasTurmas />);

    expect(await screen.findByText("Fórum")).toBeInTheDocument();
    expect(screen.queryByText("Oficina")).not.toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: /atividades presenciais/i }),
    ).not.toBeInTheDocument();
  });

  it("a atividade presencial segue oferecida para lançamento na tela da aula", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({
        atividades_presenciais: [atividade({ id: "presencial-1", titulo: "Oficina" })],
      }),
    );
    vi.spyOn(turmasApi, "listarPresencasDaAula").mockResolvedValue([]);
    vi.spyOn(turmasApi, "listarResultadosDaAula").mockResolvedValue([]);

    render(<TelaDeMinhasTurmas />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /presença e ocorrência/i }));

    const opcoes = doLancamento().getByLabelText(/^atividade$/i);
    expect(opcoes).toHaveTextContent("Oficina");
    expect(screen.queryByRole("list", { name: /atividades para lançamento/i })).toBeNull();
  });

  it("turma sem aula nem atividade mostra o estado vazio", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [], atividades_presenciais: [], atividades_on_line: [] }),
    );

    render(<TelaDeMinhasTurmas />);

    // Só aulas canceladas chegam como lista vazia: o núcleo já não as devolve.
    expect(await screen.findByText(/nenhuma aula agendada/i)).toBeInTheDocument();
    expect(screen.getByText(/nenhuma atividade on-line sua/i)).toBeInTheDocument();
  });
});

const UMA_HORA_EM_MS = 60 * 60 * 1000;

function janelaEmAndamento(): Pick<AulaDaTurma, "inicio_em" | "fim_em"> {
  const agora = Date.now();
  return {
    inicio_em: new Date(agora - UMA_HORA_EM_MS).toISOString(),
    fim_em: new Date(agora + UMA_HORA_EM_MS).toISOString(),
  };
}

function janelaFutura(): Pick<AulaDaTurma, "inicio_em" | "fim_em"> {
  const agora = Date.now();
  return {
    inicio_em: new Date(agora + UMA_HORA_EM_MS).toISOString(),
    fim_em: new Date(agora + 2 * UMA_HORA_EM_MS).toISOString(),
  };
}

function janelaPassada(): Pick<AulaDaTurma, "inicio_em" | "fim_em"> {
  const agora = Date.now();
  return {
    inicio_em: new Date(agora - 2 * UMA_HORA_EM_MS).toISOString(),
    fim_em: new Date(agora - UMA_HORA_EM_MS).toISOString(),
  };
}

describe("caminho para o painel do dia (RF-09-50)", () => {
  it("a aula em andamento oferece o caminho para o painel do dia", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [aula(janelaEmAndamento())] }),
    );

    render(<TelaDeMinhasTurmas />);

    const caminho = await screen.findByRole("link", { name: /painel do dia/i });
    expect(caminho).toHaveAttribute("href", "https://gestao.example.org/?area=painel-do-dia");
  });

  it("aula futura não oferece o caminho", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [aula(janelaFutura())] }),
    );

    render(<TelaDeMinhasTurmas />);

    await screen.findByRole("button", { name: /presença e ocorrência/i });
    expect(screen.queryByRole("link", { name: /painel do dia/i })).not.toBeInTheDocument();
  });

  it("aula já realizada não oferece o caminho", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [aula({ ...janelaPassada(), situacao: "realizada" })] }),
    );

    render(<TelaDeMinhasTurmas />);

    await screen.findByRole("button", { name: /presença e ocorrência/i });
    expect(screen.queryByRole("link", { name: /painel do dia/i })).not.toBeInTheDocument();
  });

  it("aula realizada sem lastro aparece com o rótulo próprio", async () => {
    // A pendente que chegou ao fim do horário (`RF-07-55`, `RF-01-91`).
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [aula({ ...janelaPassada(), situacao: "realizada_sem_lastro" })] }),
    );

    render(<TelaDeMinhasTurmas />);

    expect(await screen.findByText(/realizada sem lastro/i)).toBeInTheDocument();
  });

  it("aula cancelada dentro da janela não oferece o caminho", async () => {
    configurarSessao();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(
      turmas({ itens: [aula({ ...janelaEmAndamento(), situacao: "cancelada" })] }),
    );

    render(<TelaDeMinhasTurmas />);

    await screen.findByRole("button", { name: /presença e ocorrência/i });
    expect(screen.queryByRole("link", { name: /painel do dia/i })).not.toBeInTheDocument();
  });
});

describe("lançamento do resultado na tela da aula (RF-09-148 a RF-09-151)", () => {
  function situacao(sobrescreve: Partial<SituacaoDoPratico> = {}): SituacaoDoPratico {
    return {
      missao_id: "missao-1",
      tipo_do_desafio: null,
      forma_aceita: null,
      criterio_de_aceite: null,
      estado: "sem_declaracao",
      motivo_do_julgamento: null,
      comprovacao_entregue: null,
      exige_julgamento: false,
      ...sobrescreve,
    };
  }

  function lancado(sobrescreve: Partial<ResultadoDaAula> = {}): ResultadoDaAula {
    return {
      id: "resultado-1",
      guerreiro_id: "guerreiro-1",
      nick: "Zeferina",
      atividade_id: "atividade-1",
      atividade_titulo: "Montagem do robô",
      momento_do_fato: "2026-08-01T10:00:00-03:00",
      desfecho: "realizada",
      comprovante_tipo: "texto",
      comprovante_texto: "Montou o robô.",
      tem_arquivo: false,
      ...sobrescreve,
    };
  }

  async function abrir(
    pratico: SituacaoDoPratico = situacao(),
    lancados: ResultadoDaAula[] = [],
  ) {
    configurarSessao();
    configurarGuerreiros();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(turmas());
    vi.spyOn(turmasApi, "listarPresencasDaAula").mockResolvedValue([]);
    const lidos = vi.spyOn(turmasApi, "listarResultadosDaAula").mockResolvedValue(lancados);
    const situacaoEspiada = vi
      .spyOn(turmasApi, "lerSituacaoDoPratico")
      .mockResolvedValue(pratico);

    render(<TelaDeMinhasTurmas />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /presença e ocorrência/i }));
    return { usuario, lidos, situacaoEspiada };
  }

  async function preencher(usuario: ReturnType<typeof userEvent.setup>, nick = "Zeferina") {
    await usuario.selectOptions(doLancamento().getByLabelText(/^atividade$/i), "atividade-1");
    await usuario.type(doLancamento().getByLabelText(/nick do guerreiro/i), nick);
  }

  it("não lista atividades com botão: o formulário traz o select, o nick e o aviso", async () => {
    await abrir();

    expect(screen.queryByRole("button", { name: /^lançar$/i })).toBeNull();
    expect(doLancamento().getByLabelText(/^atividade$/i)).toBeInTheDocument();
    expect(doLancamento().getByLabelText(/nick do guerreiro/i)).toBeInTheDocument();
    expect(doLancamento().queryByLabelText(/identificador/i)).toBeNull();
    expect(doLancamento().queryByLabelText(/^produção$/i)).toBeNull();
    expect(screen.getByText(/coleta o comprovante do resultado/i)).toHaveAttribute(
      "role",
      "status",
    );
  });

  it("o Mestre lança um Guerreiro(a) com comprovante em texto, e a lista recarrega", async () => {
    const { usuario, lidos } = await abrir();
    const lancarEspiado = vi
      .spyOn(turmasApi, "lancarResultadoDaAtividade")
      .mockResolvedValue({} as never);

    await preencher(usuario, " zeferina ");
    await usuario.type(doLancamento().getByLabelText(/^comprovante/i), "Montou o robô.");
    await usuario.click(doLancamento().getByRole("button", { name: /lançar resultado/i }));

    await waitFor(() => expect(lancarEspiado).toHaveBeenCalled());
    const [idDaAtividade, idDaAula, participante] = lancarEspiado.mock.calls[0];
    expect(idDaAtividade).toBe("atividade-1");
    expect(idDaAula).toBe("aula-1");
    expect(participante.guerreiro_id).toBe("guerreiro-1");
    expect(participante.comprovante).toEqual({ tipo: "texto", texto: "Montou o robô." });
    expect(participante.julgamento_do_pratico).toBeUndefined();
    expect(await screen.findByText(/lançamento registrado/i)).toBeInTheDocument();
    expect(lidos).toHaveBeenCalledTimes(2);
  });

  it("o Mestre anexa uma foto: sobe antes e lança referenciando o envio", async () => {
    const { usuario } = await abrir();
    const abrirEspiado = vi
      .spyOn(turmasApi, "abrirEnvioDoComprovante")
      .mockResolvedValue({ envio_id: "envio-1", endereco_da_sessao: "/sessao" });
    const trilhasApi = await import("../trilhas/api");
    const enviarEspiado = vi.spyOn(trilhasApi, "enviarArquivo").mockResolvedValue();
    const lancarEspiado = vi
      .spyOn(turmasApi, "lancarResultadoDaAtividade")
      .mockResolvedValue({} as never);

    await preencher(usuario);
    await usuario.selectOptions(
      doLancamento().getByLabelText(/forma do comprovante/i),
      "imagem",
    );
    const foto = new File(["abc"], "foto.jpg", { type: "image/jpeg" });
    await usuario.upload(doLancamento().getByLabelText(/arquivo do comprovante/i), foto);
    await usuario.click(doLancamento().getByRole("button", { name: /lançar resultado/i }));

    await waitFor(() => expect(lancarEspiado).toHaveBeenCalled());
    expect(abrirEspiado.mock.calls[0].slice(0, 4)).toEqual([
      "atividade-1",
      "imagem",
      "image/jpeg",
      3,
    ]);
    expect(enviarEspiado.mock.calls[0][0]).toBe("/sessao");
    expect(lancarEspiado.mock.calls[0][2].comprovante).toEqual({
      tipo: "imagem",
      envio_id: "envio-1",
    });
  });

  it("sem atividade, nick conhecido ou comprovante, a tela recusa sem chamar o núcleo", async () => {
    const { usuario } = await abrir();
    const lancarEspiado = vi.spyOn(turmasApi, "lancarResultadoDaAtividade");
    const botao = () => doLancamento().getByRole("button", { name: /lançar resultado/i });

    await usuario.click(botao());
    expect(await screen.findByText(/escolha a atividade/i)).toBeInTheDocument();

    await usuario.selectOptions(doLancamento().getByLabelText(/^atividade$/i), "atividade-1");
    await usuario.type(doLancamento().getByLabelText(/nick do guerreiro/i), "Joaninha");
    await usuario.click(botao());
    expect(await screen.findByText(/não encontramos o nick "joaninha"/i)).toBeInTheDocument();

    await usuario.clear(doLancamento().getByLabelText(/nick do guerreiro/i));
    await usuario.type(doLancamento().getByLabelText(/nick do guerreiro/i), "Zeferina");
    await usuario.click(botao());
    expect(await screen.findByText(/escreva o comprovante/i)).toBeInTheDocument();
    expect(lancarEspiado).not.toHaveBeenCalled();
  });

  it("sem prático pendente, os campos do julgamento não aparecem", async () => {
    const { usuario, situacaoEspiada } = await abrir(situacao({ tipo_do_desafio: "quiz" }));
    await preencher(usuario);

    await waitFor(() =>
      expect(situacaoEspiada).toHaveBeenCalledWith(
        "missao-1",
        "guerreiro-1",
        "token-do-mestre",
      ),
    );
    expect(screen.queryByRole("group", { name: /julgamento do desafio prático/i })).toBeNull();
  });

  it("sem declaração, o julgamento aparece e avisa que o comprovante vira a comprovação", async () => {
    const { usuario } = await abrir(
      situacao({
        tipo_do_desafio: "pratico",
        forma_aceita: "texto",
        criterio_de_aceite: "Só a produção, sem rosto.",
        exige_julgamento: true,
      }),
    );
    const lancarEspiado = vi
      .spyOn(turmasApi, "lancarResultadoDaAtividade")
      .mockResolvedValue({} as never);
    await preencher(usuario);

    const julgamento = within(
      await screen.findByRole("group", { name: /julgamento do desafio prático/i }),
    );
    expect(julgamento.getByText(/só a produção, sem rosto/i)).toBeInTheDocument();
    expect(julgamento.getByText(/será a comprovação do desafio prático/i)).toBeInTheDocument();

    await usuario.type(doLancamento().getByLabelText(/^comprovante/i), "Fez.");
    await usuario.click(julgamento.getByLabelText(/pode ir à vitrine/i));
    await usuario.click(doLancamento().getByRole("button", { name: /lançar resultado/i }));

    await waitFor(() => expect(lancarEspiado).toHaveBeenCalled());
    expect(lancarEspiado.mock.calls[0][2].julgamento_do_pratico).toEqual({
      cumpriu: true,
      publicavel: true,
      motivo: null,
    });
  });

  it("declarando em nome, comprovante fora da forma aceita é recusado na tela", async () => {
    const { usuario } = await abrir(
      situacao({ tipo_do_desafio: "pratico", forma_aceita: "video", exige_julgamento: true }),
    );
    const lancarEspiado = vi.spyOn(turmasApi, "lancarResultadoDaAtividade");
    await preencher(usuario);
    await screen.findByRole("group", { name: /julgamento do desafio prático/i });

    await usuario.selectOptions(
      doLancamento().getByLabelText(/forma do comprovante/i),
      "texto",
    );
    await usuario.type(doLancamento().getByLabelText(/^comprovante/i), "Fez.");
    await usuario.click(doLancamento().getByRole("button", { name: /lançar resultado/i }));

    expect(await screen.findByText(/aceita comprovação em vídeo/i)).toBeInTheDocument();
    expect(lancarEspiado).not.toHaveBeenCalled();
  });

  it("com declaração aguardando, mostra a entrega do Guerreiro(a) e exige motivo ao recusar", async () => {
    const { usuario } = await abrir(
      situacao({
        tipo_do_desafio: "pratico",
        forma_aceita: "texto",
        estado: "aguardando",
        exige_julgamento: true,
        comprovacao_entregue: {
          forma: "texto",
          comprovacao: "Eu montei sozinha.",
          entrega_presencial: false,
          tem_arquivo: false,
          tipo_do_arquivo: null,
        },
      }),
    );
    const lancarEspiado = vi.spyOn(turmasApi, "lancarResultadoDaAtividade");
    await preencher(usuario);

    const julgamento = within(
      await screen.findByRole("group", { name: /julgamento do desafio prático/i }),
    );
    expect(julgamento.getByText("Eu montei sozinha.")).toBeInTheDocument();

    await usuario.type(doLancamento().getByLabelText(/^comprovante/i), "Visto.");
    await usuario.click(julgamento.getByLabelText(/cumpriu o desafio/i));
    await usuario.click(doLancamento().getByRole("button", { name: /lançar resultado/i }));

    expect(await screen.findByText(/escreva o motivo/i)).toBeInTheDocument();
    expect(lancarEspiado).not.toHaveBeenCalled();
  });

  it("a recusa do núcleo chega em linguagem simples (RN-09-16)", async () => {
    const { usuario } = await abrir();
    vi.spyOn(turmasApi, "lancarResultadoDaAtividade").mockRejectedValue(
      new ErroDaApi(403, { codigo: "permissao_negada", mensagem: "Só o Mestre autor lança." }),
    );
    await preencher(usuario);
    await usuario.type(doLancamento().getByLabelText(/^comprovante/i), "Fez.");
    await usuario.click(doLancamento().getByRole("button", { name: /lançar resultado/i }));

    expect(await screen.findByText(/só o mestre autor lança/i)).toBeInTheDocument();
  });

  it("lista os lançados nesta aula com o comprovante, e abre a foto a pedido", async () => {
    const lerEspiado = vi
      .spyOn(turmasApi, "lerComprovanteDoResultado")
      .mockResolvedValue(new Blob(["x"], { type: "image/jpeg" }));
    const { usuario } = await abrir(situacao(), [
      lancado(),
      lancado({
        id: "resultado-2",
        nick: "Dandara",
        comprovante_tipo: "imagem",
        comprovante_texto: null,
        tem_arquivo: true,
      }),
    ]);

    const lista = within(await screen.findByRole("list", { name: /lançados nesta aula/i }));
    expect(lista.getByText(/zeferina — montagem do robô/i)).toBeInTheDocument();
    expect(lista.getByText("Montou o robô.")).toBeInTheDocument();
    await usuario.click(lista.getByRole("button", { name: /abrir comprovante/i }));
    await waitFor(() =>
      expect(lerEspiado).toHaveBeenCalledWith("resultado-2", "token-do-mestre"),
    );
  });

  it("lista vazia é dita em linguagem simples", async () => {
    await abrir();
    expect(
      await screen.findByText(/nenhum resultado lançado nesta aula/i),
    ).toBeInTheDocument();
  });
});

describe("presença e ocorrência de conduta (RF-09-45, RF-09-46)", () => {
  async function abrirTelaDaAula() {
    configurarSessao();
    configurarGuerreiros();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(turmas());
    vi.spyOn(turmasApi, "listarPresencasDaAula").mockResolvedValue([]);
    vi.spyOn(turmasApi, "listarResultadosDaAula").mockResolvedValue([]);

    render(<TelaDeMinhasTurmas />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /presença e ocorrência/i }));
    return usuario;
  }

  it("mostra o aviso de coleta da presença e da ocorrência, sem bloquear o envio", async () => {
    await abrirTelaDaAula();

    expect(screen.getByText(/coleta a presença do guerreiro/i)).toHaveAttribute(
      "role",
      "status",
    );
    expect(
      screen.getByText(/coleta a ocorrência de conduta e o motivo da pontuação negativa/i),
    ).toHaveAttribute("role", "status");
  });

  it("o Mestre confirma a presença que faltou", async () => {
    const usuario = await abrirTelaDaAula();
    const confirmarEspiado = vi.spyOn(turmasApi, "confirmarPresenca").mockResolvedValue({
      id: "presenca-1",
      aula_id: "aula-1",
      guerreiro_id: "guerreiro-1",
      modo: "confirmacao",
      confirmador_id: "mestre-1",
      momento_do_fato: "2026-08-01T10:00:00-03:00",
    });

    await usuario.type(daPresenca().getByLabelText(/nick do guerreiro/i), "  dandara ");
    const campoDeData = screen.getByLabelText(/momento em que esteve presente/i);
    await usuario.type(campoDeData, "2026-08-01T10:00");

    await usuario.click(screen.getByRole("button", { name: /^confirmar presença$/i }));

    await waitFor(() => expect(confirmarEspiado).toHaveBeenCalled());
    expect(confirmarEspiado.mock.calls[0][1]).toBe("guerreiro-2");
    expect(await screen.findByText(/presença confirmada/i)).toBeInTheDocument();
  });

  it("a ocorrência exige o motivo", async () => {
    const usuario = await abrirTelaDaAula();
    const lancarEspiado = vi.spyOn(turmasApi, "lancarOcorrenciaDeConduta");

    await usuario.type(daOcorrencia().getByLabelText(/nick do guerreiro/i), "Zeferina");
    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    expect(await screen.findByText(/motivo é obrigatório/i)).toBeInTheDocument();
    expect(lancarEspiado).not.toHaveBeenCalled();
  });

  it("o Mestre lança a ocorrência sem informar valor algum", async () => {
    const usuario = await abrirTelaDaAula();
    const ocorrencia: OcorrenciaDeConduta = {
      id: "ocorrencia-1",
      guerreiro_id: "guerreiro-1",
      aula_id: "aula-1",
      atividade_id: "atividade-1",
      valor: 5,
      motivo: "Desrespeitou um colega.",
      momento_do_fato: "2026-08-01T10:00:00-03:00",
    };
    const lancarEspiado = vi
      .spyOn(turmasApi, "lancarOcorrenciaDeConduta")
      .mockResolvedValue(ocorrencia);

    await usuario.selectOptions(daOcorrencia().getByLabelText(/^atividade$/i), "atividade-1");
    await usuario.type(daOcorrencia().getByLabelText(/nick do guerreiro/i), "ZEFERINA");
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Desrespeitou um colega.");

    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    await waitFor(() => expect(lancarEspiado).toHaveBeenCalled());
    const chamada = lancarEspiado.mock.calls[0];
    expect(chamada[0]).toBe("guerreiro-1");
    expect(chamada[3]).toBe("Desrespeitou um colega.");
    expect(await screen.findByText(/ocorrência registrada/i)).toBeInTheDocument();
  });

  it("o Guerreiro(a) é informado pelo nick, sem campo de identificador", async () => {
    await abrirTelaDaAula();

    expect(screen.getAllByLabelText(/nick do guerreiro/i)).toHaveLength(3);
    expect(screen.queryByLabelText(/identificador do guerreiro/i)).toBeNull();
  });

  it("nick não encontrado é recusado na tela, sem chamar o núcleo", async () => {
    const usuario = await abrirTelaDaAula();
    const confirmarEspiado = vi.spyOn(turmasApi, "confirmarPresenca");

    await usuario.type(daPresenca().getByLabelText(/nick do guerreiro/i), "Joaninha");
    await usuario.click(screen.getByRole("button", { name: /^confirmar presença$/i }));

    expect(await screen.findByText(/não encontramos o nick "joaninha"/i)).toBeInTheDocument();
    expect(confirmarEspiado).not.toHaveBeenCalled();
  });

  it("enviar sem o nick é impedido nos dois formulários", async () => {
    const usuario = await abrirTelaDaAula();
    const confirmarEspiado = vi.spyOn(turmasApi, "confirmarPresenca");
    const lancarEspiado = vi.spyOn(turmasApi, "lancarOcorrenciaDeConduta");

    await usuario.click(screen.getByRole("button", { name: /^confirmar presença$/i }));
    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    expect(await screen.findAllByText(/informe o nick do guerreiro/i)).toHaveLength(2);
    expect(confirmarEspiado).not.toHaveBeenCalled();
    expect(lancarEspiado).not.toHaveBeenCalled();
  });

  it("o teto da aula é explicado em linguagem simples (RN-09-16)", async () => {
    const usuario = await abrirTelaDaAula();
    vi.spyOn(turmasApi, "lancarOcorrenciaDeConduta").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O teto da aula foi alcançado.",
      }),
    );

    await usuario.type(daOcorrencia().getByLabelText(/nick do guerreiro/i), "ZEFERINA");
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Desrespeitou um colega.");
    await usuario.click(screen.getByRole("button", { name: /^lançar ocorrência$/i }));

    expect(await screen.findByText(/teto da aula foi alcançado/i)).toBeInTheDocument();
  });
});

describe("presentes nesta aula (RF-09-145, RN-09-18)", () => {
  function presenca(sobrescreve: Partial<PresencaDaAula> = {}): PresencaDaAula {
    return {
      id: "presenca-1",
      guerreiro_id: "guerreiro-1",
      nick: "Zeferina",
      nome: "Zeferina da Silva",
      avatar: null,
      momento_do_fato: "2026-08-01T10:05:00-03:00",
      modo: "reconhecimento",
      ...sobrescreve,
    };
  }

  async function abrir() {
    configurarSessao();
    configurarGuerreiros();
    vi.spyOn(turmasApi, "listarMinhasTurmas").mockResolvedValue(turmas());
    vi.spyOn(turmasApi, "listarResultadosDaAula").mockResolvedValue([]);
    render(<TelaDeMinhasTurmas />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /presença e ocorrência/i }));
    return usuario;
  }

  it("lista cada presente por avatar desenhado, nick e nome, com hora e modo", async () => {
    const listar = vi.spyOn(turmasApi, "listarPresencasDaAula").mockResolvedValue([
      presenca(),
      presenca({
        id: "presenca-2",
        nick: "Dandara",
        nome: "Dandara dos Palmares",
        modo: "confirmacao",
      }),
    ]);

    await abrir();

    const lista = await screen.findByRole("list", { name: /^presentes$/i });
    expect(listar).toHaveBeenCalledWith("aula-1", "token-do-mestre");
    expect(lista).toHaveTextContent("Zeferina — Zeferina da Silva");
    expect(lista).toHaveTextContent("Reconhecimento");
    expect(lista).toHaveTextContent("Dandara — Dandara dos Palmares");
    expect(lista).toHaveTextContent("Confirmação");
    expect(lista.querySelectorAll("svg")).toHaveLength(2);
    expect(lista.querySelector("img")).toBeNull();
  });

  it("presente sem nome cadastrado aparece com a marca sem nome", async () => {
    vi.spyOn(turmasApi, "listarPresencasDaAula").mockResolvedValue([presenca({ nome: null })]);

    await abrir();

    const lista = await screen.findByRole("list", { name: /^presentes$/i });
    expect(lista).toHaveTextContent("Zeferina — sem nome");
  });

  it("aula sem presença diz que a lista está vazia", async () => {
    vi.spyOn(turmasApi, "listarPresencasDaAula").mockResolvedValue([]);

    await abrir();

    expect(
      await screen.findByText(/nenhuma presença registrada nesta aula/i),
    ).toBeInTheDocument();
  });

  it("a falha da leitura não trava os formulários", async () => {
    vi.spyOn(turmasApi, "listarPresencasDaAula").mockRejectedValue(new Error("rede"));

    await abrir();

    expect(
      await screen.findByText(/não foi possível carregar os presentes/i),
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /^confirmar presença$/i })).toBeEnabled();
    expect(screen.getByRole("button", { name: /^lançar ocorrência$/i })).toBeEnabled();
  });

  it("a presença confirmada recarrega a lista dos presentes", async () => {
    const listar = vi
      .spyOn(turmasApi, "listarPresencasDaAula")
      .mockResolvedValueOnce([])
      .mockResolvedValueOnce([presenca({ modo: "confirmacao" })]);
    vi.spyOn(turmasApi, "confirmarPresenca").mockResolvedValue({
      id: "presenca-1",
      aula_id: "aula-1",
      guerreiro_id: "guerreiro-1",
      modo: "confirmacao",
      confirmador_id: "mestre-1",
      momento_do_fato: "2026-08-01T10:05:00-03:00",
    });
    const usuario = await abrir();
    await screen.findByText(/nenhuma presença registrada nesta aula/i);

    await usuario.type(daPresenca().getByLabelText(/nick do guerreiro/i), "Zeferina");
    await usuario.type(
      screen.getByLabelText(/momento em que esteve presente/i),
      "2026-08-01T10:05",
    );
    await usuario.click(screen.getByRole("button", { name: /^confirmar presença$/i }));

    const lista = await screen.findByRole("list", { name: /^presentes$/i });
    expect(lista).toHaveTextContent("Zeferina");
    expect(listar).toHaveBeenCalledTimes(2);
  });
});
