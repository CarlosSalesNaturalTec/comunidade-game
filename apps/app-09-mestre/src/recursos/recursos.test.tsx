import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type {
  AporteRegistrado,
  NecessidadeDeRecurso,
  PontoDeApoioDaLista,
  TipoDeRecurso,
} from "./api";
import * as recursosApi from "./api";
import { TelaDeRecursos } from "./TelaDeRecursos";

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

const PONTO_DE_APOIO: PontoDeApoioDaLista = {
  id: "ponto-1",
  nome: "Ponto Central",
  comunidade_virtual_id: "comunidade-1",
};

const TIPO_LANCHE: TipoDeRecurso = {
  id: "tipo-lanche",
  nome: "Lanche",
  natureza: "consumivel",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "2.00",
  vigencia_inicio: "2026-01-01",
};

const TIPO_OFICINA: TipoDeRecurso = {
  id: "tipo-oficina",
  nome: "Oficina",
  natureza: "servico",
  unidade: "hora",
  exige_comprovante: false,
  valor_em_moedas: "5.00",
  vigencia_inicio: "2026-01-01",
};

function necessidade(sobrescreve: Partial<NecessidadeDeRecurso> = {}): NecessidadeDeRecurso {
  return {
    aula_id: "aula-1",
    tipo_de_recurso_id: TIPO_LANCHE.id,
    quantidade_faltante: "10",
    valor_em_moedas: "20.00",
    comunidade_virtual_id: "comunidade-1",
    ponto_de_apoio_id: PONTO_DE_APOIO.id,
    inicio_em: "2026-09-01T14:00:00-03:00",
    fim_em: "2026-09-01T16:00:00-03:00",
    ...sobrescreve,
  };
}

function aporte(sobrescreve: Partial<AporteRegistrado> = {}): AporteRegistrado {
  return {
    id: "aporte-1",
    tipo_de_recurso_id: TIPO_LANCHE.id,
    quantidade: "10",
    ponto_de_apoio_id: PONTO_DE_APOIO.id,
    valor_em_moedas: "20.00",
    ressarcivel: true,
    situacao_de_ressarcimento: "em_aberto",
    aula_id: "aula-1",
    data_do_aporte: "2026-08-29",
    ...sobrescreve,
  };
}

// A leitura base que toda tela desta suíte precisa: catálogo e pontos de
// apoio, para resolver nome e natureza sem depender de rede.
function configurarLeituraBase(tipos: TipoDeRecurso[] = [TIPO_LANCHE, TIPO_OFICINA]) {
  vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue(tipos);
  vi.spyOn(recursosApi, "listarMeusPontosDeApoio").mockResolvedValue([PONTO_DE_APOIO]);
  vi.spyOn(recursosApi, "listarMinhasAbsorcoes").mockResolvedValue([]);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("A App 09 apresenta ao Mestre as necessidades de recurso das aulas dele (RF-09-56)", () => {
  it("apresenta a falta com tipo, quantidade, valor em moedas, ponto de apoio e horário", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([necessidade()]);

    render(<TelaDeRecursos />);

    const item = await screen.findByText("Lanche");
    const linha = item.closest("li");
    expect(linha).not.toBeNull();
    expect(within(linha as HTMLElement).getByText(/falta: 10/i)).toBeInTheDocument();
    expect(within(linha as HTMLElement).getByText(/20\.00 moedas/)).toBeInTheDocument();
    expect(within(linha as HTMLElement).getByText("Ponto Central")).toBeInTheDocument();
  });

  it("a lista não traz valor em reais", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([necessidade()]);

    render(<TelaDeRecursos />);

    await screen.findByText("Lanche");
    expect(screen.queryByText(/R\$/)).not.toBeInTheDocument();
  });

  it("a necessidade sem valor de referência vigente continua na lista", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([
      necessidade({ tipo_de_recurso_id: "tipo-sem-vigencia", valor_em_moedas: null }),
    ]);

    render(<TelaDeRecursos />);

    expect(await screen.findByText(/falta: 10/i)).toBeInTheDocument();
    expect(screen.getByText(/sem valor de referência vigente/i)).toBeInTheDocument();
  });

  it("sem necessidade em aberto a lista diz isso", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([]);

    render(<TelaDeRecursos />);

    expect(
      await screen.findByText(/não há necessidade de recurso em aberto/i),
    ).toBeInTheDocument();
  });
});

