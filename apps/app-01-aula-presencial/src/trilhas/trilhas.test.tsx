import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { escreverAvatar } from "comum/avatar";
import * as trilhaApi from "comum/trilha/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { Equipe, MinhaEquipe } from "../api/equipes";
import * as equipesApi from "../api/equipes";
import type { ProducaoDaMissao } from "../api/producao";
import * as producaoApi from "../api/producao";
import type { ItemDaProgramacao } from "../api/programacao";
import * as programacaoApi from "../api/programacao";
import { ProvedorDeEstadoDeRede } from "../sessao-de-trabalho/EstadoDeRede";
import { TelaDaProgramacao } from "./TelaDaProgramacao";
import { TelaDeTrilhasDoGuerreiro } from "./TelaDeTrilhasDoGuerreiro";

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
    nome: "Onças",
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
    await usuario.type(await screen.findByLabelText("Nome da equipe"), "Onças");
    await usuario.click(screen.getByRole("button", { name: /formar a equipe desta trilha/i }));

    expect(criar).toHaveBeenCalledWith("trilha-1", "Onças", null, "token-guerreiro");
    expect(await screen.findByText("zeferina")).toBeInTheDocument();
    expect(screen.getByText("Onças")).toBeInTheDocument();
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
    await usuario.type(await screen.findByLabelText("Nome da equipe"), "Onças");
    await usuario.click(screen.getByRole("button", { name: /formar a equipe desta trilha/i }));

    expect(await screen.findByText(/já integra uma equipe desta trilha/i)).toBeInTheDocument();
  });

  it("sem nome, a formação da equipe da trilha não sai do aparelho (RF-04-69)", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    const criar = vi.spyOn(equipesApi, "criarEquipeDaTrilha");

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(
      await screen.findByRole("button", { name: /formar a equipe desta trilha/i }),
    ).toBeDisabled();
    expect(screen.getByLabelText("Nome da equipe")).toHaveAttribute("maxlength", "20");
    expect(criar).not.toHaveBeenCalled();
  });

  it("nome repetido na trilha é recusado em linguagem simples (RN-04-39)", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );
    vi.spyOn(equipesApi, "criarEquipeDaTrilha").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Já existe uma equipe com esse nome nesta trilha. Escolham outro.",
      }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText("Nome da equipe"), "Onças");
    await usuario.click(screen.getByRole("button", { name: /formar a equipe desta trilha/i }));

    expect(await screen.findByText(/já existe uma equipe com esse nome/i)).toBeInTheDocument();
  });

  it("a integrante renomeia a equipe da trilha ainda não homologada (RF-04-70)", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockResolvedValue(equipeDaTrilha());
    const renomear = vi
      .spyOn(equipesApi, "renomearEquipe")
      .mockResolvedValue(equipeDaTrilha({ nome: "Tatus" }));

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /trocar o nome/i }));
    const campo = screen.getByLabelText("Novo nome da equipe");
    await usuario.clear(campo);
    await usuario.type(campo, "Tatus");
    await usuario.click(screen.getByRole("button", { name: /salvar o nome/i }));

    expect(renomear).toHaveBeenCalledWith("equipe-da-trilha-1", "Tatus", "token-guerreiro");
    expect(await screen.findByText("Tatus")).toBeInTheDocument();
  });

  it("a formação da equipe da trilha abre com o nome da equipe focado (RF-04-61)", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrada"),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    const campo = await screen.findByLabelText("Nome da equipe");

    expect(document.activeElement).toBe(campo);
    expect(document.activeElement).not.toBe(screen.getByLabelText(/seu papel na equipe/i));
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
    expect(screen.queryByRole("button", { name: /trocar o nome/i })).not.toBeInTheDocument();
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

describe("o avatar dos integrantes da equipe da trilha (`RF-04-34`, documento 15 §7)", () => {
  it("o avatar aparece desenhado ao lado do nick, nunca em texto", async () => {
    mockarAtividadeCorrente();
    const avatar = JSON.stringify({
      formaDeTratamento: "guerreira",
      avatar: escreverAvatar({ cabelo: "dreads", tom: "t2", acessorio: "oculos" }),
    });
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockResolvedValue(
      equipeDaTrilha({ integrantes: [{ avatar, nick: "zeferina", papel: "relatora" }] }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    const linha = (await screen.findByText(/zeferina/)).closest("li");
    expect(linha).not.toBeNull();
    // biome-ignore lint/style/noNonNullAssertion: verificado na linha acima
    expect(linha!.querySelectorAll("svg.cg-avatar > g[data-camada]")).toHaveLength(9);
    // biome-ignore lint/style/noNonNullAssertion: verificado acima
    expect(linha!.textContent).not.toMatch(/dreads|formaDeTratamento|\{/);
  });

  it("avatar que falta cai no padrão do projeto, na mesma moldura", async () => {
    mockarAtividadeCorrente();
    vi.spyOn(equipesApi, "obterMinhaEquipeDaTrilha").mockResolvedValue(
      equipeDaTrilha({
        integrantes: [
          { avatar: null, nick: "sem-avatar", papel: null },
          {
            avatar: JSON.stringify({ caracteristicasDoAvatar: "trança-e-capa" }),
            nick: "do-texto-livre",
            papel: null,
          },
        ],
      }),
    );

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    const lista = (await screen.findByText("sem-avatar")).closest("ul");
    expect(lista).not.toBeNull();
    // biome-ignore lint/style/noNonNullAssertion: verificado na linha acima
    const desenhos = lista!.querySelectorAll("svg.cg-avatar");
    expect(desenhos).toHaveLength(2);
    expect(desenhos[0].outerHTML).toBe(desenhos[1].outerHTML);
  });
});

// --- O caminho das trilhas e missões no aparelho do encontro
// (`RF-04-72`, `RF-04-73`, `RF-04-74`, `RF-04-35`)

const CHAVE_DE_SESSAO_DO_PERCURSO = "teste:app-01:percurso";

function trilhaInscrita(
  sobrescreve: Partial<trilhaApi.TrilhaComProximaMissao> = {},
): trilhaApi.TrilhaComProximaMissao {
  return {
    id: "trilha-1",
    nome: "Robô Educa",
    poder_id: "poder-1",
    proxima_missao_id: "missao-1",
    proxima_missao_titulo: "Primeira Missão",
    proxima_missao_posicao: 1,
    ...sobrescreve,
  };
}

function missaoNoPercurso(
  sobrescreve: Partial<trilhaApi.MissaoNoPercurso> = {},
): trilhaApi.MissaoNoPercurso {
  return {
    id: "missao-1",
    titulo: "Primeira Missão",
    posicao: 1,
    obrigatoria: true,
    e_sondagem: false,
    desbloqueada: false,
    e_proxima: true,
    aguardando_mestre: false,
    motivo_do_bloqueio: null,
    desafio_de_desbloqueio: null,
    ...sobrescreve,
  };
}

const QUIZ_DO_DESBLOQUEIO: trilhaApi.DesafioDeDesbloqueio = {
  tipo: "quiz",
  enunciado: null,
  perguntas: [
    {
      id: "p1",
      ordem: 1,
      enunciado: "Quanto é 1 + 1?",
      alternativas: ["1", "2", "3", "4"],
      imagem_referencia: null,
    },
  ],
};

function trilhaPublicaComMissao(
  atividades: trilhaApi.AtividadeDaMissaoPublica[] = [],
): trilhaApi.TrilhaPublicaComMissoes {
  return {
    id: "trilha-1",
    nome: "Robô Educa",
    licenca: "CC BY-SA",
    autor_nome: "Mestre Ana",
    culminancia: null,
    missoes: [
      {
        id: "missao-1",
        titulo: "Primeira Missão",
        posicao: 1,
        obrigatoria: true,
        e_sondagem: false,
        atividades,
        conteudos: [],
        bibliografia: [],
      },
    ],
  };
}

function minhaEquipe(sobrescreve: Partial<MinhaEquipe> = {}): MinhaEquipe {
  return {
    id: "equipe-1",
    nome: "Os Robôs",
    aula_id: "aula-1",
    trilha_id: null,
    homologado_por_id: null,
    homologado_em: null,
    integrantes: [],
    meu_papel: "montagem",
    atividades: [
      {
        atividade: item().atividade,
        missao_id: "missao-1",
        missao_titulo: "Primeira Missão",
        trilha_id: "trilha-1",
        trilha_titulo: "Trilha Um",
        corrente: true,
      },
    ],
    ...sobrescreve,
  };
}

// O palco do caminho: o estado de rede do aparelho e a sessão do
// Guerreiro(a) em volta da tela, e a tela montada só quando `montar` pede —
// é isso que deixa o cenário sem rede começar já sem rede, como acontece no
// aparelho, em que a entrada é que barra o caminho antes da tela abrir.
function PalcoDoPercurso({ montar }: { montar: boolean }) {
  return (
    <ProvedorDeEstadoDeRede>
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO_DO_PERCURSO}>
        {montar ? (
          <TelaDeTrilhasDoGuerreiro
            aulaId="aula-1"
            token="token-do-guerreiro"
            aoVoltar={vi.fn()}
          />
        ) : null}
      </ProvedorDeSessao>
    </ProvedorDeEstadoDeRede>
  );
}

async function renderizarPercurso(offline = false) {
  sessionStorage.setItem(CHAVE_DE_SESSAO_DO_PERCURSO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  const resultado = render(<PalcoDoPercurso montar={!offline} />);
  if (offline) {
    window.dispatchEvent(new Event("offline"));
    resultado.rerender(<PalcoDoPercurso montar />);
  }
  return resultado;
}

afterEach(() => {
  sessionStorage.clear();
});

describe("o percurso do Guerreiro(a) no encontro (RF-04-72)", () => {
  it("uma trilha inscrita abre direto no percurso, sem lista de trilhas", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([trilhaInscrita()]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(missaoNoPercurso());
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();

    expect(await screen.findByRole("heading", { name: "Robô Educa" })).toBeInTheDocument();
    expect(screen.queryByRole("region", { name: "Suas trilhas" })).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /trocar de trilha/i }),
    ).not.toBeInTheDocument();
  });

  it("mais de uma trilha inscrita apresenta a lista, e a escolhida abre o percurso", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([
      trilhaInscrita(),
      trilhaInscrita({ id: "trilha-2", nome: "Horta Viva" }),
    ]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(missaoNoPercurso());
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();
    const usuario = userEvent.setup();

    expect(await screen.findByRole("region", { name: "Suas trilhas" })).toBeInTheDocument();
    await usuario.click(screen.getByRole("button", { name: "Horta Viva" }));

    // A escolhida é a que abre, e a troca de trilha segue oferecida porque há
    // mais de uma (`RF-05-17`).
    expect(await screen.findByRole("heading", { name: "Horta Viva" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /trocar de trilha/i })).toBeInTheDocument();
  });

  it("sem inscrição alguma, a tela leva ao catálogo de poderes do ciclo", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([]);
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Robótica",
        descricao: "Descrição do poder.",
        trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
      },
    ]);
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();
    const usuario = userEvent.setup();

    expect(await screen.findByText(/escolha um poder/i)).toBeInTheDocument();
    await usuario.click(await screen.findByRole("button", { name: "Robótica" }));

    expect(await screen.findByText("Robô Educa")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /inscrever-se/i })).toBeInTheDocument();
  });

  it("inscrito no encontro, o percurso abre na sondagem no mesmo atendimento", async () => {
    const listar = vi
      .spyOn(trilhaApi, "listarMinhasTrilhas")
      .mockResolvedValueOnce([])
      .mockResolvedValue([
        trilhaInscrita({
          proxima_missao_id: "sondagem-1",
          proxima_missao_titulo: "Sondagem",
        }),
      ]);
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Robótica",
        descricao: "Descrição do poder.",
        trilhas: [{ id: "trilha-1", nome: "Robô Educa" }],
      },
    ]);
    const inscrever = vi.spyOn(trilhaApi, "inscreverNaTrilha").mockResolvedValue({
      id: "inscricao-1",
      trilha_id: "trilha-1",
      momento: "2026-09-25T00:00:00-03:00",
    });
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(
      missaoNoPercurso({
        id: "sondagem-1",
        titulo: "Sondagem",
        e_sondagem: true,
        desafio_de_desbloqueio: QUIZ_DO_DESBLOQUEIO,
      }),
    );
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();
    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: "Robótica" }));
    await usuario.click(screen.getByRole("button", { name: /inscrever-se/i }));

    expect(inscrever).toHaveBeenCalledWith("trilha-1", "token-do-guerreiro");
    // A posição vem do núcleo: a aplicação nunca calcula onde o percurso
    // começa (invariante 5).
    expect(await screen.findByRole("region", { name: "Sondagem" })).toBeInTheDocument();
    expect(listar).toHaveBeenCalledTimes(2);
  });

  it("a inscrição não se desfaz e não tem teto", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([trilhaInscrita()]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(missaoNoPercurso());
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(trilhaApi, "listarPoderesDoCatalogo").mockResolvedValue([
      {
        id: "poder-1",
        nome: "Robótica",
        descricao: "Descrição do poder.",
        trilhas: [
          { id: "trilha-1", nome: "Robô Educa" },
          { id: "trilha-2", nome: "Horta Viva" },
        ],
      },
    ]);
    // Repetir a mesma trilha devolve a inscrição existente, sem erro
    // (`RN-05-43`).
    const inscrever = vi.spyOn(trilhaApi, "inscreverNaTrilha").mockResolvedValue({
      id: "inscricao-1",
      trilha_id: "trilha-1",
      momento: "2026-09-25T00:00:00-03:00",
    });
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();
    const usuario = userEvent.setup();

    // Já inscrito numa, a tela segue oferecendo escolher outro poder: não há
    // teto de quantas trilhas (`RN-05-44`).
    await usuario.click(await screen.findByRole("button", { name: /escolher outro poder/i }));
    await usuario.click(await screen.findByRole("button", { name: "Robótica" }));
    const inscricoes = screen.getAllByRole("button", { name: /inscrever-se/i });
    expect(inscricoes).toHaveLength(2);
    await usuario.click(inscricoes[0]);

    expect(inscrever).toHaveBeenCalledWith("trilha-1", "token-do-guerreiro");
    // Em nenhum momento a tela oferece desinscrever-se.
    expect(
      screen.queryByRole("button", { name: /desinscrever|cancelar a inscrição/i }),
    ).not.toBeInTheDocument();
  });

  it("quem acabou de se inscrever começa na sondagem, e a seguinte aparece trancada com o motivo", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([
      trilhaInscrita({ proxima_missao_id: "sondagem-1", proxima_missao_titulo: "Sondagem" }),
    ]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, ordem) =>
      Promise.resolve(
        ordem === 1
          ? missaoNoPercurso({
              id: "sondagem-1",
              titulo: "Sondagem",
              e_sondagem: true,
              desafio_de_desbloqueio: QUIZ_DO_DESBLOQUEIO,
            })
          : missaoNoPercurso({
              id: "missao-2",
              titulo: "Segunda Missão",
              posicao: 2,
              e_proxima: false,
              motivo_do_bloqueio: 'Responda a "Sondagem" primeiro.',
            }),
      ),
    );
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();

    expect(await screen.findByRole("region", { name: "Sondagem" })).toBeInTheDocument();
    expect(screen.getByText(/ajuda o mestre/i)).toBeInTheDocument();
    expect(screen.getByText("Segunda Missão")).toBeInTheDocument();
    expect(screen.getByText(/responda a "sondagem" primeiro/i)).toBeInTheDocument();
  });

  it("as atividades da aula vêm pelas equipes do Guerreiro(a)", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([trilhaInscrita()]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(missaoNoPercurso());
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    // A equipe da trilha, sem `aula_id`, não é deste encontro.
    const listar = vi
      .spyOn(equipesApi, "listarMinhasEquipes")
      .mockResolvedValue([
        minhaEquipe(),
        minhaEquipe({ id: "equipe-2", nome: "Equipe da Trilha", aula_id: null }),
      ]);

    await renderizarPercurso();

    expect(await screen.findByRole("heading", { name: "Os Robôs" })).toBeInTheDocument();
    expect(screen.getByText("Montagem do robô")).toBeInTheDocument();
    expect(
      screen.queryByRole("heading", { name: "Equipe da Trilha" }),
    ).not.toBeInTheDocument();
    expect(listar).toHaveBeenCalledWith("token-do-guerreiro");
  });

  it("sem equipe na aula, a tela distingue os dois vazios", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([trilhaInscrita()]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(missaoNoPercurso());
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();

    expect(
      await screen.findByText(/ainda não está em nenhuma equipe deste encontro/i),
    ).toBeInTheDocument();
    // Enunciado distinto do de encontro sem programação declarada, que é
    // outro fato (`RF-04-35`).
    expect(
      screen.queryByText(/este encontro ainda não tem atividade declarada/i),
    ).not.toBeInTheDocument();
  });
});

