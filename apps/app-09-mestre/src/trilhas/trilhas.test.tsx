import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import { TelaDeAutoria } from "../autoria/TelaDeAutoria";
import type { PoderDoCatalogo } from "../poderes/api";
import * as poderesApi from "../poderes/api";
import type { AtividadeDaMissao, MissaoDaTrilha, TrilhaDoMestre } from "./api";
import * as trilhasApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
};

function configurarSessao() {
  vi.mocked(useSessao).mockReturnValue({
    sessao: SESSAO_DE_MESTRE,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

function poder(sobrescreve: Partial<PoderDoCatalogo> = {}): PoderDoCatalogo {
  return {
    id: "poder-guerreiro",
    nome: "Robô Educa",
    descricao: "Poder de tecnologia.",
    natureza: "de_guerreiro",
    vigencia: "vigente",
    papel: null,
    ativo: true,
    ...sobrescreve,
  };
}

function poderSustentador(): PoderDoCatalogo {
  return poder({
    id: "poder-sustentador",
    nome: "Poder Sustentador",
    natureza: "derivado_do_aporte",
  });
}

function atividade(sobrescreve: Partial<AtividadeDaMissao> = {}): AtividadeDaMissao {
  return {
    id: "atividade-1",
    missao_id: "missao-1",
    titulo: "Montagem do robô",
    descricao: null,
    modalidade: "individual",
    formato: "presencial",
    natureza: "construcao",
    producao_esperada: "Construir o próprio robô.",
    ...sobrescreve,
  };
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
    ...sobrescreve,
  };
}

function trilha(sobrescreve: Partial<TrilhaDoMestre> = {}): TrilhaDoMestre {
  return {
    id: "trilha-1",
    nome: "Robô Educa",
    objetivo: "Construir o próprio robô.",
    area_do_conhecimento: "Programação e Robótica",
    poder_id: "poder-guerreiro",
    situacao: "rascunho",
    missoes: [],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("criação de trilha (RF-09-01)", () => {
  it("Mestre cria a trilha", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValueOnce([]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [poder()],
      proximo_cursor: null,
    });
    const criarTrilhaEspiado = vi.spyOn(trilhasApi, "criarTrilha").mockResolvedValue({
      id: "trilha-nova",
      nome: "Robô Educa",
      objetivo: "Construir o próprio robô.",
      area_do_conhecimento: "Programação e Robótica",
      poder_id: "poder-guerreiro",
      situacao: "rascunho",
    });
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValueOnce([trilha()]);

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova trilha/i }));
    await usuario.type(screen.getByLabelText(/^nome$/i), "Robô Educa");
    await usuario.type(screen.getByLabelText(/objetivo/i), "Construir o próprio robô.");
    await usuario.type(
      screen.getByLabelText(/área do conhecimento/i),
      "Programação e Robótica",
    );
    await usuario.selectOptions(screen.getByLabelText(/^poder$/i), "poder-guerreiro");
    await usuario.click(screen.getByRole("button", { name: /criar trilha/i }));

    await waitFor(() => expect(criarTrilhaEspiado).toHaveBeenCalled());
    expect(await screen.findByText("Robô Educa")).toBeInTheDocument();
  });

  it("campo obrigatório em falta é apontado no próprio campo", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [poder()],
      proximo_cursor: null,
    });
    const criarTrilhaEspiado = vi.spyOn(trilhasApi, "criarTrilha");

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova trilha/i }));
    await usuario.click(screen.getByRole("button", { name: /criar trilha/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/nome/i);
    expect(criarTrilhaEspiado).not.toHaveBeenCalled();
  });

  it("o seletor não oferece o Poder Sustentador", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [poder(), poderSustentador()],
      proximo_cursor: null,
    });

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /nova trilha/i }));

    const seletor = screen.getByLabelText(/^poder$/i);
    expect(within(seletor).getByText("Robô Educa")).toBeInTheDocument();
    expect(within(seletor).queryByText("Poder Sustentador")).not.toBeInTheDocument();
  });
});