describe("O Mestre assume a necessidade como absorção em um ato de confirmação (RF-09-57)", () => {
  it("absorve a necessidade em um ato, credita em nome dele e recarrega a lista", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades")
      .mockResolvedValueOnce([necessidade()])
      .mockResolvedValueOnce([]);
    vi.spyOn(recursosApi, "absorverNecessidade").mockResolvedValue(aporte());

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Lanche");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));
    await usuario.type(screen.getByLabelText(/valor de origem/i), "20");
    await usuario.click(screen.getByRole("button", { name: /confirmar absorção/i }));

    await waitFor(() =>
      expect(recursosApi.absorverNecessidade).toHaveBeenCalledWith(
        expect.objectContaining({
          tipoDeRecursoId: TIPO_LANCHE.id,
          pontoDeApoioId: PONTO_DE_APOIO.id,
          aulaId: "aula-1",
          valorDeOrigem: "20",
        }),
        "token-do-mestre",
      ),
    );
    expect(
      await screen.findByText(/não há necessidade de recurso em aberto/i),
    ).toBeInTheDocument();
  });

  it("a absorção parcial mantém a necessidade na lista, com a falta abatida", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades")
      .mockResolvedValueOnce([necessidade({ quantidade_faltante: "10" })])
      .mockResolvedValueOnce([
        necessidade({ quantidade_faltante: "6", valor_em_moedas: "12.00" }),
      ]);
    vi.spyOn(recursosApi, "absorverNecessidade").mockResolvedValue(
      aporte({ quantidade: "4", valor_em_moedas: "8.00" }),
    );

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Lanche");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));
    await usuario.clear(screen.getByLabelText(/quantidade/i));
    await usuario.type(screen.getByLabelText(/quantidade/i), "4");
    await usuario.type(screen.getByLabelText(/valor de origem/i), "8");
    await usuario.click(screen.getByRole("button", { name: /confirmar absorção/i }));

    expect(await screen.findByText(/falta: 6/i)).toBeInTheDocument();
  });

  it("a absorção que fecha o saldo tira a necessidade da lista", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades")
      .mockResolvedValueOnce([necessidade()])
      .mockResolvedValueOnce([]);
    vi.spyOn(recursosApi, "absorverNecessidade").mockResolvedValue(aporte());

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Lanche");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));
    await usuario.type(screen.getByLabelText(/valor de origem/i), "20");
    await usuario.click(screen.getByRole("button", { name: /confirmar absorção/i }));

    await waitFor(() => expect(screen.queryByText("Lanche")).not.toBeInTheDocument());
  });

  it("pede o valor de origem em reais para tipo consumível, ao lado do equivalente em moedas", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([necessidade()]);

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Lanche");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));

    expect(screen.getByLabelText(/valor de origem/i)).toBeInTheDocument();
    expect(screen.getByText(/equivalente: 20\.00 moedas/i)).toBeInTheDocument();
  });

  it("não pede valor de origem para tipo de natureza serviço, e envia sem ele", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([
      necessidade({ tipo_de_recurso_id: TIPO_OFICINA.id, valor_em_moedas: "50.00" }),
    ]);
    vi.spyOn(recursosApi, "absorverNecessidade").mockResolvedValue(aporte());

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Oficina");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));

    expect(screen.queryByLabelText(/valor de origem/i)).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /confirmar absorção/i }));

    await waitFor(() =>
      expect(recursosApi.absorverNecessidade).toHaveBeenCalledWith(
        expect.objectContaining({ valorDeOrigem: undefined }),
        "token-do-mestre",
      ),
    );
  });

  it("não apresenta campo de provedor, homologação ou destinação", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([necessidade()]);

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Lanche");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));

    expect(screen.queryByLabelText(/provedor/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/homologa/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/destinaç/i)).not.toBeInTheDocument();
    expect(
      screen.getByText(/nasce em seu nome e marcado como ressarcível/i),
    ).toBeInTheDocument();
  });

  it("a recusa por tipo sem vigência vira mensagem simples, e a necessidade continua na lista", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(recursosApi, "listarMinhasNecessidades").mockResolvedValue([necessidade()]);
    vi.spyOn(recursosApi, "absorverNecessidade").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este tipo de recurso não tem vigência que cubra a data do aporte.",
      }),
    );

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    await screen.findByText("Lanche");
    await usuario.click(screen.getByRole("button", { name: /^absorver$/i }));
    await usuario.type(screen.getByLabelText(/valor de origem/i), "20");
    await usuario.click(screen.getByRole("button", { name: /confirmar absorção/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/não tem vigência que cubra a data/i);
    expect(recusa.textContent).not.toMatch(/erro_de_validacao/i);
  });
});
