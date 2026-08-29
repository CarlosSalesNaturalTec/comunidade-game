import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PainelDoDia } from "../painel-do-dia/api";
import * as painelApi from "../painel-do-dia/api";
import type { GuerreiroDaLista } from "../personas/api";
import * as personasApi from "../personas/api";
import * as lancamentosApi from "./api";
import { TelaDeLancamentos } from "./TelaDeLancamentos";

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

function painelVazio(): PainelDoDia {
  return {
    aula_id: null,
    comunidade_virtual_id: null,
    ponto_de_apoio_id: null,
    presencas: [],
    aguardando_aparelho: [],
    equipes: [],
    atividades_previstas: [],
    recursos_providos: [],
    saldo_do_ponto_de_apoio: [],
    pendencias: [],
  };
}

function painelDoEncontro(sobrescreve: Partial<PainelDoDia> = {}): PainelDoDia {
  return {
    aula_id: "aula-1",
    comunidade_virtual_id: "comunidade-1",
    ponto_de_apoio_id: "ponto-1",
    presencas: [
      {
        id: "presenca-1",
        guerreiro_id: "guerreiro-1",
        avatar: null,
        nick: "zeferina",
        modo: "reconhecimento",
        confirmador_id: null,
      },
    ],
    aguardando_aparelho: [],
    equipes: [],
    atividades_previstas: [
      {
        id: "atividade-1",
        titulo: "Montagem",
        missao_id: "missao-1",
        missao_titulo: "Montagem do robô",
      },
    ],
    recursos_providos: [],
    saldo_do_ponto_de_apoio: [],
    pendencias: [],
    ...sobrescreve,
  };
}

