import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as aportesApi from "../aportes/api";
import * as chavesApi from "../chaves/api";
import * as comunidadesApi from "../comunidades/api";
import * as personasApi from "../personas/api";
import * as pontosDeApoioApi from "../pontos-de-apoio/api";
import * as recursosApi from "../recursos/api";
import type {
  SolicitacaoDeChave,
  SolicitacaoDeDados,
  SolicitacaoDeParticipacao,
  SolicitacaoDoResponsavel,
  Sugestao,
} from "./api";
import * as filasApi from "./api";
import { TelaDeFilas } from "./TelaDeFilas";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

const COMUNIDADE = {
  id: "comunidade-1",
  nome: "Comunidade de Teste",
  localizacao: "Bairro de teste",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const PONTO_DE_APOIO = {
  id: "ponto-1",
  nome: "Sede",
  comunidade_virtual_id: COMUNIDADE.id,
  responsavel_id: null,
  ativo: true,
};

const TIPO_DE_RECURSO = {
  id: "tipo-1",
  nome: "Lanche",
  natureza: "consumivel",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "1.50",
  vigencia_inicio: "2026-01-01",
};

function solicitacaoDeMestre(
  parcial: Partial<SolicitacaoDeParticipacao> = {},
): SolicitacaoDeParticipacao {
  return {
    id: "solicitacao-1",
    nome_ou_razao_social: "Fulano de Tal",
    email: "fulano@example.org",
    whatsapp: "11999990000",
    pretensao: "mestre",
    apresentacao: "Quero ser Mestre.",
    instituicao: null,
    links: null,
    situacao: "recebida",
    prazo: "2026-08-29T00:00:00-03:00",
    em_atraso: false,
    avaliado_por_id: null,
    parecer: null,
    decidido_em: null,
    nick: null,
    aporte_declarado: null,
    comprovante_anexado: false,
    ...parcial,
  };
}

function solicitacaoDeApoiador(
  parcial: Partial<SolicitacaoDeParticipacao> = {},
): SolicitacaoDeParticipacao {
  return solicitacaoDeMestre({
    pretensao: "apoiador",
    nick: "apoiador-pretendido",
    aporte_declarado: "R$ 100 em lanches",
    comprovante_anexado: true,
    ...parcial,
  });
}

function solicitacaoDeDados(parcial: Partial<SolicitacaoDeDados> = {}): SolicitacaoDeDados {
  return {
    id: "dados-1",
    solicitante: "Pesquisadora de Tal",
    instituicao: "Universidade de Teste",
    finalidade_declarada: "Pesquisa acadêmica sobre evasão escolar.",
    recorte_pedido: "Comunidade de Teste, 2026",
    situacao: "recebida",
    prazo: "2026-08-29T00:00:00-03:00",
    em_atraso: false,
    avaliado_por_id: null,
    parecer: null,
    decidido_em: null,
    entregue: null,
    ...parcial,
  };
}

function solicitacaoDeChave(parcial: Partial<SolicitacaoDeChave> = {}): SolicitacaoDeChave {
  return {
    id: "chave-1",
    solicitante: "Desenvolvedora de Tal",
    contato: "dev@example.org",
    instituicao: null,
    o_que_pretende_construir: "Um painel comunitário.",
    situacao: "recebida",
    prazo: "2026-08-29T00:00:00-03:00",
    em_atraso: false,
    avaliado_por_id: null,
    parecer: null,
    decidido_em: null,
    chave_emitida: false,
    ...parcial,
  };
}

function solicitacaoDoResponsavel(
  parcial: Partial<SolicitacaoDoResponsavel> = {},
): SolicitacaoDoResponsavel {
  return {
    id: "responsavel-1",
    responsavel_id: "responsavel-persona-1",
    nick_do_responsavel: "mae-da-zeferina",
    guerreiro_id: "guerreiro-1",
    nick_do_guerreiro: "zeferina",
    tipo: "acesso",
    texto: "Quero ver os dados da minha filha.",
    situacao: "recebida",
    prazo: "2026-08-29T00:00:00-03:00",
    em_atraso: false,
    tratado_por_id: null,
    desfecho: null,
    tratado_em: null,
    ...parcial,
  };
}

function sugestao(parcial: Partial<Sugestao> = {}): Sugestao {
  return {
    id: "sugestao-1",
    autor_id: "guerreiro-1",
    papel_do_autor: "guerreiro",
    alvo_tipo: "plataforma",
    alvo_id: null,
    texto: "Podíamos ter um mural entre trilhas.",
    situacao: "recebida",
    prazo: "2026-08-29T00:00:00-03:00",
    em_atraso: false,
    avaliado_por_id: null,
    parecer: null,
    motivo_do_retorno: null,
    decidido_em: null,
    ...parcial,
  };
}

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

vi.mock("../direitos/ContextoDeDireitos", async () => {
  const real = await vi.importActual<typeof import("../direitos/ContextoDeDireitos")>(
    "../direitos/ContextoDeDireitos",
  );
  return { ...real, useDireitos: () => ({ irParaDireitos: vi.fn() }) };
});

import { useSessao } from "comum/autenticacao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
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

afterEach(() => {
  vi.restoreAllMocks();
});

describe("área Filas", () => {
  it("abre com o filtro por natureza e a lista de participação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);

    expect(await screen.findByText("Fulano de Tal")).toBeInTheDocument();
    expect(screen.getByLabelText(/natureza/i)).toHaveValue("participacao");
  });

  it("o atraso aparece por rótulo legível, sem depender de cor", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre({ em_atraso: true })],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);

    const rotulo = await screen.findByText("Em atraso");
    expect(rotulo.tagName).toBe("SPAN");
  });

  it("Mestre lê a recusa em linguagem simples, não um erro cru", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    const listarEspiado = vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao");

    render(<TelaDeFilas />);

    expect(await screen.findByText(/esta área é do admin/i)).toBeInTheDocument();
    expect(listarEspiado).not.toHaveBeenCalled();
  });

  it("aceitar com parecer mostra o desfecho registrado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "avaliarSolicitacaoDeParticipacao").mockResolvedValue(
      solicitacaoDeMestre({
        situacao: "aceita",
        parecer: "Perfil compatível.",
        avaliado_por_id: "admin-1",
        decidido_em: "2026-08-22T10:00:00-03:00",
      }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.type(screen.getByLabelText(/^parecer$/i), "Perfil compatível.");
    await usuario.click(screen.getByRole("button", { name: /^aceitar$/i }));

    await waitFor(() =>
      expect(filasApi.avaliarSolicitacaoDeParticipacao).toHaveBeenCalledWith(
        "solicitacao-1",
        { situacao: "aceita", parecer: "Perfil compatível." },
        "token-do-admin",
      ),
    );
    expect(await screen.findByText("Aceita")).toBeInTheDocument();
  });

  it("mostra o aviso de coleta da solicitação de participação, sem bloquear a avaliação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Fulano de Tal"));

    expect(screen.getByText(/solicitação de participação/i)).toHaveAttribute("role", "status");
  });

  it("recusar com parecer vazio aponta o campo sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [solicitacaoDeMestre()],
      proximo_cursor: null,
    });
    const avaliarEspiado = vi.spyOn(filasApi, "avaliarSolicitacaoDeParticipacao");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(screen.getByRole("button", { name: /^recusar$/i }));

    expect(await screen.findByText(/informe o motivo da recusa/i)).toBeInTheDocument();
    expect(avaliarEspiado).not.toHaveBeenCalled();
  });

  it("solicitação já avaliada não oferece desfecho", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeMestre({
          situacao: "recusada",
          parecer: "Sem vaga.",
          avaliado_por_id: "admin-1",
          decidido_em: "2026-08-20T10:00:00-03:00",
        }),
      ],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));

    expect(screen.getByText("Recusada")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^aceitar$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^recusar$/i })).not.toBeInTheDocument();
  });

  it("aceitar não cadastra ninguém, e o formulário de Apoiador abre pré-preenchido", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(personasApi, "cadastrarApoiador");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));

    const formulario = await screen.findByRole("form", { name: /novo apoiador/i });
    expect(within(formulario).getByLabelText(/^nome$/i)).toHaveValue("Fulano de Tal");
    expect(within(formulario).getByLabelText(/^e-mail$/i)).toHaveValue("fulano@example.org");
    expect(within(formulario).getByLabelText(/nick pretendido/i)).toHaveValue(
      "apoiador-pretendido",
    );
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("cadastro pré-preenchido sem artefato comprobatório é apontado e não é criado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(personasApi, "cadastrarApoiador");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /^cadastrar$/i }));

    expect(
      await screen.findByText(/ao menos um artefato comprobatório é obrigatório/i),
    ).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("a homologação mostra o valor em moedas, e nenhum valor em reais", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    vi.spyOn(personasApi, "cadastrarApoiador").mockResolvedValue({
      id: "apoiador-1",
      nome: "Fulano de Tal",
      email: "fulano@example.org",
      whatsapp: "11999990000",
      nick: "apoiador-pretendido",
      artefatos: [{ endereco: "https://exemplo.org", rotulo: "Perfil" }],
    });
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_DE_RECURSO]);
    vi.spyOn(aportesApi, "homologarAporte").mockResolvedValue({
      id: "aporte-1",
      provedor_id: "apoiador-1",
      tipo_de_recurso_id: TIPO_DE_RECURSO.id,
      quantidade: "10",
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      valor_em_moedas: "15.00",
      forma: "material",
      data_do_aporte: "2026-08-22",
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /acrescentar artefato/i }));
    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Perfil");
    await usuario.type(screen.getByLabelText(/^endereço$/i), "https://exemplo.org");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await usuario.selectOptions(
      await screen.findByLabelText(/tipo de recurso/i),
      TIPO_DE_RECURSO.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-22");
    await usuario.click(screen.getByRole("button", { name: /homologar aporte/i }));

    const aviso = await screen.findByText(/aporte homologado: 15\.00 moedas/i);
    expect(aviso).toBeInTheDocument();
    // O valor oficial creditado nunca aparece em reais (`RN-02-19`) — o
    // "R$" que existe na tela é só o texto livre que o próprio pré-cadastro
    // declarou, mostrado como referência ao Admin (`RF-02-83`).
    expect(aviso.textContent).not.toMatch(/r\$/i);
  });

  it("solicitação já homologada não oferece homologar de novo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [
        solicitacaoDeApoiador({ situacao: "aceita", decidido_em: "2026-08-21T10:00:00" }),
      ],
      proximo_cursor: null,
    });
    vi.spyOn(personasApi, "cadastrarApoiador").mockResolvedValue({
      id: "apoiador-1",
      nome: "Fulano de Tal",
      email: "fulano@example.org",
      whatsapp: "11999990000",
      nick: "apoiador-pretendido",
      artefatos: [{ endereco: "https://exemplo.org", rotulo: "Perfil" }],
    });
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_DE_RECURSO]);
    vi.spyOn(aportesApi, "homologarAporte").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Esta solicitação de participação já foi homologada.",
        campo: "solicitacao_de_participacao_id",
      }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Fulano de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /acrescentar artefato/i }));
    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Perfil");
    await usuario.type(screen.getByLabelText(/^endereço$/i), "https://exemplo.org");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await usuario.selectOptions(
      await screen.findByLabelText(/tipo de recurso/i),
      TIPO_DE_RECURSO.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-22");
    await usuario.click(screen.getByRole("button", { name: /homologar aporte/i }));

    expect(
      await screen.findByText(/o aporte desta solicitação já foi homologado/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /homologar aporte/i }),
    ).not.toBeInTheDocument();
  });

  it("o filtro alcança as cinco naturezas", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeParticipacao").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "listarSolicitacoesDeDados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "listarSolicitacoesDeChave").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "listarSugestoes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "listarSolicitacoesDoResponsavel").mockResolvedValue([]);

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    const seletor = await screen.findByLabelText(/natureza/i);

    const opcoes = within(seletor)
      .getAllByRole("option")
      .map((opcao) => opcao.textContent);
    expect(opcoes).toEqual(["Participação", "Dados", "Chave", "Sugestões", "Responsável"]);

    await usuario.selectOptions(seletor, "dados");
    await waitFor(() => expect(filasApi.listarSolicitacoesDeDados).toHaveBeenCalled());

    await usuario.selectOptions(seletor, "chave");
    await waitFor(() => expect(filasApi.listarSolicitacoesDeChave).toHaveBeenCalled());

    await usuario.selectOptions(seletor, "sugestao");
    await waitFor(() => expect(filasApi.listarSugestoes).toHaveBeenCalled());

    await usuario.selectOptions(seletor, "responsavel");
    await waitFor(() => expect(filasApi.listarSolicitacoesDoResponsavel).toHaveBeenCalled());
  });

  it("a natureza responsável mostra protocolo, tipo, situação e prazo na lista", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDoResponsavel").mockResolvedValue([
      solicitacaoDoResponsavel(),
    ]);

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "responsavel");

    expect(await screen.findByText("mae-da-zeferina")).toBeInTheDocument();
    expect(screen.getByText(/acesso.*zeferina/i)).toBeInTheDocument();
    expect(screen.getByText("Recebida")).toBeInTheDocument();
  });

  it("o destaque de atraso da solicitação do responsável não bloqueia o tratamento", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDoResponsavel").mockResolvedValue([
      solicitacaoDoResponsavel({ em_atraso: true }),
    ]);
    vi.spyOn(filasApi, "tratarSolicitacaoDoResponsavel").mockResolvedValue(
      solicitacaoDoResponsavel({
        situacao: "aceita",
        desfecho: "Acesso concedido.",
        tratado_por_id: "admin-1",
        tratado_em: "2026-08-29T10:00:00-03:00",
      }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "responsavel");

    const rotulo = await screen.findByText("Em atraso");
    expect(rotulo.tagName).toBe("SPAN");

    await usuario.click(screen.getByText("mae-da-zeferina"));
    await usuario.type(screen.getByLabelText(/o que foi tratado/i), "Acesso concedido.");
    await usuario.click(screen.getByRole("button", { name: /^aceitar$/i }));

    expect(await screen.findByText("Tratada por")).toBeInTheDocument();
    expect(screen.getByText("admin-1")).toBeInTheDocument();
  });

  it("solicitação do responsável já tratada é apresentada em leitura", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDoResponsavel").mockResolvedValue([
      solicitacaoDoResponsavel({
        situacao: "aceita",
        desfecho: "Acesso concedido por escrito.",
        tratado_por_id: "admin-1",
        tratado_em: "2026-08-25T10:00:00-03:00",
      }),
    ]);

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "responsavel");
    await usuario.click(await screen.findByText("mae-da-zeferina"));

    expect(screen.getByText("Acesso concedido por escrito.")).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^aceitar$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /^recusar$/i })).not.toBeInTheDocument();
  });

  it("a natureza dados mostra solicitante, instituição, finalidade e recorte", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeDados").mockResolvedValue({
      itens: [solicitacaoDeDados()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "dados");

    expect(await screen.findByText("Pesquisadora de Tal")).toBeInTheDocument();
    expect(screen.getByText("Universidade de Teste")).toBeInTheDocument();

    await usuario.click(screen.getByText("Pesquisadora de Tal"));

    expect(screen.getByText("Pesquisa acadêmica sobre evasão escolar.")).toBeInTheDocument();
    expect(screen.getByText("Comunidade de Teste, 2026")).toBeInTheDocument();
    expect(screen.getByText(/solicitação de dados/i)).toHaveAttribute("role", "status");
  });

  it("a natureza chave mostra quem pediu e o que pretende construir", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeChave").mockResolvedValue({
      itens: [solicitacaoDeChave()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "chave");

    expect(await screen.findByText("Desenvolvedora de Tal")).toBeInTheDocument();
    expect(screen.getByText("Um painel comunitário.")).toBeInTheDocument();
  });

  it("a natureza sugestão mostra o autor, a persona dele e o teor", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSugestoes").mockResolvedValue({
      itens: [sugestao()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "sugestao");

    expect(await screen.findByText("Guerreiro(a)")).toBeInTheDocument();
    expect(screen.getByText("Podíamos ter um mural entre trilhas.")).toBeInTheDocument();
  });

  it("os três critérios de aprovação de dados aparecem antes da decisão", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeDados").mockResolvedValue({
      itens: [solicitacaoDeDados()],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "dados");
    await usuario.click(await screen.findByText("Pesquisadora de Tal"));

    expect(screen.getByText("Solicitante identificado")).toBeInTheDocument();
    expect(
      screen.getByText("Finalidade declarada compatível com pesquisa ou política pública"),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Compromisso de não tentar reidentificar ninguém"),
    ).toBeInTheDocument();
  });

  it("aprovar dados sem o compromisso é apontado no campo sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeDados").mockResolvedValue({
      itens: [solicitacaoDeDados()],
      proximo_cursor: null,
    });
    const avaliarEspiado = vi.spyOn(filasApi, "avaliarSolicitacaoDeDados");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "dados");
    await usuario.click(await screen.findByText("Pesquisadora de Tal"));
    await usuario.type(screen.getByLabelText(/^parecer$/i), "Finalidade compatível.");
    await usuario.click(screen.getByRole("button", { name: /^aceitar$/i }));

    expect(
      await screen.findByText(/afirme o compromisso de não tentar reidentificar ninguém/i),
    ).toBeInTheDocument();
    expect(avaliarEspiado).not.toHaveBeenCalled();
  });

  it("a entrega registrada é apresentada como gratuita e anonimizada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeDados").mockResolvedValue({
      itens: [solicitacaoDeDados()],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "avaliarSolicitacaoDeDados").mockResolvedValue(
      solicitacaoDeDados({
        situacao: "aceita",
        parecer: "Finalidade compatível.",
        decidido_em: "2026-08-22T10:00:00-03:00",
        entregue: "CSV anonimizado enviado a pesquisadora@example.org",
      }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "dados");
    await usuario.click(await screen.findByText("Pesquisadora de Tal"));
    await usuario.type(screen.getByLabelText(/^parecer$/i), "Finalidade compatível.");
    await usuario.click(screen.getByLabelText(/compromisso de não tentar reidentificar/i));
    await usuario.type(
      screen.getByLabelText(/o que foi entregue/i),
      "CSV anonimizado enviado a pesquisadora@example.org",
    );
    await usuario.click(screen.getByRole("button", { name: /^aceitar$/i }));

    expect(await screen.findByText(/gratuita e anonimizada/i)).toBeInTheDocument();
  });

  it("aprovar chave não emite e passa a oferecer a emissão", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeChave").mockResolvedValue({
      itens: [solicitacaoDeChave()],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "avaliarSolicitacaoDeChave").mockResolvedValue(
      solicitacaoDeChave({
        situacao: "aceita",
        parecer: "Projeto compatível.",
        decidido_em: "2026-08-22T10:00:00-03:00",
      }),
    );
    const emitirEspiado = vi.spyOn(chavesApi, "emitirChave");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "chave");
    await usuario.click(await screen.findByText("Desenvolvedora de Tal"));
    await usuario.click(screen.getByRole("button", { name: /^aceitar$/i }));

    expect(await screen.findByRole("button", { name: /^emitir chave$/i })).toBeInTheDocument();
    expect(emitirEspiado).not.toHaveBeenCalled();
  });

  it("o segredo aparece uma vez com o aviso, e some ao voltar à mesma solicitação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const aprovada = solicitacaoDeChave({
      situacao: "aceita",
      parecer: "Projeto compatível.",
      decidido_em: "2026-08-22T10:00:00-03:00",
    });
    vi.spyOn(filasApi, "listarSolicitacoesDeChave").mockResolvedValue({
      itens: [aprovada],
      proximo_cursor: null,
    });
    vi.spyOn(chavesApi, "emitirChave").mockResolvedValue({
      id: "chave-emitida-1",
      segredo: "producao.chave-emitida-1.segredo-em-claro",
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "chave");
    await usuario.click(await screen.findByText("Desenvolvedora de Tal"));
    await usuario.click(await screen.findByRole("button", { name: /^emitir chave$/i }));

    expect(await screen.findByText(/segredo-em-claro/)).toBeInTheDocument();
    expect(screen.getByText(/não será mostrado de novo/i)).toBeInTheDocument();

    await usuario.click(screen.getByText(/voltar para a fila/i));
    await usuario.click(await screen.findByText("Desenvolvedora de Tal"));

    expect(screen.queryByText(/segredo-em-claro/)).not.toBeInTheDocument();
  });

  it("solicitação de chave que já rendeu chave não oferece emitir de novo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSolicitacoesDeChave").mockResolvedValue({
      itens: [
        solicitacaoDeChave({
          situacao: "aceita",
          decidido_em: "2026-08-21T10:00:00-03:00",
          chave_emitida: true,
        }),
      ],
      proximo_cursor: null,
    });

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "chave");
    await usuario.click(await screen.findByText("Desenvolvedora de Tal"));

    expect(screen.queryByRole("button", { name: /^emitir chave$/i })).not.toBeInTheDocument();
    expect(screen.getByText(/chave já emitida/i)).toBeInTheDocument();
  });

  it("a não adotada sem motivo é apontada no campo sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSugestoes").mockResolvedValue({
      itens: [sugestao()],
      proximo_cursor: null,
    });
    const avaliarEspiado = vi.spyOn(filasApi, "avaliarSugestao");

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "sugestao");
    await usuario.click(await screen.findByText("Guerreiro(a)"));
    await usuario.click(screen.getByRole("button", { name: /^não adotar$/i }));

    expect(await screen.findByText(/informe o motivo do retorno/i)).toBeInTheDocument();
    expect(avaliarEspiado).not.toHaveBeenCalled();
  });

  it("a sugestão adotada mostra o que foi creditado, sem caminho de e-mail", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(filasApi, "listarSugestoes").mockResolvedValue({
      itens: [sugestao()],
      proximo_cursor: null,
    });
    vi.spyOn(filasApi, "avaliarSugestao").mockResolvedValue(
      sugestao({ situacao: "adotada", decidido_em: "2026-08-22T10:00:00-03:00" }),
    );

    render(<TelaDeFilas />);
    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/natureza/i), "sugestao");
    await usuario.click(await screen.findByText("Guerreiro(a)"));
    await usuario.click(screen.getByRole("button", { name: /^adotar$/i }));

    expect(
      await screen.findByText(/20 pontos extras e o badge de protagonismo/i),
    ).toBeInTheDocument();
    expect(screen.queryByText(/e-mail/i)).not.toBeInTheDocument();
  });
});
