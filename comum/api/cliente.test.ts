import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  chamarNucleo,
  configurarAcessoAoNucleo,
  ErroDaApi,
  ehRecusaDeChave,
  ehRecusaDeSessao,
  enviarParteComProgresso,
  lerArquivoDoNucleo,
} from "./cliente";

function respostaMock(
  status: number,
  corpo: unknown,
  cabecalhos: Record<string, string> = {},
) {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: () => Promise.resolve(corpo),
    headers: new Headers(cabecalhos),
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

  it("leva o tempo de espera do freio por origem, do cabeçalho Retry-After", async () => {
    vi.mocked(fetch).mockResolvedValue(
      respostaMock(
        429,
        { codigo: "freio_por_origem_acionado", mensagem: "Muitas tentativas em pouco tempo." },
        { "Retry-After": "120" },
      ),
    );

    const erro = await chamarNucleo("/v1/solicitacoes-de-participacao").catch((e) => e);

    expect(erro).toBeInstanceOf(ErroDaApi);
    expect((erro as InstanceType<typeof ErroDaApi>).tempoDeEsperaEmSegundos).toBe(120);
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

describe("lerArquivoDoNucleo", () => {
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

  it("devolve o Blob com a chave e a credencial nos cabeçalhos", async () => {
    const bytes = new Blob(["imagem"], { type: "image/png" });
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      status: 200,
      blob: () => Promise.resolve(bytes),
      headers: new Headers(),
    } as unknown as Response);

    const recebido = await lerArquivoDoNucleo("/v1/perguntas-do-desbloqueio/p1/imagem", {
      token: "token-da-persona",
    });

    expect(recebido).toBe(bytes);
    const [url, opcoes] = vi.mocked(fetch).mock.calls[0];
    expect(url).toBe("https://nucleo.teste/v1/perguntas-do-desbloqueio/p1/imagem");
    const cabecalhos = opcoes?.headers as Record<string, string>;
    expect(cabecalhos["X-Chave-Aplicacao"]).toBe("chave-de-teste");
    expect(cabecalhos.Authorization).toBe("Bearer token-da-persona");
  });

  it("recusa vira ErroDaApi, com o corpo de erro do núcleo", async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      status: 403,
      json: () =>
        Promise.resolve({ codigo: "permissao_negada", mensagem: "Não é para você." }),
      headers: new Headers(),
    } as unknown as Response);

    const erro = await lerArquivoDoNucleo("/v1/perguntas-do-desbloqueio/p1/imagem").catch(
      (e) => e,
    );

    expect(erro).toBeInstanceOf(ErroDaApi);
    expect(erro.status).toBe(403);
  });
});

// O envio de bytes não passa por `fetch`: usa `XMLHttpRequest`, porque só
// ele expõe o progresso. O dublê abaixo reproduz o que a camada lê da
// requisição — status, corpo e cabeçalho `Range` — e dispara `onload` ou
// `onerror` conforme o desfecho que o caso quer exercitar.
class RequisicaoDeMentira {
  static desfecho: {
    status?: number;
    corpo?: string;
    range?: string;
    semResposta?: boolean;
  } = {};

  status = 0;
  responseText = "";
  upload = { onprogress: null as ((evento: ProgressEvent) => void) | null };
  onload: (() => void) | null = null;
  onerror: (() => void) | null = null;
  private cabecalhos: Record<string, string> = {};

  open() {}
  setRequestHeader() {}
  getResponseHeader(nome: string): string | null {
    return this.cabecalhos[nome] ?? null;
  }

  send() {
    const desfecho = RequisicaoDeMentira.desfecho;
    queueMicrotask(() => {
      if (desfecho.semResposta) {
        this.onerror?.();
        return;
      }
      this.status = desfecho.status ?? 200;
      this.responseText = desfecho.corpo ?? "";
      if (desfecho.range) this.cabecalhos.Range = desfecho.range;
      this.onload?.();
    });
  }
}

