import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ItemDaProgramacao } from "../api/programacao";
import * as programacaoApi from "../api/programacao";
import { TelaDaProgramacao } from "./TelaDaProgramacao";

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

afterEach(() => {
  vi.restoreAllMocks();
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
