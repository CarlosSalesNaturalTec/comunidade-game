import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as comunidadesApi from "../comunidades/api";
import * as personasApi from "../personas/api";
import * as pontosDeApoioApi from "../pontos-de-apoio/api";
import * as recursosApi from "../recursos/api";
import type { EntregaDeRecompensa, ItemPatrimonialDaLista } from "./api";
import * as acervoApi from "./api";
import { TelaDoAcervo } from "./TelaDoAcervo";

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
  nome: "Comunidade Um",
  localizacao: "Bairro Um",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const PONTO_DE_APOIO = {
  id: "ponto-1",
  nome: "Sede",
  comunidade_virtual_id: COMUNIDADE.id,
  responsavel_id: "mestre-1",
  ativo: true,
};

const MESTRE = {
  id: "mestre-1",
  nome: "Mestre Um",
  email: "m@x.com",
  whatsapp: null,
  nick: null,
  artefatos: [],
};

const APOIADOR = {
  id: "apoiador-1",
  nome: "Apoiador Um",
  email: "a@x.com",
  whatsapp: null,
  nick: null,
  artefatos: [],
};

const GUERREIRA = {
  id: "guerreiro-1",
  nome: "Zeferina de Tal",
  nascimento: "2015-01-01",
  nick: "zeferina",
  avatar: "avatar-1",
  comunidade_virtual_id: COMUNIDADE.id,
  vinculo_iniciado_em: "2026-01-01T00:00:00-03:00",
};

const TIPO_ALPHA = {
  id: "tipo-alpha",
  nome: "Exemplar Linha Alpha",
  natureza: "duravel",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "0.00",
  vigencia_inicio: "2026-01-01",
};

const TIPO_CAMISA = {
  id: "tipo-camisa",
  nome: "Camisa",
  natureza: "duravel",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "0.00",
  vigencia_inicio: "2026-01-01",
};

const ENTREGA_DO_ALPHA: EntregaDeRecompensa = {
  id: "entrega-1",
  recompensa_de_marco_id: "recompensa-1",
  missao_id: "missao-1",
  trilha_id: "trilha-1",
  tipo_de_recurso_id: TIPO_ALPHA.id,
  quantidade: "1.00",
  guerreiro_id: GUERREIRA.id,
  ponto_de_apoio_id: PONTO_DE_APOIO.id,
  lancamento_id: "lancamento-1",
  autor_id: MESTRE.id,
  registrado_em: "2026-08-10T10:00:00-03:00",
};

const ENTREGA_DA_CAMISA: EntregaDeRecompensa = {
  ...ENTREGA_DO_ALPHA,
  id: "entrega-2",
  tipo_de_recurso_id: TIPO_CAMISA.id,
};

const ITEM_SEM_ANOTACAO: ItemPatrimonialDaLista = {
  id: "item-1",
  aporte_de_origem_id: null,
  titulo: "Violão",
  numero_de_tombo: "001",
  ponto_de_apoio_id: PONTO_DE_APOIO.id,
  estado_de_conservacao: "Bom",
  responsavel_id: "mestre-1",
  ficha_de_vida: [],
  autor_id: "admin-1",
  registrado_em: "2026-08-01T10:00:00-03:00",
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
  });
}

