import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as equipesApi from "../api/equipes";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { TelaInicial } from "./TelaInicial";

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

function renderizar(aoVoltarAoInicio = vi.fn()) {
  return render(
    <ProvedorDeSessao chaveDeArmazenamento="teste:app-01:sessao-guerreiro">
      <TelaInicial
        tokenDeTrabalho="token-de-trabalho"
        aulaId="aula-1"
        aoVoltarAoInicio={aoVoltarAoInicio}
      />
    </ProvedorDeSessao>,
  );
}

describe("tela inicial da App 01", () => {
  it("os dois caminhos aparecem, e os dois estão habilitados", async () => {
    renderizar();

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /onboarding/i })).toBeEnabled();
    expect(screen.getByRole("button", { name: /trilhas/i })).toBeEnabled();
  });

  it("onboarding leva à tela de cadastro do Guerreiro(a)", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /onboarding/i }));

    expect(await screen.findByText(/novo guerreiro/i)).toBeInTheDocument();
  });

  it("trilhas sem sessão leva à entrada do Guerreiro(a), nunca ao cadastro", async () => {
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas/i }));

    expect(await screen.findByText(/quem está chegando/i)).toBeInTheDocument();
    expect(screen.queryByText(/cadastr/i)).not.toBeInTheDocument();
  });

  it("a confirmação do Mestre abre a sessão do Guerreiro(a) e leva às equipes", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(await screen.findByText(/equipes desta aula/i)).toBeInTheDocument();
  });

  it("voltar ao início encerra a sessão do Guerreiro(a) e limpa a tela", async () => {
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });
    vi.spyOn(sessaoApi, "eu").mockResolvedValue({
      persona_id: "guerreiro-1",
      papel: "guerreiro",
      permissoes: {},
    });
    vi.spyOn(sessaoApi, "encerrarSessao").mockResolvedValue(undefined);
    vi.spyOn(equipesApi, "listarEquipesDaAula").mockResolvedValue({
      itens: [],
      proximo_cursor: null,
    });

    const aoVoltarAoInicio = vi.fn();
    renderizar(aoVoltarAoInicio);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /trilhas/i }));
    await usuario.type(await screen.findByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));
    await screen.findByText(/equipes desta aula/i);

    await usuario.click(screen.getByRole("button", { name: /voltar ao início/i }));

    expect(await screen.findByText(/o que você quer fazer/i)).toBeInTheDocument();
    expect(sessaoApi.encerrarSessao).toHaveBeenCalledWith("token-do-guerreiro");
    // A volta ao início relê a janela da aula — design decisão 3.
    expect(aoVoltarAoInicio).toHaveBeenCalled();
  });
});
