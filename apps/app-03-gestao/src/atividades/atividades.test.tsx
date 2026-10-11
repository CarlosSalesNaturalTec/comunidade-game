import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as agendaApi from "../agenda/api";
import * as comunidadesApi from "../comunidades/api";
import * as poderesApi from "../poderes/api";
import * as atividadesApi from "./api";
import { FormularioDeAtividadeAvulsa } from "./FormularioDeAtividadeAvulsa";
import { TelaDeAtividades } from "./TelaDeAtividades";

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
  nome: "Jardim das Flores",
  localizacao: "Bairro de teste",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const OUTRA_COMUNIDADE = { ...COMUNIDADE, id: "comunidade-2", nome: "Vila Nova" };

const AULA = {
  id: "aula-1",
  comunidade_virtual_id: COMUNIDADE.id,
  ponto_de_apoio_id: "ponto-1",
  inicio_em: "2026-10-14T13:00:00-03:00",
  fim_em: "2026-10-14T15:00:00-03:00",
  situacao: "agendada",
  cancelamento_motivo: null,
  recursos_faltantes: [],
};

const AULA_CANCELADA = {
  ...AULA,
  id: "aula-2",
  situacao: "cancelada",
  cancelamento_motivo: "Chuva.",
};

const PODER = {
  id: "poder-1",
  nome: "Meio Ambiente",
  descricao: "Descrição do poder.",
  natureza: "de_guerreiro" as const,
  vigencia: "vigente" as const,
  papel: null,
  tecnico: false,
  ativo: true,
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

beforeEach(() => {
  vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
    itens: [COMUNIDADE, OUTRA_COMUNIDADE],
    proximo_cursor: null,
    ciclo_rotulo: "Ciclo 01",
  });
  vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({
    itens: [AULA, AULA_CANCELADA],
    proximo_cursor: null,
  });
});

afterEach(() => {
  vi.restoreAllMocks();
});

describe("atividade avulsa", () => {
  it("Admin cadastra a atividade avulsa", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi
      .spyOn(atividadesApi, "cadastrarAtividadeAvulsa")
      .mockResolvedValue({
        id: "atividade-1",
        titulo: "Mutirão de limpeza",
        descricao: null,
        modalidade: "em_equipe",
        formato: "presencial",
        natureza: "meio ambiente",
        producao_esperada: "Registro fotográfico.",
        poder_id: PODER.id,
        aula_id: AULA.id,
      });

    render(<FormularioDeAtividadeAvulsa onCadastrada={vi.fn()} />);
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: PODER.nome });

    await usuario.type(screen.getByLabelText(/^título$/i), "Mutirão de limpeza");
    await usuario.type(screen.getByLabelText(/^natureza$/i), "meio ambiente");
    await usuario.type(screen.getByLabelText(/produção esperada/i), "Registro fotográfico.");
    await usuario.selectOptions(screen.getByLabelText(/poder que ela desenvolve/i), PODER.id);
    await usuario.selectOptions(screen.getByLabelText(/^comunidade$/i), COMUNIDADE.id);
    await screen.findByRole("option", { name: /14\/10\/2026/ });
    await usuario.selectOptions(screen.getByLabelText(/aula do encontro/i), AULA.id);

    await usuario.click(screen.getByRole("button", { name: /cadastrar atividade/i }));

    await waitFor(() => expect(cadastrarEspiado).toHaveBeenCalledTimes(1));
    const [entrada] = vi.mocked(cadastrarEspiado).mock.calls[0];
    expect(entrada.titulo).toBe("Mutirão de limpeza");
    expect(entrada.poder_id).toBe(PODER.id);
    expect(entrada.aula_id).toBe(AULA.id);
    expect(entrada.formato).toBe("presencial");
    expect("comunidade_virtual_id" in entrada).toBe(false);
  });

  it("a tela não oferece campo de pontuação nem de recurso", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });

    render(<FormularioDeAtividadeAvulsa onCadastrada={vi.fn()} />);
    const formulario = await screen.findByRole("form", {
      name: /cadastrar atividade avulsa/i,
    });

    expect(within(formulario).queryByLabelText(/pontuação/i)).not.toBeInTheDocument();
    expect(within(formulario).queryByLabelText(/recurso/i)).not.toBeInTheDocument();
    expect(within(formulario).queryByLabelText(/quantidade/i)).not.toBeInTheDocument();
  });

  it("cadastro sem poder é apontado no campo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(atividadesApi, "cadastrarAtividadeAvulsa");

    render(<FormularioDeAtividadeAvulsa onCadastrada={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/^título$/i), "Mutirão de limpeza");
    await usuario.type(screen.getByLabelText(/^natureza$/i), "meio ambiente");
    await usuario.type(screen.getByLabelText(/produção esperada/i), "Registro fotográfico.");

    await usuario.click(screen.getByRole("button", { name: /cadastrar atividade/i }));

    expect(await screen.findByText(/escolha o poder que ela desenvolve/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("RN-02-24: a área diz que cadastra só atividade avulsa e onde fica a de missão", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });

    render(<TelaDeAtividades />);

    expect(
      await screen.findByText(/cadastra apenas atividade avulsa, fora de trilha/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/autoria do mestre, na app 09/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /criar trilha|criar missão|editar trilha/i }),
    ).not.toBeInTheDocument();
  });

  it("quem não é Admin não alcança o cadastro", async () => {
    configurarSessao(SESSAO_DE_MESTRE);

    render(<TelaDeAtividades />);

    expect(
      await screen.findByText(/só o admin acessa a área atividades/i),
    ).toBeInTheDocument();
    expect(
      screen.queryByRole("form", { name: /cadastrar atividade avulsa/i }),
    ).not.toBeInTheDocument();
  });
});

