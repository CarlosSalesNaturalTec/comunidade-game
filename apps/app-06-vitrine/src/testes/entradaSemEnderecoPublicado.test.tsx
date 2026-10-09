import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it } from "vitest";
import App from "./TelaDaVitrine";

// Sem as variáveis de ambiente — o caso do desenvolvimento local e o de uma
// aplicação ainda não publicada —, a tela nomeia o destino em texto e não
// apresenta link quebrado (design — decisão 4).
describe("sem endereço publicado", () => {
  beforeEach(() => {
    window.history.pushState(null, "", "/");
  });

  it("nomeia o destino em texto, sem link (RF-03-59)", async () => {
    render(<App />);
    const testeDeUsuario = userEvent.setup();

    await testeDeUsuario.click(screen.getByRole("button", { name: "Entrar" }));
    await testeDeUsuario.click(screen.getByRole("button", { name: "Sou Mestre" }));

    expect(
      screen.getByText(/o endereço da Área do Mestre ainda não foi publicado/i),
    ).toBeVisible();
    // Sem endereço da Área do Mestre, o único link **do diálogo** é o do
    // formulário de participação da própria vitrine (RF-03-62). Escopado ao
    // diálogo porque a abertura, desde o herói, tem o seu próprio link.
    const dialogo = screen.getByRole("dialog", { name: /quem está entrando/i });
    const links = within(dialogo)
      .getAllByRole("link")
      .map((no) => no.getAttribute("href"));
    expect(links).toEqual(["/participar"]);
  });
});