function configurarListas(
  itens: ItemPatrimonialDaLista[],
  entregas: EntregaDeRecompensa[] = [],
) {
  vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
    itens: [COMUNIDADE],
    proximo_cursor: null,
    ciclo_rotulo: "2026",
  });
  vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
    itens: [PONTO_DE_APOIO],
    proximo_cursor: null,
  });
  vi.spyOn(personasApi, "listarMestres").mockResolvedValue({
    itens: [MESTRE],
    proximo_cursor: null,
  });
  vi.spyOn(personasApi, "listarApoiadores").mockResolvedValue({
    itens: [APOIADOR],
    proximo_cursor: null,
  });
  vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
    itens: [GUERREIRA],
    proximo_cursor: null,
  });
  vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_ALPHA, TIPO_CAMISA]);
  vi.spyOn(acervoApi, "listarAcervo").mockResolvedValue(itens);
  vi.spyOn(acervoApi, "listarEntregas").mockResolvedValue(entregas);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("acervo", () => {
  it("apresenta os exemplares com título, tombo, ponto de apoio, estado e o nome do responsável", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([ITEM_SEM_ANOTACAO]);

    render(<TelaDoAcervo />);

    expect(await screen.findByText("Violão")).toBeInTheDocument();
    expect(screen.getByText("Tombo 001")).toBeInTheDocument();
    expect(screen.getByText("Sede")).toBeInTheDocument();
    expect(screen.getByText("Bom")).toBeInTheDocument();
    expect(screen.getByText("Mestre Um")).toBeInTheDocument();
  });

  it("exemplar de ponto de apoio sem responsável aparece assim mesmo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([{ ...ITEM_SEM_ANOTACAO, responsavel_id: null }]);

    render(<TelaDoAcervo />);

    const semResponsavel = await screen.findByText(/sem responsável designado/i);
    expect(semResponsavel).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("comunidade sem acervo tem texto próprio", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([]);

    render(<TelaDoAcervo />);

    expect(
      await screen.findByText(/nenhum exemplar tombado nesta comunidade/i),
    ).toBeInTheDocument();
  });

  it("Admin tomba um exemplar", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([]);
    vi.spyOn(acervoApi, "tombarItem").mockResolvedValue({
      ...ITEM_SEM_ANOTACAO,
      id: "item-novo",
    });

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /tombar exemplar/i }));
    await usuario.type(screen.getByLabelText(/^título$/i), "Violão");
    await usuario.type(screen.getByLabelText(/número de tombo/i), "001");
    await usuario.selectOptions(screen.getByLabelText(/ponto de apoio/i), PONTO_DE_APOIO.id);
    await usuario.type(screen.getByLabelText(/estado de conservação/i), "Bom");
    await usuario.click(screen.getByRole("button", { name: /^tombar$/i }));

    await waitFor(() =>
      expect(acervoApi.tombarItem).toHaveBeenCalledWith(
        {
          titulo: "Violão",
          numero_de_tombo: "001",
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          estado_de_conservacao: "Bom",
        },
        "token-do-admin",
      ),
    );
  });

  it("campo em falta é apontado antes de enviar", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([]);
    const tombarEspiado = vi.spyOn(acervoApi, "tombarItem");

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /tombar exemplar/i }));
    await usuario.click(screen.getByRole("button", { name: /^tombar$/i }));

    expect(await screen.findByText(/informe o título/i)).toBeInTheDocument();
    expect(tombarEspiado).not.toHaveBeenCalled();
  });

  it("tombo repetido é explicado sem apagar o que foi digitado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([]);
    vi.spyOn(acervoApi, "tombarItem").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Já existe um exemplar com este número de tombo neste ponto de apoio.",
        campo: "numero_de_tombo",
      }),
    );

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /tombar exemplar/i }));
    await usuario.type(screen.getByLabelText(/^título$/i), "Violão");
    await usuario.type(screen.getByLabelText(/número de tombo/i), "001");
    await usuario.selectOptions(screen.getByLabelText(/ponto de apoio/i), PONTO_DE_APOIO.id);
    await usuario.type(screen.getByLabelText(/estado de conservação/i), "Bom");
    await usuario.click(screen.getByRole("button", { name: /^tombar$/i }));

    expect(await screen.findByText(/já existe um exemplar/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/^título$/i)).toHaveValue("Violão");
    expect(screen.getByLabelText(/número de tombo/i)).toHaveValue("001");
  });

  it("Mestre não recebe o caminho do tombamento", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    configurarListas([ITEM_SEM_ANOTACAO]);

    render(<TelaDoAcervo />);

    await screen.findByText("Violão");
    expect(screen.queryByRole("button", { name: /tombar exemplar/i })).not.toBeInTheDocument();
  });

  it("nenhuma ação de retirada, empréstimo, devolução ou transferência é oferecida", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([ITEM_SEM_ANOTACAO]);

    render(<TelaDoAcervo />);

    await screen.findByText("Violão");
    expect(
      screen.queryByRole("button", {
        name: /retirar|empréstimo|emprestar|devolver|devolução|transferir/i,
      }),
    ).not.toBeInTheDocument();
    expect(screen.queryByText(/R\$/)).not.toBeInTheDocument();
  });
});

describe("entregas confirmadas", () => {
  it("mostra o exemplar Alpha com Guerreiro(a), Mestre, ponto de apoio, data e baixa definitiva", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([], [ENTREGA_DO_ALPHA]);

    render(<TelaDoAcervo />);

    expect(await screen.findByText("zeferina")).toBeInTheDocument();
    expect(screen.getByText("Exemplar Linha Alpha")).toBeInTheDocument();
    expect(screen.getByText(/entregue por mestre um/i)).toBeInTheDocument();
    expect(screen.getByText("Sede")).toBeInTheDocument();
    expect(screen.getByText(/baixa definitiva/i)).toBeInTheDocument();
  });

  it("mostra a entrega da camisa ao Guerreiro(a) inscrito com a mesma baixa", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([], [ENTREGA_DO_ALPHA, ENTREGA_DA_CAMISA]);

    render(<TelaDoAcervo />);

    expect(await screen.findByText("Exemplar Linha Alpha")).toBeInTheDocument();
    expect(screen.getByText("Camisa")).toBeInTheDocument();
    expect(screen.getAllByText(/baixa definitiva/i)).toHaveLength(2);
  });

  it("a lista de entregas não mostra nenhum valor nem caminho de escrita", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([], [ENTREGA_DO_ALPHA]);

    render(<TelaDoAcervo />);

    await screen.findByText("Exemplar Linha Alpha");
    expect(screen.queryByText(/R\$/)).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /confirmar|corrigir|desfazer/i }),
    ).not.toBeInTheDocument();
  });

  it("comunidade sem entregas tem texto próprio", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([], []);

    render(<TelaDoAcervo />);

    expect(
      await screen.findByText(/nenhuma entrega confirmada nesta comunidade/i),
    ).toBeInTheDocument();
  });
});

