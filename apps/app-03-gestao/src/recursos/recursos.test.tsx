import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as agendaApi from "../agenda/api";
import * as comunidadesApi from "../comunidades/api";
import * as personasApi from "../personas/api";
import * as pontosDeApoioApi from "../pontos-de-apoio/api";
import * as recursosApi from "./api";
import { ListaDeNecessidades } from "./ListaDeNecessidades";
import { RegistroDeAporte } from "./RegistroDeAporte";
import { TelaDeRecursos } from "./TelaDeRecursos";

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
  responsavel_id: null,
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

const TIPO_SEM_COMPROVANTE = {
  id: "tipo-1",
  nome: "Lanche",
  natureza: "material",
  unidade: "unidade",
  exige_comprovante: false,
  valor_em_moedas: "1",
  vigencia_inicio: "2026-01-01",
};

const TIPO_COM_COMPROVANTE = {
  id: "tipo-2",
  nome: "Transporte",
  natureza: "material",
  unidade: "passagem",
  exige_comprovante: true,
  valor_em_moedas: "2",
  vigencia_inicio: "2026-01-01",
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

function configurarCatalogos() {
  vi.spyOn(personasApi, "listarMestres").mockResolvedValue({
    itens: [MESTRE],
    proximo_cursor: null,
  });
  vi.spyOn(personasApi, "listarApoiadores").mockResolvedValue({
    itens: [APOIADOR],
    proximo_cursor: null,
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
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("registro de aporte", () => {
  it("Admin registra o aporte e a tela mostra o valor em moedas, nunca em reais", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarCatalogos();
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_SEM_COMPROVANTE]);
    const registrarEspiado = vi.spyOn(recursosApi, "registrarAporte").mockResolvedValue({
      id: "aporte-1",
      provedor_id: APOIADOR.id,
      tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
      quantidade: "10",
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      valor_em_moedas: "10",
      forma: "material",
      data_do_aporte: "2026-08-20",
    });

    render(<RegistroDeAporte onRegistrado={vi.fn()} />);
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: APOIADOR.nome });
    await usuario.selectOptions(screen.getByLabelText(/provedor/i), APOIADOR.id);
    await usuario.selectOptions(screen.getByLabelText(/^ponto de apoio$/i), PONTO_DE_APOIO.id);
    await usuario.selectOptions(
      screen.getByLabelText(/^tipo de recurso$/i),
      TIPO_SEM_COMPROVANTE.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-20");

    await usuario.click(screen.getByRole("button", { name: /registrar aporte/i }));

    await waitFor(() => expect(registrarEspiado).toHaveBeenCalledTimes(1));

    expect(screen.queryByText(/reais|R\$/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/pix|banco|conta/i)).not.toBeInTheDocument();
  });

  it("tipo que exige comprovante bloqueia o envio sem ele", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarCatalogos();
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_COM_COMPROVANTE]);
    const registrarEspiado = vi.spyOn(recursosApi, "registrarAporte");

    render(<RegistroDeAporte onRegistrado={vi.fn()} />);
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: APOIADOR.nome });
    await usuario.selectOptions(screen.getByLabelText(/provedor/i), APOIADOR.id);
    await usuario.selectOptions(screen.getByLabelText(/^ponto de apoio$/i), PONTO_DE_APOIO.id);
    await usuario.selectOptions(
      screen.getByLabelText(/^tipo de recurso$/i),
      TIPO_COM_COMPROVANTE.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-20");

    await usuario.click(screen.getByRole("button", { name: /registrar aporte/i }));

    expect(await screen.findByText(/exige o comprovante/i)).toBeInTheDocument();
    expect(registrarEspiado).not.toHaveBeenCalled();
  });

  it("aporte em causa própria é apresentado como recusa", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarCatalogos();
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_SEM_COMPROVANTE]);
    vi.spyOn(recursosApi, "registrarAporte").mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "permissao_negada",
        mensagem: "Quem homologa o aporte não pode ser o próprio provedor.",
      }),
    );

    render(<RegistroDeAporte onRegistrado={vi.fn()} />);
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: APOIADOR.nome });
    await usuario.selectOptions(screen.getByLabelText(/provedor/i), APOIADOR.id);
    await usuario.selectOptions(screen.getByLabelText(/^ponto de apoio$/i), PONTO_DE_APOIO.id);
    await usuario.selectOptions(
      screen.getByLabelText(/^tipo de recurso$/i),
      TIPO_SEM_COMPROVANTE.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "10");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-20");

    await usuario.click(screen.getByRole("button", { name: /registrar aporte/i }));

    expect(await screen.findByText(/não pode ser o próprio provedor/i)).toBeInTheDocument();
  });
});

