import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as desafiosEEquipesApi from "../api/desafiosEEquipes";
import { DesafiosEEquipes } from "./DesafiosEEquipes";

const CHAVE_DE_SESSAO = "app-05:teste-desafios-e-equipes";

async function renderizar() {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  vi.spyOn(desafiosEEquipesApi, "listarMeusDesafios").mockResolvedValue({
    semanais: [],
    extras: [],
  });
  vi.spyOn(desafiosEEquipesApi, "listarMinhasEquipes").mockResolvedValue([]);
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <DesafiosEEquipes />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("bloco de desafios e equipes", () => {
  it("abre na aba dos desafios", async () => {
    await renderizar();

    expect(await screen.findByText(/não tem nenhum desafio em aberto/i)).toBeInTheDocument();
  });

  it("troca para a aba das equipes ao clicar nela", async () => {
    await renderizar();
    await screen.findByText(/não tem nenhum desafio em aberto/i);

    await act(async () => {
      screen.getByRole("button", { name: "Minhas equipes" }).click();
    });

    expect(await screen.findByText(/ainda não integra nenhuma equipe/i)).toBeInTheDocument();
  });

  it("nenhuma tela do bloco oferece canal de conversa", async () => {
    await renderizar();
    await screen.findByText(/não tem nenhum desafio em aberto/i);
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByText(/mensagem|comentário|conversa/i)).not.toBeInTheDocument();

    await act(async () => {
      screen.getByRole("button", { name: "Minhas equipes" }).click();
    });
    await screen.findByText(/ainda não integra nenhuma equipe/i);
    expect(screen.queryByRole("textbox")).not.toBeInTheDocument();
    expect(screen.queryByText(/mensagem|comentário|conversa/i)).not.toBeInTheDocument();
  });
});