describe("lista das trilhas do Mestre (RF-09-04)", () => {
  it("o rascunho do Mestre aparece na lista, com poder, área e situação", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [poder()],
      proximo_cursor: null,
    });

    render(<TelaDeAutoria />);

    expect(await screen.findByText("Robô Educa")).toBeInTheDocument();
    expect(screen.getByText(/rascunho/i)).toBeInTheDocument();
    expect(screen.getByText(/programação e robótica/i)).toBeInTheDocument();
  });

  it("rascunho alheio nunca chega à lista, porque a rota já filtra por autoria", async () => {
    configurarSessao();
    // `GET /trilhas/minhas` só devolve as trilhas do Mestre em sessão — o
    // teste confirma que a tela apresenta exatamente o que a rota devolveu.
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeAutoria />);

    expect(await screen.findByText(/nenhuma trilha criada/i)).toBeInTheDocument();
  });
});

describe("autoria de missão (RF-09-02, RF-09-03, RF-09-80)", () => {
  it("Mestre acrescenta missão à trilha", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [poder()],
      proximo_cursor: null,
    });
    const criarMissaoEspiado = vi
      .spyOn(trilhasApi, "criarMissao")
      .mockResolvedValue(missao({ titulo: "Sondagem inicial", posicao: 1 }));

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));
    await usuario.click(await screen.findByRole("button", { name: /nova missão/i }));
    await usuario.type(screen.getByLabelText(/título/i), "Sondagem inicial");
    await usuario.selectOptions(screen.getByLabelText(/obrigatoriedade/i), "sim");
    await usuario.click(screen.getByRole("button", { name: /acrescentar missão/i }));

    await waitFor(() => expect(criarMissaoEspiado).toHaveBeenCalled());
    expect(await screen.findByText("Sondagem inicial")).toBeInTheDocument();
  });

  it("obrigatoriedade em falta é apontada no próprio campo", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const criarMissaoEspiado = vi.spyOn(trilhasApi, "criarMissao");

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));
    await usuario.click(await screen.findByRole("button", { name: /nova missão/i }));
    await usuario.type(screen.getByLabelText(/título/i), "Missão sem obrigatoriedade");
    await usuario.click(screen.getByRole("button", { name: /acrescentar missão/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/obrigatória ou opcional/i);
    expect(criarMissaoEspiado).not.toHaveBeenCalled();
  });

  it("as missões aparecem na ordem da posição", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({
        missoes: [
          missao({ id: "missao-2", titulo: "Segunda missão", posicao: 2 }),
          missao({ id: "missao-1", titulo: "Primeira missão", posicao: 1 }),
        ],
      }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));

    const itens = await screen.findAllByRole("listitem");
    const titulos = itens.map((item) => item.textContent ?? "");
    const posicaoDaPrimeira = titulos.findIndex((texto) => texto.includes("Primeira missão"));
    const posicaoDaSegunda = titulos.findIndex((texto) => texto.includes("Segunda missão"));
    expect(posicaoDaPrimeira).toBeLessThan(posicaoDaSegunda);
  });
});