describe("a aula do encontro no cadastro da avulsa (RF-02-29)", () => {
  it("a comunidade escolhida estreita as aulas, e a cancelada não é oferecida", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });

    render(<FormularioDeAtividadeAvulsa onCadastrada={vi.fn()} />);
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: COMUNIDADE.nome });
    expect(screen.queryByRole("option", { name: /14\/10\/2026/ })).not.toBeInTheDocument();

    await usuario.selectOptions(screen.getByLabelText(/^comunidade$/i), COMUNIDADE.id);

    expect(await screen.findByRole("option", { name: /14\/10\/2026/ })).toBeInTheDocument();
    expect(vi.mocked(agendaApi.listarAgenda).mock.calls[0][1]).toEqual({
      comunidadeId: COMUNIDADE.id,
    });
    const seletorDeAula = screen.getByLabelText(/aula do encontro/i);
    expect(within(seletorDeAula).getAllByRole("option")).toHaveLength(2);
  });

  it("cadastro sem aula é apontado no campo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });
    const cadastrarEspiado = vi.spyOn(atividadesApi, "cadastrarAtividadeAvulsa");

    render(<FormularioDeAtividadeAvulsa onCadastrada={vi.fn()} />);
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: PODER.nome });
    await usuario.type(screen.getByLabelText(/^título$/i), "Mutirão de limpeza");
    await usuario.type(screen.getByLabelText(/^natureza$/i), "meio ambiente");
    await usuario.type(screen.getByLabelText(/produção esperada/i), "Registro fotográfico.");
    await usuario.selectOptions(screen.getByLabelText(/poder que ela desenvolve/i), PODER.id);

    await usuario.click(screen.getByRole("button", { name: /cadastrar atividade/i }));

    expect(await screen.findByText(/escolha a aula do encontro/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("o formato não é escolha, e a tela diz que a avulsa é do encontro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [PODER],
      proximo_cursor: null,
    });

    render(<FormularioDeAtividadeAvulsa onCadastrada={vi.fn()} />);
    const formulario = await screen.findByRole("form", {
      name: /cadastrar atividade avulsa/i,
    });

    expect(within(formulario).queryByLabelText(/formato/i)).not.toBeInTheDocument();
    expect(
      within(formulario).getByText(/acontece no encontro: é sempre presencial/i),
    ).toBeInTheDocument();
  });
});