describe("ficha de vida", () => {
  const ANOTACAO_DE_CUIDADO = {
    id: "anotacao-1",
    teor: "cuidado" as const,
    estado_de_conservacao: "Bom, limpo",
    autor_id: "mestre-1",
    registrado_em: "2026-08-05T09:00:00-03:00",
  };
  const ANOTACAO_MAIS_RECENTE = {
    id: "anotacao-2",
    teor: "dano" as const,
    estado_de_conservacao: "Corda partida",
    autor_id: "admin-1",
    registrado_em: "2026-08-10T09:00:00-03:00",
  };

  it("as anotações vêm em ordem do tempo, com teor, estado, autor e data", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([
      { ...ITEM_SEM_ANOTACAO, ficha_de_vida: [ANOTACAO_DE_CUIDADO, ANOTACAO_MAIS_RECENTE] },
    ]);

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /ver ficha de vida/i }));

    const itens = screen.getAllByRole("listitem");
    const anotacoes = itens.filter((item) => item.className.includes("ficha-de-vida__item"));
    expect(anotacoes).toHaveLength(2);
    expect(anotacoes[0]).toHaveTextContent("Cuidado");
    expect(anotacoes[0]).toHaveTextContent("Mestre Um");
    expect(anotacoes[1]).toHaveTextContent("Dano");
  });

  it("exemplar sem anotação tem texto próprio", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([ITEM_SEM_ANOTACAO]);

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /ver ficha de vida/i }));

    expect(await screen.findByText(/ainda não há anotação/i)).toBeInTheDocument();
  });

  it("nenhuma anotação oferece caminho de edição ou de remoção", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([{ ...ITEM_SEM_ANOTACAO, ficha_de_vida: [ANOTACAO_DE_CUIDADO] }]);

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /ver ficha de vida/i }));
    await screen.findByText("Cuidado");

    expect(
      screen.queryByRole("button", { name: /editar|excluir|remover/i }),
    ).not.toBeInTheDocument();
  });

  it("Mestre anota o cuidado do exemplar", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    configurarListas([ITEM_SEM_ANOTACAO]);
    vi.spyOn(acervoApi, "anotarFichaDeVida").mockResolvedValue({
      ...ITEM_SEM_ANOTACAO,
      ficha_de_vida: [ANOTACAO_DE_CUIDADO],
    });

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /ver ficha de vida/i }));
    await usuario.click(screen.getByRole("button", { name: /^anotar$/i }));
    await usuario.type(screen.getByLabelText(/estado de conservação apurado/i), "Bom, limpo");
    await usuario.click(screen.getByRole("button", { name: /confirmar anotação/i }));

    await waitFor(() =>
      expect(acervoApi.anotarFichaDeVida).toHaveBeenCalledWith(
        ITEM_SEM_ANOTACAO.id,
        { teor: "cuidado", estado_de_conservacao: "Bom, limpo" },
        "token-do-mestre",
      ),
    );
  });

  it("a perda ou o dano avisam que nada é debitado, sem campo de culpado", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([ITEM_SEM_ANOTACAO]);

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /ver ficha de vida/i }));
    await usuario.click(screen.getByRole("button", { name: /^anotar$/i }));
    await usuario.selectOptions(screen.getByLabelText(/^teor$/i), "perda");

    expect(
      await screen.findByText(/nada é debitado ao guerreiro.*nem à família/i),
    ).toBeInTheDocument();
    expect(screen.queryByLabelText(/guerreiro/i)).not.toBeInTheDocument();
  });

  it("estado de conservação em falta é apontado antes de enviar", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarListas([ITEM_SEM_ANOTACAO]);
    const anotarEspiado = vi.spyOn(acervoApi, "anotarFichaDeVida");

    render(<TelaDoAcervo />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /ver ficha de vida/i }));
    await usuario.click(screen.getByRole("button", { name: /^anotar$/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar anotação/i }));

    expect(
      await screen.findByText(/informe o estado de conservação apurado/i),
    ).toBeInTheDocument();
    expect(anotarEspiado).not.toHaveBeenCalled();
  });
});
