import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import * as poderesApi from "../poderes/api";
import type { TipoDeColeta, TrilhaDoMestre } from "../trilhas/api";
import * as trilhasApi from "../trilhas/api";
import type { ComunidadeDaLista, LocalDaLista, SolicitacaoDeLocalDaLista } from "./api";
import * as territorioApi from "./api";
import { TelaDeTerritorio } from "./TelaDeTerritorio";

const COMUNIDADE: ComunidadeDaLista = { id: "comunidade-1", nome: "Comunidade de Teste" };
const OUTRA_COMUNIDADE: ComunidadeDaLista = { id: "comunidade-2", nome: "Outra Comunidade" };

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

const BAIRRO: LocalDaLista = {
  id: "local-bairro",
  comunidade_virtual_id: COMUNIDADE.id,
  nivel: "bairro",
  rotulo: "Bairro Central",
  local_pai_id: null,
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

const TIPO: TipoDeColeta = {
  id: "tipo-1",
  nome: "Temperatura",
  forma_de_registro: "numero",
  unidade: "°C",
  faixa_minima: -10,
  faixa_maxima: 55,
  ativo: true,
};

const TRILHA_COM_DESAFIO: TrilhaDoMestre = {
  id: "trilha-1",
  nome: "Robô Educa",
  objetivo: "Construir o próprio robô.",
  area_do_conhecimento: "Programação e Robótica",
  poder_id: "poder-1",
  situacao: "publicada",
  motivo_da_situacao: null,
  etiquetas_ods: [],
  cobertura_ods: { objetivos: [], ciclo: "Ciclo 01" },
  missoes: [
    {
      id: "missao-1",
      trilha_id: "trilha-1",
      titulo: "Primeira missão",
      posicao: 1,
      nivel_de_dificuldade: 1,
      obrigatoria: true,
      e_sondagem: false,
      etapa_do_ciclo: "abertura",
      cadencia_de_retomada: null,
      atividades: [],
      etiquetas_ods: [],
      desafios_de_coleta: [
        {
          id: "desafio-1",
          tipo_de_coleta_id: "tipo-1",
          cadencia: "semanal",
          vigencia_inicio: "2026-01-01T00:00:00-03:00",
          vigencia_fim: "2026-12-31T00:00:00-03:00",
          granularidade_exigida: "quadra",
          registros_que_pontuam_por_periodo: 1,
        },
      ],
    },
  ],
};

function grupo(solicitacoes: SolicitacaoDeLocalDaLista[], comunidade = COMUNIDADE) {
  return [{ comunidade, solicitacoes }];
}

// A leitura base que toda tela desta suíte precisa: trilhas do Mestre (para
// resolver o desafio de origem), o catálogo de tipos e a hierarquia de
// locais da comunidade com solicitação.
function configurarLeituraBase() {
  vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([TRILHA_COM_DESAFIO]);
  vi.spyOn(trilhasApi, "listarTiposDeColeta").mockResolvedValue([TIPO]);
  vi.spyOn(territorioApi, "listarTodosOsLocais").mockResolvedValue([BAIRRO]);
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("O Mestre avalia a solicitação de novo local (RF-09-53)", () => {
  it("aprova a solicitação informando o local pai", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      grupo([SOLICITACAO]),
    );
    vi.spyOn(territorioApi, "avaliarSolicitacaoDeLocal").mockResolvedValue({
      ...SOLICITACAO,
      situacao: "aprovada",
      local_criado_id: "local-novo",
    });

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    expect(await screen.findByText("Quadra Nova")).toBeInTheDocument();
    await usuario.selectOptions(
      screen.getByLabelText(/local pai \(para aprovar\)/i),
      BAIRRO.id,
    );
    await usuario.click(screen.getByRole("button", { name: /^aprovar$/i }));

    await waitFor(() =>
      expect(territorioApi.avaliarSolicitacaoDeLocal).toHaveBeenCalledWith(
        SOLICITACAO.id,
        { situacao: "aprovada", local_pai_id: BAIRRO.id },
        "token-do-mestre",
      ),
    );
  });

  it("a recusa exige o motivo antes de enviar", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      grupo([SOLICITACAO]),
    );
    const avaliarEspiado = vi.spyOn(territorioApi, "avaliarSolicitacaoDeLocal");

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await screen.findByText("Quadra Nova");
    await usuario.click(screen.getByRole("button", { name: /^recusar$/i }));

    expect(await screen.findByText(/informe o motivo da recusa/i)).toBeInTheDocument();
    expect(avaliarEspiado).not.toHaveBeenCalled();
  });

  it("a tela não alcança solicitação de trilha alheia", async () => {
    configurarSessao();
    configurarLeituraBase();
    // O núcleo já recorta pelas trilhas do Mestre (`listar_solicitacoes_de_
    // local_abertas`); simula a exclusão devolvendo nenhum grupo.
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      [],
    );

    render(<TelaDeTerritorio />);

    expect(
      await screen.findByText(/nenhuma solicitação de novo local em aberto/i),
    ).toBeInTheDocument();
    expect(screen.queryByText("Quadra Nova")).not.toBeInTheDocument();
  });

  it("a App 09 não cadastra local nem comunidade", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      grupo([SOLICITACAO]),
    );

    render(<TelaDeTerritorio />);

    await screen.findByText("Quadra Nova");
    expect(
      screen.queryByRole("button", { name: /novo local|cadastrar local/i }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /nova comunidade|criar comunidade/i }),
    ).not.toBeInTheDocument();
  });

  it("a hierarquia inválida vira mensagem simples, e a solicitação continua em aberto", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      grupo([SOLICITACAO]),
    );
    vi.spyOn(territorioApi, "avaliarSolicitacaoDeLocal").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "O local pai precisa ser do nível imediatamente acima.",
        campo: "local_pai_id",
      }),
    );

    render(<TelaDeTerritorio />);
    const usuario = userEvent.setup();

    await screen.findByText("Quadra Nova");
    await usuario.selectOptions(
      screen.getByLabelText(/local pai \(para aprovar\)/i),
      BAIRRO.id,
    );
    await usuario.click(screen.getByRole("button", { name: /^aprovar$/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/nível imediatamente acima/i);
    expect(recusa.textContent).not.toMatch(/erro_de_validacao/i);
    expect(screen.getByText("Quadra Nova")).toBeInTheDocument();
  });
});

