import { render, screen } from "@testing-library/react";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { act } from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AreaDoGuerreiro } from "./AreaDoGuerreiro";

const UM_MINUTO_EM_MS = 60_000;
// A duração do teste (design — vite.config.ts `test.env`): 5 minutos.
const DURACAO_EM_MS = 5 * UM_MINUTO_EM_MS;

async function renderizarComSessaoAberta() {
  sessionStorage.setItem("app-05:sessao-guerreiro-teste", "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
  });
  render(
    <ProvedorDeSessao chaveDeArmazenamento="app-05:sessao-guerreiro-teste">
      <AreaDoGuerreiro />
    </ProvedorDeSessao>,
  );
  await screen.findByRole("heading", { name: /minha área/i });
}

describe("encerramento por saída e por inatividade", () => {
  beforeEach(() => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    sessionStorage.clear();
  });

  it("avisa um minuto antes do encerramento por inatividade", async () => {
    await renderizarComSessaoAberta();

    expect(screen.queryByRole("alert")).not.toBeInTheDocument();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(DURACAO_EM_MS - UM_MINUTO_EM_MS);
    });

    expect(screen.getByRole("alert")).toHaveTextContent(/sessão vai fechar/i);
  });

  it("sem resposta ao aviso, a sessão encerra", async () => {
    // O retorno ao pedido de nick é responsabilidade de
    // `AparelhoDaAreaDoGuerreiro` — coberto em
    // `AparelhoDaAreaDoGuerreiro.test.tsx`. Aqui, isolado, confere só que o
    // encerramento por inatividade chama a saída da sessão.
    const encerrarSessaoDoGuerreiro = vi
      .spyOn(autenticacaoApi, "encerrarSessao")
      .mockResolvedValue(undefined);
    await renderizarComSessaoAberta();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(DURACAO_EM_MS);
    });

    await vi.waitFor(() =>
      expect(encerrarSessaoDoGuerreiro).toHaveBeenCalledWith("token-do-guerreiro"),
    );
  });

  it("continuar recomeça a contagem, e a sessão segue aberta", async () => {
    vi.spyOn(autenticacaoApi, "encerrarSessao").mockResolvedValue(undefined);
    await renderizarComSessaoAberta();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(DURACAO_EM_MS - UM_MINUTO_EM_MS);
    });
    screen.getByRole("button", { name: /continuar/i }).click();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(UM_MINUTO_EM_MS);
    });

    expect(screen.getByRole("heading", { name: /minha área/i })).toBeInTheDocument();
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
  });
});
