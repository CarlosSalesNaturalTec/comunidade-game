import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { IdentidadeDoApoiador } from "./api";
import * as identidadeApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const IDENTIDADE_ABAIXO_DO_PISO: IdentidadeDoApoiador = {
  nick: "ApoiadorDoPreCadastro",
  avatar: null,
  moedas_acumuladas: "5.00",
  avatar_proprio_liberado: false,
  moedas_faltantes_para_avatar_proprio: "5.00",
};

const IDENTIDADE_NO_PISO: IdentidadeDoApoiador = {
  nick: "ApoiadorDoPreCadastro",
  avatar: null,
  moedas_acumuladas: "10.00",
  avatar_proprio_liberado: true,
  moedas_faltantes_para_avatar_proprio: null,
};

async function entrarNaIdentidade(identidade: IdentidadeDoApoiador) {
  vi.spyOn(authApi, "loginPorCredencial").mockResolvedValue({
    token: "token-do-apoiador",
    expira_em: new Date().toISOString(),
    papel: "apoiador",
  });
  vi.spyOn(authApi, "eu").mockResolvedValue({
    persona_id: "algum-id",
    papel: "apoiador",
    permissoes: {},
  });
  vi.spyOn(identidadeApi, "lerMinhaIdentidade").mockResolvedValue(identidade);

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "apoiadora");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.click(
    await screen.findByRole("button", { name: /identidade pública/i }),
  );
  await screen.findByRole("heading", { name: /identidade pública/i });
  return testeDeUsuario;
}

describe("identidade pública do Apoiador", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("o nick do pré-cadastro já vem preenchido, sem ser pedido de novo", async () => {
    await entrarNaIdentidade(IDENTIDADE_ABAIXO_DO_PISO);

    expect(screen.getByLabelText(/^nick$/i)).toHaveValue("ApoiadorDoPreCadastro");
  });

  it("nick já em uso é recusado com sugestões, sem revelar de quem é", async () => {
    const testeDeUsuario = await entrarNaIdentidade(IDENTIDADE_ABAIXO_DO_PISO);
    vi.spyOn(identidadeApi, "gravarMinhaIdentidade").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Este nick já está em uso.",
        campo: "nick",
      }),
    );
    vi.spyOn(identidadeApi, "conferirDisponibilidadeDeNick").mockResolvedValue({
      disponivel: false,
      sugestoes: ["NickNovo2", "NickNovo3"],
    });

    await testeDeUsuario.clear(screen.getByLabelText(/^nick$/i));
    await testeDeUsuario.type(screen.getByLabelText(/^nick$/i), "NickEmUso");
    await testeDeUsuario.click(screen.getByRole("button", { name: /gravar nick/i }));

    expect(await screen.findByText(/nicknovo2/i)).toBeInTheDocument();
    expect(screen.getByText(/já está em uso/i)).toBeInTheDocument();
    // A recusa nunca diz de quem é o nick — só a mensagem fixa e as
    // sugestões de variação (`RN-01-22`).
    expect(screen.queryByText(/pertence a|de outro|persona_id/i)).not.toBeInTheDocument();
  });

  it("com 5 moedas o card mostra o avatar padrão e diz quanto falta, sem pedir aporte", async () => {
    await entrarNaIdentidade(IDENTIDADE_ABAIXO_DO_PISO);

    expect(screen.getByRole("img", { name: /avatar padrão do projeto/i })).toBeInTheDocument();
    expect(screen.getByText(/faltam 5\.00 moedas/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/avatar \(endereço/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/faça um aporte/i)).not.toBeInTheDocument();
  });

  it("com 10 moedas o envio do avatar próprio está aberto", async () => {
    await entrarNaIdentidade(IDENTIDADE_NO_PISO);

    expect(screen.getByLabelText(/avatar \(endereço/i)).toBeInTheDocument();
  });

  it("a recusa 409 do núcleo aparece com quanto falta", async () => {
    const testeDeUsuario = await entrarNaIdentidade(IDENTIDADE_NO_PISO);
    vi.spyOn(identidadeApi, "gravarMinhaIdentidade").mockRejectedValue(
      new ErroDaApi(409, {
        codigo: "piso_de_moedas_nao_alcancado",
        mensagem: "Faltam 3.00 moedas acumuladas para liberar o avatar próprio.",
      }),
    );

    await testeDeUsuario.type(
      screen.getByLabelText(/avatar \(endereço/i),
      "https://exemplo.org/avatar.png",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /gravar avatar/i }));

    expect(await screen.findByText(/faltam 3\.00 moedas/i)).toBeInTheDocument();
  });

  it("troca nick e avatar já gravados", async () => {
    const testeDeUsuario = await entrarNaIdentidade(IDENTIDADE_NO_PISO);
    vi.spyOn(identidadeApi, "gravarMinhaIdentidade").mockResolvedValue({
      ...IDENTIDADE_NO_PISO,
      nick: "NickTrocado",
      avatar: "https://exemplo.org/avatar-novo.png",
    });

    await testeDeUsuario.clear(screen.getByLabelText(/^nick$/i));
    await testeDeUsuario.type(screen.getByLabelText(/^nick$/i), "NickTrocado");
    await testeDeUsuario.click(screen.getByRole("button", { name: /gravar nick/i }));
    expect(await screen.findByText(/nick gravado/i)).toBeInTheDocument();

    await testeDeUsuario.type(
      screen.getByLabelText(/avatar \(endereço/i),
      "https://exemplo.org/avatar-novo.png",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /gravar avatar/i }));
    expect(await screen.findByText(/avatar gravado/i)).toBeInTheDocument();
  });

  it("nenhuma saída da tela mostra valor em reais", async () => {
    await entrarNaIdentidade(IDENTIDADE_ABAIXO_DO_PISO);

    // A tela só declara, em texto fixo, que nunca mostra reais — o que ela
    // nunca faz é exibir um valor de moeda corrente (`RN-14-09`).
    expect(screen.queryByText(/r\$\s*\d/i)).not.toBeInTheDocument();
  });
});
