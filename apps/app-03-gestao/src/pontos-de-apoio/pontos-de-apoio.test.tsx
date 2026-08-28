import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import * as comunidadesApi from "../comunidades/api";
import * as personasApi from "../personas/api";
import * as recursosApi from "../recursos/api";
import type { LancamentoDoExtrato, PontoDeApoioDaLista } from "./api";
import * as pontosDeApoioApi from "./api";
import { ExtratoDoPontoDeApoio } from "./ExtratoDoPontoDeApoio";
import { FormularioDePontoDeApoio } from "./FormularioDePontoDeApoio";
import { TelaDePontosDeApoio } from "./TelaDePontosDeApoio";
import { TransferenciaDeSaldo } from "./TransferenciaDeSaldo";

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

afterEach(() => {
  vi.restoreAllMocks();
});

// Os Mestres e Apoiadores cadastrados são carregados sempre que a tela
// abre, para resolver o nome do responsável e oferecer a designação
// (`RF-07-49`) — vazio por padrão, sobrescrito nos testes de designação.
beforeEach(() => {
  vi.spyOn(personasApi, "listarMestres").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
  vi.spyOn(personasApi, "listarApoiadores").mockResolvedValue({
    itens: [],
    proximo_cursor: null,
  });
});

describe("cadastro de ponto de apoio", () => {
  it("Admin cadastra o ponto de apoio e ele aparece entre os existentes", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio")
      .mockResolvedValueOnce({ itens: [], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [
          {
            id: "ponto-1",
            nome: "Sede",
            comunidade_virtual_id: COMUNIDADE.id,
            responsavel_id: null,
            ativo: true,
          },
        ],
        proximo_cursor: null,
      });
    vi.spyOn(pontosDeApoioApi, "cadastrarPontoDeApoio").mockResolvedValue({
      id: "ponto-1",
      nome: "Sede",
      comunidade_virtual_id: COMUNIDADE.id,
      responsavel_id: null,
      ativo: true,
    });

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /novo ponto de apoio/i }));
    await usuario.type(screen.getByLabelText(/^nome$/i), "Sede");

    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    await waitFor(() =>
      expect(pontosDeApoioApi.cadastrarPontoDeApoio).toHaveBeenCalledWith(
        { nome: "Sede", comunidade_id: COMUNIDADE.id },
        "token-do-admin",
      ),
    );

    expect(await screen.findByText("Sede")).toBeInTheDocument();
  });

  it("campo obrigatório em falta é apontado no campo, sem cadastrar nada", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const cadastrarEspiado = vi.spyOn(pontosDeApoioApi, "cadastrarPontoDeApoio");

    render(
      <FormularioDePontoDeApoio
        comunidades={[COMUNIDADE]}
        onCriado={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /^cadastrar$/i }));

    expect(await screen.findByText(/informe o nome do ponto de apoio/i)).toBeInTheDocument();
    expect(cadastrarEspiado).not.toHaveBeenCalled();
  });

  it("ponto de apoio sem responsável é apresentado como informação, não como erro", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [
        {
          id: "ponto-1",
          nome: "Sede",
          comunidade_virtual_id: COMUNIDADE.id,
          responsavel_id: null,
          ativo: true,
        },
      ],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    const semResponsavel = await screen.findByText(/sem responsável designado/i);
    expect(semResponsavel).toHaveAttribute("role", "status");
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });

  it("Mestre não recebe o caminho de cadastro", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    await screen.findByText(/nenhum ponto de apoio cadastrado/i);
    expect(
      screen.queryByRole("button", { name: /novo ponto de apoio/i }),
    ).not.toBeInTheDocument();
  });
});

const PONTO_ATIVO: PontoDeApoioDaLista = {
  id: "ponto-1",
  nome: "Sede",
  comunidade_virtual_id: COMUNIDADE.id,
  responsavel_id: null,
  ativo: true,
};

const PONTO_INATIVO: PontoDeApoioDaLista = {
  id: "ponto-2",
  nome: "Anexo",
  comunidade_virtual_id: COMUNIDADE.id,
  responsavel_id: null,
  ativo: false,
};