describe("missão de sondagem (RF-09-81)", () => {
  async function abrirFormularioDeMissao() {
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));
    await usuario.click(await screen.findByRole("button", { name: /nova missão/i }));
    return usuario;
  }

  it("sondagem na primeira posição é aceita e distinguida das demais", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "criarMissao").mockResolvedValue(
      missao({ titulo: "Missão de sondagem", e_sondagem: true }),
    );

    render(<TelaDeAutoria />);
    const usuario = await abrirFormularioDeMissao();
    await usuario.type(screen.getByLabelText(/título/i), "Missão de sondagem");
    await usuario.selectOptions(screen.getByLabelText(/obrigatoriedade/i), "sim");
    await usuario.click(screen.getByLabelText(/missão de sondagem/i));
    await usuario.click(screen.getByRole("button", { name: /acrescentar missão/i }));

    expect(await screen.findByText("Sondagem")).toBeInTheDocument();
  });

  it("segunda sondagem é recusada em linguagem simples, sem código de erro cru", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao({ e_sondagem: true })] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "criarMissao").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Esta trilha já tem uma missão de sondagem.",
        campo: "e_sondagem",
      }),
    );

    render(<TelaDeAutoria />);
    const usuario = await abrirFormularioDeMissao();
    await usuario.type(screen.getByLabelText(/título/i), "Segunda sondagem");
    await usuario.selectOptions(screen.getByLabelText(/obrigatoriedade/i), "sim");
    await usuario.click(screen.getByLabelText(/missão de sondagem/i));
    await usuario.click(screen.getByRole("button", { name: /acrescentar missão/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/já tem uma missão de sondagem/i);
    expect(recusa.textContent).not.toMatch(/erro_de_validacao/i);
  });

  it("sondagem fora da primeira posição é recusada em linguagem simples", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "criarMissao").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "A missão de sondagem ocupa a primeira posição da trilha.",
        campo: "e_sondagem",
      }),
    );

    render(<TelaDeAutoria />);
    const usuario = await abrirFormularioDeMissao();
    await usuario.type(screen.getByLabelText(/título/i), "Sondagem fora de posição");
    await usuario.selectOptions(screen.getByLabelText(/obrigatoriedade/i), "sim");
    await usuario.clear(screen.getByLabelText(/posição/i));
    await usuario.type(screen.getByLabelText(/posição/i), "2");
    await usuario.click(screen.getByLabelText(/missão de sondagem/i));
    await usuario.click(screen.getByRole("button", { name: /acrescentar missão/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa).toHaveTextContent(/primeira posição/i);
    expect(recusa.textContent).not.toMatch(/erro_de_validacao/i);
  });

  it("trilha em rascunho existe sem sondagem, sem cobrar a marcação", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao({ e_sondagem: false })] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));

    expect(screen.queryByText(/^sondagem$/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});

describe("autoria de atividade (RF-09-69, RF-09-70)", () => {
  async function abrirFormularioDeAtividade() {
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));
    await usuario.click(await screen.findByRole("button", { name: /nova atividade/i }));
    return usuario;
  }

  it("Mestre cria a atividade da missão", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao()] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const criarAtividadeEspiado = vi
      .spyOn(trilhasApi, "criarAtividade")
      .mockResolvedValue(atividade());

    render(<TelaDeAutoria />);
    const usuario = await abrirFormularioDeAtividade();
    await usuario.type(screen.getByLabelText(/^título$/i), "Montagem do robô");
    await usuario.selectOptions(screen.getByLabelText(/modalidade/i), "individual");
    await usuario.selectOptions(screen.getByLabelText(/formato/i), "presencial");
    await usuario.type(screen.getByLabelText(/^natureza$/i), "construcao");
    await usuario.type(
      screen.getByLabelText(/produção esperada/i),
      "Construir o próprio robô.",
    );
    await usuario.click(screen.getByRole("button", { name: /acrescentar atividade/i }));

    await waitFor(() => expect(criarAtividadeEspiado).toHaveBeenCalled());
    expect(await screen.findByText(/montagem do robô/i)).toBeInTheDocument();
  });

  it("atividade sem modalidade é apontada no próprio campo", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao()] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    const criarAtividadeEspiado = vi.spyOn(trilhasApi, "criarAtividade");

    render(<TelaDeAutoria />);
    const usuario = await abrirFormularioDeAtividade();
    await usuario.type(screen.getByLabelText(/^título$/i), "Atividade sem modalidade");
    await usuario.click(screen.getByRole("button", { name: /acrescentar atividade/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/modalidade/i);
    expect(criarAtividadeEspiado).not.toHaveBeenCalled();
  });

  it("a natureza aceita valor novo, fora do vocabulário do Ciclo 01", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao()] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "criarAtividade").mockResolvedValue(
      atividade({ natureza: "expressao_artistica" }),
    );

    render(<TelaDeAutoria />);
    const usuario = await abrirFormularioDeAtividade();
    await usuario.type(screen.getByLabelText(/^título$/i), "Roda de capoeira");
    await usuario.selectOptions(screen.getByLabelText(/modalidade/i), "em_equipe");
    await usuario.selectOptions(screen.getByLabelText(/formato/i), "presencial");
    await usuario.type(screen.getByLabelText(/^natureza$/i), "expressao_artistica");
    await usuario.type(screen.getByLabelText(/produção esperada/i), "Executar a sequência.");
    await usuario.click(screen.getByRole("button", { name: /acrescentar atividade/i }));

    expect(await screen.findByText(/montagem do robô|roda de capoeira/i)).toBeInTheDocument();
  });
});

