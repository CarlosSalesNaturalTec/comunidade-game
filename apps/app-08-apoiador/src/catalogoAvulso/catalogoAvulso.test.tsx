import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { MinhaOfertaDeCatalogoAvulso } from "./api";
import * as catalogoApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const OFERTA_BASE: MinhaOfertaDeCatalogoAvulso = {
  id: "item-1",
  nome: "Kit de Robótica",
  tipo_de_recurso_id: "tipo-1",
  estoque: "5",
  comunidade_virtual_id: "comunidade-1",
  ponto_de_apoio_id: "ponto-1",
  origem_do_cadastro: "apoiador",
  situacao_de_homologacao: "pendente",
  homologacao_motivo: null,
  ativo: false,
  preco_em_pontos_extras: null,
  preco_de_referencia_ausente: false,
  quantidade_faltante: null,
  quantidade_de_trocas: 0,
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
  await screen.findByRole("button", { name: /ofertar item/i });
  return testeDeUsuario;
}

describe("oferta ao catálogo avulso", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("a tela de oferta não tem campo de preço e declara a tabela da gestão e a homologação do Admin", async () => {
    const testeDeUsuario = await entrarComoApoiador();

    await testeDeUsuario.click(screen.getByRole("button", { name: /^ofertar item$/i }));

    expect(screen.queryByLabelText(/preço/i)).not.toBeInTheDocument();
    expect(screen.getByText(/tabela de referência da gestão/i)).toBeInTheDocument();
    expect(screen.getByText(/homologado por um admin/i)).toBeInTheDocument();
  });

  it("nenhuma tela de catálogo avulso oferece campo de mensagem, telefone ou e-mail", async () => {
    await entrarComoApoiador();

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/telefone/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/e-mail/i)).not.toBeInTheDocument();
  });

  it("mostra o item pendente na lista de minhas ofertas", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(catalogoApi, "listarMinhasOfertas").mockResolvedValue([OFERTA_BASE]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^minhas ofertas$/i }));

    expect(await screen.findByText(/pendente de homologação/i)).toBeInTheDocument();
  });

  it("mostra o item recusado com o motivo", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(catalogoApi, "listarMinhasOfertas").mockResolvedValue([
      {
        ...OFERTA_BASE,
        situacao_de_homologacao: "recusado",
        homologacao_motivo: "Item fora da política de recompensas.",
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^minhas ofertas$/i }));

    expect(await screen.findByText(/fora da política de recompensas/i)).toBeInTheDocument();
  });

  it("item ativo mostra estoque restante, preço e quantas trocas", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(catalogoApi, "listarMinhasOfertas").mockResolvedValue([
      {
        ...OFERTA_BASE,
        situacao_de_homologacao: "homologado",
        ativo: true,
        estoque: "3",
        preco_em_pontos_extras: 20,
        quantidade_de_trocas: 3,
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^minhas ofertas$/i }));

    expect(await screen.findByText(/estoque restante: 3/i)).toBeInTheDocument();
    expect(screen.getByText(/preço: 20 pontos extras/i)).toBeInTheDocument();
    expect(screen.getByText(/trocas entregues: 3/i)).toBeInTheDocument();
  });

  it("item inativo por falta de lastro mostra o que falta", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(catalogoApi, "listarMinhasOfertas").mockResolvedValue([
      {
        ...OFERTA_BASE,
        situacao_de_homologacao: "homologado",
        ativo: false,
        quantidade_faltante: "6",
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^minhas ofertas$/i }));

    expect(await screen.findByText(/faltam 6 unidades de lastro/i)).toBeInTheDocument();
  });

  it("item inativo por falta de preço de referência mostra o que falta", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(catalogoApi, "listarMinhasOfertas").mockResolvedValue([
      {
        ...OFERTA_BASE,
        situacao_de_homologacao: "homologado",
        ativo: false,
        preco_de_referencia_ausente: true,
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^minhas ofertas$/i }));

    expect(await screen.findByText(/não há preço de referência vigente/i)).toBeInTheDocument();
  });

  it("nenhuma resposta identifica quem trocou nem oferece campo de contato", async () => {
    const testeDeUsuario = await entrarComoApoiador();
    vi.spyOn(catalogoApi, "listarMinhasOfertas").mockResolvedValue([
      {
        ...OFERTA_BASE,
        situacao_de_homologacao: "homologado",
        ativo: true,
        estoque: "3",
        preco_em_pontos_extras: 20,
        quantidade_de_trocas: 3,
      },
    ]);

    await testeDeUsuario.click(screen.getByRole("button", { name: /^minhas ofertas$/i }));
    await screen.findByText(/trocas entregues: 3/i);

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/telefone/i)).not.toBeInTheDocument();
    expect(screen.queryByText(/nick/i)).not.toBeInTheDocument();
  });
});
