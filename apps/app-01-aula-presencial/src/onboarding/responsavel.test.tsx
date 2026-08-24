import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as responsaveisApi from "../api/responsaveis";
import { TelaDoResponsavel } from "./TelaDoResponsavel";

afterEach(() => {
  vi.restoreAllMocks();
});

function renderizar(aoConcluir = vi.fn(), aoVoltar = vi.fn()) {
  return render(
    <TelaDoResponsavel
      tokenDeTrabalho="token-de-trabalho"
      guerreiroId="guerreiro-1"
      aoConcluir={aoConcluir}
      aoVoltar={aoVoltar}
    />,
  );
}

describe("cadastro do responsável no encontro", () => {
  it("cadastra o responsável com nome e cria o vínculo com o grau de parentesco", async () => {
    const cadastrar = vi
      .spyOn(responsaveisApi, "cadastrarResponsavelNoEncontro")
      .mockResolvedValue({ id: "responsavel-1", nome: "Maria" });
    const criarVinculo = vi.spyOn(responsaveisApi, "criarVinculo").mockResolvedValue({
      id: "vinculo-1",
      responsavel_id: "responsavel-1",
      guerreiro_id: "guerreiro-1",
      grau_de_parentesco: "mãe",
      inicio: new Date().toISOString(),
    });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "mãe");
    await usuario.click(screen.getByRole("button", { name: /continuar para o termo/i }));

    expect(cadastrar).toHaveBeenCalledWith({ nome: "Maria" }, "token-de-trabalho");
    expect(criarVinculo).toHaveBeenCalledWith(
      "responsavel-1",
      { guerreiro_id: "guerreiro-1", grau_de_parentesco: "mãe" },
      "token-de-trabalho",
    );
    expect(aoConcluir).toHaveBeenCalledWith("responsavel-1");
  });

  it("recusa sem o grau de parentesco", async () => {
    const cadastrar = vi.spyOn(responsaveisApi, "cadastrarResponsavelNoEncontro");
    renderizar();
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.click(screen.getByRole("button", { name: /continuar para o termo/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/grau de parentesco/i);
    expect(cadastrar).not.toHaveBeenCalled();
  });

  it("nenhuma tela pede e-mail, senha ou documento", () => {
    renderizar();

    expect(screen.queryByLabelText(/e-mail/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/senha/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/documento/i)).not.toBeInTheDocument();
  });

  it("retomada: falha no vínculo não recria o responsável na nova tentativa", async () => {
    const cadastrar = vi
      .spyOn(responsaveisApi, "cadastrarResponsavelNoEncontro")
      .mockResolvedValue({ id: "responsavel-1", nome: "Maria" });
    const criarVinculo = vi
      .spyOn(responsaveisApi, "criarVinculo")
      .mockRejectedValueOnce(
        new ErroDaApi(500, { codigo: "erro_de_rede", mensagem: "Falha de rede." }),
      )
      .mockResolvedValueOnce({
        id: "vinculo-1",
        responsavel_id: "responsavel-1",
        guerreiro_id: "guerreiro-1",
        grau_de_parentesco: "mãe",
        inicio: new Date().toISOString(),
      });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = userEvent.setup();

    await usuario.type(screen.getByLabelText(/nome do responsável/i), "Maria");
    await usuario.type(screen.getByLabelText(/grau de parentesco/i), "mãe");
    await usuario.click(screen.getByRole("button", { name: /continuar para o termo/i }));
    await screen.findByRole("alert");

    await usuario.click(screen.getByRole("button", { name: /continuar para o termo/i }));

    expect(cadastrar).toHaveBeenCalledTimes(1);
    expect(criarVinculo).toHaveBeenCalledTimes(2);
    expect(aoConcluir).toHaveBeenCalledWith("responsavel-1");
  });
});
