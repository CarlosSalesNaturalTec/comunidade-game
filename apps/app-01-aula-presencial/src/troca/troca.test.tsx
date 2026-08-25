import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as sessaoApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App, { CHAVE_DE_SESSAO_DE_TRABALHO } from "../App";
import type { AulaVigente } from "../api/aulas";
import * as aulasApi from "../api/aulas";
import type { ItemDeCatalogoAvulso } from "../api/catalogoAvulso";
import * as catalogoAvulsoApi from "../api/catalogoAvulso";
import type { PontosExtras } from "../api/pontosExtras";
import * as pontosExtrasApi from "../api/pontosExtras";
import * as trocasApi from "../api/trocas";
import { TelaDeTroca } from "./TelaDeTroca";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: ({
      aoReceberIdToken,
    }: {
      aoReceberIdToken: (t: string) => void;
    }) => (
      <button type="button" onClick={() => aoReceberIdToken("id-token-de-teste")}>
        Entrar com Google
      </button>
    ),
  };
});

function aula(sobrescreve: Partial<AulaVigente> = {}): AulaVigente {
  return {
    id: "aula-1",
    comunidade_virtual_id: "comunidade-1",
    inicio_em: "2026-08-24T10:00:00-03:00",
    fim_em: "2026-08-24T12:00:00-03:00",
    ...sobrescreve,
  };
}

function item(sobrescreve: Partial<ItemDeCatalogoAvulso> = {}): ItemDeCatalogoAvulso {
  return {
    id: "item-1",
    nome: "Caderno de desenho",
    tipo_de_recurso_id: "tipo-1",
    estoque: "5",
    comunidade_virtual_id: "comunidade-1",
    ponto_de_apoio_id: "ponto-1",
    origem_do_cadastro: "mestre",
    situacao_de_homologacao: "dispensada",
    homologacao_motivo: null,
    ativo: true,
    preco_em_pontos_extras: 40,
    preco_de_referencia_ausente: false,
    quantidade_faltante: null,
    ...sobrescreve,
  };
}

function pontos(sobrescreve: Partial<PontosExtras> = {}): PontosExtras {
  return { acumulado: 300, saldo_disponivel: 100, ...sobrescreve };
}

async function entrarComoMestre() {
  vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
    token: "token-do-mestre",
    expira_em: new Date().toISOString(),
    papel: "mestre",
  });
  vi.spyOn(sessaoApi, "eu").mockResolvedValue({
    persona_id: "mestre-1",
    papel: "mestre",
    permissoes: {},
  });
  vi.spyOn(aulasApi, "listarAulasVigentes").mockResolvedValue({
    itens: [aula()],
    proximo_cursor: null,
  });
  const usuario = userEvent.setup();
  const renderizado = render(<App />);
  await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));
  await screen.findByText(/o que você quer fazer/i);
  return { usuario, ...renderizado };
}

async function entrarComoAdmin() {
  vi.spyOn(sessaoApi, "loginSocial").mockResolvedValue({
    token: "token-do-admin",
    expira_em: new Date().toISOString(),
    papel: "admin",
  });
  vi.spyOn(sessaoApi, "eu").mockResolvedValue({
    persona_id: "admin-1",
    papel: "admin",
    permissoes: {},
  });
  vi.spyOn(aulasApi, "listarAulasVigentes").mockResolvedValue({
    itens: [aula()],
    proximo_cursor: null,
  });
  const usuario = userEvent.setup();
  render(<App />);
  await usuario.click(await screen.findByRole("button", { name: /entrar com google/i }));
  await screen.findByText(/o que você quer fazer/i);
  return usuario;
}

beforeEach(() => {
  limparToken(CHAVE_DE_SESSAO_DE_TRABALHO);
  limparToken("app-01:sessao-guerreiro");
  sessionStorage.removeItem("app-01:sessao-trabalho:aula");
});

afterEach(() => {
  vi.restoreAllMocks();
  sessionStorage.clear();
});

