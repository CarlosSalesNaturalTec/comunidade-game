import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { DesafioExtra } from "./api";
import * as desafiosApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const DESAFIO_BASE: DesafioExtra = {
  id: "desafio-1",
  trilha_id: "trilha-1",
  missao_id: null,
  modalidade: "aberto",
  nick_do_destinatario: null,
  justificativa_do_vinculo: null,
  tipo_de_recurso_id: "tipo-1",
  ponto_de_apoio_id: "ponto-1",
  quantidade_disponivel: 5,
  quantidade_restante: 5,
  criterio_de_atribuicao: "Quem entregar primeiro.",
  pontos_extras: 5,
  formato: "on_line",
  custeio: "saldo_de_recurso",
  aporte_id: null,
  vigencia_inicio: "2026-01-01",
  vigencia_fim: "2026-12-31",
  situacao: "em_validacao_do_mestre",
  motivo_da_recusa: null,
  lastro_provido: true,
  lastro_faltante: null,
};

async function entrarComoApoiador() {
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

  render(<App />);
  const testeDeUsuario = userEvent.setup();
  await testeDeUsuario.click(await screen.findByRole("button", { name: /^entrar$/i }));
  await testeDeUsuario.type(await screen.findByLabelText(/^usuário$/i), "apoiadora");
  await testeDeUsuario.type(screen.getByLabelText(/^senha$/i), "senha-123");
  await testeDeUsuario.click(screen.getByRole("button", { name: /^entrar$/i }));
  await screen.findByRole("button", { name: /propor desafio extra/i });
  return testeDeUsuario;
}

describe("proposição do desafio extra", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a tela recusa pontos extras acima do teto, sem chamar o núcleo", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    const chamada = vi.spyOn(desafiosApi, "proporDesafioExtra");

    const campoDePontos = screen.getByLabelText(/pontos extras/i);
    await testeDeUsuario.clear(campoDePontos);
    await testeDeUsuario.type(campoDePontos, "11");
    await testeDeUsuario.click(screen.getByRole("button", { name: /^propor desafio$/i }));

    expect(await screen.findByText(/teto é 10 pontos/i)).toBeInTheDocument();
    expect(chamada).not.toHaveBeenCalled();
  });

  it("proposta direcionada com nick desconhecido é aceita sem indicar que ele não existe", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(desafiosApi, "proporDesafioExtra").mockResolvedValue({
      ...DESAFIO_BASE,
      modalidade: "direcionado",
      nick_do_destinatario: "nick-que-nao-existe",
    });

    await testeDeUsuario.type(screen.getByLabelText(/^trilha$/i), "trilha-1");
    await testeDeUsuario.type(screen.getByLabelText(/tipo de recurso/i), "tipo-1");
    await testeDeUsuario.type(screen.getByLabelText(/ponto de apoio/i), "ponto-1");
    await testeDeUsuario.type(
      screen.getByLabelText(/critério de atribuição/i),
      "Primeiro a entregar.",
    );
    await testeDeUsuario.selectOptions(screen.getByLabelText(/^modalidade$/i), "direcionado");
    await testeDeUsuario.type(
      screen.getByLabelText(/nick do destinatário/i),
      "nick-que-nao-existe",
    );
    await testeDeUsuario.type(
      screen.getByLabelText(/justificativa do vínculo/i),
      "É meu vizinho.",
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /^propor desafio$/i }));

    expect(await screen.findByText(/proposta registrada/i)).toBeInTheDocument();
    expect(screen.queryByText(/não existe/i)).not.toBeInTheDocument();
  });

  it("nenhuma tela de desafio oferece campo de mensagem, telefone ou e-mail", async () => {
    await entrarComoApoiador();

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/telefone/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/e-mail/i)).not.toBeInTheDocument();
  });
});

describe("acompanhamento do desafio extra", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("mostra o que falta de lastro quando ele não está provido", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(desafiosApi, "listarMeusDesafiosExtras").mockResolvedValue([
      {
        ...DESAFIO_BASE,
        lastro_provido: false,
        lastro_faltante: "Falta saldo suficiente do tipo de recurso declarado.",
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /meus desafios/i }));

    expect(await screen.findByText(/falta saldo suficiente/i)).toBeInTheDocument();
  });

  it("desafio publicado mostra a quantidade restante e nenhuma edição", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(desafiosApi, "listarMeusDesafiosExtras").mockResolvedValue([
      { ...DESAFIO_BASE, situacao: "publicado", quantidade_restante: 3 },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /meus desafios/i }));

    expect(await screen.findByText(/recompensas restantes: 3/i)).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /editar/i })).not.toBeInTheDocument();
  });

  it("nenhuma resposta identifica Guerreiro(a) nem oferece campo de mensagem", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(desafiosApi, "listarMeusDesafiosExtras").mockResolvedValue([
      {
        ...DESAFIO_BASE,
        modalidade: "direcionado",
        nick_do_destinatario: "nick-do-destinatario",
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /meus desafios/i }));
    await screen.findByText(/nick-do-destinatario/i);

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/telefone/i)).not.toBeInTheDocument();
  });
});
