import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { AtividadeDaMissao, EstruturaSugerida, MissaoDaTrilha } from "./api";
import * as trilhasApi from "./api";
import { TemplateDaMissao } from "./TemplateDaMissao";

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

function missao(sobrescreve: Partial<MissaoDaTrilha> = {}): MissaoDaTrilha {
  return {
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
    ...sobrescreve,
  };
}

function estrutura(sobrescreve: Partial<EstruturaSugerida> = {}): EstruturaSugerida {
  return {
    sugestao_id: "sugestao-1",
    disponivel: true,
    aviso: null,
    atividades: [
      {
        titulo: "Atividade sobre robótica",
        descricao: null,
        modalidade: "individual",
        formato: "presencial",
        natureza: "construcao",
        producao_esperada: "Uma produção própria sobre robótica.",
        desplugada: false,
      },
    ],
    objetivo_ods: 9,
    meta_ods: null,
    cadencia_de_retomada: [2, 7, 21],
    lacunas: ["Esta missão ainda não tem nenhuma atividade."],
    ...sobrescreve,
  };
}

function atividadeCriada(): AtividadeDaMissao {
  return {
    id: "atividade-1",
    missao_id: "missao-1",
    titulo: "Atividade sobre robótica",
    descricao: null,
    modalidade: "individual",
    formato: "presencial",
    natureza: "construcao",
    producao_esperada: "Uma produção própria sobre robótica.",
    aula_id: null,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("Template da missão", () => {
  it("envia o tópico e apresenta as lacunas em linguagem simples", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "pedirEstruturaDaMissao").mockResolvedValue(estrutura());

    render(<TemplateDaMissao missao={missao()} onAtualizada={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/o que você quer ensinar/i), "Robótica básica");
    await usuario.click(screen.getByRole("button", { name: /pedir estrutura sugerida/i }));

    await waitFor(() =>
      expect(trilhasApi.pedirEstruturaDaMissao).toHaveBeenCalledWith(
        "missao-1",
        "Robótica básica",
        "token-do-mestre",
      ),
    );
    expect(
      await screen.findByText(/esta missão ainda não tem nenhuma atividade/i),
    ).toBeInTheDocument();
    expect(screen.getAllByText("Proposta").length).toBeGreaterThan(0);
  });

  it("sugestão que não vem avisa em linguagem simples e não trava a autoria", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "pedirEstruturaDaMissao").mockResolvedValue(
      estrutura({
        disponivel: false,
        atividades: [],
        objetivo_ods: null,
        aviso:
          "A sugestão de estrutura não veio agora. Você pode seguir escrevendo a missão à mão.",
      }),
    );

    render(<TemplateDaMissao missao={missao()} onAtualizada={vi.fn()} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/o que você quer ensinar/i), "Robótica");
    await usuario.click(screen.getByRole("button", { name: /pedir estrutura sugerida/i }));

    expect(
      await screen.findByText(/você pode seguir escrevendo a missão à mão/i),
    ).toBeInTheDocument();
  });

  it("aceitar uma atividade grava só ela e registra o desfecho como aceita", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "pedirEstruturaDaMissao").mockResolvedValue(estrutura());
    vi.spyOn(trilhasApi, "criarAtividade").mockResolvedValue(atividadeCriada());
    vi.spyOn(trilhasApi, "registrarDesfechoDaSugestao").mockResolvedValue({
      id: "sugestao-1",
      situacao: "aceita",
    });
    const aoAtualizar = vi.fn();

    render(<TemplateDaMissao missao={missao()} onAtualizada={aoAtualizar} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/o que você quer ensinar/i), "Robótica");
    await usuario.click(screen.getByRole("button", { name: /pedir estrutura sugerida/i }));
    await usuario.click(
      await screen.findByRole("button", { name: /aceitar esta atividade/i }),
    );

    await waitFor(() =>
      expect(trilhasApi.criarAtividade).toHaveBeenCalledWith(
        "missao-1",
        expect.objectContaining({ titulo: "Atividade sobre robótica" }),
        "token-do-mestre",
      ),
    );
    expect(trilhasApi.registrarDesfechoDaSugestao).toHaveBeenCalledWith(
      "sugestao-1",
      "aceita",
      "token-do-mestre",
    );
    expect(aoAtualizar).toHaveBeenCalledWith(
      expect.objectContaining({ atividades: [atividadeCriada()] }),
    );
  });

  it("recusar a sugestão não grava nada na missão", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "pedirEstruturaDaMissao").mockResolvedValue(estrutura());
    const criarAtividadeEspiado = vi.spyOn(trilhasApi, "criarAtividade");
    vi.spyOn(trilhasApi, "registrarDesfechoDaSugestao").mockResolvedValue({
      id: "sugestao-1",
      situacao: "recusada",
    });
    const aoAtualizar = vi.fn();

    render(<TemplateDaMissao missao={missao()} onAtualizada={aoAtualizar} />);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/o que você quer ensinar/i), "Robótica");
    await usuario.click(screen.getByRole("button", { name: /pedir estrutura sugerida/i }));
    await usuario.click(await screen.findByRole("button", { name: /^recusar sugestão$/i }));

    await waitFor(() =>
      expect(trilhasApi.registrarDesfechoDaSugestao).toHaveBeenCalledWith(
        "sugestao-1",
        "recusada",
        "token-do-mestre",
      ),
    );
    expect(criarAtividadeEspiado).not.toHaveBeenCalled();
    expect(aoAtualizar).not.toHaveBeenCalled();
    expect(screen.queryByText("Proposta")).not.toBeInTheDocument();
  });
});
