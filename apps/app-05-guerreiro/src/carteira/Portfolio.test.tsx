import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as criacaoOriginalApi from "../api/criacaoOriginal";
import { Portfolio } from "./Portfolio";

const CHAVE_DE_SESSAO = "app-05:teste-portfolio";

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
        <Portfolio />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("portfólio", () => {
  it("traz trilha, data e autoria de cada criação validada", async () => {
    vi.spyOn(criacaoOriginalApi, "obterPortfolio").mockResolvedValue([
      {
        id: "criacao-1",
        trilha_id: "trilha-1",
        tipo: "texto",
        producao: "Meu robô de sucata.",
        referencia: null,
        validado_em: "2026-08-20T12:00:00Z",
        autores: [{ avatar: null, nick: "guerreira-zeferina" }],
        publica: true,
      },
    ]);

    await renderizar();

    expect(await screen.findByText("Meu robô de sucata.")).toBeInTheDocument();
    expect(screen.getByText(/guerreira-zeferina/)).toBeInTheDocument();
    expect(screen.getByText(/Pública na vitrine/i)).toBeInTheDocument();
  });

  it("criação sem autorização aparece como dependente de autorização", async () => {
    vi.spyOn(criacaoOriginalApi, "obterPortfolio").mockResolvedValue([
      {
        id: "criacao-1",
        trilha_id: "trilha-1",
        tipo: "texto",
        producao: "Meu robô de sucata.",
        referencia: null,
        validado_em: "2026-08-20T12:00:00Z",
        autores: [{ avatar: null, nick: "guerreira-zeferina" }],
        publica: false,
      },
    ]);

    await renderizar();

    expect(
      await screen.findByText(/depende da autorização de divulgação/i),
    ).toBeInTheDocument();
  });

  it("sem nenhuma criação validada mostra o estado vazio", async () => {
    vi.spyOn(criacaoOriginalApi, "obterPortfolio").mockResolvedValue([]);

    await renderizar();

    expect(
      await screen.findByText(/ainda não tem nenhuma criação original/i),
    ).toBeInTheDocument();
  });
});
