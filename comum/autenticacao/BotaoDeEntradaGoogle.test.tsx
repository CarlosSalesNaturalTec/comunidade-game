import { render } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { BotaoDeEntradaGoogle } from "./BotaoDeEntradaGoogle";

// O jsdom não busca recurso externo (`resources` não é habilitado na
// configuração do Vitest), então nem o caso configurado alcança a rede.
const SELETOR_DO_PROVEDOR = 'script[src="https://accounts.google.com/gsi/client"]';

describe("a dependência externa de identidade só é acionada quando configurada", () => {
  afterEach(() => {
    for (const script of document.querySelectorAll(SELETOR_DO_PROVEDOR)) {
      script.remove();
    }
  });

  it("sem client ID, nenhum script do provedor é carregado e a tela segue apresentável", () => {
    const { getByTestId } = render(
      <BotaoDeEntradaGoogle clientId="" aoReceberIdToken={() => {}} />,
    );

    expect(document.querySelector(SELETOR_DO_PROVEDOR)).toBeNull();
    expect(getByTestId("botao-de-entrada-google")).toBeInTheDocument();
  });

  it("com client ID, o caminho de entrada pela conta social é oferecido", () => {
    render(
      <BotaoDeEntradaGoogle
        clientId="client-id-de-teste.apps.googleusercontent.com"
        aoReceberIdToken={() => {}}
      />,
    );

    expect(document.querySelector(SELETOR_DO_PROVEDOR)).not.toBeNull();
  });
});
