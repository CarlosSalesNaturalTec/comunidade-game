import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as consentimentosApi from "../api/consentimentos";
import { TelaDoTermo } from "./TelaDoTermo";

afterEach(() => {
  vi.restoreAllMocks();
});

function renderizar(aoConcluir = vi.fn(), aoVoltar = vi.fn()) {
  return render(
    <TelaDoTermo
      tokenDeTrabalho="token-de-trabalho"
      personaIdDeTrabalho="mestre-1"
      responsavelId="responsavel-1"
      guerreiroId="guerreiro-1"
      aoConcluir={aoConcluir}
      aoVoltar={aoVoltar}
    />,
  );
}

describe("termo de consentimento", () => {
  it("o termo é exibido na tela", () => {
    renderizar();
    expect(screen.getByText(/termo de consentimento/i)).toBeInTheDocument();
  });

  it("a confirmação registra o consentimento com quem confirma como testemunha", async () => {
    const registrar = vi
      .spyOn(consentimentosApi, "registrarConsentimento")
      .mockResolvedValue({ id: "consentimento-1", registrado_em: new Date().toISOString() });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.click(
      screen.getByRole("button", { name: /confirmo: o termo impresso foi assinado/i }),
    );

    expect(registrar).toHaveBeenCalledWith(
      {
        responsavel_id: "responsavel-1",
        guerreiro_id: "guerreiro-1",
        tipo: "biometria",
        decisao: "concede",
        origem: "impressa",
        testemunha_id: "mestre-1",
      },
      "token-de-trabalho",
    );
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("falha ao registrar mantém a tela do termo, sem avançar", async () => {
    vi.spyOn(consentimentosApi, "registrarConsentimento").mockRejectedValue(
      new ErroDaApi(500, { codigo: "erro_de_rede", mensagem: "Falha de rede." }),
    );
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.click(
      screen.getByRole("button", { name: /confirmo: o termo impresso foi assinado/i }),
    );

    expect(await screen.findByRole("alert")).toHaveTextContent(/falha de rede/i);
    expect(aoConcluir).not.toHaveBeenCalled();
  });
});
