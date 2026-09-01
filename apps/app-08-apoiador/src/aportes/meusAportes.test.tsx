import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { MeusAportesSaida, NecessidadeDeRecurso } from "./api";
import * as aportesApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

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

describe("Meus aportes", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("mostra o total do Poder Sustentador e os aportes homologados", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    const saida: MeusAportesSaida = {
      poder_sustentador_em_moedas: "12.50",
      aportes: [
        {
          id: "aporte-1",
          tipo_de_recurso_id: "tipo-1",
          tipo_de_recurso_nome: "Lanche",
          quantidade: "5.00",
          ponto_de_apoio_id: "ponto-1",
          ponto_de_apoio_nome: "Sede Central",
          valor_em_moedas: "5.00",
          forma: "financeira",
          situacao_de_ressarcimento: "nao_se_aplica",
          data_do_aporte: "2026-06-01",
        },
      ],
    };
    vi.spyOn(aportesApi, "listarMeusAportes").mockResolvedValue(saida);

    await testeDeUsuario.click(screen.getByRole("button", { name: /meus aportes/i }));

    expect(await screen.findByText(/12.50 moedas/i)).toBeInTheDocument();
    expect(screen.getByText(/5.00 moedas/i)).toBeInTheDocument();
    expect(screen.getByText(/lanche/i)).toBeInTheDocument();
    expect(screen.getByText(/sede central/i)).toBeInTheDocument();
  });

  it("sem aporte homologado explica o vazio com o total em zero", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(aportesApi, "listarMeusAportes").mockResolvedValue({
      poder_sustentador_em_moedas: "0.00",
      aportes: [],
    });

    await testeDeUsuario.click(screen.getByRole("button", { name: /meus aportes/i }));

    expect(await screen.findByText(/0.00 moedas/i)).toBeInTheDocument();
    expect(screen.getByText(/ainda não há aporte homologado/i)).toBeInTheDocument();
  });
});

describe("Necessidades em aberto", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  const NECESSIDADE_BASE: NecessidadeDeRecurso = {
    aula_id: "aula-1",
    tipo_de_recurso_id: "tipo-1",
    tipo_de_recurso_nome: "Lanche",
    quantidade_faltante: "3.00",
    valor_em_moedas: "7.50",
    comunidade_virtual_id: "comunidade-1",
    comunidade_virtual_nome: "Guerreira Zeferina",
    ponto_de_apoio_id: "ponto-1",
    ponto_de_apoio_nome: "Sede Central",
    inicio_em: "2026-06-01T13:00:00-03:00",
    fim_em: "2026-06-01T15:00:00-03:00",
  };

  it("traz atividade, comunidade e o que falta em moedas", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(aportesApi, "listarNecessidadesEmAberto").mockResolvedValue([NECESSIDADE_BASE]);

    await testeDeUsuario.click(
      screen.getByRole("button", { name: /necessidades em aberto/i }),
    );

    expect(await screen.findByText(/lanche/i)).toBeInTheDocument();
    expect(screen.getByText(/guerreira zeferina/i)).toBeInTheDocument();
    expect(screen.getByText(/7.50 moedas/i)).toBeInTheDocument();
  });

  it("necessidade sem valor de referência continua na lista, sem valor em moedas", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(aportesApi, "listarNecessidadesEmAberto").mockResolvedValue([
      { ...NECESSIDADE_BASE, valor_em_moedas: null },
    ]);

    await testeDeUsuario.click(
      screen.getByRole("button", { name: /necessidades em aberto/i }),
    );

    expect(await screen.findByText(/sem valor de referência ainda/i)).toBeInTheDocument();
  });

  it("sem necessidade em aberto a tela diz", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(aportesApi, "listarNecessidadesEmAberto").mockResolvedValue([]);

    await testeDeUsuario.click(
      screen.getByRole("button", { name: /necessidades em aberto/i }),
    );

    expect(await screen.findByText(/não há necessidade em aberto/i)).toBeInTheDocument();
  });
});
