import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { AparelhoDaAreaDoGuerreiro } from "./AparelhoDaAreaDoGuerreiro";

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("guarda do aparelho compartilhado", () => {
  it("sair volta ao pedido de nick, sem dado do Guerreiro(a) anterior e sem reiniciar a aplicação", async () => {
    vi.spyOn(biometriaModulo, "existeCamera").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(sessoesDeGuerreiroApi, "abrirSessaoPorReconhecimento").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(autenticacaoApi, "encerrarSessao").mockResolvedValue(undefined);

    render(
      <ProvedorDeSessao chaveDeArmazenamento="app-05:sessao-guerreiro-teste">
        <AparelhoDaAreaDoGuerreiro />
      </ProvedorDeSessao>,
    );
    const usuario = userEvent.setup();
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /entrar/i }));

    await screen.findByRole("heading", { name: /minha área/i });
    await usuario.click(screen.getByRole("button", { name: /sair/i }));

    const campoDeNick = await screen.findByLabelText(/nick/i);
    expect(campoDeNick).toHaveValue("");
    expect(screen.queryByText(/zeferina/i)).not.toBeInTheDocument();
  });
});
