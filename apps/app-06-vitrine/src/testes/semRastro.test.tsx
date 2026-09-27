import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { configurarAcessoAoNucleo } from "comum/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import { lerDoNucleo } from "../api/nucleo";

describe("a vitrine não deixa rastro no aparelho", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
    localStorage.clear();
    sessionStorage.clear();
  });

  it("uma visita inteira não guarda nada (RF-03-51, RF-03-60, RN-03-22)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Pesquisadores" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Gestores públicos" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Apoiador" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: /fechar/i }));

    expect(localStorage.length).toBe(0);
    expect(sessionStorage.length).toBe(0);
    expect(document.cookie).toBe("");
  });
});

describe("a chamada ao núcleo leva a chave e nenhuma credencial de persona", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("o cabeçalho de sessão nunca é enviado (RN-03-33)", async () => {
    configurarAcessoAoNucleo({
      chaveDeAplicacao: "chave-da-vitrine",
      urlDoNucleo: "https://nucleo.example.org",
    });
    const buscar = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify([]), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await lerDoNucleo("/v1/vitrine/guerreiros");

    const [, opcoes] = buscar.mock.calls[0];
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-da-vitrine");
    expect(cabecalhos.Authorization).toBeUndefined();
  });
});
