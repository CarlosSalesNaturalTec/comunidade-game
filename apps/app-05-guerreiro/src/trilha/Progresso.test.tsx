import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { Progresso } from "./Progresso";

const CHAVE_DE_SESSAO = "app-05:teste-progresso";

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <Progresso />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("progresso", () => {
  it("mostra o nível e quantas faltam, nunca saldo de pontos como nível", async () => {
    vi.spyOn(trilhaApi, "obterProgresso").mockResolvedValue([
      {
        trilha_id: "trilha-1",
        trilha_nome: "Robô Educa",
        nivel_atual: 2,
        obrigatorias_desbloqueadas: 2,
        obrigatorias_totais: 5,
        pontos_regulares: 40,
        badges: ["de_nivel", "de_nivel"],
      },
    ]);

    await renderizar();

    expect(await screen.findByText("Robô Educa")).toBeInTheDocument();
    expect(screen.getByText(/nível: 2/i)).toBeInTheDocument();
    expect(screen.getByText(/faltam 3 de 5/i)).toBeInTheDocument();
    expect(screen.getByText(/pontos: 40/i)).toBeInTheDocument();
  });

  it("sem trilha inscrita, avisa sem erro", async () => {
    vi.spyOn(trilhaApi, "obterProgresso").mockResolvedValue([]);

    await renderizar();

    expect(await screen.findByText(/não está inscrito/i)).toBeInTheDocument();
  });
});
