import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { DesafioDeDesbloqueio } from "./DesafioDeDesbloqueio";

const CHAVE_DE_SESSAO = "app-05:teste-desafio-de-desbloqueio";

async function renderizar(desafio: trilhaApi.DesafioDeDesbloqueio, aoDesbloquear = vi.fn()) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <DesafioDeDesbloqueio
          missaoId="missao-1"
          desafio={desafio}
          aoDesbloquear={aoDesbloquear}
        />
      </ProvedorDeSessao>,
    );
  });
  return aoDesbloquear;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("desafio de desbloqueio", () => {
  it("passar no quiz chama aoDesbloquear", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
    });
    const aoDesbloquear = await renderizar({
      tipo: "quiz",
      enunciado: "Quanto é 1 + 1?",
      alternativas: ["1", "2", "3", "4"],
    });

    await act(async () => {
      screen.getByRole("button", { name: "2" }).click();
    });

    expect(aoDesbloquear).toHaveBeenCalled();
  });

  it("não passar convida a tentar de novo, sem punição", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: false,
      aguardando_mestre: false,
    });
    await renderizar({
      tipo: "quiz",
      enunciado: "Quanto é 1 + 1?",
      alternativas: ["1", "2", "3", "4"],
    });

    await act(async () => {
      screen.getByRole("button", { name: "1" }).click();
    });

    expect(await screen.findByText(/não foi dessa vez/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "1" })).not.toBeDisabled();
  });

  it("prático declarado fica aguardando o Mestre", async () => {
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: null,
      aguardando_mestre: true,
    });
    await renderizar({
      tipo: "pratico",
      enunciado: "Monte o robô e mostre ao Mestre.",
      alternativas: null,
    });

    await act(async () => {
      screen.getByRole("button", { name: /já cumpri/i }).click();
    });

    expect(await screen.findByText(/aguardando|esperar o mestre/i)).toBeInTheDocument();
  });
});