describe("a sondagem e o desbloqueio no encontro (RF-04-73)", () => {
  async function abrirMissaoComDesafio(missao: Partial<trilhaApi.MissaoNoPercurso>) {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([trilhaInscrita()]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(missaoNoPercurso(missao));
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(trilhaPublicaComMissao());
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);
    await renderizarPercurso();
    return userEvent.setup();
  }

  it("respondida a sondagem, a trilha abre sem exigir entrada nova", async () => {
    // O núcleo abre a trilha ao ser respondida, não ao ser acertada
    // (documento 11 §2.2, `RN-05-46`).
    const submeter = vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 0,
      total: 1,
    });
    const usuario = await abrirMissaoComDesafio({
      id: "sondagem-1",
      titulo: "Sondagem",
      e_sondagem: true,
      desafio_de_desbloqueio: QUIZ_DO_DESBLOQUEIO,
    });

    await usuario.click(await screen.findByRole("radio", { name: "1" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(submeter).toHaveBeenCalledWith(
      "sondagem-1",
      [{ pergunta_id: "p1", alternativa_escolhida: 1 }],
      "token-do-guerreiro",
    );
    // A trilha já reabre no mesmo atendimento: nenhuma entrada nova é pedida.
    expect(screen.queryByLabelText(/nick/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/não foi dessa vez/i)).not.toBeInTheDocument();
  });

  it("o quiz do desbloqueio é aferido pelo núcleo, que diz quantas ele acertou", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: false,
      aguardando_mestre: false,
      acertos: 1,
      total: 2,
    });
    const usuario = await abrirMissaoComDesafio({
      desafio_de_desbloqueio: QUIZ_DO_DESBLOQUEIO,
    });

    await usuario.click(await screen.findByRole("radio", { name: "2" }));
    await usuario.click(screen.getByRole("button", { name: /enviar respostas/i }));

    expect(await screen.findByText(/acertou 1 de 2/i)).toBeInTheDocument();
  });

  it("o desafio prático deixa a missão aguardando o Mestre, nunca reprovada", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: null,
      aguardando_mestre: true,
      acertos: 0,
      total: 0,
    });
    const usuario = await abrirMissaoComDesafio({
      desafio_de_desbloqueio: {
        tipo: "pratico",
        enunciado: "Monte o robô e mostre ao Mestre.",
        perguntas: null,
      },
    });

    await usuario.click(await screen.findByRole("button", { name: /já cumpri/i }));

    expect(await screen.findByText(/esperar o mestre conferir/i)).toBeInTheDocument();
    expect(screen.queryByText(/reprovad/i)).not.toBeInTheDocument();
  });

  it("a entrega individual da produção não acontece por este caminho", async () => {
    vi.spyOn(trilhaApi, "listarMinhasTrilhas").mockResolvedValue([trilhaInscrita()]);
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(
      missaoNoPercurso({ desbloqueada: true, e_proxima: false }),
    );
    vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue(
      trilhaPublicaComMissao([
        { id: "atividade-1", titulo: "Atividade Única", producao_esperada: "Um texto." },
      ]),
    );
    vi.spyOn(equipesApi, "listarMinhasEquipes").mockResolvedValue([]);

    await renderizarPercurso();

    expect(
      await screen.findByRole("heading", { name: "Primeira Missão" }),
    ).toBeInTheDocument();
    // A entrega desta aplicação é por equipe, e segue no caminho das equipes
    // (`RF-04-45`, `RF-05-74`).
    expect(screen.queryByText(/o que a equipe fez/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /entregar/i })).not.toBeInTheDocument();
  });

  it("sem rede, o percurso não abre e nada é enfileirado", async () => {
    const listar = vi.spyOn(trilhaApi, "listarMinhasTrilhas");
    const listarEquipes = vi.spyOn(equipesApi, "listarMinhasEquipes");

    await renderizarPercurso(true);

    expect(await screen.findByText(/este caminho precisa de rede/i)).toBeInTheDocument();
    expect(screen.getByText(/nada ficou guardado neste aparelho/i)).toBeInTheDocument();
    expect(listar).not.toHaveBeenCalled();
    expect(listarEquipes).not.toHaveBeenCalled();
  });
});
