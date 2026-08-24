import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as sessoesDeGuerreiroApi from "../api/sessoesDeGuerreiro";
import { TelaDeEntradaDoGuerreiro } from "./TelaDeEntradaDoGuerreiro";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    useSessao: vi.fn(),
  };
});

import { useSessao } from "comum/autenticacao";

function configurarSessao(entrarComToken = vi.fn()) {
  vi.mocked(useSessao).mockReturnValue({
    sessao: null,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken,
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("entrada do Guerreiro(a) por confirmação", () => {
  it("confirma pelo nick informado, sem pedir identificador algum", async () => {
    const entrarComToken = vi.fn().mockResolvedValue(undefined);
    configurarSessao(entrarComToken);
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockResolvedValue({
      token: "token-do-guerreiro",
      expira_em: new Date().toISOString(),
      papel: "guerreiro",
    });

    render(
      <TelaDeEntradaDoGuerreiro tokenDeTrabalho="token-de-trabalho" aoVoltar={vi.fn()} />,
    );
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "zeferina");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    expect(sessoesDeGuerreiroApi.confirmarSessaoDeGuerreiro).toHaveBeenCalledWith(
      "zeferina",
      "token-de-trabalho",
    );
    expect(entrarComToken).toHaveBeenCalledWith("token-do-guerreiro");
  });

  it("nick sem correspondência é recusado sem revelar o motivo", async () => {
    configurarSessao();
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro").mockRejectedValue(
      new ErroDaApi(401, {
        codigo: "confirmacao_de_guerreiro_recusada",
        mensagem:
          "Não foi possível confirmar esse nick. Confira com o Guerreiro(a) e tente de novo.",
      }),
    );

    render(
      <TelaDeEntradaDoGuerreiro tokenDeTrabalho="token-de-trabalho" aoVoltar={vi.fn()} />,
    );
    const usuario = userEvent.setup();
    await usuario.type(screen.getByLabelText(/nick/i), "nick-que-nao-existe");
    await usuario.click(screen.getByRole("button", { name: /confirmar identidade/i }));

    const recusa = await screen.findByRole("alert");
    expect(recusa.textContent).not.toMatch(/confirmacao_de_guerreiro_recusada/i);
    expect(recusa).toHaveTextContent(/não foi possível confirmar/i);
  });

  it("o botão de confirmar não abre sem nick digitado", () => {
    configurarSessao();

    render(
      <TelaDeEntradaDoGuerreiro tokenDeTrabalho="token-de-trabalho" aoVoltar={vi.fn()} />,
    );

    expect(screen.getByRole("button", { name: /confirmar identidade/i })).toBeDisabled();
  });

  it("voltar aciona aoVoltar sem chamar a confirmação", async () => {
    configurarSessao();
    const aoVoltar = vi.fn();
    vi.spyOn(sessoesDeGuerreiroApi, "confirmarSessaoDeGuerreiro");

    render(
      <TelaDeEntradaDoGuerreiro tokenDeTrabalho="token-de-trabalho" aoVoltar={aoVoltar} />,
    );
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /voltar/i }));

    expect(aoVoltar).toHaveBeenCalled();
    expect(sessoesDeGuerreiroApi.confirmarSessaoDeGuerreiro).not.toHaveBeenCalled();
  });
});
