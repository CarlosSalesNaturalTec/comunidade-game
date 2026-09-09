import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as trilhaApi from "../api/trilha";
import { Sondagem } from "./Sondagem";

const CHAVE_DE_SESSAO = "app-05:teste-sondagem";

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("sondagem", () => {
  it("diz que serve para o Mestre ajustar e não muda o nível", async () => {
    sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });

    await act(async () => {
      render(
        <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
          <Sondagem
            missaoId="sondagem-1"
            desafio={{
              tipo: "quiz",
              enunciado: null,
              perguntas: [
                {
                  id: "p1",
                  ordem: 1,
                  enunciado: "Pergunta",
                  alternativas: ["a", "b", "c", "d"],
                },
              ],
            }}
            aoResponder={vi.fn()}
          />
        </ProvedorDeSessao>,
      );
    });

    expect(screen.getByText(/ajuda o mestre/i)).toBeInTheDocument();
    expect(screen.getByText(/não muda o seu nível/i)).toBeInTheDocument();
    expect(screen.queryByText(/prova/i)).not.toBeInTheDocument();
  });

  it("responder chama aoResponder", async () => {
    sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(trilhaApi, "submeterDesafioDeDesbloqueio").mockResolvedValue({
      aprovado: true,
      aguardando_mestre: false,
      acertos: 0,
      total: 1,
    });
    const aoResponder = vi.fn();

    await act(async () => {
      render(
        <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
          <Sondagem
            missaoId="sondagem-1"
            desafio={{
              tipo: "quiz",
              enunciado: null,
              perguntas: [
                {
                  id: "p1",
                  ordem: 1,
                  enunciado: "Pergunta",
                  alternativas: ["a", "b", "c", "d"],
                },
              ],
            }}
            aoResponder={aoResponder}
          />
        </ProvedorDeSessao>,
      );
    });

    // Errar tudo na sondagem abre a trilha do mesmo jeito: quem afere é o
    // núcleo, e ele não aplica o corte de 60% aqui (`RN-05-46`).
    await act(async () => {
      screen.getByRole("radio", { name: "a" }).click();
    });
    await act(async () => {
      screen.getByRole("button", { name: /enviar respostas/i }).click();
    });

    expect(aoResponder).toHaveBeenCalled();
    expect(screen.queryByText(/não foi dessa vez/i)).not.toBeInTheDocument();
  });
});