describe("desativar e reativar ponto de apoio", () => {
  it("Admin desativa um ponto de apoio informando o motivo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio")
      .mockResolvedValueOnce({ itens: [PONTO_ATIVO], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [{ ...PONTO_ATIVO, ativo: false }],
        proximo_cursor: null,
      });
    vi.spyOn(pontosDeApoioApi, "desativarPontoDeApoio").mockResolvedValue({
      ...PONTO_ATIVO,
      ativo: false,
    });

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^desativar$/i }));
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Fechou o espaço.");
    await usuario.click(screen.getByRole("button", { name: /confirmar desativar/i }));

    await waitFor(() =>
      expect(pontosDeApoioApi.desativarPontoDeApoio).toHaveBeenCalledWith(
        PONTO_ATIVO.id,
        "Fechou o espaço.",
        "token-do-admin",
      ),
    );
    expect(await screen.findByText("Inativo")).toBeInTheDocument();
  });

  it("inativo continua na lista, distinguido do ativo", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_ATIVO, PONTO_INATIVO],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    expect(await screen.findByText("Ativo")).toBeInTheDocument();
    expect(screen.getByText("Inativo")).toBeInTheDocument();
    expect(screen.getByText("Anexo")).toBeInTheDocument();
  });

  it("Mestre não vê a ação de desativar nem reativar", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_ATIVO],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    await screen.findByText("Sede");
    expect(screen.queryByRole("button", { name: /desativar/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reativar/i })).not.toBeInTheDocument();
  });

  it("sem motivo não confirma a desativação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_ATIVO],
      proximo_cursor: null,
    });
    const desativarEspiado = vi.spyOn(pontosDeApoioApi, "desativarPontoDeApoio");

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^desativar$/i }));
    await usuario.click(screen.getByRole("button", { name: /confirmar desativar/i }));

    expect(await screen.findByText(/informe o motivo/i)).toBeInTheDocument();
    expect(desativarEspiado).not.toHaveBeenCalled();
  });

  it("recusa por aula futura é explicada, sem jargão de TI", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_ATIVO],
      proximo_cursor: null,
    });
    vi.spyOn(pontosDeApoioApi, "desativarPontoDeApoio").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este ponto de apoio tem 2 aulas futuras agendadas; cancele-as ou aguarde.",
        campo: "aulas_futuras",
      }),
    );

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^desativar$/i }));
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Fechou o espaço.");
    await usuario.click(screen.getByRole("button", { name: /confirmar desativar/i }));

    expect(await screen.findByText(/2 aulas futuras agendadas/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /transferir saldo/i }),
    ).not.toBeInTheDocument();
  });

  it("recusa por saldo oferece o caminho da transferência", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_ATIVO],
      proximo_cursor: null,
    });
    vi.spyOn(pontosDeApoioApi, "desativarPontoDeApoio").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este ponto de apoio ainda tem saldo de: Lanche.",
        campo: "saldo",
      }),
    );
    vi.spyOn(pontosDeApoioApi, "listarSaldosDoPontoDeApoio").mockResolvedValue([
      { tipo_de_recurso_id: "tipo-1", nome: "Lanche", saldo: "3.00" },
    ]);

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^desativar$/i }));
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Fechou o espaço.");
    await usuario.click(screen.getByRole("button", { name: /confirmar desativar/i }));

    expect(await screen.findByText(/ainda tem saldo de: lanche/i)).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: /transferir saldo/i }));

    expect(
      await screen.findByRole("form", { name: /transferir saldo de sede/i }),
    ).toBeInTheDocument();
  });
});

