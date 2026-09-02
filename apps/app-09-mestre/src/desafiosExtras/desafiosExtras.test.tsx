import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { TrilhaDoMestre } from "../trilhas/api";
import * as trilhasApi from "../trilhas/api";
import type { DesafioExtra } from "./api";
import * as desafiosApi from "./api";
import { TelaDeDesafiosExtras } from "./TelaDeDesafiosExtras";

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

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

const TRILHA_PROPRIA: TrilhaDoMestre = {
  id: "trilha-propria",
  nome: "Robô Educa",
  objetivo: "Construir o próprio robô.",
  area_do_conhecimento: "Programação e Robótica",
  poder_id: "poder-1",
  situacao: "publicada",
  motivo_da_situacao: null,
  etiquetas_ods: [],
  cobertura_ods: { objetivos: [], ciclo: "Ciclo 01" },
  missoes: [],
};

const DESAFIO_BASE: DesafioExtra = {
  id: "desafio-1",
  trilha_id: "trilha-alheia",
  missao_id: null,
  modalidade: "aberto",
  nick_do_destinatario: null,
  justificativa_do_vinculo: null,
  tipo_de_recurso_id: "tipo-1",
  ponto_de_apoio_id: "ponto-1",
  quantidade_disponivel: 5,
  quantidade_restante: 5,
  criterio_de_atribuicao: "Quem entregar primeiro.",
  pontos_extras: 5,
  formato: "on_line",
  custeio: "saldo_de_recurso",
  aporte_id: null,
  vigencia_inicio: "2026-01-01",
  vigencia_fim: "2026-12-31",
  situacao: "em_validacao_do_mestre",
  parecer_do_mestre: null,
  motivo_da_recusa: null,
  lastro_provido: true,
  lastro_faltante: null,
};

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

function configurarLeituraBase(
  sobrescreve: {
    fila?: DesafioExtra[];
    minhasTrilhas?: TrilhaDoMestre[];
    meusDesafios?: DesafioExtra[];
  } = {},
) {
  vi.spyOn(desafiosApi, "listarFilaDeValidacao").mockResolvedValue(sobrescreve.fila ?? []);
  vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue(
    sobrescreve.minhasTrilhas ?? [TRILHA_PROPRIA],
  );
  vi.spyOn(desafiosApi, "listarMeusDesafiosExtras").mockResolvedValue(
    sobrescreve.meusDesafios ?? [],
  );
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("fila de desafios extras a validar (RF-09-51, RN-09-11)", () => {
  it("a fila traz só o que há por validar", async () => {
    configurarSessao();
    configurarLeituraBase({ fila: [DESAFIO_BASE] });

    render(<TelaDeDesafiosExtras />);

    expect(await screen.findByText(/quem entregar primeiro/i)).toBeInTheDocument();
  });

  it("sem nada pendente, avisa sem erro", async () => {
    configurarSessao();
    configurarLeituraBase({ fila: [] });

    render(<TelaDeDesafiosExtras />);

    expect(
      await screen.findByText(/nenhum desafio extra esperando validação/i),
    ).toBeInTheDocument();
  });

  it("validar sem parecer é recusado, sem chamar a API", async () => {
    configurarSessao();
    configurarLeituraBase({ fila: [DESAFIO_BASE] });
    const validarEspiado = vi.spyOn(desafiosApi, "validarDesafioExtra");

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^validar$/i }));

    expect(await screen.findByText(/escreva o parecer/i)).toBeInTheDocument();
    expect(validarEspiado).not.toHaveBeenCalled();
  });

  it("validar com parecer manda o desafio para a aprovação do Admin e tira da fila", async () => {
    configurarSessao();
    configurarLeituraBase({ fila: [DESAFIO_BASE] });
    const validarEspiado = vi.spyOn(desafiosApi, "validarDesafioExtra").mockResolvedValue({
      ...DESAFIO_BASE,
      situacao: "em_aprovacao_do_admin",
      parecer_do_mestre: "Boa proposta.",
    });

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.type(await screen.findByLabelText(/^parecer$/i), "Boa proposta.");
    await usuario.click(screen.getByRole("button", { name: /^validar$/i }));

    await waitFor(() =>
      expect(validarEspiado).toHaveBeenCalledWith(
        "desafio-1",
        "Boa proposta.",
        "token-do-mestre",
      ),
    );
    expect(screen.queryByText(/quem entregar primeiro/i)).not.toBeInTheDocument();
  });

  it("recusar sem motivo é recusado, sem chamar a API", async () => {
    configurarSessao();
    configurarLeituraBase({ fila: [DESAFIO_BASE] });
    const recusarEspiado = vi.spyOn(desafiosApi, "recusarDesafioExtraPeloMestre");

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /^recusar$/i }));

    expect(await screen.findByText(/escreva o motivo/i)).toBeInTheDocument();
    expect(recusarEspiado).not.toHaveBeenCalled();
  });

  it("recusar com motivo tira o desafio da fila", async () => {
    configurarSessao();
    configurarLeituraBase({ fila: [DESAFIO_BASE] });
    const recusarEspiado = vi
      .spyOn(desafiosApi, "recusarDesafioExtraPeloMestre")
      .mockResolvedValue({
        ...DESAFIO_BASE,
        situacao: "recusado",
        motivo_da_recusa: "Sem mérito pedagógico.",
      });

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.type(
      await screen.findByLabelText(/motivo da recusa/i),
      "Sem mérito pedagógico.",
    );
    await usuario.click(screen.getByRole("button", { name: /^recusar$/i }));

    await waitFor(() =>
      expect(recusarEspiado).toHaveBeenCalledWith(
        "desafio-1",
        "Sem mérito pedagógico.",
        "token-do-mestre",
      ),
    );
    expect(screen.queryByText(/quem entregar primeiro/i)).not.toBeInTheDocument();
  });
});

