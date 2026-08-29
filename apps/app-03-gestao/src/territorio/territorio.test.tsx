import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as comunidadesApi from "../comunidades/api";
import * as personasApi from "../personas/api";
import type { DesafioPublicadoDaLista, LocalDaLista, SolicitacaoDeLocalDaLista } from "./api";
import * as territorioApi from "./api";
import { TelaDeTerritorio } from "./TelaDeTerritorio";

const COMUNIDADE = {
  id: "comunidade-1",
  nome: "Comunidade de Teste",
  localizacao: "Bairro de teste",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const OUTRA_COMUNIDADE = {
  ...COMUNIDADE,
  id: "comunidade-2",
  nome: "Outra Comunidade",
};

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

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
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

const BAIRRO: LocalDaLista = {
  id: "local-bairro",
  comunidade_virtual_id: COMUNIDADE.id,
  nivel: "bairro",
  rotulo: "Bairro Central",
  local_pai_id: null,
};

const RUA: LocalDaLista = {
  id: "local-rua",
  comunidade_virtual_id: COMUNIDADE.id,
  nivel: "rua",
  rotulo: "Rua das Flores",
  local_pai_id: BAIRRO.id,
};

const SOLICITACAO: SolicitacaoDeLocalDaLista = {
  id: "solicitacao-1",
  solicitante_id: "guerreiro-1",
  comunidade_virtual_id: COMUNIDADE.id,
  desafio_de_coleta_id: "desafio-1",
  nivel_pretendido: "quadra",
  rotulo: "Quadra Nova",
  justificativa: "Não existe local para a minha rua ainda.",
  situacao: "recebida",
  avaliador_id: null,
  motivo_da_recusa: null,
  local_criado_id: null,
  avaliado_em: null,
  registrado_em: "2026-08-20T10:00:00-03:00",
};

const DESAFIO: DesafioPublicadoDaLista = {
  id: "desafio-1",
  missao_id: "missao-1",
  trilha_id: "trilha-1",
  tipo_de_coleta: { nome: "Temperatura", forma_de_registro: "numero", unidade: "°C" },
  cadencia: "semanal",
  vigencia_inicio: "2026-01-01T00:00:00-03:00",
  vigencia_fim: "2026-12-31T00:00:00-03:00",
  granularidade_exigida: "rua",
  quantidade_de_series_ativas: 3,
};

function configurarComunidadesEGuerreiros() {
  vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
    itens: [COMUNIDADE, OUTRA_COMUNIDADE],
    proximo_cursor: null,
    ciclo_rotulo: "2026",
  });
  vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
    itens: [
      {
        id: "guerreiro-1",
        nome: "Zeferina",
        nascimento: "2015-03-20",
        nick: "ZeferinaGuerreira",
        avatar: "avatar-opaco",
        comunidade_virtual_id: COMUNIDADE.id,
        vinculo_iniciado_em: "2026-08-01T10:00:00-03:00",
      },
    ],
    proximo_cursor: null,
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("hierarquia de locais", () => {
  it("apresenta os locais da comunidade escolhida, cada um sob o pai", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([BAIRRO, RUA]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);

    const bairro = await screen.findByText("Bairro Central");
    const item = bairro.closest("li");
    expect(item ? within(item).getByText("Rua das Flores") : null).toBeInTheDocument();
  });

  it("trocar a comunidade troca a hierarquia apresentada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    const listarLocaisEspiado = vi
      .spyOn(territorioApi, "listarTodosOsLocais")
      .mockResolvedValueOnce([BAIRRO])
      .mockResolvedValueOnce([]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await screen.findByText("Bairro Central");
    await usuario.selectOptions(screen.getByLabelText(/^comunidade$/i), OUTRA_COMUNIDADE.id);

    await waitFor(() => expect(listarLocaisEspiado).toHaveBeenCalledWith(OUTRA_COMUNIDADE.id));
    expect(screen.queryByText("Bairro Central")).not.toBeInTheDocument();
  });

  it("comunidade sem local não é apresentada como falha", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);

    const semLocais = await screen.findByText(/ainda não tem locais cadastrados/i);
    expect(semLocais).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("cadastro de local", () => {
  it("Admin cadastra local com pai escolhido entre os já cadastrados", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais")
      .mockResolvedValueOnce([BAIRRO])
      .mockResolvedValueOnce([BAIRRO, RUA]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "cadastrarLocal").mockResolvedValue(RUA);

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await screen.findByText("Bairro Central");
    await usuario.click(screen.getByRole("button", { name: /novo local/i }));
    await usuario.selectOptions(screen.getByLabelText(/^nível$/i), "rua");
    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Rua das Flores");
    await usuario.selectOptions(screen.getByLabelText(/local pai/i), BAIRRO.id);
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() =>
      expect(territorioApi.cadastrarLocal).toHaveBeenCalledWith(
        {
          comunidade_id: COMUNIDADE.id,
          nivel: "rua",
          rotulo: "Rua das Flores",
          local_pai_id: BAIRRO.id,
        },
        "token-do-admin",
      ),
    );
  });

  it("o nível comunidade é o único oferecido sem pai", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi
      .spyOn(territorioApi, "cadastrarLocal")
      .mockResolvedValue(BAIRRO);

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /novo local/i }));
    await usuario.selectOptions(screen.getByLabelText(/^nível$/i), "comunidade");
    expect(screen.queryByLabelText(/^local pai$/i)).not.toBeInTheDocument();

    await usuario.type(screen.getByLabelText(/^rótulo$/i), "A Comunidade");
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() =>
      expect(cadastrarEspiado).toHaveBeenCalledWith(
        {
          comunidade_id: COMUNIDADE.id,
          nivel: "comunidade",
          rotulo: "A Comunidade",
          local_pai_id: undefined,
        },
        "token-do-admin",
      ),
    );
  });

  it("a recusa da hierarquia é apresentada no campo, e nenhum local é criado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([BAIRRO]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "cadastrarLocal").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O nível imediatamente acima de 'quadra' é 'bloco'.",
        campo: "local_pai_id",
      }),
    );

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /novo local/i }));
    await usuario.selectOptions(screen.getByLabelText(/^nível$/i), "quadra");
    await usuario.type(screen.getByLabelText(/^rótulo$/i), "Quadra 1");
    await usuario.selectOptions(screen.getByLabelText(/local pai/i), BAIRRO.id);
    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(await screen.findByText(/nível imediatamente acima/i)).toBeInTheDocument();
  });

  it("quem não é Admin não vê o caminho de cadastro", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);

    await screen.findByText(/ainda não tem locais cadastrados/i);
    expect(screen.queryByRole("button", { name: /novo local/i })).not.toBeInTheDocument();
  });
});