describe("o momento de troca", () => {
  it("o Admin não recebe o controle de abertura", async () => {
    await entrarComoAdmin();

    expect(
      screen.queryByRole("button", { name: /abrir o momento de troca/i }),
    ).not.toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /troca por recompensa/i }),
    ).not.toBeInTheDocument();
  });

  it("o Mestre abre o momento e o terceiro caminho aparece", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([]);
    const { usuario } = await entrarComoMestre();

    expect(
      screen.queryByRole("button", { name: /troca por recompensa/i }),
    ).not.toBeInTheDocument();

    await usuario.click(screen.getByRole("button", { name: /abrir o momento de troca/i }));

    expect(
      await screen.findByRole("button", { name: /troca por recompensa/i }),
    ).toBeInTheDocument();
    expect(catalogoAvulsoApi.listarCatalogoAvulso).toHaveBeenCalledWith("token-do-mestre");
  });

  it("sem rede o momento não abre e avisa que a troca exige rede", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockRejectedValue(
      new TypeError("fetch failed"),
    );
    const { usuario } = await entrarComoMestre();

    await usuario.click(screen.getByRole("button", { name: /abrir o momento de troca/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/exige rede/i);
    expect(
      screen.queryByRole("button", { name: /troca por recompensa/i }),
    ).not.toBeInTheDocument();
  });

  it("a recarga fecha o momento de novo", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([]);
    const { usuario, unmount } = await entrarComoMestre();
    await usuario.click(screen.getByRole("button", { name: /abrir o momento de troca/i }));
    await screen.findByRole("button", { name: /troca por recompensa/i });

    // A "recarga" descarta o estado em memória — a sessão de trabalho
    // persiste em `sessionStorage`, o momento de troca não (design —
    // decisão 2).
    unmount();
    render(<App />);

    await screen.findByText(/o que você quer fazer/i);
    expect(
      screen.queryByRole("button", { name: /troca por recompensa/i }),
    ).not.toBeInTheDocument();
  });
});

