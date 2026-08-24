import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as guerreirosApi from "../api/guerreiros";
import { TelaDeCadastro } from "./TelaDeCadastro";

afterEach(() => {
  vi.restoreAllMocks();
});

function nascimentoComIdade(idade: number): string {
  const hoje = new Date();
  const ano = hoje.getFullYear() - idade;
  const mes = String(hoje.getMonth() + 1).padStart(2, "0");
  const dia = String(hoje.getDate()).padStart(2, "0");
  return `${ano}-${mes}-${dia}`;
}

function renderizar(aoConcluir = vi.fn(), aoVoltar = vi.fn()) {
  return render(
    <TelaDeCadastro
      tokenDeTrabalho="token-de-trabalho"
      aulaId="aula-1"
      aoConcluir={aoConcluir}
      aoVoltar={aoVoltar}
    />,
  );
}

async function preencherFormulario(idade = 10, nick = "ZeferinaGuerreira") {
  const usuario = userEvent.setup();
  await usuario.type(screen.getByLabelText(/^nome$/i), "Zeferina");
  await usuario.type(screen.getByLabelText(/^nick$/i), nick);
  await usuario.type(screen.getByLabelText(/data de nascimento/i), nascimentoComIdade(idade));
  await usuario.type(screen.getByLabelText(/características do avatar/i), "trança-e-capa");
  return usuario;
}

describe("cadastro do Guerreiro(a) no encontro", () => {
  it("coleta os cinco dados e cadastra", async () => {
    const cadastrar = vi
      .spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro")
      .mockResolvedValue({
        id: "guerreiro-1",
        nome: "Zeferina",
        nascimento: "2016-01-01",
        nick: "ZeferinaGuerreira",
        avatar: "opaco",
      });
    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = await preencherFormulario();
    await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));

    expect(cadastrar).toHaveBeenCalledWith(
      expect.objectContaining({
        nome: "Zeferina",
        nick: "ZeferinaGuerreira",
        nascimento: nascimentoComIdade(10),
        aula_id: "aula-1",
      }),
      "token-de-trabalho",
    );
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("não conclui faltando qualquer um dos cinco dados", async () => {
    const cadastrar = vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro");
    renderizar();
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/informe o nome/i);
    expect(cadastrar).not.toHaveBeenCalled();
  });

  it("recusa de nick oferece variações aceitas em um toque, sem digitar de novo", async () => {
    vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro")
      .mockRejectedValueOnce(
        new ErroDaApi(422, {
          codigo: "erro_de_validacao",
          mensagem: "Este nick já está em uso.",
          campo: "nick",
          sugestoes: ["ZeferinaGuerreira2", "ZeferinaGuerreira3"],
        }),
      )
      .mockResolvedValueOnce({
        id: "guerreiro-1",
        nome: "Zeferina",
        nascimento: "2016-01-01",
        nick: "ZeferinaGuerreira2",
        avatar: "opaco",
      });

    const aoConcluir = vi.fn();
    renderizar(aoConcluir);
    const usuario = await preencherFormulario();
    await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/já está em uso/i);
    const variacao = await screen.findByRole("button", { name: "ZeferinaGuerreira2" });
    await usuario.click(variacao);

    expect(screen.getByLabelText(/^nick$/i)).toHaveValue("ZeferinaGuerreira2");
    await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));

    expect(guerreirosApi.cadastrarGuerreiroNoEncontro).toHaveBeenLastCalledWith(
      expect.objectContaining({ nick: "ZeferinaGuerreira2" }),
      "token-de-trabalho",
    );
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("idade fora da faixa interrompe o cadastro e orienta a chamar o Mestre ou o Admin", async () => {
    const cadastrar = vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro");
    renderizar();
    const usuario = await preencherFormulario(17);
    await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));

    expect(await screen.findByText(/chame o mestre ou o admin/i)).toBeInTheDocument();
    expect(cadastrar).not.toHaveBeenCalled();
  });

  it("voltar aciona aoVoltar sem cadastrar nada", async () => {
    const cadastrar = vi.spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro");
    const aoVoltar = vi.fn();
    renderizar(vi.fn(), aoVoltar);
    const usuario = userEvent.setup();
    await usuario.click(screen.getByRole("button", { name: /voltar ao início/i }));

    expect(aoVoltar).toHaveBeenCalled();
    expect(cadastrar).not.toHaveBeenCalled();
  });
});
