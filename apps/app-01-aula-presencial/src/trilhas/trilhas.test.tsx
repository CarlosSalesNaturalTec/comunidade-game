import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { Equipe } from "../api/equipes";
import * as equipesApi from "../api/equipes";
import type { ProducaoDaMissao } from "../api/producao";
import * as producaoApi from "../api/producao";
import type { ItemDaProgramacao } from "../api/programacao";
import * as programacaoApi from "../api/programacao";
import { TelaDaProgramacao } from "./TelaDaProgramacao";

// Duplo da Web Speech API do navegador — o mesmo padrão de
// `assistente.test.tsx` e de `comum/fala/fala.test.ts` (`RF-05-76`,
// `RN-04-20`, `RN-05-32`).
class ReconhecimentoFalso {
  lang = "";
  continuous = true;
  interimResults = true;
  // biome-ignore lint/suspicious/noExplicitAny: espelha os eventos mínimos que comum/fala consome
  onresult: ((evento: any) => void) | null = null;
  // biome-ignore lint/suspicious/noExplicitAny: espelha os eventos mínimos que comum/fala consome
  onerror: ((evento: any) => void) | null = null;
  onend: (() => void) | null = null;
  parado = false;

  start() {}

  stop() {
    this.parado = true;
    this.onend?.();
  }
}

let reconhecimentoAtual: ReconhecimentoFalso | null = null;

function instalarReconhecimentoFalso() {
  reconhecimentoAtual = null;
  class Construtor extends ReconhecimentoFalso {
    constructor() {
      super();
      reconhecimentoAtual = this;
    }
  }
  vi.stubGlobal("SpeechRecognition", Construtor);
}

function item(sobrescreve: Partial<ItemDaProgramacao> = {}): ItemDaProgramacao {
  return {
    atividade: {
      id: "atividade-1",
      missao_id: "missao-1",
      titulo: "Montagem do robô",
      descricao: "Montar o chassi e conectar os sensores.",
      modalidade: "em_equipe",
      formato: "presencial",
      natureza: "construcao",
      producao_esperada: "Construir o próprio robô.",
      aula_id: "aula-1",
    },
    missao_id: "missao-1",
    missao_titulo: "Primeira missão",
    trilha_id: "trilha-1",
    trilha_titulo: "Trilha Um",
    conteudos: [
      {
        id: "conteudo-1",
        missao_id: "missao-1",
        ordem: 1,
        tipo: "texto",
        corpo: "Texto da missão.",
        endereco: null,
        referencia: null,
        tamanho: null,
        autoria: "propria",
        fonte: null,
      },
    ],
    bibliografia: [],
    corrente: false,
    ...sobrescreve,
  };
}

const SEGUNDA_ATIVIDADE: ItemDaProgramacao = item({
  atividade: {
    id: "atividade-2",
    missao_id: "missao-2",
    titulo: "Fórum de discussão",
    descricao: null,
    modalidade: "individual",
    formato: "presencial",
    natureza: "reflexao",
    producao_esperada: "Escrever uma reflexão.",
    aula_id: "aula-1",
  },
  missao_id: "missao-2",
  missao_titulo: "Segunda missão",
  conteudos: [],
});

function equipeDaTrilha(sobrescreve: Partial<Equipe> = {}): Equipe {
  return {
    id: "equipe-da-trilha-1",
    aula_id: null,
    trilha_id: "trilha-1",
    homologado_por_id: null,
    homologado_em: null,
    integrantes: [{ avatar: "avatar-1", nick: "zeferina", papel: null }],
    ...sobrescreve,
  };
}

function producao(sobrescreve: Partial<ProducaoDaMissao> = {}): ProducaoDaMissao {
  return {
    id: "producao-1",
    equipe_id: "equipe-1",
    guerreiro_id: null,
    missao_id: "missao-1",
    atividade_id: "atividade-1",
    forma: "texto",
    transcricao: "O que a equipe escreveu.",
    devolutiva: "Bom trabalho! Pensem no próximo passo.",
    registrado_em: "2026-08-30T12:00:00Z",
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.unstubAllGlobals();
});