describe("fila de solicitações de novo local", () => {
  it("alerta enquanto houver solicitação sem desfecho", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([BAIRRO]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [SOLICITACAO],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [DESAFIO],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);

    expect(await screen.findByRole("alert")).toHaveTextContent(/aguardando avaliação/i);
    expect(screen.getByText("ZeferinaGuerreira")).toBeInTheDocument();
    expect(screen.getByText("Quadra Nova")).toBeInTheDocument();
    expect(screen.getByText(/não existe local para a minha rua/i)).toBeInTheDocument();
  });

  it("sem solicitação em aberto, nenhum alerta aparece", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);

    await screen.findByText(/nenhuma solicitação de novo local em aberto/i);
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("a aprovação cria o local e ele aparece na hierarquia sem recarregar a tela", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais")
      .mockResolvedValueOnce([BAIRRO])
      .mockResolvedValueOnce([BAIRRO, RUA]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas")
      .mockResolvedValueOnce({ itens: [SOLICITACAO], proximo_cursor: null })
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [DESAFIO],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "avaliarSolicitacaoDeLocal").mockResolvedValue({
      ...SOLICITACAO,
      situacao: "aprovada",
      local_criado_id: RUA.id,
    });

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /avaliar/i }));
    await usuario.selectOptions(
      screen.getByLabelText(/local pai \(para aprovar\)/i),
      BAIRRO.id,
    );
    await usuario.click(screen.getByRole("button", { name: /^aprovar$/i }));

    await waitFor(() =>
      expect(territorioApi.avaliarSolicitacaoDeLocal).toHaveBeenCalledWith(
        SOLICITACAO.id,
        { situacao: "aprovada", local_pai_id: BAIRRO.id },
        "token-do-admin",
      ),
    );
    expect(await screen.findByText("Rua das Flores")).toBeInTheDocument();
    expect(
      await screen.findByText(/nenhuma solicitação de novo local em aberto/i),
    ).toBeInTheDocument();
  });

  it("a recusa sem motivo não é confirmada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([BAIRRO]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [SOLICITACAO],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const avaliarEspiado = vi.spyOn(territorioApi, "avaliarSolicitacaoDeLocal");

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /avaliar/i }));
    await usuario.click(screen.getByRole("button", { name: /^recusar$/i }));

    expect(await screen.findByText(/informe o motivo da recusa/i)).toBeInTheDocument();
    expect(avaliarEspiado).not.toHaveBeenCalled();
  });
});

describe("desafios de coleta publicados", () => {
  it("apresenta os desafios em leitura, sem caminho de escrita", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarComunidadesEGuerreiros();
    vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([]);
    vi.spyOn(territorioApi, "listarSolicitacoesDeLocalAbertas").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(territorioApi, "listarDesafiosDeColetaPublicados").mockResolvedValue({
      itens: [DESAFIO],
      proximo_cursor: null,
    });

    render(<TelaDeTerritorio />);

    await screen.findByText("Temperatura");
    expect(screen.getByText(/3 série\(s\) ativa\(s\)/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /criar desafio|editar desafio|apagar desafio/i }),
    ).not.toBeInTheDocument();
  });
});
