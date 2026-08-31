import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { EvolucaoDoGuerreiro } from "../evolucao/api";
import * as evolucaoApi from "../evolucao/api";
import type { GuerreiroVinculado } from "../vinculados/api";
import * as vinculadosApi from "../vinculados/api";
import type { Autorizacao } from "./api";
import * as autorizacaoApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const GUERREIRO_1: GuerreiroVinculado = {
  id: "guerreiro-1",
  nick: "zeferina",
  avatar: "avatar-1",
  grau_de_parentesco: "mãe",
};

const GUERREIRO_2: GuerreiroVinculado = {
  id: "guerreiro-2",
  nick: "joaozinho",
  avatar: "avatar-2",
  grau_de_parentesco: "avó",
};

const EVOLUCAO_VAZIA: EvolucaoDoGuerreiro = {
  presencas: [],
  atividades: [],
  trilhas: [],
  pontos_por_poder: [],
  criacoes_validadas: [],
};

const NAO_AUTORIZADA: Autorizacao = {
  estado: "nao_autorizada",
  suspensa_por: null,
  historico: [],
};

const PERSONA_ID = "responsavel-1";

async function entrarComoResponsavel() {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-responsavel",
    expira_em: new Date().toISOString(),
    papel: "responsavel",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: PERSONA_ID,
    papel: "responsavel",
    permissoes: {},
  });

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "mae-da-zeferina");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  return testeDeUsuario;
}

async function abrirAbaDeAutorizacao(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^autorização$/i }));
}

