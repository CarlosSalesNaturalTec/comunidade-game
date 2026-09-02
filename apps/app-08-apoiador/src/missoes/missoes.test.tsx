import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { AporteDeclarado } from "../aportes/api";
import * as aportesApi from "../aportes/api";
import type { MissaoDoApoiador, MissoesAgrupadas } from "./api";
import * as missoesApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

function arquivoDeComprovante(nome = "comprovante.pdf", tipo = "application/pdf") {
  return new File(["conteudo do comprovante"], nome, { type: tipo });
}

const MISSAO_BASE: MissaoDoApoiador = {
  id: "missao-1",
  nivel_de_necessidade: "acontecer",
  titulo: "O lanche do encontro",
  o_que_se_pede: "Um lanche para vinte crianças",
  quantidade: "100.00",
  falta: "40.00",
  coberto: "60.00",
  prazo: "2026-12-01",
  selo_nome: "Lanche garantido",
  selo_familia: "frente",
};

const AGRUPADAS_VAZIAS: MissoesAgrupadas = {
  existir: [],
  acontecer: [],
  reconhecer: [],
  permanecer: [],
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
  await testeDeUsuario.click(screen.getByRole("button", { name: /^missões$/i }));
  return testeDeUsuario;
}

describe("Tela de missões", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("agrupa as missões por nível e mostra o coberto sem identificar quem cobriu", async () => {
    vi.spyOn(missoesApi, "listarMissoesAbertas").mockResolvedValue({
      ...AGRUPADAS_VAZIAS,
      acontecer: [MISSAO_BASE],
    });

    await entrarComoApoiador();

    expect(await screen.findByRole("heading", { name: "Acontecer" })).toBeInTheDocument();
    expect(screen.getByText(/o lanche do encontro/i)).toBeInTheDocument();
    expect(screen.getByText(/falta 40.00 moedas/i)).toBeInTheDocument();
    expect(screen.getByText(/já coberto: 60.00/i)).toBeInTheDocument();
    expect(screen.queryByText(/nick/i)).not.toBeInTheDocument();
  });

  it("sem missão aberta a tela diz", async () => {
    vi.spyOn(missoesApi, "listarMissoesAbertas").mockResolvedValue(AGRUPADAS_VAZIAS);

    await entrarComoApoiador();

    expect(await screen.findByText(/não há missão aberta/i)).toBeInTheDocument();
  });

  it("nenhuma tela ordena ou compara por valor aportado", async () => {
    vi.spyOn(missoesApi, "listarMissoesAbertas").mockResolvedValue({
      ...AGRUPADAS_VAZIAS,
      acontecer: [MISSAO_BASE],
    });

    await entrarComoApoiador();
    await screen.findByText(/o lanche do encontro/i);

    expect(screen.queryByText(/ranking/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/posição/i)).not.toBeInTheDocument();
  });

  it("escolher uma missão abre a declaração, avisando que ela entra pendente", async () => {
    vi.spyOn(missoesApi, "listarMissoesAbertas").mockResolvedValue({
      ...AGRUPADAS_VAZIAS,
      acontecer: [MISSAO_BASE],
    });
    const testeDeUsuario = await entrarComoApoiador();
    await screen.findByText(/o lanche do encontro/i);

    await testeDeUsuario.click(screen.getByRole("button", { name: /cobrir esta missão/i }));

    expect(
      screen.getByRole("heading", { name: /cobrir: o lanche do encontro/i }),
    ).toBeInTheDocument();
    expect(screen.getByText(/pendente de homologação/i)).toBeInTheDocument();
    expect(screen.getByText(/não abate o que falta/i)).toBeInTheDocument();
  });

  it("declara o aporte pela missão escolhida, inteira ou em parte", async () => {
    vi.spyOn(missoesApi, "listarMissoesAbertas").mockResolvedValue({
      ...AGRUPADAS_VAZIAS,
      acontecer: [MISSAO_BASE],
    });
    const chamada = vi
      .spyOn(aportesApi, "declararAporte")
      .mockResolvedValue({} as AporteDeclarado);
    const testeDeUsuario = await entrarComoApoiador();
    await screen.findByText(/o lanche do encontro/i);
    await testeDeUsuario.click(screen.getByRole("button", { name: /cobrir esta missão/i }));

    await testeDeUsuario.clear(screen.getByLabelText(/valor a cobrir/i));
    await testeDeUsuario.type(screen.getByLabelText(/valor a cobrir/i), "50");
    await testeDeUsuario.upload(
      screen.getByLabelText(/comprovante da transferência/i),
      arquivoDeComprovante(),
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /^enviar declaração$/i }));

    expect(await screen.findByText(/registrada na fila da gestão/i)).toBeInTheDocument();
    expect(chamada).toHaveBeenCalledWith(
      expect.objectContaining({
        origem_da_escolha: "missao",
        missao_do_apoiador_id: "missao-1",
        valor_declarado: 50,
      }),
      "token-do-apoiador",
    );
  });
});