describe("proposta de desafio extra pelo Mestre (RF-09-105 a RF-09-111, RN-09-40, RN-09-41)", () => {
  it("a tela recusa pontos extras acima do teto, sem chamar o núcleo", async () => {
    configurarSessao();
    configurarLeituraBase();
    const chamada = vi.spyOn(desafiosApi, "proporDesafioExtra");

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    const campoDePontos = await screen.findByLabelText(/pontos extras/i);
    await usuario.clear(campoDePontos);
    await usuario.type(campoDePontos, "11");
    await usuario.click(screen.getByRole("button", { name: /^propor desafio$/i }));

    expect(await screen.findByText(/teto é 10 pontos/i)).toBeInTheDocument();
    expect(chamada).not.toHaveBeenCalled();
  });

  it("direcionado sem justificativa pedagógica é recusado pelo núcleo, e a tela mostra o erro", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(desafiosApi, "proporDesafioExtra").mockRejectedValue(
      new ErroDaApi(422, {
        mensagem: "O direcionado exige a justificativa do vínculo.",
        codigo: "erro_de_validacao",
        campo: "justificativa_do_vinculo",
      }),
    );

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.selectOptions(await screen.findByLabelText(/^modalidade$/i), "direcionado");
    await usuario.type(screen.getByLabelText(/nick do destinatário/i), "nick-que-nao-existe");
    // A justificativa pedagógica fica em branco de propósito.
    await usuario.type(screen.getByLabelText(/^trilha$/i), "trilha-alheia");
    await usuario.type(screen.getByLabelText(/tipo de recurso/i), "tipo-1");
    await usuario.type(screen.getByLabelText(/ponto de apoio/i), "ponto-1");
    await usuario.type(
      screen.getByLabelText(/critério de atribuição/i),
      "Primeiro a entregar.",
    );
    await usuario.click(screen.getByRole("button", { name: /^propor desafio$/i }));

    expect(await screen.findByText(/exige a justificativa/i)).toBeInTheDocument();
  });

  it("na trilha própria a tela anuncia a dispensa da validação pedagógica", async () => {
    configurarSessao();
    configurarLeituraBase();

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.type(await screen.findByLabelText(/^trilha$/i), "trilha-propria");

    expect(await screen.findByText(/validação pedagógica é dispensada/i)).toBeInTheDocument();
  });

  it("na trilha alheia a tela anuncia a validação do Mestre autor", async () => {
    configurarSessao();
    configurarLeituraBase();

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.type(await screen.findByLabelText(/^trilha$/i), "trilha-alheia");

    expect(
      await screen.findByText(/passa antes pela validação do mestre autor/i),
    ).toBeInTheDocument();
    expect(screen.queryByText(/dispensada/i)).not.toBeInTheDocument();
  });

  it("proposta direcionada com nick desconhecido é aceita sem indicar que ele não existe", async () => {
    configurarSessao();
    configurarLeituraBase();
    vi.spyOn(desafiosApi, "proporDesafioExtra").mockResolvedValue({
      ...DESAFIO_BASE,
      modalidade: "direcionado",
      nick_do_destinatario: "nick-que-nao-existe",
    });

    render(<TelaDeDesafiosExtras />);
    const usuario = userEvent.setup();

    await usuario.type(await screen.findByLabelText(/^trilha$/i), "trilha-alheia");
    await usuario.type(screen.getByLabelText(/tipo de recurso/i), "tipo-1");
    await usuario.type(screen.getByLabelText(/ponto de apoio/i), "ponto-1");
    await usuario.type(
      screen.getByLabelText(/critério de atribuição/i),
      "Primeiro a entregar.",
    );
    await usuario.selectOptions(screen.getByLabelText(/^modalidade$/i), "direcionado");
    await usuario.type(screen.getByLabelText(/nick do destinatário/i), "nick-que-nao-existe");
    await usuario.type(
      screen.getByLabelText(/justificativa pedagógica/i),
      "Aluno com dificuldade em matemática.",
    );
    await usuario.click(screen.getByRole("button", { name: /^propor desafio$/i }));

    expect(await screen.findByText(/proposta registrada/i)).toBeInTheDocument();
    expect(screen.queryByText(/não existe/i)).not.toBeInTheDocument();
  });
});