describe("a tela da troca", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("mostra o catálogo com preço e estoque, e o saldo disponível — nunca o acumulado", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([item()]);
    vi.spyOn(pontosExtrasApi, "consultarMeusPontosExtras").mockResolvedValue(pontos());

    render(
      <TelaDeTroca
        tokenDeTrabalho="token-de-trabalho"
        aulaId="aula-1"
        tokenDoGuerreiro="token-guerreiro"
        guerreiroId="guerreiro-1"
        aoConcluir={vi.fn()}
        aoVoltar={vi.fn()}
      />,
    );

    expect(await screen.findByText("Caderno de desenho")).toBeInTheDocument();
    expect(screen.getByText(/40 pontos/i)).toBeInTheDocument();
    expect(screen.getByText(/estoque 5/i)).toBeInTheDocument();
    expect(screen.getByText(/saldo dispon[ií]vel: 100 pontos/i)).toBeInTheDocument();
    expect(screen.queryByText(/300/)).not.toBeInTheDocument();
    expect(screen.queryByText(/r\$|reais|moedas/i)).not.toBeInTheDocument();
    expect(catalogoAvulsoApi.listarCatalogoAvulso).toHaveBeenCalledWith("token-guerreiro");
    expect(pontosExtrasApi.consultarMeusPontosExtras).toHaveBeenCalledWith("token-guerreiro");
  });

  it("item de estoque zero não é oferecido", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([
      item({ id: "item-zerado", nome: "Item zerado", estoque: "0" }),
      item(),
    ]);
    vi.spyOn(pontosExtrasApi, "consultarMeusPontosExtras").mockResolvedValue(pontos());

    render(
      <TelaDeTroca
        tokenDeTrabalho="token-de-trabalho"
        aulaId="aula-1"
        tokenDoGuerreiro="token-guerreiro"
        guerreiroId="guerreiro-1"
        aoConcluir={vi.fn()}
        aoVoltar={vi.fn()}
      />,
    );

    expect(await screen.findByText("Caderno de desenho")).toBeInTheDocument();
    expect(screen.queryByText("Item zerado")).not.toBeInTheDocument();
  });

  it("item mais caro que o saldo mostra a diferença em pontos e não envia nada", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([
      item({ preco_em_pontos_extras: 130 }),
    ]);
    vi.spyOn(pontosExtrasApi, "consultarMeusPontosExtras").mockResolvedValue(
      pontos({ saldo_disponivel: 100 }),
    );
    const registrarTroca = vi.spyOn(trocasApi, "registrarTroca");

    render(
      <TelaDeTroca
        tokenDeTrabalho="token-de-trabalho"
        aulaId="aula-1"
        tokenDoGuerreiro="token-guerreiro"
        guerreiroId="guerreiro-1"
        aoConcluir={vi.fn()}
        aoVoltar={vi.fn()}
      />,
    );

    expect(await screen.findByText(/faltam 30 pontos/i)).toBeInTheDocument();
    expect(
      screen.queryByRole("button", { name: /confirmar entrega/i }),
    ).not.toBeInTheDocument();
    expect(registrarTroca).not.toHaveBeenCalled();
  });

  it("a confirmação da entrega envia um único POST e volta ao início", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([item()]);
    vi.spyOn(pontosExtrasApi, "consultarMeusPontosExtras").mockResolvedValue(pontos());
    vi.spyOn(trocasApi, "registrarTroca").mockResolvedValue({
      id: "troca-1",
      item_de_catalogo_avulso_id: "item-1",
      guerreiro_id: "guerreiro-1",
      preco_cobrado: 40,
      aula_id: "aula-1",
      autor_id: "mestre-1",
      registrado_em: new Date().toISOString(),
    });
    const aoConcluir = vi.fn();

    render(
      <TelaDeTroca
        tokenDeTrabalho="token-de-trabalho"
        aulaId="aula-1"
        tokenDoGuerreiro="token-guerreiro"
        guerreiroId="guerreiro-1"
        aoConcluir={aoConcluir}
        aoVoltar={vi.fn()}
      />,
    );

    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /confirmar entrega/i }));

    expect(trocasApi.registrarTroca).toHaveBeenCalledTimes(1);
    expect(trocasApi.registrarTroca).toHaveBeenCalledWith(
      "aula-1",
      { item_de_catalogo_avulso_id: "item-1", guerreiro_id: "guerreiro-1" },
      "token-de-trabalho",
    );
    expect(aoConcluir).toHaveBeenCalled();
  });

  it("a recusa do núcleo aparece em linguagem simples e mantém a sessão aberta", async () => {
    vi.spyOn(catalogoAvulsoApi, "listarCatalogoAvulso").mockResolvedValue([item()]);
    vi.spyOn(pontosExtrasApi, "consultarMeusPontosExtras").mockResolvedValue(pontos());
    vi.spyOn(trocasApi, "registrarTroca").mockRejectedValue(
      new ErroDaApi(422, {
        codigo: "erro_de_validacao",
        mensagem: "Item sem estoque para a troca.",
      }),
    );
    const aoConcluir = vi.fn();

    render(
      <TelaDeTroca
        tokenDeTrabalho="token-de-trabalho"
        aulaId="aula-1"
        tokenDoGuerreiro="token-guerreiro"
        guerreiroId="guerreiro-1"
        aoConcluir={aoConcluir}
        aoVoltar={vi.fn()}
      />,
    );

    const usuario = userEvent.setup();
    await usuario.click(await screen.findByRole("button", { name: /confirmar entrega/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/sem estoque/i);
    expect(aoConcluir).not.toHaveBeenCalled();
    // A tela segue mostrando o catálogo — a escolha de outro item não
    // repete a entrada do Guerreiro(a) (`RF-04-53`).
    expect(screen.getByText("Caderno de desenho")).toBeInTheDocument();
  });
});
