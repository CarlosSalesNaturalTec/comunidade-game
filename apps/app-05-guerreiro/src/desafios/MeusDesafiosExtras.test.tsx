import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import type { DesafioExtraDoGuerreiro } from "../api/desafiosEEquipes";
import { MeusDesafiosExtras } from "./MeusDesafiosExtras";

const DESAFIO_EXTRA: DesafioExtraDoGuerreiro = {
  id: "desafio-extra-1",
  trilha_id: "trilha-1",
  trilha_nome: "Trilha da Robótica",
  missao_id: "missao-1",
  missao_titulo: "Missão do robô",
  modalidade: "aberto",
  formato: "on_line",
  criterio_de_atribuicao: "Quem entregar primeiro.",
  pontos_extras: 5,
  recompensa: {
    tipo_de_recurso_nome: "Kit de robótica",
    ponto_de_apoio_nome: "Biblioteca Central",
  },
  quantidade_disponivel: 5,
  quantidade_restante: 3,
  vigencia_inicio: "2026-01-01",
  vigencia_fim: "2026-12-31",
};

describe("meus desafios extras", () => {
  it("o cartão mostra recompensa, quantidade, vigência e critério", () => {
    render(<MeusDesafiosExtras extras={[DESAFIO_EXTRA]} />);

    expect(screen.getByText(/Kit de robótica/)).toBeInTheDocument();
    expect(screen.getByText(/Biblioteca Central/)).toBeInTheDocument();
    expect(screen.getByText(/3 de 5 ainda disponíveis/)).toBeInTheDocument();
    expect(screen.getByText(/31\/12\/2026/)).toBeInTheDocument();
    expect(screen.getByText(/Quem entregar primeiro\./)).toBeInTheDocument();
  });

  it("o esgotado aparece marcado, sem sumir", () => {
    render(<MeusDesafiosExtras extras={[{ ...DESAFIO_EXTRA, quantidade_restante: 0 }]} />);

    expect(screen.getByText(/Kit de robótica/)).toBeInTheDocument();
    expect(screen.getByText(/já acabaram/i)).toBeInTheDocument();
  });

  it("o direcionado é apresentado como dirigido a ela, sem nomear terceiro", () => {
    render(<MeusDesafiosExtras extras={[{ ...DESAFIO_EXTRA, modalidade: "direcionado" }]} />);

    expect(screen.getByText(/feito especialmente para você/i)).toBeInTheDocument();
  });

  it("a tela diz que o ponto extra não sobe nível", () => {
    render(<MeusDesafiosExtras extras={[DESAFIO_EXTRA]} />);

    expect(screen.getByText(/não contam para o seu nível/i)).toBeInTheDocument();
  });

  it("sem extras, a mensagem explica em vez de lista vazia muda", () => {
    render(<MeusDesafiosExtras extras={[]} />);

    expect(screen.getByText(/não tem nenhum desafio extra disponível/i)).toBeInTheDocument();
  });

  it("nenhuma ação de concluir, disputar, comprar ou trocar é oferecida", () => {
    render(<MeusDesafiosExtras extras={[DESAFIO_EXTRA]} />);

    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
});
