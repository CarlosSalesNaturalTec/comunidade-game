import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { AporteDeclarado, NecessidadeDeRecurso } from "./api";
import * as aportesApi from "./api";

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
  await testeDeUsuario.click(screen.getByRole("button", { name: /^declarar aporte$/i }));
  return testeDeUsuario;
}

describe("declaração do aporte", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(aportesApi, "listarNecessidadesEmAberto").mockResolvedValue([NECESSIDADE_BASE]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a escada troca com o perfil declarado", async () => {
    const testeDeUsuario = await entrarComoApoiador();

    const selectDaEscada = (await screen.findByLabelText(
      /^valor sugerido$/i,
    )) as HTMLSelectElement;
    expect(selectDaEscada.options[0]?.textContent).toMatch(/1 moeda\b/);

    await testeDeUsuario.click(screen.getByLabelText(/pessoa jurídica/i));

    expect(selectDaEscada.options[0]?.textContent).toMatch(/50 moedas/);
  });

  it("o valor livre é aceito com o equivalente em moedas", async () => {
    const testeDeUsuario = await entrarComoApoiador();

    await testeDeUsuario.click(screen.getByLabelText("Um valor livre"));
    await testeDeUsuario.type(screen.getByLabelText("Valor livre (R$)"), "5");

    expect(await screen.findByText(/equivalente a 0,5 moeda/i)).toBeInTheDocument();
  });

  it("declara a partir de uma necessidade escolhida", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    const chamada = vi
      .spyOn(aportesApi, "declararAporte")
      .mockResolvedValue({} as AporteDeclarado);

    await testeDeUsuario.click(screen.getByLabelText(/uma necessidade publicada/i));
    await testeDeUsuario.selectOptions(
      await screen.findByLabelText(/^necessidade$/i),
      "aula-1",
    );
    await testeDeUsuario.upload(
      screen.getByLabelText(/comprovante da transferência/i),
      arquivoDeComprovante(),
    );
    await testeDeUsuario.click(screen.getByRole("button", { name: /^enviar declaração$/i }));

    expect(await screen.findByText(/registrada na fila da gestão/i)).toBeInTheDocument();
    expect(chamada).toHaveBeenCalledWith(
      expect.objectContaining({ origem_da_escolha: "necessidade", aula_id: "aula-1" }),
      "token-do-apoiador",
    );
  });

  it("sem comprovante a declaração não é enviada", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    const chamada = vi.spyOn(aportesApi, "declararAporte");

    await testeDeUsuario.click(screen.getByRole("button", { name: /^enviar declaração$/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/pdf, jpg ou png/i);
    expect(chamada).not.toHaveBeenCalled();
  });

  it("declara que o aporte entra pendente antes do envio", async () => {
    await entrarComoApoiador();

    expect(screen.getByText(/pendente de homologação/i)).toBeInTheDocument();
    expect(screen.getByText(/não vira moeda/i)).toBeInTheDocument();
  });

  it("orienta a procurar a gestão para material, serviço ou divulgação", async () => {
    const testeDeUsuario = await entrarComoApoiador();

    await testeDeUsuario.click(screen.getByLabelText(/sem transferir dinheiro/i));

    expect(await screen.findByText(/entram pelo cadastro do admin/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /^enviar declaração$/i }),
    ).not.toBeInTheDocument();
  });
});

describe("situação das declarações", () => {
  beforeEach(() => {
    limparToken();
    vi.spyOn(aportesApi, "listarNecessidadesEmAberto").mockResolvedValue([]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  const DECLARACAO_BASE: AporteDeclarado = {
    id: "declaracao-1",
    valor_declarado: "50.00",
    origem_da_escolha: "valor_livre",
    aula_id: null,
    tipo_de_recurso_id: null,
    missao_do_apoiador_id: null,
    situacao: "pendente",
    registrado_em: "2026-06-01T12:00:00Z",
    motivo_da_recusa: null,
  };

  async function abrirSituacao() {
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
    await testeDeUsuario.click(
      screen.getByRole("button", { name: /situação das declarações/i }),
    );
    return testeDeUsuario;
  }

  it("mostra as três situações, com o valor em moedas", async () => {
    vi.spyOn(aportesApi, "listarMinhasDeclaracoesDeAporte").mockResolvedValue([
      { ...DECLARACAO_BASE, id: "1", situacao: "pendente" },
      { ...DECLARACAO_BASE, id: "2", situacao: "homologada" },
      {
        ...DECLARACAO_BASE,
        id: "3",
        situacao: "recusada",
        motivo_da_recusa: "Comprovante ilegível.",
      },
    ]);

    await abrirSituacao();
    const cartoes = await screen.findAllByRole("article");

    expect(cartoes).toHaveLength(3);
    expect(cartoes[0]).toHaveTextContent(/situação: pendente/i);
    expect(cartoes[1]).toHaveTextContent(/situação: homologada/i);
    expect(cartoes[2]).toHaveTextContent(/situação: recusada/i);
    expect(cartoes[2]).toHaveTextContent(/comprovante ilegível/i);
    expect(screen.getAllByText(/5 moedas/i).length).toBeGreaterThan(0);
  });

  it("não oferece nenhum ato sobre a situação", async () => {
    vi.spyOn(aportesApi, "listarMinhasDeclaracoesDeAporte").mockResolvedValue([
      DECLARACAO_BASE,
    ]);

    await abrirSituacao();
    await screen.findAllByRole("article");

    expect(screen.queryByRole("button", { name: /homologar/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /editar/i })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /reenviar/i })).not.toBeInTheDocument();
  });
});
