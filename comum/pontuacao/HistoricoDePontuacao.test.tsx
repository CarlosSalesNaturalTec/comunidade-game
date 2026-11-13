import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { ErroDaApi } from "../api/cliente";
import type { HistoricoDePontuacao as Historico, LancamentoDePontuacao } from "./api";
import { HistoricoDePontuacao } from "./HistoricoDePontuacao";

function lancamento(parcial: Partial<LancamentoDePontuacao>): LancamentoDePontuacao {
  return {
    id: crypto.randomUUID(),
    registrado_em: "2026-11-10T13:00:00Z",
    conta: "regular",
    origem: "resultado",
    valor: 10,
    valor_no_acumulado: null,
    trilha_id: "t1",
    poder_id: null,
    nome_da_trilha_ou_poder: "Robótica",
    detalhe: null,
    motivo: null,
    ...parcial,
  };
}

const SALDOS: Historico["saldos"] = {
  regular: [{ trilha_id: "t1", poder_id: null, nome: "Robótica", total: 15 }],
  extra: { acumulado: 30, saldo_disponivel: 5 },
};

describe("HistoricoDePontuacao", () => {
  it("mostra os saldos separados e cada lançamento com origem e valor", async () => {
    const ler = vi.fn().mockResolvedValue({
      saldos: SALDOS,
      itens: [
        lancamento({
          origem: "ocorrencia_de_conduta",
          valor: -5,
          motivo: "Desrespeitou um colega.",
        }),
        lancamento({
          conta: "extra",
          origem: "troca",
          valor: -25,
          valor_no_acumulado: 0,
          trilha_id: null,
          nome_da_trilha_ou_poder: null,
          detalhe: "Camiseta",
        }),
        lancamento({
          conta: "extra",
          origem: "estorno_de_presenca",
          valor: -2,
          valor_no_acumulado: -5,
          trilha_id: null,
          nome_da_trilha_ou_poder: null,
        }),
      ],
      proximo_cursor: null,
    });
    render(<HistoricoDePontuacao ler={ler} />);

    expect(await screen.findByText("Robótica: 15 pontos")).toBeInTheDocument();
    expect(screen.getByText("Acumulado: 30")).toBeInTheDocument();
    expect(screen.getByText("Saldo disponível: 5")).toBeInTheDocument();
    expect(screen.getByText("Ocorrência de conduta")).toBeInTheDocument();
    expect(screen.getByText(/-5 pontos/)).toBeInTheDocument();
    expect(screen.getByText("Motivo: Desrespeitou um colega.")).toBeInTheDocument();
    expect(screen.getByText(/-25 no saldo disponível/)).toBeInTheDocument();
    expect(screen.getByText(/-5 no acumulado, -2 no saldo disponível/)).toBeInTheDocument();
    expect(ler).toHaveBeenCalledWith(null);
  });

  it("carrega mais pelo cursor do núcleo", async () => {
    const ler = vi
      .fn()
      .mockResolvedValueOnce({
        saldos: SALDOS,
        itens: [lancamento({ detalhe: "Primeira página" })],
        proximo_cursor: "c1",
      })
      .mockResolvedValueOnce({
        saldos: SALDOS,
        itens: [lancamento({ origem: "saldo_anterior", detalhe: null, valor: 5 })],
        proximo_cursor: null,
      });
    render(<HistoricoDePontuacao ler={ler} />);

    await userEvent.click(await screen.findByRole("button", { name: "Carregar mais" }));

    expect(await screen.findByText("Saldo anterior ao histórico")).toBeInTheDocument();
    expect(screen.getByText(/Primeira página/)).toBeInTheDocument();
    expect(ler).toHaveBeenLastCalledWith("c1");
    expect(screen.queryByRole("button", { name: "Carregar mais" })).not.toBeInTheDocument();
  });

  it("avisa quando ainda não há lançamento", async () => {
    const ler = vi.fn().mockResolvedValue({
      saldos: { regular: [], extra: { acumulado: 0, saldo_disponivel: 0 } },
      itens: [],
      proximo_cursor: null,
    });
    render(<HistoricoDePontuacao ler={ler} />);

    expect(
      await screen.findByText("Ainda não há lançamento de pontuação."),
    ).toBeInTheDocument();
  });

  it("mostra a recusa do núcleo como recusa, nunca como lista vazia", async () => {
    const ler = vi.fn().mockRejectedValue(
      new ErroDaApi(403, {
        codigo: "permissao_negada",
        mensagem: "O Mestre lê só o histórico de Guerreiro(a) da comunidade do seu vínculo.",
      }),
    );
    render(<HistoricoDePontuacao ler={ler} />);

    expect(
      await screen.findByText(
        "O Mestre lê só o histórico de Guerreiro(a) da comunidade do seu vínculo.",
      ),
    ).toBeInTheDocument();
    expect(
      screen.queryByText("Ainda não há lançamento de pontuação."),
    ).not.toBeInTheDocument();
  });

  it("devolve a sessão recusada a quem chamou", async () => {
    const aoRecusarSessao = vi.fn();
    const ler = vi
      .fn()
      .mockRejectedValue(new ErroDaApi(401, { codigo: "sessao_invalida", mensagem: "x" }));
    render(<HistoricoDePontuacao ler={ler} aoRecusarSessao={aoRecusarSessao} />);

    await vi.waitFor(() => expect(aoRecusarSessao).toHaveBeenCalled());
  });
});
