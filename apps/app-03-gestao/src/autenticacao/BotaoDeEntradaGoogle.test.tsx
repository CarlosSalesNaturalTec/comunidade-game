import { render } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

// Este arquivo monta `BotaoDeEntradaGoogle` de verdade — `entrada.test.tsx` o
// substitui por um duplo, e por isso nunca exercita o curto-circuito que
// impede o acesso ao provedor externo em ambiente sem client ID.
//
// O jsdom não busca recurso externo (`resources` não é habilitado na
// configuração do Vitest), então nem o caso configurado alcança a rede.
const SELETOR_DO_PROVEDOR = 'script[src="https://accounts.google.com/gsi/client"]';

async function montarCom(clientId: string) {
  vi.stubEnv("VITE_GOOGLE_CLIENT_ID", clientId);
  vi.resetModules();
  const { BotaoDeEntradaGoogle } = await import("./BotaoDeEntradaGoogle");
  return render(<BotaoDeEntradaGoogle aoReceberIdToken={() => {}} />);
}

describe("a dependência externa de identidade só é acionada quando configurada", () => {
  beforeEach(() => {
    vi.resetModules();
  });

  afterEach(() => {
    vi.unstubAllEnvs();
    for (const script of document.querySelectorAll(SELETOR_DO_PROVEDOR)) {
      script.remove();
    }
  });

  it("sem client ID, nenhum script do provedor é carregado e a tela segue apresentável", async () => {
    const { getByTestId } = await montarCom("");

    expect(document.querySelector(SELETOR_DO_PROVEDOR)).toBeNull();
    expect(getByTestId("botao-de-entrada-google")).toBeInTheDocument();
  });

  it("com client ID, o caminho de entrada pela conta social é oferecido", async () => {
    await montarCom("client-id-de-teste.apps.googleusercontent.com");

    expect(document.querySelector(SELETOR_DO_PROVEDOR)).not.toBeNull();
  });
});