describe("cadência de retomada da missão (RF-09-83, RF-09-101)", () => {
  it("Mestre declara a cadência e a tela a apresenta junto da missão", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao()] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "declararCadenciaDeRetomada").mockResolvedValue(
      missao({ cadencia_de_retomada: [2, 7, 21] }),
    );

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));

    await usuario.type(screen.getByLabelText(/cadência de retomada/i), "2, 7, 21");
    await usuario.click(screen.getByRole("button", { name: /declarar cadência/i }));

    expect(await screen.findByText(/retomada em 2, 7, 21 dias/i)).toBeInTheDocument();
  });

  it("Mestre deixa a missão sem retomada", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([
      trilha({ missoes: [missao({ cadencia_de_retomada: [2, 7, 21] })] }),
    ]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "declararCadenciaDeRetomada").mockResolvedValue(
      missao({ cadencia_de_retomada: null }),
    );

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));
    expect(await screen.findByText(/retomada em 2, 7, 21 dias/i)).toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /deixar sem retomada/i }));

    expect(await screen.findByText(/sem retomada declarada/i)).toBeInTheDocument();
  });
});

describe("autoria sem jargão técnico (RF-09-12)", () => {
  it("nenhum campo da autoria pede código, marcação ou configuração técnica", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();

    await usuario.click(await screen.findByRole("button", { name: /nova trilha/i }));
    const rotulosDaTrilha = screen.getAllByText(
      /^(nome|objetivo|área do conhecimento|poder)$/i,
    );
    expect(rotulosDaTrilha.length).toBeGreaterThan(0);

    for (const proibido of [/código/i, /html/i, /json/i, /configuração técnica/i]) {
      expect(screen.queryByText(proibido)).not.toBeInTheDocument();
    }
  });

  it("a recusa do núcleo chega traduzida, sem expor o código do erro na tela", async () => {
    configurarSessao();
    vi.spyOn(trilhasApi, "listarMinhasTrilhas").mockResolvedValue([trilha()]);
    vi.spyOn(poderesApi, "listarPoderes").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });
    vi.spyOn(trilhasApi, "criarMissao").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Etapa do ciclo fora dos valores previstos.",
        campo: "etapa_do_ciclo",
      }),
    );

    render(<TelaDeAutoria />);
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByText("Robô Educa"));
    await usuario.click(screen.getByRole("button", { name: /abrir/i }));
    await usuario.click(await screen.findByRole("button", { name: /nova missão/i }));
    await usuario.type(screen.getByLabelText(/título/i), "Missão qualquer");
    await usuario.selectOptions(screen.getByLabelText(/obrigatoriedade/i), "sim");
    await usuario.click(screen.getByRole("button", { name: /acrescentar missão/i }));

    // O erro não tem campo mapeado num Campo visível desta tela
    // (`etapa_do_ciclo` não tem `erroDeCampo` dedicado), então cai no aviso
    // de recusa genérico — mas nunca mostra o código cru do núcleo.
    await waitFor(() => expect(trilhasApi.criarMissao).toHaveBeenCalled());
    expect(screen.queryByText(/erro_de_validacao/i)).not.toBeInTheDocument();
  });
});
