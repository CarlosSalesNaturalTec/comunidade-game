import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { AVATAR_PADRAO_DO_PROJETO, camadaDoAvatar } from "comum/avatar";
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
  return usuario;
}

/** O objeto do documento 15 §7.2 que a tela gravou, de dentro do campo
 * `avatar` — que leva também a forma de tratamento, campo próprio ao lado
 * dele (design — decisão 3). */
function avatarGravado(chamada: { avatar: string }): Record<string, unknown> {
  const campo = JSON.parse(chamada.avatar);
  return campo.avatar;
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

  it("o cadastro abre com o nome focado, e os campos seguintes não (RF-04-07)", () => {
    renderizar();

    expect(document.activeElement).toBe(screen.getByLabelText(/^nome$/i));
    expect(document.activeElement).not.toBe(screen.getByLabelText(/^nick$/i));
    expect(document.activeElement).not.toBe(screen.getByLabelText(/data de nascimento/i));
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

describe("o avatar do onboarding se compõe no catálogo (`RF-04-07`, documento 15 §7)", () => {
  it("o avatar nasce do catálogo, não de texto livre", () => {
    renderizar();

    // Nenhum campo pede característica em texto livre: a escolha é uma por
    // camada, pelo nome dizível de cada traço.
    expect(screen.queryByLabelText(/características do avatar/i)).not.toBeInTheDocument();

    for (const camada of ["Tom de pele", "Cabelo", "Cor do cabelo", "Roupa", "Acessório"]) {
      const escolha = screen.getByLabelText(camada);
      expect(escolha.tagName).toBe("SELECT");
    }

    const tons = screen.getByLabelText("Tom de pele");
    const nomes = [...tons.querySelectorAll("option")].map((opcao) => opcao.textContent);
    expect(nomes[0]).toBe("Pele retinta");
    expect(nomes).toHaveLength(8);
  });

  it("nasce no avatar padrão do projeto, com o avatar já desenhado", () => {
    const { container } = renderizar();

    expect(screen.getByLabelText("Cabelo")).toHaveValue(AVATAR_PADRAO_DO_PROJETO.cabelo);
    expect(screen.getByLabelText("Roupa")).toHaveValue(AVATAR_PADRAO_DO_PROJETO.roupa);
    expect(container.querySelectorAll("svg.cg-avatar")).toHaveLength(1);
    expect(container.querySelectorAll("svg.cg-avatar g[data-camada]")).toHaveLength(9);
  });

  it("o que se grava é o objeto versionado, e a forma de tratamento fica ao lado dele", async () => {
    const cadastrar = vi
      .spyOn(guerreirosApi, "cadastrarGuerreiroNoEncontro")
      .mockResolvedValue({
        id: "guerreiro-1",
        nome: "Zeferina",
        nascimento: "2016-01-01",
        nick: "ZeferinaGuerreira",
        avatar: "opaco",
      });

    renderizar();
    const usuario = await preencherFormulario();
    const trancas = camadaDoAvatar("cabelo").tracos.find((traco) => traco.id === "trancas");
    if (!trancas) throw new Error("O catálogo perdeu as tranças.");
    await usuario.selectOptions(screen.getByLabelText("Cabelo"), trancas.id);
    await usuario.selectOptions(screen.getByLabelText("Tom de pele"), "t3");
    await usuario.selectOptions(screen.getByLabelText("Forma de tratamento"), "guerreira");
    await usuario.click(screen.getByRole("button", { name: /concluir cadastro/i }));

    const enviado = cadastrar.mock.calls[0][0] as unknown as { avatar: string };
    expect(JSON.parse(enviado.avatar).formaDeTratamento).toBe("guerreira");
    expect(avatarGravado(enviado)).toEqual({
      ...AVATAR_PADRAO_DO_PROJETO,
      cabelo: "trancas",
      tom: "t3",
    });
    // Nada de texto livre vai gravado: o que sai é só o objeto do §7.2.
    expect(enviado.avatar).not.toMatch(/caracteristicasDoAvatar/);
  });

  it("compor não depende de rede", async () => {
    const rede = vi.spyOn(globalThis, "fetch");
    const { container } = renderizar();
    const usuario = userEvent.setup();

    await usuario.selectOptions(screen.getByLabelText("Cabelo"), "dreads");
    await usuario.selectOptions(screen.getByLabelText("Acessório"), "oculos");

    expect(rede).not.toHaveBeenCalled();
    const desenho = container.querySelector("svg.cg-avatar");
    expect(desenho?.querySelector("image")).toBeNull();
    expect(desenho?.outerHTML).not.toMatch(/https?:|url\(/);
  });
});
