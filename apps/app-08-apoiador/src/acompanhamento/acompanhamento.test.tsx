import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import * as comumApi from "comum/api";
import { ErroDaApi } from "comum/api";
import { limparToken } from "comum/autenticacao";
import * as authApi from "comum/autenticacao/api";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import App from "../App";
import type { Favoritos } from "./api";
import * as acompanhamentoApi from "./api";

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return {
    ...real,
    BotaoDeEntradaGoogle: () => <div data-testid="botao-de-entrada-google" />,
  };
});

const PAGINA_VAZIA = { itens: [], proximo_cursor: null };
const FAVORITOS_VAZIOS: Favoritos = { guerreiros: [], mestres: [] };

function mockarPainelPublico(
  sobrescritas: Partial<{
    guerreiros: { avatar: string | null; nick: string }[];
    poderes: acompanhamentoApi.PoderPublico[];
    criacoes: acompanhamentoApi.CriacaoPublica[];
    cobertura: acompanhamentoApi.CoberturaPublicaDeOds[];
  }> = {},
) {
  vi.spyOn(acompanhamentoApi, "listarGuerreirosPublicos").mockResolvedValue({
    itens: sobrescritas.guerreiros ?? [],
    proximo_cursor: null,
  });
  vi.spyOn(acompanhamentoApi, "listarPoderesPublicos").mockResolvedValue(
    sobrescritas.poderes ?? [],
  );
  vi.spyOn(acompanhamentoApi, "listarCriacoesPublicas").mockResolvedValue({
    itens: sobrescritas.criacoes ?? [],
    proximo_cursor: null,
  });
  vi.spyOn(acompanhamentoApi, "listarCoberturaPublicaDeOds").mockResolvedValue(
    sobrescritas.cobertura ?? [],
  );
}

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

async function abrirAcompanhamento(testeDeUsuario: ReturnType<typeof userEvent.setup>) {
  await testeDeUsuario.click(screen.getByRole("button", { name: /^acompanhamento$/i }));
}

