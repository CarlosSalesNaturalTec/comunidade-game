import { act, fireEvent, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as criacaoOriginalApi from "../api/criacaoOriginal";
import type { CulminanciaDaTrilha } from "../api/trilha";
import { EntregaDeCriacao } from "./EntregaDeCriacao";

const CHAVE_DE_SESSAO = "app-05:teste-entrega-de-criacao";

const CULMINANCIA_INDIVIDUAL: CulminanciaDaTrilha = {
  id: "culminancia-1",
  trilha_id: "trilha-1",
  descricao: "Descrição.",
  modalidade: "individual",
  criterio_de_validacao: "Critério.",
};

const CULMINANCIA_EM_EQUIPE: CulminanciaDaTrilha = {
  ...CULMINANCIA_INDIVIDUAL,
  modalidade: "em_equipe",
};

async function renderizar(culminancia: CulminanciaDaTrilha, aoEntregar = vi.fn()) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <EntregaDeCriacao
          trilhaId="trilha-1"
          culminancia={culminancia}
          criacaoDevolvida={null}
          aoEntregar={aoEntregar}
        />
      </ProvedorDeSessao>,
    );
  });
  return aoEntregar;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("entrega da criação original", () => {
  it("entrega em texto ou link registra a entrega", async () => {
    const entregar = vi
      .spyOn(criacaoOriginalApi, "entregarCriacaoOriginal")
      .mockResolvedValue({
        id: "criacao-1",
        trilha_id: "trilha-1",
        equipe_id: null,
        guerreiro_id: "guerreiro-1",
        tipo: "texto",
        producao: "Meu diário.",
        referencia: null,
        tamanho: null,
        situacao: "entregue",
        motivo_da_devolucao: null,
      });
    const aoEntregar = await renderizar(CULMINANCIA_INDIVIDUAL);

    fireEvent.change(screen.getByLabelText(/sua criação/i), {
      target: { value: "Meu diário." },
    });
    await act(async () => {
      fireEvent.click(screen.getByRole("button", { name: /entregar/i }));
    });

    expect(entregar).toHaveBeenCalledWith(
      "culminancia-1",
      { equipe_id: undefined, tipo: "texto", producao: "Meu diário." },
      "token-do-guerreiro",
    );
    expect(aoEntregar).toHaveBeenCalled();
  });

  it("entrega de equipe apresenta os integrantes e registra o papel de cada um", async () => {
    vi.spyOn(criacaoOriginalApi, "obterMinhaEquipeDaTrilha").mockResolvedValue({
      id: "equipe-1",
      aula_id: null,
      integrantes: [
        { avatar: null, nick: "criadora", papel: "quem construiu" },
        { avatar: null, nick: "colega", papel: null },
      ],
    });

    await renderizar(CULMINANCIA_EM_EQUIPE);

    expect(await screen.findByText(/criadora/)).toBeInTheDocument();
    expect(screen.getByText(/quem construiu/)).toBeInTheDocument();
    expect(screen.getByText(/colega/)).toBeInTheDocument();
  });

  it("não oferece formar nem editar a equipe", async () => {
    vi.spyOn(criacaoOriginalApi, "obterMinhaEquipeDaTrilha").mockResolvedValue({
      id: "equipe-1",
      aula_id: null,
      integrantes: [{ avatar: null, nick: "criadora", papel: null }],
    });

    await renderizar(CULMINANCIA_EM_EQUIPE);
    await screen.findByText(/criadora/);

    expect(screen.queryByRole("button", { name: /formar equipe/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /editar equipe/i })).not.toBeInTheDocument();
  });

  it("sem equipe homologada avisa e não oferece entrega", async () => {
    vi.spyOn(criacaoOriginalApi, "obterMinhaEquipeDaTrilha").mockRejectedValue(
      new Error("não encontrado"),
    );

    await renderizar(CULMINANCIA_EM_EQUIPE);

    expect(
      await screen.findByText(/precisa integrar uma equipe homologada/i),
    ).toBeInTheDocument();
    expect(screen.queryByRole("form")).not.toBeInTheDocument();
  });
});