describe("transferência de saldo entre pontos de apoio", () => {
  const DESTINO_ATIVO: PontoDeApoioDaLista = {
    id: "ponto-destino-ativo",
    nome: "Destino Ativo",
    comunidade_virtual_id: COMUNIDADE.id,
    responsavel_id: null,
    ativo: true,
  };
  const DESTINO_INATIVO: PontoDeApoioDaLista = {
    id: "ponto-destino-inativo",
    nome: "Destino Inativo",
    comunidade_virtual_id: COMUNIDADE.id,
    responsavel_id: null,
    ativo: false,
  };

  it("Admin transfere um tipo de recurso e a transferência é enviada como um fato só", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarSaldosDoPontoDeApoio").mockResolvedValue([
      { tipo_de_recurso_id: "tipo-1", nome: "Lanche", saldo: "10.00" },
    ]);
    vi.spyOn(pontosDeApoioApi, "transferirSaldo").mockResolvedValue({
      debito: { id: "d1", ponto_de_apoio_id: PONTO_ATIVO.id, quantidade: "4" },
      credito: { id: "c1", ponto_de_apoio_id: DESTINO_ATIVO.id, quantidade: "4" },
    });
    const aoConcluir = vi.fn();

    render(
      <TransferenciaDeSaldo
        origem={PONTO_ATIVO}
        pontosDeApoio={[PONTO_ATIVO, DESTINO_ATIVO, DESTINO_INATIVO]}
        onConcluida={aoConcluir}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.selectOptions(await screen.findByLabelText(/tipo de recurso/i), "tipo-1");
    await usuario.type(screen.getByLabelText(/^quantidade$/i), "4");
    await usuario.selectOptions(
      screen.getByLabelText(/ponto de apoio de destino/i),
      DESTINO_ATIVO.id,
    );
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Redistribuição de acervo.");
    await usuario.click(screen.getByRole("button", { name: /^transferir$/i }));

    await waitFor(() =>
      expect(pontosDeApoioApi.transferirSaldo).toHaveBeenCalledWith(
        {
          tipo_de_recurso_id: "tipo-1",
          ponto_de_apoio_origem_id: PONTO_ATIVO.id,
          ponto_de_apoio_destino_id: DESTINO_ATIVO.id,
          quantidade: "4",
          motivo: "Redistribuição de acervo.",
        },
        "token-do-admin",
      ),
    );
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("o destino inativo e a própria origem não são oferecidos", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarSaldosDoPontoDeApoio").mockResolvedValue([
      { tipo_de_recurso_id: "tipo-1", nome: "Lanche", saldo: "10.00" },
    ]);

    render(
      <TransferenciaDeSaldo
        origem={PONTO_ATIVO}
        pontosDeApoio={[PONTO_ATIVO, DESTINO_ATIVO, DESTINO_INATIVO]}
        onConcluida={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );

    const seletorDeDestino = await screen.findByLabelText(/ponto de apoio de destino/i);
    expect(within(seletorDeDestino).getByText("Destino Ativo")).toBeInTheDocument();
    expect(within(seletorDeDestino).queryByText("Destino Inativo")).not.toBeInTheDocument();
    expect(within(seletorDeDestino).queryByText(PONTO_ATIVO.nome)).not.toBeInTheDocument();
  });

  it("quantidade acima do saldo é barrada antes de enviar", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarSaldosDoPontoDeApoio").mockResolvedValue([
      { tipo_de_recurso_id: "tipo-1", nome: "Lanche", saldo: "3.00" },
    ]);
    const transferirEspiado = vi.spyOn(pontosDeApoioApi, "transferirSaldo");

    render(
      <TransferenciaDeSaldo
        origem={PONTO_ATIVO}
        pontosDeApoio={[PONTO_ATIVO, DESTINO_ATIVO]}
        onConcluida={vi.fn()}
        onCancelar={vi.fn()}
      />,
    );
    const usuario = userEvent.setup();

    await usuario.selectOptions(await screen.findByLabelText(/tipo de recurso/i), "tipo-1");
    await usuario.type(screen.getByLabelText(/^quantidade$/i), "5");
    await usuario.selectOptions(
      screen.getByLabelText(/ponto de apoio de destino/i),
      DESTINO_ATIVO.id,
    );
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Redistribuição de acervo.");
    await usuario.click(screen.getByRole("button", { name: /^transferir$/i }));

    expect(
      await screen.findByText(/o saldo dispon[íi]vel na origem é 3\.00/i),
    ).toBeInTheDocument();
    expect(transferirEspiado).not.toHaveBeenCalled();
  });
});

