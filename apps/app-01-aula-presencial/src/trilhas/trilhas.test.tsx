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
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("programação do encontro (RF-04-35)", () => {
  it("a equipe vê a missão, o conteúdo e a atividade do dia", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([item()]);

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByText("Primeira missão")).toBeInTheDocument();
    expect(screen.getByText("Texto da missão.")).toBeInTheDocument();
    expect(screen.getByText("Montagem do robô")).toBeInTheDocument();
    expect(programacaoApi.obterProgramacaoDoEncontro).toHaveBeenCalledWith(
      "equipe-1",
      "token-guerreiro",
    );
  });

  it("duas atividades viram escolha da equipe, sem envio ao núcleo", async () => {
    const espiado = vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([
      item(),
      item({
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
      }),
    ]);

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /segunda missão/i }));

    expect(await screen.findByText("Segunda missão")).toBeInTheDocument();
    expect(screen.queryByText("Primeira missão")).not.toBeInTheDocument();
    // A escolha é do aparelho — nenhuma chamada nova ao núcleo por conta dela.
    expect(espiado).toHaveBeenCalledTimes(1);
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

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );

    expect(await screen.findByText(/fonte: instituto exemplo/i)).toBeInTheDocument();
  });

  it("nenhum dado pessoal de Guerreiro(a) aparece na tela", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro").mockResolvedValue([item()]);

    render(
      <TelaDaProgramacao equipeId="equipe-1" token="token-guerreiro" aoVoltar={vi.fn()} />,
    );
    await screen.findByText("Primeira missão");

    expect(screen.queryByText(/nick|avatar/i)).not.toBeInTheDocument();
  });

  it("a rede cai e o conteúdo já carregado continua legível", async () => {
    vi.spyOn(programacaoApi, "obterProgramacaoDoEncontro")
      .mockResolvedValueOnce([item()])
      .mockRejectedValueOnce(new Error("falha de rede"));

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
});