describe("lista de necessidades", () => {
  const NECESSIDADE = {
    aula_id: "aula-1",
    tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
    quantidade_faltante: "5",
    valor_em_moedas: "5",
    comunidade_virtual_id: COMUNIDADE.id,
    ponto_de_apoio_id: PONTO_DE_APOIO.id,
    inicio_em: "2026-08-21T10:00:00-03:00",
    fim_em: "2026-08-21T12:00:00-03:00",
  };

  const identidade = (id: string) => id;

  it("a necessidade aparece com o recurso, a falta, o valor, a comunidade e o horário", () => {
    render(
      <ListaDeNecessidades
        necessidades={[NECESSIDADE]}
        nomeDoTipoDeRecurso={() => TIPO_SEM_COMPROVANTE.nome}
        nomeDaComunidade={() => COMUNIDADE.nome}
        nomeDoPontoDeApoio={() => PONTO_DE_APOIO.nome}
      />,
    );

    expect(screen.getByText(TIPO_SEM_COMPROVANTE.nome)).toBeInTheDocument();
    expect(screen.getByText(/falta: 5/i)).toBeInTheDocument();
    expect(screen.getByText(/5 moedas/i)).toBeInTheDocument();
    expect(screen.getByText(COMUNIDADE.nome)).toBeInTheDocument();
    expect(screen.getByText(PONTO_DE_APOIO.nome)).toBeInTheDocument();
  });

  it("tipo sem vigência aparece sem valor em moedas", () => {
    render(
      <ListaDeNecessidades
        necessidades={[{ ...NECESSIDADE, valor_em_moedas: null }]}
        nomeDoTipoDeRecurso={identidade}
        nomeDaComunidade={identidade}
        nomeDoPontoDeApoio={identidade}
      />,
    );

    expect(screen.getByText(/sem valor de referência vigente/i)).toBeInTheDocument();
    expect(screen.queryByText(/moedas/i)).not.toBeInTheDocument();
  });

  it("sem necessidade em aberto a área diz isso, em vez de lista vazia sem explicação", () => {
    render(
      <ListaDeNecessidades
        necessidades={[]}
        nomeDoTipoDeRecurso={identidade}
        nomeDaComunidade={identidade}
        nomeDoPontoDeApoio={identidade}
      />,
    );

    expect(screen.getByText(/não há necessidade de recurso em aberto/i)).toBeInTheDocument();
  });
});

