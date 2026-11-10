import { act, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { ProvedorDeSessao } from "comum/autenticacao";
import * as autenticacaoApi from "comum/autenticacao/api";
import { AVATAR_PADRAO_DO_PROJETO, escreverAvatar } from "comum/avatar";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as carteiraApi from "../api/carteira";
import { AlterarMeuAvatar } from "./AlterarMeuAvatar";

const CHAVE_DE_SESSAO = "app-05:teste-alterar-meu-avatar";

async function renderizar(avatar: string | undefined) {
  sessionStorage.setItem(CHAVE_DE_SESSAO, "token-do-guerreiro");
  vi.spyOn(autenticacaoApi, "eu").mockResolvedValue({
    persona_id: "guerreiro-1",
    papel: "guerreiro",
    permissoes: {},
    nick: "Zeferina",
    avatar,
  });
  const aoSalvar = vi.fn();
  const aoVoltar = vi.fn();
  await act(async () => {
    render(
      <ProvedorDeSessao chaveDeArmazenamento={CHAVE_DE_SESSAO}>
        <AlterarMeuAvatar aoSalvar={aoSalvar} aoVoltar={aoVoltar} />
      </ProvedorDeSessao>,
    );
  });
  return { aoSalvar, aoVoltar };
}

function valorDe(rotulo: string): string {
  return (screen.getByLabelText(rotulo) as HTMLSelectElement).value;
}

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("o Guerreiro(a) altera o próprio avatar (`RF-05-51`)", () => {
  it("a montagem abre no avatar vigente, com as nove camadas", async () => {
    await renderizar(JSON.stringify(escreverAvatar({ fundo: "moeda-100", cabelo: "dreads" })));

    expect(screen.getAllByRole("combobox")).toHaveLength(9);
    expect(valorDe("Cor do fundo")).toBe("moeda-100");
    expect(valorDe("Cabelo")).toBe("dreads");
  });

  it("sem avatar gravado, ou com texto que não é do catálogo, abre no padrão do projeto", async () => {
    await renderizar("cabelo cacheado e boné");

    expect(valorDe("Cor do fundo")).toBe(AVATAR_PADRAO_DO_PROJETO.fundo);
    expect(valorDe("Roupa")).toBe(AVATAR_PADRAO_DO_PROJETO.roupa);
  });

  it("salvar grava pela rota e preserva a forma de tratamento", async () => {
    const alterar = vi
      .spyOn(carteiraApi, "alterarMeuAvatar")
      .mockResolvedValue({ avatar: "gravado" });
    const { aoSalvar } = await renderizar(
      JSON.stringify({ formaDeTratamento: "guerreiro", avatar: escreverAvatar({}) }),
    );
    const usuario = userEvent.setup();

    await usuario.selectOptions(screen.getByLabelText("Cor do fundo"), "ponto-100");
    await usuario.click(screen.getByRole("button", { name: "Salvar o meu avatar" }));

    expect(alterar).toHaveBeenCalledTimes(1);
    const [token, texto] = alterar.mock.calls[0];
    expect(token).toBe("token-do-guerreiro");
    const gravado = JSON.parse(texto);
    expect(gravado.formaDeTratamento).toBe("guerreiro");
    expect(gravado.avatar.fundo).toBe("ponto-100");
    expect(aoSalvar).toHaveBeenCalledTimes(1);
  });

  it("trocar traço e voltar sem salvar não chama a rota", async () => {
    const alterar = vi.spyOn(carteiraApi, "alterarMeuAvatar");
    const { aoVoltar } = await renderizar(JSON.stringify(escreverAvatar({})));
    const usuario = userEvent.setup();

    await usuario.selectOptions(screen.getByLabelText("Cor do fundo"), "ponto-100");
    await usuario.click(screen.getByRole("button", { name: "Voltar sem salvar" }));

    expect(alterar).not.toHaveBeenCalled();
    expect(aoVoltar).toHaveBeenCalledTimes(1);
  });

  it("falha ao salvar é dita em linguagem de criança e mantém o que foi escolhido", async () => {
    vi.spyOn(carteiraApi, "alterarMeuAvatar").mockRejectedValue(new Error("rede fora"));
    const { aoSalvar } = await renderizar(JSON.stringify(escreverAvatar({})));
    const usuario = userEvent.setup();

    await usuario.selectOptions(screen.getByLabelText("Cor do fundo"), "ponto-100");
    await usuario.click(screen.getByRole("button", { name: "Salvar o meu avatar" }));

    expect(
      await screen.findByText(
        "Não deu para salvar o seu avatar agora. Tente de novo em instantes.",
      ),
    ).toBeInTheDocument();
    expect(valorDe("Cor do fundo")).toBe("ponto-100");
    expect(aoSalvar).not.toHaveBeenCalled();
  });

  it("recusa de sessão ao salvar encerra a sessão", async () => {
    vi.spyOn(carteiraApi, "alterarMeuAvatar").mockRejectedValue(
      new ErroDaApi(401, { codigo: "sessao_invalida", mensagem: "Sessão inválida." }),
    );
    await renderizar(JSON.stringify(escreverAvatar({})));
    const usuario = userEvent.setup();

    await usuario.click(screen.getByRole("button", { name: "Salvar o meu avatar" }));

    expect(sessionStorage.getItem(CHAVE_DE_SESSAO)).toBeNull();
  });
});
