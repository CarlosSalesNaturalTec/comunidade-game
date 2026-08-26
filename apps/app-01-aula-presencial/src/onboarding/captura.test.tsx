import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import * as biometriaModulo from "comum/biometria";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as descritorApi from "../api/descritor";
import { TelaDeCaptura } from "./TelaDeCaptura";

afterEach(() => {
  vi.restoreAllMocks();
});

function renderizar(aoConcluir = vi.fn(), aoVoltar = vi.fn()) {
  return render(
    <TelaDeCaptura
      tokenDeTrabalho="token-de-trabalho"
      guerreiroId="guerreiro-1"
      aoConcluir={aoConcluir}
      aoVoltar={aoVoltar}
    />,
  );
}

describe("captura da imagem", () => {
  it("vivacidade aprovada gera o descritor e envia só ele, sem imagem", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    const enviar = vi.spyOn(descritorApi, "enviarDescritor").mockResolvedValue({
      guerreiro_id: "guerreiro-1",
      gravado_em: new Date().toISOString(),
    });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(enviar).toHaveBeenCalledWith(
      "guerreiro-1",
      { descritor: [0.1, 0.2, 0.3] },
      "token-de-trabalho",
    );
    const corpoEnviado = enviar.mock.calls[0][1];
    expect(Object.keys(corpoEnviado)).toEqual(["descritor"]);
    await vi.waitFor(() => expect(aoConcluir).toHaveBeenCalled());
  });

  it("vivacidade reprovada não envia nada e oferece nova tentativa", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(false);
    const gerarDescritor = vi.spyOn(biometriaModulo, "gerarDescritor");
    const enviar = vi.spyOn(descritorApi, "enviarDescritor");
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/não foi possível confirmar/i);
    expect(gerarDescritor).not.toHaveBeenCalled();
    expect(enviar).not.toHaveBeenCalled();
    expect(aoConcluir).not.toHaveBeenCalled();
    expect(screen.getByRole("button", { name: /iniciar captura/i })).toBeEnabled();
  });

  it("recusa por falta de consentimento explica em linguagem simples", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockResolvedValue(true);
    vi.spyOn(biometriaModulo, "gerarDescritor").mockResolvedValue([0.1, 0.2, 0.3]);
    vi.spyOn(descritorApi, "enviarDescritor").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Sem consentimento vigente.",
      }),
    );
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/consentimento/i);
  });

  it("nenhuma imagem aparece em registro de erro", async () => {
    vi.spyOn(biometriaModulo, "provarVivacidade").mockRejectedValue(
      new Error("falha ao abrir a câmera"),
    );
    renderizar();
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: /iniciar captura/i }));

    const alerta = await screen.findByRole("alert");
    expect(alerta.textContent).not.toMatch(/data:image|base64/i);
  });
});