describe("programação do encontro (RF-04-35, RF-02-42)", () => {
  it("única atividade é declarada ao núcleo sem escolha do Guerreiro(a)", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([item()]);
    const declarar = vi
      .spyOn(programacaoApi, "declararEscolhaDaEquipe")
      .mockResolvedValue({ equipe_id: "equipe-1", atividade_corrente_id: "atividade-1" });

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByText("Primeira missão")).toBeInTheDocument();
    expect(screen.getByText("Texto da missão.")).toBeInTheDocument();
    await waitFor(() =>
      expect(declarar).toHaveBeenCalledWith("equipe-1", "atividade-1", "token-guerreiro"),
    );
  });

  it("programação com duas atividades não é decidida pela aplicação", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([
      item(),
      SEGUNDA_ATIVIDADE,
    ]);
    const declarar = vi.spyOn(programacaoApi, "declararEscolhaDaEquipe");

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByRole("button", { name: /segunda missão/i })).toBeInTheDocument();
    expect(screen.queryByText("Primeira missão")).not.toBeInTheDocument();
    expect(screen.queryByText("Segunda missão")).not.toBeInTheDocument();
    expect(declarar).not.toHaveBeenCalled();
  });

  it("a equipe escolhe a atividade e o aparelho declara ao núcleo", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([
      item(),
      SEGUNDA_ATIVIDADE,
    ]);
    const declarar = vi
      .spyOn(programacaoApi, "declararEscolhaDaEquipe")
      .mockResolvedValue({ equipe_id: "equipe-1", atividade_corrente_id: "atividade-2" });

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByRole("button", { name: /segunda missão/i });

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /segunda missão/i }));

    expect(declarar).toHaveBeenCalledWith("equipe-1", "atividade-2", "token-guerreiro");
    expect(await screen.findByText("Segunda missão")).toBeInTheDocument();
  });

  it("a equipe troca de atividade no mesmo encontro", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([
      item({ corrente: true }),
      SEGUNDA_ATIVIDADE,
    ]);
    const declarar = vi
      .spyOn(programacaoApi, "declararEscolhaDaEquipe")
      .mockResolvedValue({ equipe_id: "equipe-1", atividade_corrente_id: "atividade-2" });

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /segunda missão/i }));

    expect(declarar).toHaveBeenCalledWith("equipe-1", "atividade-2", "token-guerreiro");
    expect(await screen.findByText("Segunda missão")).toBeInTheDocument();
    expect(screen.queryByText("Primeira missão")).not.toBeInTheDocument();
  });

  it("encontro sem programação avisa em linguagem simples", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([]);

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByText(/ainda não tem atividade declarada/i)).toBeInTheDocument();
  });

  it("o conteúdo de terceiro sai com a fonte", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([
      item({
        conteudos: [
          {
            id: "conteudo-2",
            missao_id: "missao-1",
            ordem: 1,
            tipo: "texto",
            corpo: "Trecho de terceiro.",
            endereco: null,
            referencia: null,
            tamanho: null,
            autoria: "terceiro",
            fonte: "Instituto Exemplo",
          },
        ],
      }),
    ]);
    vi.spyOn(programacaoApi, "declararEscolhaDaEquipe").mockResolvedValue({
      equipe_id: "equipe-1",
      atividade_corrente_id: "atividade-1",
    });

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByText(/fonte: instituto exemplo/i)).toBeInTheDocument();
  });

  it("nenhum dado pessoal de Guerreiro(a) aparece na tela", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([item()]);
    vi.spyOn(programacaoApi, "declararEscolhaDaEquipe").mockResolvedValue({
      equipe_id: "equipe-1",
      atividade_corrente_id: "atividade-1",
    });

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    expect(screen.queryByText(/nick|avatar/i)).not.toBeInTheDocument();
  });

  it("a rede cai e o conteúdo já carregado continua legível", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro")
      .mockResolvedValueOnce([item({ corrente: true })])
      .mockRejectedValueOnce(new Error("falha de rede"));
    vi.spyOn(programacaoApi, "declararEscolhaDaEquipe").mockResolvedValue({
      equipe_id: "equipe-1",
      atividade_corrente_id: "atividade-1",
    });

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /^atualizar$/i }));

    await waitFor(() =>
      expect(
        screen.getByText(/não foi possível atualizar a programação/i),
      ).toBeInTheDocument(),
    );
    expect(screen.getByText("Primeira missão")).toBeInTheDocument();
    expect(screen.getByText("Texto da missão.")).toBeInTheDocument();
  });

  it("sem rede, a escolha não é declarada nem enfileirada", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro")
      .mockResolvedValueOnce([item(), SEGUNDA_ATIVIDADE])
      .mockRejectedValueOnce(new Error("falha de rede"));
    const declarar = vi.spyOn(programacaoApi, "declararEscolhaDaEquipe");

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByRole("button", { name: /segunda missão/i });

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /^atualizar$/i }));
    await waitFor(() =>
      expect(
        screen.getByText(/não foi possível atualizar a programação/i),
      ).toBeInTheDocument(),
    );

    await usuario.click(screen.getByRole("button", { name: /segunda missão/i }));

    expect(declarar).not.toHaveBeenCalled();
    expect(screen.getByText(/escolha está indisponível sem rede/i)).toBeInTheDocument();
  });
});

