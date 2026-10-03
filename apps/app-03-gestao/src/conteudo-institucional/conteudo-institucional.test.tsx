import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { SessaoAberta } from "comum/autenticacao";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { SecaoInstitucional, SecaoPublicada } from "./api";
import * as api from "./api";
import { TelaDoConteudoInstitucional } from "./TelaDoConteudoInstitucional";

const SESSAO_DE_ADMIN: SessaoAberta = {
  token: "token-do-admin",
  papel: "admin",
  permissoes: {},
  persona_id: "admin-1",
};

const SESSAO_DE_MESTRE: SessaoAberta = {
  token: "token-do-mestre",
  papel: "mestre",
  permissoes: {},
  persona_id: "mestre-1",
};

function secao(
  chave: SecaoInstitucional,
  parcial: Partial<SecaoPublicada> = {},
): SecaoPublicada {
  return {
    secao: chave,
    texto: `Texto de ${chave}`,
    video_url: null,
    autor_id: "admin-1",
    publicado_em: "2026-10-01T10:00:00-03:00",
    ...parcial,
  };
}

const AS_TRES_SECOES = [secao("quem-somos"), secao("contatos"), secao("como-apoiar")];

vi.mock("comum/autenticacao", async () => {
  const real =
    await vi.importActual<typeof import("comum/autenticacao")>("comum/autenticacao");
  return { ...real, useSessao: vi.fn() };
});

import { useSessao } from "comum/autenticacao";

function configurarSessao(sessao: SessaoAberta | null) {
  vi.mocked(useSessao).mockReturnValue({
    sessao,
    restaurando: false,
    entrando: false,
    erroDeEntrada: null,
    entrarComGoogle: vi.fn(),
    entrarComToken: vi.fn(),
    sair: vi.fn(),
    tratarRecusaDeSessao: vi.fn(),
    entrarComCredencial: vi.fn(),
    trocaDeSenhaPendente: false,
    trocandoSenha: false,
    erroDeTrocaDeSenha: null,
    trocarSenhaProvisoria: vi.fn(),
  });
}

afterEach(() => {
  vi.restoreAllMocks();
});

describe("área Conteúdo institucional", () => {
  it("as três seções aparecem na ordem fixa, com o texto e a autoria", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(api, "lerConteudoInstitucional").mockResolvedValue(AS_TRES_SECOES);

    render(<TelaDoConteudoInstitucional />);

    const titulos = await screen.findAllByRole("heading", { level: 3 });
    expect(titulos.map((titulo) => titulo.textContent)).toEqual([
      "Quem somos",
      "Contatos",
      "Como apoiar",
    ]);
    expect(screen.getAllByText(/publicado por admin-1 em/i)).toHaveLength(3);
    expect(screen.getByDisplayValue("Texto de quem-somos")).toBeInTheDocument();
  });

  it("publicar substitui a versão vigente e a autoria apresentada passa a ser de quem publicou", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(api, "lerConteudoInstitucional").mockResolvedValue([
      secao("quem-somos", { texto: "Texto antigo", autor_id: "admin-antigo" }),
      secao("contatos", { autor_id: "outro-admin" }),
      secao("como-apoiar", { autor_id: "outro-admin" }),
    ]);
    const publicar = vi.spyOn(api, "publicarSecao").mockResolvedValue(
      secao("quem-somos", {
        texto: "Texto novo",
        autor_id: "admin-1",
        publicado_em: "2026-10-02T09:00:00-03:00",
      }),
    );

    render(<TelaDoConteudoInstitucional />);
    const usuario = userEvent.setup();

    const campo = await screen.findByDisplayValue("Texto antigo");
    await usuario.clear(campo);
    await usuario.type(campo, "Texto novo");
    await usuario.click(screen.getByRole("button", { name: "Publicar Quem somos" }));

    await waitFor(() =>
      expect(publicar).toHaveBeenCalledWith(
        "quem-somos",
        { texto: "Texto novo", video_url: null },
        "token-do-admin",
      ),
    );
    expect(await screen.findByText(/passou a valer com o texto novo/i)).toBeInTheDocument();
    expect(screen.getByText(/publicado por admin-1 em/i)).toBeInTheDocument();
    expect(screen.queryByText(/publicado por admin-antigo/i)).not.toBeInTheDocument();
  });

  it('o campo de vídeo só existe em "Quem somos"', async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(api, "lerConteudoInstitucional").mockResolvedValue(AS_TRES_SECOES);

    render(<TelaDoConteudoInstitucional />);

    await screen.findByRole("form", { name: "Publicar Quem somos" });
    expect(screen.getAllByLabelText(/link do vídeo de apresentação/i)).toHaveLength(1);
    const contatos = screen.getByRole("form", { name: "Publicar Contatos" });
    expect(contatos.querySelector('input[type="text"]')).toBeNull();
  });

  it("seção nunca publicada aparece vazia, sem autor nem data, e aceita a primeira publicação", async () => {
    configurarSessao(SESSAO_DE_ADMIN);
    vi.spyOn(api, "lerConteudoInstitucional").mockResolvedValue([
      secao("quem-somos"),
      secao("contatos", { texto: null, autor_id: null, publicado_em: null }),
      secao("como-apoiar"),
    ]);
    const publicar = vi
      .spyOn(api, "publicarSecao")
      .mockResolvedValue(secao("contatos", { texto: "Primeiro texto" }));

    render(<TelaDoConteudoInstitucional />);
    const usuario = userEvent.setup();

    expect(await screen.findByText("Nunca publicada.")).toBeInTheDocument();
    const contatos = screen.getByRole("form", { name: "Publicar Contatos" });
    const campo = contatos.querySelector("textarea") as HTMLTextAreaElement;
    expect(campo.value).toBe("");

    await usuario.type(campo, "Primeiro texto");
    await usuario.click(screen.getByRole("button", { name: "Publicar Contatos" }));

    await waitFor(() =>
      expect(publicar).toHaveBeenCalledWith(
        "contatos",
        { texto: "Primeiro texto", video_url: null },
        "token-do-admin",
      ),
    );
  });

  it("Mestre lê a recusa em linguagem simples, e a leitura de Admin nem é chamada", async () => {
    configurarSessao(SESSAO_DE_MESTRE);
    const ler = vi.spyOn(api, "lerConteudoInstitucional");

    render(<TelaDoConteudoInstitucional />);

    expect(await screen.findByText(/esta área é do admin/i)).toBeInTheDocument();
    expect(ler).not.toHaveBeenCalled();
  });
});