describe("o que o Mestre propôs (RF-09-105, RF-09-112)", () => {
  it("mostra a situação e o motivo da recusa de cada proposta", async () => {
    configurarSessao();
    configurarLeituraBase({
      meusDesafios: [
        { ...DESAFIO_BASE, situacao: "recusado", motivo_da_recusa: "Sem mérito pedagógico." },
      ],
    });

    render(<TelaDeDesafiosExtras />);

    expect(await screen.findByText(/recusado/i)).toBeInTheDocument();
    expect(await screen.findByText(/sem mérito pedagógico/i)).toBeInTheDocument();
  });

  it("desafio publicado mostra a quantidade restante", async () => {
    configurarSessao();
    configurarLeituraBase({
      meusDesafios: [{ ...DESAFIO_BASE, situacao: "publicado", quantidade_restante: 3 }],
    });

    render(<TelaDeDesafiosExtras />);

    expect(await screen.findByText(/recompensas restantes: 3/i)).toBeInTheDocument();
  });

  it("nenhuma tela de desafio identifica Guerreiro(a) além do nick digitado", async () => {
    configurarSessao();
    configurarLeituraBase({
      meusDesafios: [
        {
          ...DESAFIO_BASE,
          modalidade: "direcionado",
          nick_do_destinatario: "nick-do-destino",
        },
      ],
    });

    render(<TelaDeDesafiosExtras />);
    await screen.findByText(/nick-do-destino/i);

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/telefone/i)).not.toBeInTheDocument();
  });
});