function mockarAtividadeCorrente() {
  vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([item()]);
  vi.spyOn(programacaoApi, "declararEscolhaDaEquipe").mockResolvedValue({
    equipe_id: "equipe-1",
    atividade_corrente_id: "atividade-1",
  });
}

describe("equipe da trilha (RF-04-61, RN-01-44)", () => {
  it("a formação parte da atividade escolhida, sem pedir a trilha de novo", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    const criar = vi
      .spyOn(equipesApi, "criarEquipeDaTrilha")
      .mockResolvedValue(equipeDaTrilha());

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.click(
      await screen.findByRole("button", { name: /formar a equipe desta trilha/i }),
    );

    expect(criar).toHaveBeenCalledWith("trilha-1", null, "token-guerreiro");
    expect(await screen.findByText("zeferina")).toBeInTheDocument();
  });

  it("a segunda equipe da mesma trilha é recusada em linguagem simples", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    vi.spyOn(equipesApi, "criarEquipeDaTrilha").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este Guerreiro(a) já integra uma equipe desta trilha.",
      }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    const usuario = userEvent.setup();
    await usuario.click(
      await screen.findByRole("button", { name: /formar a equipe desta trilha/i }),
    );

    expect(await screen.findByText(/já integra uma equipe desta trilha/i)).toBeInTheDocument();
  });

  it("equipe homologada não oferece entrar nem sair", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockResolvedValue(
      equipeDaTrilha({ homologado_por_id: "mestre-1", homologado_em: "2026-08-30T10:00:00Z" }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByText(/composição fixa/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /sair desta equipe/i }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /formar a equipe desta trilha/i }),
    ).not.toBeInTheDocument();
  });

  it("o Mestre em sessão de trabalho homologa a equipe formada", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockResolvedValue(equipeDaTrilha());
    const homologar = vi.spyOn(equipesApi, "homologarEquipeDaTrilha").mockResolvedValue({
      equipe_id: "equipe-da-trilha-1",
      homologado_por_id: "mestre-1",
      homologado_em: "2026-08-30T10:00:00Z",
    });

    render(
      <TelaDaProgramacao
        equipeId="equipe-1"
        token="token-guerreiro"
        aoVoltar={vi.fn()}
        podeHomologarEquipeDaTrilha
        tokenDeTrabalho="token-mestre"
      />,
    );

    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /homologar esta equipe/i }));

    expect(homologar).toHaveBeenCalledWith("equipe-da-trilha-1", "token-mestre");
  });

  it("o Guerreiro(a) não vê a ação de homologar", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockResolvedValue(equipeDaTrilha());

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    await screen.findByText("zeferina");
    expect(screen.queryByRole("button", { name: /homologar/i })).not.toBeInTheDocument();
  });
});

