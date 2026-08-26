import { act, render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { MinhaCarteira } from "./MinhaCarteira";

const CHAVE_DE_SESSAO = "app-05:teste-minha-carteira";

async function renderizar(divulgacaoAutorizada?: boolean) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    divulgacao_autorizada: divulgacaoAutorizada,
  });
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <MinhaCarteira />
      </ProvedorDeSessao>,
    );
  });
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("carteira de pontos extras", () => {
  it("mostra o acumulado e o saldo disponível separados, sem soma", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 30,
      saldo_disponivel: 18,
    });

    await renderizar(true);

    expect(await screen.findByText(/30 pontos extras/i)).toBeInTheDocument();
    expect(screen.getByText(/18 pontos extras/i)).toBeInTheDocument();
    expect(screen.queryByText(/48 pontos extras/i)).not.toBeInTheDocument();
  });

  it("diz que a divulgação está autorizada quando o responsável concedeu", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 0,
      saldo_disponivel: 0,
    });

    await renderizar(true);

    expect(await screen.findByText(/autorizou mostrar seu avatar/i)).toBeInTheDocument();
  });

  it("diz que o perfil ainda não aparece quando não há autorização, sem ação de decidir", async () => {
    vi.spyOn(carteiraApi, "listarMeusPontosExtras").mockResolvedValue({
      acumulado: 0,
      saldo_disponivel: 0,
    });

    await renderizar(false);

    expect(await screen.findByText(/ainda não aparece/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /autorizar/i })).not.toBeInTheDocument();
  });
});