describe("área Recursos", () => {
  it("quem não é Admin lê a recusa, sem dado de gestão", () => {
    configurarSessao(SESSAO_DE_MESTRE);

    render(<TelaDeRecursos />);

    expect(screen.getByText(/só o admin acessa a área recursos/i)).toBeInTheDocument();
    expect(screen.queryByRole("form", { name: /registrar aporte/i })).not.toBeInTheDocument();
  });

  it("o aporte que fecha a falta confirma a aula e a necessidade some da lista", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarCatalogos();
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_SEM_COMPROVANTE]);
    vi.spyOn(recursosApi, "listarNecessidades")
      .mockResolvedValueOnce([
        {
          aula_id: "aula-1",
          tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
          quantidade_faltante: "5",
          valor_em_moedas: "5",
          comunidade_virtual_id: COMUNIDADE.id,
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          inicio_em: "2026-08-21T10:00:00-03:00",
          fim_em: "2026-08-21T12:00:00-03:00",
        },
      ])
      .mockResolvedValueOnce([]);
    vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({
      itens: [
        {
          id: "aula-1",
          comunidade_virtual_id: COMUNIDADE.id,
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          inicio_em: "2026-08-21T10:00:00-03:00",
          fim_em: "2026-08-21T12:00:00-03:00",
          situacao: "confirmada",
          cancelamento_motivo: null,
          recursos_faltantes: [],
        },
      ],
      proximo_cursor: null,
    });
    vi.spyOn(recursosApi, "registrarAporte").mockResolvedValue({
      id: "aporte-1",
      provedor_id: APOIADOR.id,
      tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
      quantidade: "5",
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      valor_em_moedas: "5",
      forma: "material",
      data_do_aporte: "2026-08-20",
    });

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    expect(await screen.findByText(/falta: 5/i)).toBeInTheDocument();

    await usuario.selectOptions(screen.getByLabelText(/provedor/i), APOIADOR.id);
    await usuario.selectOptions(screen.getByLabelText(/^ponto de apoio$/i), PONTO_DE_APOIO.id);
    await usuario.selectOptions(
      screen.getByLabelText(/^tipo de recurso$/i),
      TIPO_SEM_COMPROVANTE.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "5");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-20");
    await usuario.click(screen.getByRole("button", { name: /registrar aporte/i }));

    expect(
      await screen.findByText(/não há necessidade de recurso em aberto/i),
    ).toBeInTheDocument();
    expect(
      await screen.findByText(/aula confirmada, com a reserva efetivada/i),
    ).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /confirmar/i })).not.toBeInTheDocument();
  });

  it("o aporte parcial mantém a necessidade na lista, com a falta abatida", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    configurarCatalogos();
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([TIPO_SEM_COMPROVANTE]);
    vi.spyOn(recursosApi, "listarNecessidades")
      .mockResolvedValueOnce([
        {
          aula_id: "aula-1",
          tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
          quantidade_faltante: "5",
          valor_em_moedas: "5",
          comunidade_virtual_id: COMUNIDADE.id,
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          inicio_em: "2026-08-21T10:00:00-03:00",
          fim_em: "2026-08-21T12:00:00-03:00",
        },
      ])
      .mockResolvedValueOnce([
        {
          aula_id: "aula-1",
          tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
          quantidade_faltante: "3",
          valor_em_moedas: "3",
          comunidade_virtual_id: COMUNIDADE.id,
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          inicio_em: "2026-08-21T10:00:00-03:00",
          fim_em: "2026-08-21T12:00:00-03:00",
        },
      ]);
    vi.spyOn(recursosApi, "registrarAporte").mockResolvedValue({
      id: "aporte-2",
      provedor_id: APOIADOR.id,
      tipo_de_recurso_id: TIPO_SEM_COMPROVANTE.id,
      quantidade: "2",
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      valor_em_moedas: "2",
      forma: "material",
      data_do_aporte: "2026-08-20",
    });

    render(<TelaDeRecursos />);
    const usuario = userEvent.setup();

    expect(await screen.findByText(/falta: 5/i)).toBeInTheDocument();

    await usuario.selectOptions(screen.getByLabelText(/provedor/i), APOIADOR.id);
    await usuario.selectOptions(screen.getByLabelText(/^ponto de apoio$/i), PONTO_DE_APOIO.id);
    await usuario.selectOptions(
      screen.getByLabelText(/^tipo de recurso$/i),
      TIPO_SEM_COMPROVANTE.id,
    );
    await usuario.type(screen.getByLabelText(/quantidade/i), "2");
    await usuario.type(screen.getByLabelText(/data do aporte/i), "2026-08-20");
    await usuario.click(screen.getByRole("button", { name: /registrar aporte/i }));

    expect(await screen.findByText(/falta: 3/i)).toBeInTheDocument();
  });
});