describe("tela de autorização", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([GUERREIRO_1]);
    vi.spyOn(evolucaoApi, "obterEvolucao").mockResolvedValue(EVOLUCAO_VAZIA);
    vi.spyOn(evolucaoApi, "listarOcorrencias").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a declaração aparece antes de qualquer botão de decisão, sem decisão por finalidade", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue(NAO_AUTORIZADA);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);

    const declaracao = await screen.findByText(/o que a autorização libera/i);
    const conceder = screen.getByRole("button", { name: /^conceder$/i });
    expect(
      declaracao.compareDocumentPosition(conceder) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
    expect(screen.getAllByRole("button", { name: /^conceder$/i })).toHaveLength(1);
  });

  it("conceder diz o efeito no mesmo ato", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue(NAO_AUTORIZADA);
    vi.spyOn(autorizacaoApi, "decidirAutorizacao").mockResolvedValue({
      id: "consentimento-1",
      decisao: "concede",
      registrado_em: new Date().toISOString(),
      estado: "vigente",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);
    await testeDeUsuario.click(await screen.findByRole("button", { name: /^conceder$/i }));

    expect(
      await screen.findByText(/passa a aparecer na vitrine e nos rankings públicos/i),
    ).toBeInTheDocument();
  });

  it("revogar diz o efeito no mesmo ato, sem sugerir apagamento", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue({
      estado: "vigente",
      suspensa_por: null,
      historico: [
        {
          id: "c1",
          responsavel_id: PERSONA_ID,
          decisao: "concede",
          versao_do_termo: "2026-08",
          origem: "propria",
          registrado_em: "2026-08-01T10:00:00Z",
        },
      ],
    });
    vi.spyOn(autorizacaoApi, "decidirAutorizacao").mockResolvedValue({
      id: "consentimento-2",
      decisao: "nega",
      registrado_em: new Date().toISOString(),
      estado: "nao_autorizada",
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);
    await testeDeUsuario.click(await screen.findByRole("button", { name: /^revogar$/i }));

    const aviso = await screen.findByText(/saem do que é público agora/i);
    expect(aviso.textContent).toMatch(/nada foi apagado/i);
    expect(aviso.textContent).not.toMatch(/apagad[oa]s? (?!.*nada)/i);
  });

  it("falha de rede não dá a decisão por tomada", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue(NAO_AUTORIZADA);
    vi.spyOn(autorizacaoApi, "decidirAutorizacao").mockRejectedValue(
      new TypeError("Failed to fetch"),
    );

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);
    await testeDeUsuario.click(await screen.findByRole("button", { name: /^conceder$/i }));

    expect(await screen.findByText(/não foi registrada/i)).toBeInTheDocument();
    expect(screen.getByText(/ainda não autorizada/i)).toBeInTheDocument();
  });

  it("a alternativa equivalente aparece quando não autorizada", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue(NAO_AUTORIZADA);

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);

    expect(
      await screen.findByText(/entrega a produção ao Mestre no encontro/i),
    ).toBeInTheDocument();
  });

  it("a alternativa equivalente também aparece quando suspensa", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue({
      estado: "suspensa",
      suspensa_por: {
        responsavel_id: "outro-responsavel",
        decidido_em: "2026-08-01T10:00:00Z",
      },
      historico: [],
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);

    expect(
      await screen.findByText(/entrega a produção ao Mestre no encontro/i),
    ).toBeInTheDocument();
  });

  it("suspensa nomeia quem motivou, com data e hora", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue({
      estado: "suspensa",
      suspensa_por: {
        responsavel_id: "outro-responsavel",
        decidido_em: "2026-08-01T10:00:00Z",
      },
      historico: [],
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);

    expect(await screen.findByText(/motivada por outro responsável/i)).toBeInTheDocument();
    expect(screen.getByText(/a gestão vai tratar o caso com a família/i)).toBeInTheDocument();
  });

  it("a concessão colidente vira orientação, sem código de erro", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue(NAO_AUTORIZADA);
    vi.spyOn(autorizacaoApi, "decidirAutorizacao").mockRejectedValue(
      new ErroDaApi(409, {
        codigo: "autorizacao_suspensa_por_outro_responsavel",
        mensagem:
          "A autorização deste Guerreiro(a) está suspensa: outro responsável recusou, e a " +
          "recusa prevalece. Procure a gestão no encontro.",
      }),
    );

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);
    await testeDeUsuario.click(await screen.findByRole("button", { name: /^conceder$/i }));

    expect(await screen.findByText(/procure a gestão no encontro/i)).toBeInTheDocument();
    expect(
      screen.queryByText(/autorizacao_suspensa_por_outro_responsavel/i),
    ).not.toBeInTheDocument();
    expect(screen.queryByText(/^409$/)).not.toBeInTheDocument();
  });

  it("o histórico aparece ordenado e sem caminho de editar ou apagar", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue({
      estado: "vigente",
      suspensa_por: null,
      historico: [
        {
          id: "c3",
          responsavel_id: PERSONA_ID,
          decisao: "concede",
          versao_do_termo: "2026-09",
          origem: "propria",
          registrado_em: "2026-09-01T10:00:00Z",
        },
        {
          id: "c2",
          responsavel_id: PERSONA_ID,
          decisao: "nega",
          versao_do_termo: "2026-08",
          origem: "propria",
          registrado_em: "2026-08-15T10:00:00Z",
        },
        {
          id: "c1",
          responsavel_id: PERSONA_ID,
          decisao: "concede",
          versao_do_termo: "2026-08",
          origem: "propria",
          registrado_em: "2026-08-01T10:00:00Z",
        },
      ],
    });

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);
    const lista = await screen.findByRole("list", { name: /histórico da autorização/i });

    const itens = within(lista).getAllByRole("listitem");
    expect(itens).toHaveLength(3);
    expect(itens[0].textContent).toMatch(/concedida/i);
    expect(itens[0].textContent).toMatch(/2026-09|09\/2026|9\/2026/);
    expect(itens[1].textContent).toMatch(/revogada/i);
    expect(itens[2].textContent).toMatch(/concedida/i);
    expect(screen.queryByRole("button", { name: /editar/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /apagar/i })).not.toBeInTheDocument();
  });

  it("vai da evolução à autorização e volta, sem sair da aplicação", async () => {
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockResolvedValue(NAO_AUTORIZADA);

    const testeDeUsuario = await entrarComoResponsavel();
    await screen.findByRole("heading", { name: /seus vinculados/i });

    await abrirAbaDeAutorizacao(testeDeUsuario);
    await screen.findByText(/o que a autorização libera/i);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^evolução$/i }));

    await waitFor(() => {
      expect(screen.queryByText(/o que a autorização libera/i)).not.toBeInTheDocument();
    });
    expect(screen.getByRole("heading", { name: /seus vinculados/i })).toBeInTheDocument();
  });

  it("trocar de vinculado troca a autorização apresentada", async () => {
    vi.spyOn(vinculadosApi, "listarMeusGuerreiros").mockResolvedValue([
      GUERREIRO_1,
      GUERREIRO_2,
    ]);
    vi.spyOn(autorizacaoApi, "lerAutorizacao").mockImplementation((guerreiroId) =>
      Promise.resolve(
        guerreiroId === GUERREIRO_1.id
          ? { estado: "vigente", suspensa_por: null, historico: [] }
          : { estado: "nao_autorizada", suspensa_por: null, historico: [] },
      ),
    );

    const testeDeUsuario = await entrarComoResponsavel();
    await abrirAbaDeAutorizacao(testeDeUsuario);

    await screen.findByText(/vigente: o perfil aparece/i);

    await testeDeUsuario.click(screen.getByRole("button", { name: /joaozinho · avó/i }));

    expect(await screen.findByText(/ainda não autorizada/i)).toBeInTheDocument();
  });
});