describe("área de acompanhamento", () => {
  beforeEach(() => {
    limparToken();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    limparToken();
  });

  it("o painel público traz o que a vitrine traz", async () => {
    mockarPainelPublico({
      guerreiros: [{ avatar: null, nick: "guerreira-da-vitrine" }],
      poderes: [{ id: "poder-1", nome: "Poder das Águas", descricao: "", trilhas: [] }],
      criacoes: [{ trilha_id: "trilha-1", producao: "Um poema", autores: [] }],
      cobertura: [
        {
          comunidade_id: "comunidade-1",
          comunidade_nome: "Zeferina",
          objetivos: [6],
          ciclo: "Ciclo 01",
        },
      ],
    });
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue(FAVORITOS_VAZIOS);

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    expect(await screen.findByText(/guerreira-da-vitrine/i)).toBeInTheDocument();
    expect(screen.getByText(/poder das águas/i)).toBeInTheDocument();
    expect(screen.getByText(/um poema/i)).toBeInTheDocument();
    expect(screen.getByText(/zeferina/i)).toBeInTheDocument();
  });

  it("a chamada pública vai sem token de sessão", async () => {
    const espiao = vi.spyOn(comumApi, "chamarNucleo").mockImplementation((caminho: string) => {
      if (caminho === "/v1/vitrine/guerreiros") return Promise.resolve(PAGINA_VAZIA);
      if (caminho === "/v1/vitrine/poderes") return Promise.resolve([]);
      if (caminho === "/v1/vitrine/criacoes") return Promise.resolve(PAGINA_VAZIA);
      if (caminho === "/v1/vitrine/ods/cobertura") return Promise.resolve([]);
      if (caminho === "/v1/eu/favoritos") return Promise.resolve(FAVORITOS_VAZIOS);
      return Promise.reject(new Error(`rota inesperada: ${caminho}`));
    });

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    await waitFor(() => {
      expect(espiao.mock.calls.some(([caminho]) => caminho === "/v1/vitrine/guerreiros")).toBe(
        true,
      );
    });

    const chamadasPublicas = espiao.mock.calls.filter(([caminho]) =>
      (caminho as string).startsWith("/v1/vitrine"),
    );
    expect(chamadasPublicas.length).toBeGreaterThan(0);
    for (const [, opcoes] of chamadasPublicas) {
      expect((opcoes as { token?: string } | undefined)?.token).toBeUndefined();
    }
  });

  it("o campo é de nick exato e explica de onde vem o nick", async () => {
    mockarPainelPublico();
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue(FAVORITOS_VAZIOS);

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    expect(await screen.findByLabelText(/nick exato do guerreiro/i)).toBeInTheDocument();
    expect(screen.getByText(/o nick é cedido pela família/i)).toBeInTheDocument();
    expect(screen.queryByRole("listbox")).not.toBeInTheDocument();
  });

  it("as duas recusas mostram a mesma mensagem", async () => {
    mockarPainelPublico();
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue(FAVORITOS_VAZIOS);
    vi.spyOn(acompanhamentoApi, "favoritarGuerreiroPeloNick").mockRejectedValue(
      new ErroDaApi(404, {
        codigo: "nao_encontrado",
        mensagem: "Guerreiro(a) não encontrado(a).",
      }),
    );

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    const campo = await screen.findByLabelText(/nick exato do guerreiro/i);

    await testeDeUsuario.type(campo, "nao-existe");
    await testeDeUsuario.click(screen.getByRole("button", { name: /^favoritar$/i }));
    const primeiraMensagem = await screen.findByRole("alert");

    await testeDeUsuario.clear(campo);
    await testeDeUsuario.type(campo, "sem-autorizacao");
    await testeDeUsuario.click(screen.getByRole("button", { name: /^favoritar$/i }));
    const segundaMensagem = await screen.findByRole("alert");

    expect(primeiraMensagem.textContent).toBe(segundaMensagem.textContent);
  });

  it("favoritos aparecem com novidade e data, e a tela declara os 30 dias", async () => {
    mockarPainelPublico();
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue({
      guerreiros: [
        {
          id: "favorito-1",
          avatar: "avatar-x",
          nick: "guerreira-favorita",
          novidades: [
            {
              tipo: "badge",
              data: "2026-06-01T10:00:00Z",
              trilha_id: null,
              trilha_nome: null,
              badge_tipo: "de_nivel",
              nivel_valor: null,
            },
          ],
        },
      ],
      mestres: [],
    });

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    expect(await screen.findByText(/guerreira-favorita/i)).toBeInTheDocument();
    expect(screen.getByText(/ganhou um badge novo/i)).toBeInTheDocument();
    expect(screen.getByText(/01\/06\/2026/)).toBeInTheDocument();
    expect(screen.getByText(/destaque dura|30 dias/i)).toBeInTheDocument();
    expect(screen.getByText(/só dentro desta aplicação/i)).toBeInTheDocument();
  });

  it("sem favorito a tela orienta", async () => {
    mockarPainelPublico();
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue(FAVORITOS_VAZIOS);

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    expect(await screen.findByText(/ainda não favoritou ninguém/i)).toBeInTheDocument();
  });

  it("remover some da lista", async () => {
    mockarPainelPublico();
    const favoritoUnico: Favoritos = {
      guerreiros: [
        { id: "favorito-removivel", avatar: null, nick: "guerreira-removivel", novidades: [] },
      ],
      mestres: [],
    };
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos")
      .mockResolvedValueOnce(favoritoUnico)
      .mockResolvedValueOnce(FAVORITOS_VAZIOS);
    vi.spyOn(acompanhamentoApi, "removerFavorito").mockResolvedValue(undefined);

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);

    expect(await screen.findByText(/guerreira-removivel/i)).toBeInTheDocument();
    await testeDeUsuario.click(screen.getByRole("button", { name: /^remover$/i }));

    await waitFor(() => {
      expect(screen.queryByText(/guerreira-removivel/i)).not.toBeInTheDocument();
    });
  });

  it("nenhuma tela de acompanhamento oferece campo de mensagem ou contato", async () => {
    mockarPainelPublico();
    vi.spyOn(acompanhamentoApi, "listarMeusFavoritos").mockResolvedValue({
      guerreiros: [
        { id: "favorito-1", avatar: null, nick: "guerreira-sem-contato", novidades: [] },
      ],
      mestres: [
        { id: "favorito-mestre-1", avatar: null, nome: "Mestre Sem Contato", novidades: [] },
      ],
    });

    const testeDeUsuario = await entrarComoApoiador();
    await abrirAcompanhamento(testeDeUsuario);
    await screen.findByText(/guerreira-sem-contato/i);

    expect(screen.queryByLabelText(/mensagem/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/telefone/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/e-mail/i)).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: /contatar/i })).not.toBeInTheDocument();
  });
});