describe("entrega da produção (RF-04-45 a RF-04-47, RN-04-09, RN-04-12, RN-04-20)", () => {
  it("entrega por texto e mostra a devolutiva dizendo que não vale ponto", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    const entregar = vi.spyOn(producaoApi, "entregarProducao").mockResolvedValue(producao());

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");
    expect(screen.getAllByText("Construir o próprio robô.").length).toBeGreaterThan(0);

    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/o que a equipe produziu/i), "Nossa produção.");
    await usuario.click(screen.getByRole("button", { name: /^entregar$/i }));

    expect(entregar).toHaveBeenCalledWith(
      "equipe-1",
      { forma: "texto", texto: "Nossa produção.", arquivo: undefined },
      "token-guerreiro",
    );
    expect(await screen.findByText(/bom trabalho/i)).toBeInTheDocument();
    expect(screen.getByText(/não vale ponto/i)).toBeInTheDocument();
  });

  it("entrega a foto do manuscrito", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    const entregar = vi
      .spyOn(producaoApi, "entregarProducao")
      .mockResolvedValue(producao({ forma: "foto" }));

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/como vocês querem entregar/i), "foto");
    const arquivo = new File(["conteudo"], "manuscrito.jpg", { type: "image/jpeg" });
    await usuario.upload(screen.getByLabelText(/foto do manuscrito/i), arquivo);
    await usuario.click(screen.getByRole("button", { name: /^entregar$/i }));

    await waitFor(() => expect(entregar).toHaveBeenCalled());
    expect(entregar.mock.calls[0][1].forma).toBe("foto");
    expect(entregar.mock.calls[0][1].arquivo).toBe(arquivo);
  });

  it("devolutiva que não veio no texto confirma a entrega sem perder o que a equipe escreveu", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    vi.spyOn(producaoApi, "entregarProducao").mockResolvedValue(
      producao({ devolutiva: null }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/o que a equipe produziu/i), "Nossa produção.");
    await usuario.click(screen.getByRole("button", { name: /^entregar$/i }));

    expect(await screen.findByText(/o retorno não veio desta vez/i)).toBeInTheDocument();
    expect(screen.queryByText(/não deu para ler a foto agora/i)).not.toBeInTheDocument();
  });

  it("leitura indisponível na foto pede reenvio, sem dizer que a produção se perdeu", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    vi.spyOn(producaoApi, "entregarProducao").mockRejectedValue(
      new ErroDaApi(503, {
        codigo: "leitura_da_producao_indisponivel",
        mensagem: "A leitura da produção não veio agora.",
      }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/como vocês querem entregar/i), "foto");
    const arquivo = new File(["conteudo"], "manuscrito.jpg", { type: "image/jpeg" });
    await usuario.upload(screen.getByLabelText(/foto do manuscrito/i), arquivo);
    await usuario.click(screen.getByRole("button", { name: /^entregar$/i }));

    expect(await screen.findByText(/não deu para ler a foto agora/i)).toBeInTheDocument();
    expect(screen.queryByText(/perdid/i)).not.toBeInTheDocument();
  });

  it("a entrega por texto é sempre oferecida, mesmo sem tocar câmera nem microfone", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    const entregar = vi.spyOn(producaoApi, "entregarProducao").mockResolvedValue(producao());

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    expect(screen.getByLabelText(/como vocês querem entregar/i)).toHaveValue("texto");
    const usuario = userEvent.setup();
    await usuario.type(
      screen.getByLabelText(/o que a equipe produziu/i),
      "Produção por texto.",
    );
    await usuario.click(screen.getByRole("button", { name: /^entregar$/i }));

    await waitFor(() => expect(entregar).toHaveBeenCalled());
  });

  it("a fala transcrita no aparelho segue como texto, com a forma áudio", async () => {
    instalarReconhecimentoFalso();
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    const entregar = vi
      .spyOn(producaoApi, "entregarProducao")
      .mockResolvedValue(producao({ forma: "audio" }));

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/como vocês querem entregar/i), "audio");
    await usuario.click(screen.getByRole("button", { name: /falar a produção/i }));
    expect(await screen.findByText(/ouvindo/i)).toBeInTheDocument();

    reconhecimentoAtual?.onresult?.({
      results: { 0: { 0: { transcript: "o que a equipe falou" } } },
    });
    reconhecimentoAtual?.onend?.();

    expect(await screen.findByLabelText(/o que a equipe falou/i)).toHaveValue(
      "o que a equipe falou",
    );

    // A transcrição é editável antes do envio, e é o texto corrigido que
    // segue ao núcleo (documento 09 §1, decisão de 2026-09-10).
    await usuario.clear(screen.getByLabelText(/o que a equipe falou/i));
    await usuario.type(
      screen.getByLabelText(/o que a equipe falou/i),
      "o que a equipe falou, corrigido",
    );
    await usuario.click(screen.getByRole("button", { name: /^entregar$/i }));

    await waitFor(() => expect(entregar).toHaveBeenCalled());
    expect(entregar).toHaveBeenCalledWith(
      "equipe-1",
      { forma: "audio", texto: "o que a equipe falou, corrigido", arquivo: undefined },
      "token-guerreiro",
    );
  });

  it("quando a fala não é entendida, avisa sem apagar o que já estava escrito", async () => {
    instalarReconhecimentoFalso();
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/como vocês querem entregar/i), "audio");
    await usuario.type(
      screen.getByLabelText(/o que a equipe falou/i),
      "texto que não deve sumir",
    );
    await usuario.click(screen.getByRole("button", { name: /falar a produção/i }));

    reconhecimentoAtual?.onerror?.({ error: "no-speech" });
    reconhecimentoAtual?.onend?.();

    expect(await screen.findByText(/não foi possível entender a fala/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/o que a equipe falou/i)).toHaveValue(
      "texto que não deve sumir",
    );
  });

  it("sem toque no botão de falar, nenhum microfone é aberto", async () => {
    instalarReconhecimentoFalso();
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.selectOptions(screen.getByLabelText(/como vocês querem entregar/i), "audio");

    expect(reconhecimentoAtual).toBeNull();
  });

  it("sem transcrição no aparelho, a fala não é oferecida e a tela o diz", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    expect(screen.getByRole("option", { name: "Texto" })).toBeInTheDocument();
    expect(screen.getByRole("option", { name: /foto do que fizeram/i })).toBeInTheDocument();
    expect(screen.queryByRole("option", { name: "Fala" })).not.toBeInTheDocument();
    expect(screen.getByText(/não transcreve fala/i)).toBeInTheDocument();
  });
});
