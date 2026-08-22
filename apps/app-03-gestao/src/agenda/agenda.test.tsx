import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as comunidadesApi from "../comunidades/api";
import * as pontosDeApoioApi from "../pontos-de-apoio/api";
import * as agendaApi from "./api";
import { FormularioDeAgendamento } from "./FormularioDeAgendamento";
import { TelaDaAgenda } from "./TelaDaAgenda";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
};

const COMUNIDADE_UM = {
  id: "comunidade-1",
  nome: "Comunidade Um",
  localizacao: "Bairro Um",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const COMUNIDADE_DOIS = {
  id: "comunidade-2",
  nome: "Comunidade Dois",
  localizacao: "Bairro Dois",
  series_abertas: null,
  series_ativas: null,
  registros_validos: null,
  continuidade: null,
};

const PONTO_DE_APOIO = {
  id: "ponto-1",
  nome: "Sede",
  comunidade_virtual_id: COMUNIDADE_UM.id,
  responsavel_id: null,
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
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("agenda de aulas", () => {
  it("Admin agenda a aula e ela nasce confirmada, na agenda", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE_UM],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    vi.spyOn(agendaApi, "listarAgenda")
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [
          {
            id: "aula-1",
            comunidade_virtual_id: COMUNIDADE_UM.id,
            ponto_de_apoio_id: PONTO_DE_APOIO.id,
            inicio_em: "2026-08-10T10:00:00Z",
            fim_em: "2026-08-10T12:00:00Z",
            situacao: "confirmada",
            cancelamento_motivo: null,
          },
        ],
        proximo_cursor: null,
      });
    vi.spyOn(agendaApi, "agendarAula").mockResolvedValue({
      id: "aula-1",
      comunidade_virtual_id: COMUNIDADE_UM.id,
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      inicio_em: "2026-08-10T10:00:00Z",
      fim_em: "2026-08-10T12:00:00Z",
      situacao: "confirmada",
      cancelamento_motivo: null,
    });

    render(<TelaDaAgenda />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova aula/i }));

    const formulario = screen.getByRole("form", { name: /nova aula/i });
    const campoInicial = within(formulario).getByLabelText(/horário inicial/i);
    const campoFinal = within(formulario).getByLabelText(/horário final/i);
    // jsdom não simula a digitação segmentada de `datetime-local`; o valor
    // chega por `fireEvent.change`, como o próprio navegador reportaria ao
    // confirmar cada segmento (mesma limitação documentada em
    // `CampoDeDataHora.test.tsx`).
    fireEvent.change(campoInicial, { target: { value: "2026-08-10T10:00" } });
    fireEvent.change(campoFinal, { target: { value: "2026-08-10T12:00" } });

    await usuario.click(within(formulario).getByRole("button", { name: /^agendar$/i }));

    await waitFor(() => expect(agendaApi.agendarAula).toHaveBeenCalledTimes(1));
    const [entrada] = vi.mocked(agendaApi.agendarAula).mock.calls[0];
    expect(entrada.comunidade_virtual_id).toBe(COMUNIDADE_UM.id);
    expect(entrada.ponto_de_apoio_id).toBe(PONTO_DE_APOIO.id);

    expect(await screen.findByText("Confirmada")).toBeInTheDocument();
  });

  it("horário final não posterior ao inicial é apontado no campo, sem agendar nada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    const agendarEspiado = vi.spyOn(agendaApi, "agendarAula");

    render(
      <FormularioDeAgendamento
        comunidades={[COMUNIDADE_UM]}
        onAgendada={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await screen.findByRole("option", { name: PONTO_DE_APOIO.nome });

    const campoInicial = screen.getByLabelText(/horário inicial/i);
    const campoFinal = screen.getByLabelText(/horário final/i);
    fireEvent.change(campoInicial, { target: { value: "2026-08-10T12:00" } });
    fireEvent.change(campoFinal, { target: { value: "2026-08-10T10:00" } });

    await usuario.click(screen.getByRole("button", { name: /^agendar$/i }));

    expect(
      await screen.findByText(/horário final precisa ser posterior ao inicial/i),
    ).toBeInTheDocument();
    expect(agendarEspiado).not.toHaveBeenCalled();
  });

  it("o seletor de ponto de apoio é restrito à comunidade escolhida", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const listarPontosDeApoioEspiado = vi
      .spyOn(pontosDeApoioApi, "listarPontosDeApoio")
      .mockResolvedValue({ itens: [PONTO_DE_APOIO], proximo_cursor: null });

    render(
      <FormularioDeAgendamento
        comunidades={[COMUNIDADE_UM, COMUNIDADE_DOIS]}
        onAgendada={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );

    await waitFor(() =>
      expect(listarPontosDeApoioEspiado).toHaveBeenCalledWith(
        "token-do-admin",
        COMUNIDADE_UM.id,
      ),
    );

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/^comunidade$/i), COMUNIDADE_DOIS.id);

    await waitFor(() =>
      expect(listarPontosDeApoioEspiado).toHaveBeenCalledWith(
        "token-do-admin",
        COMUNIDADE_DOIS.id,
      ),
    );
  });

  it("a agenda distingue as situações e Mestre lê só as suas comunidades", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE_UM],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    const listarAgendaEspiado = vi.spyOn(agendaApi, "listarAgenda").mockResolvedValue({
      itens: [
        {
          id: "aula-confirmada",
          comunidade_virtual_id: COMUNIDADE_UM.id,
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          inicio_em: "2026-08-10T10:00:00Z",
          fim_em: "2026-08-10T12:00:00Z",
          situacao: "confirmada",
          cancelamento_motivo: null,
        },
        {
          id: "aula-pendente",
          comunidade_virtual_id: COMUNIDADE_UM.id,
          ponto_de_apoio_id: PONTO_DE_APOIO.id,
          inicio_em: "2026-08-11T10:00:00Z",
          fim_em: "2026-08-11T12:00:00Z",
          situacao: "pendente_de_lastro",
          cancelamento_motivo: null,
        },
      ],
      proximo_cursor: null,
    });

    render(<TelaDaAgenda />);

    expect(await screen.findByText("Confirmada")).toBeInTheDocument();
    expect(screen.getByText("Pendente de lastro")).toBeInTheDocument();
    // O Mestre não declara comunidade — o núcleo já deriva do vínculo
    // (`RF-01-18`).
    expect(listarAgendaEspiado).toHaveBeenCalledWith(
      "token-do-mestre",
      expect.objectContaining({ comunidadeId: undefined }),
    );
    expect(screen.queryByRole("button", { name: /nova aula/i })).not.toBeInTheDocument();
  });

  it("cancelamento com motivo cancela a aula, e sem motivo é recusado no campo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE_UM],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_DE_APOIO],
      proximo_cursor: null,
    });
    vi.spyOn(agendaApi, "listarAgenda")
      .mockResolvedValueOnce({
        itens: [
          {
            id: "aula-1",
            comunidade_virtual_id: COMUNIDADE_UM.id,
            ponto_de_apoio_id: PONTO_DE_APOIO.id,
            inicio_em: "2026-08-10T10:00:00Z",
            fim_em: "2026-08-10T12:00:00Z",
            situacao: "confirmada",
            cancelamento_motivo: null,
          },
        ],
        proximo_cursor: null,
      })
      .mockResolvedValueOnce({
        itens: [
          {
            id: "aula-1",
            comunidade_virtual_id: COMUNIDADE_UM.id,
            ponto_de_apoio_id: PONTO_DE_APOIO.id,
            inicio_em: "2026-08-10T10:00:00Z",
            fim_em: "2026-08-10T12:00:00Z",
            situacao: "cancelada",
            cancelamento_motivo: "Chuva forte.",
          },
        ],
        proximo_cursor: null,
      });
    const cancelarEspiado = vi.spyOn(agendaApi, "cancelarAula").mockResolvedValue({
      id: "aula-1",
      comunidade_virtual_id: COMUNIDADE_UM.id,
      ponto_de_apoio_id: PONTO_DE_APOIO.id,
      inicio_em: "2026-08-10T10:00:00Z",
      fim_em: "2026-08-10T12:00:00Z",
      situacao: "cancelada",
      cancelamento_motivo: "Chuva forte.",
    });

    render(<TelaDaAgenda />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /cancelar aula/i }));
    expect(
      screen.getByText(/libera os recursos reservados desta aula e não pode ser desfeito/i),
    ).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /confirmar cancelamento/i }));
    expect(await screen.findByText(/informe o motivo do cancelamento/i)).toBeInTheDocument();
    expect(cancelarEspiado).not.toHaveBeenCalled();

    await usuario.type(screen.getByLabelText(/motivo do cancelamento/i), "Chuva forte.");
    await usuario.click(screen.getByRole("button", { name: /confirmar cancelamento/i }));

    await waitFor(() =>
      expect(cancelarEspiado).toHaveBeenCalledWith("aula-1", "Chuva forte.", "token-do-admin"),
    );
    expect(await screen.findByText("Cancelada")).toBeInTheDocument();
    expect(await screen.findByText(/motivo: chuva forte\./i)).toBeInTheDocument();
  });
});
