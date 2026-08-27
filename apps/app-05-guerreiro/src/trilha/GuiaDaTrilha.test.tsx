import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { GuiaDaTrilha } from "./GuiaDaTrilha";

const CHAVE_DE_SESSAO = "app-05:teste-guia-da-trilha";

const TRILHA: trilhaApi.TrilhaComProximaMissao = {
  id: "trilha-1",
  nome: "Robô Educa",
  poder_id: "poder-1",
  proxima_missao_id: "missao-1",
  proxima_missao_titulo: "Primeira Missão",
  proxima_missao_posicao: 1,
};

const MISSAO_ATUAL: trilhaApi.MissaoNoPercurso = {
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
};

async function renderizar(props: Partial<Parameters<typeof GuiaDaTrilha>[0]> = {}) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  vi.spyOn(trilhaApi, "obterTrilhaPublica").mockResolvedValue({
    id: "trilha-1",
    nome: "Robô Educa",
    licenca: "CC BY-SA",
    autor_nome: "Mestre Ana",
    missoes: [],
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <GuiaDaTrilha
          trilha={TRILHA}
          aoAtualizarTrilhas={vi.fn()}
          aoTrocarDeTrilha={vi.fn()}
          {...props}
        />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("guia da trilha", () => {
  it("a tela inicial já mostra a próxima missão", async () => {
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockImplementation((_id, ordem) =>
      Promise.resolve(
        ordem === 1
          ? MISSAO_ATUAL
          : { ...MISSAO_ATUAL, id: "missao-2", titulo: "Segunda Missão", posicao: 2 },
      ),
    );

    await renderizar();

    expect(await screen.findByText("Primeira Missão")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Robô Educa" })).toBeInTheDocument();
  });

  it("trocar de trilha aciona aoTrocarDeTrilha", async () => {
    vi.spyOn(trilhaApi, "obterMissaoNoPercurso").mockResolvedValue(MISSAO_ATUAL);
    const aoTrocarDeTrilha = vi.fn();

    await renderizar({ aoTrocarDeTrilha });

    await act(async () => {
      screen.getByRole("button", { name: /trocar de trilha/i }).click();
    });

    expect(aoTrocarDeTrilha).toHaveBeenCalled();
  });

  it("trilha inteira desbloqueada mostra sucesso", async () => {
    await renderizar({ trilha: { ...TRILHA, proxima_missao_posicao: null } });

    expect(await screen.findByText(/já desbloqueou todas as missões/i)).toBeInTheDocument();
  });
});