describe("extrato e ajuste do livro-razão (RF-02-40)", () => {
  const PONTO_DO_EXTRATO: PontoDeApoioDaLista = {
    id: "ponto-1",
    nome: "Sede",
    comunidade_virtual_id: COMUNIDADE.id,
    responsavel_id: null,
    ativo: true,
  };

  const CREDITO: LancamentoDoExtrato = {
    id: "lancamento-1",
    natureza: "credito",
    tipo_de_recurso_id: "tipo-1",
    ponto_de_apoio_id: PONTO_DO_EXTRATO.id,
    quantidade: "3.00",
    valor_em_moedas: "3.00",
    lancamento_original_id: null,
    motivo_do_ajuste: null,
    lancamento_relacionado_id: null,
  };

  beforeEach(() => {
    vi.spyOn(recursosApi, "listarTiposDeRecurso").mockResolvedValue([
      {
        id: "tipo-1",
        nome: "Lanche",
        natureza: "consumivel",
        unidade: "unidade",
        exige_comprovante: false,
        valor_em_moedas: "1.00",
        vigencia_inicio: "2026-01-01",
      },
    ]);
  });

  it("apresenta o extrato do ponto de apoio", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarLancamentos").mockResolvedValue({
      itens: [CREDITO],
      proximo_cursor: null,
    });

    render(<ExtratoDoPontoDeApoio pontoDeApoio={PONTO_DO_EXTRATO} onVoltar={vi.fn()} />);

    expect(await screen.findByText(/credito/i)).toBeInTheDocument();
    expect(screen.getByText(/3\.00/)).toBeInTheDocument();
  });

  it("nenhum lançamento oferece caminho de edição ou de remoção", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarLancamentos").mockResolvedValue({
      itens: [CREDITO],
      proximo_cursor: null,
    });

    render(<ExtratoDoPontoDeApoio pontoDeApoio={PONTO_DO_EXTRATO} onVoltar={vi.fn()} />);
    await screen.findByText(/credito/i);

    expect(
      screen.queryByRole("button", { name: /editar|excluir|remover/i }),
    ).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: /ajustar/i })).toBeInTheDocument();
  });

  it("lança o ajuste referenciando o original, e o extrato o mostra", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarLancamentos")
      .mockResolvedValueOnce({ itens: [CREDITO], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [
          CREDITO,
          {
            id: "lancamento-2",
            natureza: "ajuste",
            tipo_de_recurso_id: "tipo-1",
            ponto_de_apoio_id: PONTO_DO_EXTRATO.id,
            quantidade: "-1.00",
            valor_em_moedas: "-1.00",
            lancamento_original_id: CREDITO.id,
            motivo_do_ajuste: "Corrige a maior.",
            lancamento_relacionado_id: null,
          },
        ],
        proximo_cursor: null,
      });
    const ajustar = vi.spyOn(pontosDeApoioApi, "lancarAjuste").mockResolvedValue({
      id: "lancamento-2",
      natureza: "ajuste",
      tipo_de_recurso_id: "tipo-1",
      ponto_de_apoio_id: PONTO_DO_EXTRATO.id,
      quantidade: "-1.00",
      valor_em_moedas: "-1.00",
      lancamento_original_id: CREDITO.id,
      motivo_do_ajuste: "Corrige a maior.",
      lancamento_relacionado_id: null,
    });

    render(<ExtratoDoPontoDeApoio pontoDeApoio={PONTO_DO_EXTRATO} onVoltar={vi.fn()} />);
    await screen.findByText(/credito/i);

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /ajustar/i }));
    await usuario.type(screen.getByLabelText(/quantidade do ajuste/i), "-1");
    await usuario.type(screen.getByLabelText(/valor em moedas do ajuste/i), "-1");
    await usuario.type(screen.getByLabelText(/^motivo$/i), "Corrige a maior.");
    await usuario.click(screen.getByRole("button", { name: /confirmar ajuste/i }));

    await waitFor(() =>
      expect(ajustar).toHaveBeenCalledWith(
        CREDITO.id,
        { quantidade: "-1", valor_em_moedas: "-1", motivo: "Corrige a maior." },
        "token-do-admin",
      ),
    );
    expect(await screen.findByText(/corrige a maior/i)).toBeInTheDocument();
  });

  it("motivo é obrigatório para o ajuste", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(pontosDeApoioApi, "listarLancamentos").mockResolvedValue({
      itens: [CREDITO],
      proximo_cursor: null,
    });
    const ajustar = vi.spyOn(pontosDeApoioApi, "lancarAjuste");

    render(<ExtratoDoPontoDeApoio pontoDeApoio={PONTO_DO_EXTRATO} onVoltar={vi.fn()} />);
    await screen.findByText(/credito/i);

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /ajustar/i }));
    await usuario.type(screen.getByLabelText(/quantidade do ajuste/i), "-1");
    await usuario.type(screen.getByLabelText(/valor em moedas do ajuste/i), "-1");
    await usuario.click(screen.getByRole("button", { name: /confirmar ajuste/i }));

    expect(await screen.findByText(/informe o motivo do ajuste/i)).toBeInTheDocument();
    expect(ajustar).not.toHaveBeenCalled();
  });

  it("filtra o extrato por período e por tipo de recurso", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    const listar = vi.spyOn(pontosDeApoioApi, "listarLancamentos").mockResolvedValue({
      itens: [CREDITO],
      proximo_cursor: null,
    });

    render(<ExtratoDoPontoDeApoio pontoDeApoio={PONTO_DO_EXTRATO} onVoltar={vi.fn()} />);
    await screen.findByText(/credito/i);

    const usuario = userEvent.setup();
    await usuario.selectOptions(await screen.findByLabelText(/tipo de recurso/i), "tipo-1");

    await waitFor(() =>
      expect(listar).toHaveBeenLastCalledWith(
        PONTO_DO_EXTRATO.id,
        "token-do-admin",
        expect.objectContaining({ tipoDeRecursoId: "tipo-1" }),
      ),
    );
  });
});