describe("A App 09 alerta enquanto houver solicitação sem desfecho (RF-09-54)", () => {
  function configurarAutoriaVazia() {
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
  }

  it("o alerta aparece enquanto há pedido parado", async () => {
    configurarSessao();
    configurarLeituraBase();
    configurarAutoriaVazia();
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      grupo([SOLICITACAO]),
    );

    render(<App />);

    expect(
      await screen.findByText(/1 solicitação\(ões\) de novo local em aberto/i),
    ).toBeInTheDocument();
  });

  it("o alerta some quando a última é tratada", async () => {
    configurarSessao();
    configurarLeituraBase();
    configurarAutoriaVazia();
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades")
      .mockResolvedValueOnce(grupo([SOLICITACAO]))
      .mockResolvedValueOnce(grupo([SOLICITACAO]))
      .mockResolvedValue([]);
    vi.spyOn(territorioApi, "avaliarSolicitacaoDeLocal").mockResolvedValue({
      ...SOLICITACAO,
      situacao: "aprovada",
      local_criado_id: "local-novo",
    });

    render(<App />);
    const usuario = userEvent.setup();

    await screen.findByText(/1 solicitação\(ões\) de novo local em aberto/i);
    await usuario.click(screen.getByRole("button", { name: /^território/i }));
    await screen.findByText("Quadra Nova");
    await usuario.selectOptions(
      screen.getByLabelText(/local pai \(para aprovar\)/i),
      BAIRRO.id,
    );
    await usuario.click(screen.getByRole("button", { name: /^aprovar$/i }));

    await waitFor(() =>
      expect(
        screen.queryByText(/solicitação\(ões\) de novo local em aberto/i),
      ).not.toBeInTheDocument(),
    );
  });

  it("o alerta não depende de escolher comunidade", async () => {
    configurarSessao();
    configurarLeituraBase();
    configurarAutoriaVazia();
    // Só a segunda comunidade tem solicitação em aberto — o alerta alcança
    // as duas sem que o Mestre escolha nenhuma (`RN-01-42`).
    vi.spyOn(territorioApi, "listarSolicitacoesAbertasDeTodasAsComunidades").mockResolvedValue(
      grupo([SOLICITACAO], OUTRA_COMUNIDADE),
    );

    render(<App />);

    expect(screen.queryByLabelText(/^comunidade$/i)).not.toBeInTheDocument();
    expect(
      await screen.findByText(/1 solicitação\(ões\) de novo local em aberto/i),
    ).toBeInTheDocument();
  });
});
