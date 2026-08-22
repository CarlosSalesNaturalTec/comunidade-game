import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  chamarNucleo,
  configurarAcessoAoNucleo,
  ErroDaApi,
  ehRecusaDeChave,
  ehRecusaDeSessao,
} from "./cliente";

function respostaMock(status: number, corpo: unknown) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(corpo),
  } as Response;
}

describe("chamarNucleo", () => {
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    configurarAcessoAoNucleo({
      chaveDeAplicacao: "chave-de-teste",
      urlDoNucleo: "https://nucleo.teste",
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("leva a chave de aplicação em toda chamada", async () => {
    vi.mocked(fetch).mockResolvedValue(respostaMock(200, { ok: true }));

    await chamarNucleo("/v1/comunidades");

    const [, opcoes] = vi.mocked(fetch).mock.calls[0];
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-de-teste");
  });

  it("leva a sessão em Authorization: Bearer quando um token é passado", async () => {
    vi.mocked(fetch).mockResolvedValue(respostaMock(200, { ok: true }));

    await chamarNucleo("/v1/eu", { token: "token-de-teste" });

    const [, opcoes] = vi.mocked(fetch).mock.calls[0];
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos.Authorization).toBe("Bearer token-de-teste");
  });

  it("interpreta o corpo de erro único do núcleo", async () => {
    vi.mocked(fetch).mockResolvedValue(
      respostaMock(422, {
        codigo: "erro_de_validacao",
        mensagem: "Campo obrigatório.",
        campo: "nome",
      }),
    );

    await expect(chamarNucleo("/v1/comunidades")).rejects.toMatchObject({
      codigo: "erro_de_validacao",
      campo: "nome",
      message: "Campo obrigatório.",
    });
  });

  it("distingue a recusa da chave da recusa da sessão", async () => {
    vi.mocked(fetch).mockResolvedValue(
      respostaMock(401, { codigo: "chave_invalida", mensagem: "Chave inválida." }),
    );
    const erroDeChave = await chamarNucleo("/v1/comunidades").catch((e) => e);

    vi.mocked(fetch).mockResolvedValue(
      respostaMock(401, { codigo: "sessao_invalida", mensagem: "Sessão expirada." }),
    );
    const erroDeSessao = await chamarNucleo("/v1/eu").catch((e) => e);

    expect(ehRecusaDeChave(erroDeChave)).toBe(true);
    expect(ehRecusaDeSessao(erroDeChave)).toBe(false);

    expect(ehRecusaDeSessao(erroDeSessao)).toBe(true);
    expect(ehRecusaDeChave(erroDeSessao)).toBe(false);

    expect(erroDeChave).toBeInstanceOf(ErroDaApi);
    expect(erroDeSessao).toBeInstanceOf(ErroDaApi);
  });

  it("duas aplicações levam cada uma a própria chave", async () => {
    vi.mocked(fetch).mockResolvedValue(respostaMock(200, { ok: true }));

    configurarAcessoAoNucleo({
      chaveDeAplicacao: "chave-da-app-09",
      urlDoNucleo: "https://x",
    });
    await chamarNucleo("/v1/trilhas/minhas");

    const [, opcoes] = vi.mocked(fetch).mock.calls[0];
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-da-app-09");
  });
});

describe("chamarNucleo sem configuração", () => {
  // O módulo guarda a configuração em variável de topo de arquivo — este
  // teste roda isolado (`vi.resetModules`) para não herdar a configuração
  // que os `beforeEach` acima já aplicaram (design — decisão 6).
  beforeEach(() => {
    vi.stubGlobal("fetch", vi.fn());
    vi.resetModules();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("falha explícito em vez de chamar o núcleo com chave vazia", async () => {
    const { chamarNucleo: chamarNucleoNaoConfigurado } = await import("./cliente");

    await expect(chamarNucleoNaoConfigurado("/v1/comunidades")).rejects.toThrow(
      /configurarAcessoAoNucleo/,
    );
    expect(fetch).not.toHaveBeenCalled();
  });
});