function guerreiroDaLista(sobrescreve: Partial<GuerreiroDaLista> = {}): GuerreiroDaLista {
  return {
    id: "guerreiro-2",
    nome: "Tais",
    nascimento: "2015-01-01",
    nick: "tais",
    avatar: "avatar-1",
    comunidade_virtual_id: "comunidade-1",
    vinculo_iniciado_em: "2026-08-01T00:00:00-03:00",
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Lançamentos (RF-02-34, RF-02-36, RF-02-37, RF-02-39)", () => {
  it("abre sobre a aula vigente", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeLancamentos />);

    expect((await screen.findAllByText(/zeferina/)).length).toBeGreaterThan(0);
  });

  it("fora da janela de qualquer aula, diz que não há encontro em andamento", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelVazio());

    render(<TelaDeLancamentos />);

    expect(await screen.findByText(/não há encontro em andamento/i)).toBeInTheDocument();
  });

  it("lança a atividade com o desfecho de cada participante, incluindo o mérito extra", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const lancar = vi
      .spyOn(lancamentosApi, "lancarAtividadeRealizada")
      .mockResolvedValue({ id: "aula-1", situacao: "realizada" });

    render(<TelaDeLancamentos />);
    await screen.findByLabelText(/o que zeferina produziu/i);

    const usuario = userEvent.setup();
    await usuario.selectOptions(
      screen.getByLabelText(/desfecho de zeferina/i),
      "merito_extra_por_auxilio",
    );
    await usuario.type(screen.getByLabelText(/o que zeferina produziu/i), "Ajudou o colega");
    await usuario.click(screen.getByRole("button", { name: /lançar atividade realizada/i }));

    await waitFor(() =>
      expect(lancar).toHaveBeenCalledWith(
        "aula-1",
        [
          expect.objectContaining({
            guerreiro_id: "guerreiro-1",
            atividade_id: "atividade-1",
            producao: "Ajudou o colega",
            desfecho: "merito_extra_por_auxilio",
          }),
        ],
        "token-do-admin",
      ),
    );
    expect(await screen.findByText(/aula passou a realizada/i)).toBeInTheDocument();
  });

  it("bloqueia o envio quando falta a produção de um participante, sem chamar o núcleo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const lancar = vi.spyOn(lancamentosApi, "lancarAtividadeRealizada");

    render(<TelaDeLancamentos />);
    await screen.findByLabelText(/o que zeferina produziu/i);

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /lançar atividade realizada/i }));

    expect(
      await screen.findByText(/informe o que este guerreiro\(a\) produziu/i),
    ).toBeInTheDocument();
    expect(lancar).not.toHaveBeenCalled();
  });

  it("a tela de lançamento não oferece campo de valor de pontuação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeLancamentos />);
    await screen.findByLabelText(/o que zeferina produziu/i);

    expect(screen.queryByLabelText(/valor/i)).not.toBeInTheDocument();
  });

  it("confirma a presença que faltou", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [guerreiroDaLista()],
      proximo_cursor: null,
    });
    const confirmar = vi.spyOn(lancamentosApi, "confirmarPresenca").mockResolvedValue({
      id: "presenca-2",
      aula_id: "aula-1",
      guerreiro_id: "guerreiro-2",
      modo: "confirmacao",
      confirmador_id: "admin-1",
      momento_do_fato: "2026-08-27T10:00:00-03:00",
      anulada_em: null,
      anulada_por_id: null,
      motivo_da_anulacao: null,
    });

    render(<TelaDeLancamentos />);
    await screen.findByLabelText(/quem chegou/i);

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/quem chegou/i), "guerreiro-2");
    await usuario.click(screen.getByRole("button", { name: /confirmar presença/i }));

    await waitFor(() =>
      expect(confirmar).toHaveBeenCalledWith(
        "aula-1",
        expect.objectContaining({ guerreiro_id: "guerreiro-2", modo: "confirmacao" }),
        "token-do-admin",
      ),
    );
  });

  it("anula a presença com motivo, e o motivo é obrigatório", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const anular = vi.spyOn(lancamentosApi, "anularPresenca").mockResolvedValue({
      id: "presenca-1",
      aula_id: "aula-1",
      guerreiro_id: "guerreiro-1",
      modo: "reconhecimento",
      confirmador_id: null,
      momento_do_fato: "2026-08-27T10:00:00-03:00",
      anulada_em: "2026-08-27T10:05:00-03:00",
      anulada_por_id: "admin-1",
      motivo_da_anulacao: "Reconheceu a pessoa errada.",
    });

    render(<TelaDeLancamentos />);
    const areaDaConferencia = await screen.findByRole("region", {
      name: /conferência de presenças/i,
    });
    const dentro = within(areaDaConferencia);

    const usuario = userEvent.setup();
    await usuario.click(dentro.getByRole("button", { name: /anular presença/i }));
    expect(await dentro.findByText(/informe o motivo/i)).toBeInTheDocument();
    expect(anular).not.toHaveBeenCalled();

    await usuario.type(
      dentro.getByLabelText(/motivo da anulação de zeferina/i),
      "Reconheceu a pessoa errada.",
    );
    await usuario.click(dentro.getByRole("button", { name: /anular presença/i }));

    await waitFor(() =>
      expect(anular).toHaveBeenCalledWith(
        "aula-1",
        "presenca-1",
        "Reconheceu a pessoa errada.",
        "token-do-admin",
      ),
    );
  });

  it("registra a infração no ato, com o aviso do descuido acidental", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const registrar = vi
      .spyOn(lancamentosApi, "registrarOcorrenciaDeConduta")
      .mockResolvedValue({
        id: "ocorrencia-1",
        guerreiro_id: "guerreiro-1",
        aula_id: "aula-1",
        atividade_id: "atividade-1",
        valor: 5,
        motivo: "Descumpriu combinado.",
        momento_do_fato: "2026-08-27T10:00:00-03:00",
      });

    render(<TelaDeLancamentos />);
    await screen.findByText(/descuido acidental com material comum não é infração/i);

    const usuario = userEvent.setup();
    const areaDaInfracao = screen.getByRole("region", { name: /registrar infração/i });
    const dentro = within(areaDaInfracao);
    await usuario.selectOptions(dentro.getByLabelText(/guerreiro\(a\)/i), "guerreiro-1");
    await usuario.selectOptions(dentro.getByLabelText(/atividade/i), "atividade-1");
    await usuario.type(dentro.getByLabelText(/motivo/i), "Descumpriu combinado.");
    await usuario.click(dentro.getByRole("button", { name: /registrar infração/i }));

    await waitFor(() =>
      expect(registrar).toHaveBeenCalledWith(
        expect.objectContaining({
          guerreiro_id: "guerreiro-1",
          aula_id: "aula-1",
          atividade_id: "atividade-1",
          motivo: "Descumpriu combinado.",
        }),
        "token-do-admin",
      ),
    );
    expect(await dentro.findByText(/valeu no ato/i)).toBeInTheDocument();
  });

  it("motivo obrigatório impede o envio da infração", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const registrar = vi.spyOn(lancamentosApi, "registrarOcorrenciaDeConduta");

    render(<TelaDeLancamentos />);
    const areaDaInfracao = await screen.findByRole("region", { name: /registrar infração/i });
    const dentro = within(areaDaInfracao);

    const usuario = userEvent.setup();
    await usuario.selectOptions(dentro.getByLabelText(/guerreiro\(a\)/i), "guerreiro-1");
    await usuario.selectOptions(dentro.getByLabelText(/atividade/i), "atividade-1");
    await usuario.click(dentro.getByRole("button", { name: /registrar infração/i }));

    expect(await dentro.findByText(/informe o motivo/i)).toBeInTheDocument();
    expect(registrar).not.toHaveBeenCalled();
  });

  it("o teto da aula é apresentado em uma frase", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(lancamentosApi, "registrarOcorrenciaDeConduta").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O teto de pontuação negativa da aula foi alcançado.",
      }),
    );

    render(<TelaDeLancamentos />);
    const areaDaInfracao = await screen.findByRole("region", { name: /registrar infração/i });
    const dentro = within(areaDaInfracao);

    const usuario = userEvent.setup();
    await usuario.selectOptions(dentro.getByLabelText(/guerreiro\(a\)/i), "guerreiro-1");
    await usuario.selectOptions(dentro.getByLabelText(/atividade/i), "atividade-1");
    await usuario.type(dentro.getByLabelText(/motivo/i), "Nova ocorrência.");
    await usuario.click(dentro.getByRole("button", { name: /registrar infração/i }));

    expect(
      await dentro.findByText(/teto de pontuação negativa da aula foi alcançado/i),
    ).toBeInTheDocument();
  });

  it("mostra o aviso de coleta em cada tela, nomeando o dado dela", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeLancamentos />);
    await screen.findByLabelText(/o que zeferina produziu/i);

    expect(screen.getByText(/resultado da atividade do guerreiro/i)).toHaveAttribute(
      "role",
      "status",
    );
    expect(screen.getByText(/presença do guerreiro\(a\) no encontro/i)).toHaveAttribute(
      "role",
      "status",
    );
    expect(screen.getByText(/infração e a pontuação negativa/i)).toHaveAttribute(
      "role",
      "status",
    );
  });

  it("RN-02-23: quem não tem autorização aparece no lançamento como qualquer outro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());
    vi.spyOn(personasApi, "listarGuerreiros").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeLancamentos />);
    await screen.findByLabelText(/o que zeferina produziu/i);

    // A lista é a do encontro inteiro — nenhum campo do painel carrega
    // consentimento, e nenhuma tela oferece filtro, marcação ou ação por
    // ele (`RN-02-23`).
    expect((await screen.findAllByText(/zeferina/i)).length).toBeGreaterThan(0);
    expect(screen.queryByText(/consentimento/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/consentimento/i)).not.toBeInTheDocument();
  });

  it("o Mestre alcança apenas o registro da infração", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(painelApi, "obterPainelDoDia").mockResolvedValue(painelDoEncontro());

    render(<TelaDeLancamentos />);
    await screen.findByRole("region", { name: /registrar infração/i });

    expect(
      screen.queryByRole("button", { name: /lançar atividade realizada/i }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /confirmar presença/i }),
    ).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /anular presença/i })).not.toBeInTheDocument();
  });
});