describe("enviarParteComProgresso", () => {
  beforeEach(() => {
    vi.stubGlobal("XMLHttpRequest", RequisicaoDeMentira);
    RequisicaoDeMentira.desfecho = {};
    configurarAcessoAoNucleo({
      chaveDeAplicacao: "chave-de-teste",
      urlDoNucleo: "https://nucleo.teste",
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("a parte aceita conclui o envio", async () => {
    RequisicaoDeMentira.desfecho = { status: 200 };

    const resultado = await enviarParteComProgresso(
      "/v1/armazenamento/sessoes/uma-sessao",
      new Blob(["abc"]),
      "bytes 0-2/3",
      () => {},
    );

    expect(resultado.concluido).toBe(true);
  });

  it("o 308 diz de onde retomar, pelo cabeçalho Range", async () => {
    RequisicaoDeMentira.desfecho = { status: 308, range: "bytes=0-1023" };

    const resultado = await enviarParteComProgresso(
      "/v1/armazenamento/sessoes/uma-sessao",
      new Blob(["abc"]),
      "bytes */4096",
      () => {},
    );

    expect(resultado.concluido).toBe(false);
    expect(resultado.bytesRecebidos).toBe(1024);
  });

  it("a recusa com corpo de erro chega com o código e a mensagem", async () => {
    // Era aqui que o motivo se perdia: toda recusa virava a mesma frase
    // própria, e o Mestre lia "tente de novo" no lugar do que o núcleo
    // tinha dito (`RF-01-02`).
    RequisicaoDeMentira.desfecho = {
      status: 413,
      corpo: JSON.stringify({
        codigo: "arquivo_acima_do_teto",
        mensagem: "A imagem enviada tem 2,3 MB e o limite é 1,0 MB.",
      }),
    };

    const erro = await enviarParteComProgresso(
      "/v1/armazenamento/sessoes/uma-sessao",
      new Blob(["abc"]),
      "bytes 0-2/3",
      () => {},
    ).catch((e) => e);

    expect(erro).toBeInstanceOf(ErroDaApi);
    expect(erro.status).toBe(413);
    expect(erro.codigo).toBe("arquivo_acima_do_teto");
    expect(erro.message).toBe("A imagem enviada tem 2,3 MB e o limite é 1,0 MB.");
  });

  it("a recusa de sessão no envio é reconhecida como tal", async () => {
    RequisicaoDeMentira.desfecho = {
      status: 401,
      corpo: JSON.stringify({ codigo: "sessao_invalida", mensagem: "Sessão expirada." }),
    };

    const erro = await enviarParteComProgresso(
      "/v1/armazenamento/sessoes/uma-sessao",
      new Blob(["abc"]),
      "bytes 0-2/3",
      () => {},
    ).catch((e) => e);

    expect(ehRecusaDeSessao(erro)).toBe(true);
  });

  it("a recusa sem corpo do nosso formato preserva o status", async () => {
    // O armazenamento de produção é de terceiro e responde no formato dele:
    // não há corpo a preservar, mas o status ainda diz que houve recusa.
    RequisicaoDeMentira.desfecho = {
      status: 403,
      corpo: "<?xml version='1.0'?><Error><Code>AccessDenied</Code></Error>",
    };

    const erro = await enviarParteComProgresso(
      "https://armazenamento.externo/sessao",
      new Blob(["abc"]),
      "bytes 0-2/3",
      () => {},
    ).catch((e) => e);

    expect(erro).toBeInstanceOf(ErroDaApi);
    expect(erro.status).toBe(403);
  });

  it("a falha sem resposta não se apresenta como recusa do núcleo", async () => {
    // O preflight barrado pelo navegador cai aqui: não houve resposta, e
    // atribuir ao núcleo uma recusa que ele não deu esconde o defeito.
    RequisicaoDeMentira.desfecho = { semResposta: true };

    const erro = await enviarParteComProgresso(
      "https://armazenamento.externo/sessao",
      new Blob(["abc"]),
      "bytes 0-2/3",
      () => {},
    ).catch((e) => e);

    expect(erro).toBeInstanceOf(Error);
    expect(erro).not.toBeInstanceOf(ErroDaApi);
  });
});