describe("designação do responsável pelo acervo (RF-07-49)", () => {
  const MESTRE = {
    id: "mestre-1",
    nome: "Mestre Um",
    email: "m@x.com",
    whatsapp: null,
    nick: null,
    artefatos: [],
  };
  const OUTRO_MESTRE = {
    id: "mestre-2",
    nome: "Mestre Dois",
    email: "m2@x.com",
    whatsapp: null,
    nick: null,
    artefatos: [],
  };

  it("Admin designa um Mestre, e a lista passa a apresentar o nome", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "listarMestres").mockResolvedValue({
      itens: [MESTRE],
      proximo_cursor: null,
    });
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio")
      .mockResolvedValueOnce({ itens: [PONTO_ATIVO], proximo_cursor: null })
      .mockResolvedValueOnce({
        itens: [{ ...PONTO_ATIVO, responsavel_id: MESTRE.id }],
        proximo_cursor: null,
      });
    const designar = vi.spyOn(pontosDeApoioApi, "designarResponsavel").mockResolvedValue({
      ...PONTO_ATIVO,
      responsavel_id: MESTRE.id,
    });

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /designar responsável/i }));
    await usuario.selectOptions(screen.getByLabelText(/responsável pelo acervo/i), MESTRE.id);
    await usuario.click(screen.getByRole("button", { name: /^confirmar$/i }));

    await waitFor(() =>
      expect(designar).toHaveBeenCalledWith(PONTO_ATIVO.id, MESTRE.id, "token-do-admin"),
    );
    expect(await screen.findByText("Mestre Um")).toBeInTheDocument();
  });

  it("a troca substitui o responsável anterior", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(personasApi, "listarMestres").mockResolvedValue({
      itens: [MESTRE, OUTRO_MESTRE],
      proximo_cursor: null,
    });
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio")
      .mockResolvedValueOnce({
        itens: [{ ...PONTO_ATIVO, responsavel_id: MESTRE.id }],
        proximo_cursor: null,
      })
      .mockResolvedValueOnce({
        itens: [{ ...PONTO_ATIVO, responsavel_id: OUTRO_MESTRE.id }],
        proximo_cursor: null,
      });
    vi.spyOn(pontosDeApoioApi, "designarResponsavel").mockResolvedValue({
      ...PONTO_ATIVO,
      responsavel_id: OUTRO_MESTRE.id,
    });

    render(<TelaDePontosDeApoio />);
    const usuario = userEvent.setup();

    expect(await screen.findByText("Mestre Um")).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /designar responsável/i }));
    await usuario.selectOptions(
      screen.getByLabelText(/responsável pelo acervo/i),
      OUTRO_MESTRE.id,
    );
    await usuario.click(screen.getByRole("button", { name: /^confirmar$/i }));

    expect(await screen.findByText("Mestre Dois")).toBeInTheDocument();
    expect(screen.queryByText("Mestre Um")).not.toBeInTheDocument();
  });

  it("Mestre não recebe o caminho da designação", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    vi.spyOn(comunidadesApi, "listarComunidades").mockResolvedValue({
      itens: [COMUNIDADE],
      proximo_cursor: null,
      ciclo_rotulo: "2026",
    });
    vi.spyOn(pontosDeApoioApi, "listarPontosDeApoio").mockResolvedValue({
      itens: [PONTO_ATIVO],
      proximo_cursor: null,
    });

    render(<TelaDePontosDeApoio />);

    await screen.findByText("Sede");
    expect(
      screen.queryByRole("button", { name: /designar responsável/i }),
    ).not.toBeInTheDocument();
  });
});
