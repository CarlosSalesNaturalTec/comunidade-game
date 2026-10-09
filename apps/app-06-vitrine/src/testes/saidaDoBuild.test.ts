import { execFile } from "node:child_process";
import { readFileSync } from "node:fs";
import type { Server } from "node:http";
import { join } from "node:path";
import { promisify } from "node:util";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { ENDERECOS_FORA_DO_SITEMAP, ENDERECOS_INDEXAVEIS } from "../descoberta/enderecos";
import { alvoDaHospedagem, arquivosPublicados, resolverEndereco } from "./enderecoServido";
import { criarNucleoDeMentira } from "./nucleoDeMentira.mjs";

const executar = promisify(execFile);

/**
 * O **nível 2** dos testes (design — decisão 7): confere a saída de um build
 * real, contra um núcleo de mentira, em vez de uma tela montada no jsdom.
 *
 * É o único nível que consegue afirmar o que as specs desta fatia exigem — "o
 * documento devolvido já traz o conteúdo", "a resposta declara que não deve
 * ser indexada" —, porque essas são afirmações sobre o arquivo servido.
 *
 * E é o que guarda `TelaDaVitrine.tsx` contra desvio: se uma página de
 * `src/pages/` perder uma seção, a composição de teste não percebe e os
 * títulos por rota, conferidos aqui, percebem.
 */

const RAIZ = join(__dirname, "..", "..");
const DIST = join(RAIZ, "dist");

let servidor: Server | undefined;

function ler(arquivo: string): string {
  return readFileSync(join(DIST, arquivo), "utf-8");
}

beforeAll(async () => {
  // Porta **efêmera**, pedida ao sistema. O `frontend-ci.yml` sobe o mesmo
  // núcleo de mentira na porta padrão, para o `npm run build --workspaces`
  // ter o que ler, e fixar a porta aqui faria os dois brigarem pela mesma
  // (`EADDRINUSE`) sempre que rodassem na mesma máquina.
  const aberto = await criarNucleoDeMentira(0);
  servidor = aberto;
  const endereco = aberto.address();
  if (endereco === null || typeof endereco === "string") {
    throw new Error("o núcleo de mentira não abriu porta");
  }

  // Assíncrono, e nunca `execFileSync`: o núcleo de mentira vive **neste**
  // processo, e a versão síncrona bloquearia o event loop — o build não
  // conseguiria ser atendido e cairia na decisão 4, como se o núcleo
  // estivesse fora do ar.
  await executar("npx", ["astro", "build"], {
    cwd: RAIZ,
    env: {
      ...process.env,
      VITE_URL_DO_NUCLEO: `http://127.0.0.1:${endereco.port}`,
      VITE_CHAVE_DE_APLICACAO: "chave-de-teste",
      // O proxy do ambiente não deve alcançar o laço local.
      NO_PROXY: "127.0.0.1,localhost",
      no_proxy: "127.0.0.1,localhost",
    },
  });
}, 180_000);

afterAll(async () => {
  // Pode não existir: se o `beforeAll` falhou antes de abrir, fechar aqui
  // trocaria a causa real por um `TypeError`.
  if (servidor === undefined) return;
  await new Promise<void>((pronto) => servidor?.close(() => pronto()));
});

describe("o institucional sai no documento servido", () => {
  it("a abertura traz o texto publicado, sem executar script (RF-03-45, PRD-03 §10)", () => {
    expect(ler("index.html")).toContain("A plataforma usa IA e declara isso em público.");
  });

  it("a área detalhada de coleta traz o conteúdo dela (RF-03-52, RF-03-53)", () => {
    const html = ler("o-que-coletamos.html");

    expect(html).toMatch(/coleta/i);
    expect(html.length).toBeGreaterThan(2000);
  });

  it("“Como apoiar” traz a chave PIX que o Admin publicou (RF-03-46)", () => {
    expect(ler("index.html")).toContain("51.730.395/0001-19");
  });
});

describe("cada rota indexável declara título e canônica próprios", () => {
  const rotas: [string, string][] = [
    ["index.html", "https://comunidadegame.org/"],
    ["pesquisadores.html", "https://comunidadegame.org/pesquisadores"],
    ["gestores-publicos.html", "https://comunidadegame.org/gestores-publicos"],
    ["o-que-coletamos.html", "https://comunidadegame.org/o-que-coletamos"],
    ["quero-participar.html", "https://comunidadegame.org/quero-participar"],
  ];

  it("nenhuma repete o título de outra", () => {
    const titulos = rotas.map(
      ([arquivo]) => /<title>([^<]*)<\/title>/.exec(ler(arquivo))?.[1],
    );

    expect(titulos.every((titulo) => (titulo ?? "").length > 0)).toBe(true);
    expect(new Set(titulos).size).toBe(rotas.length);
  });

  it("cada uma aponta a canônica para si mesma", () => {
    for (const [arquivo, canonica] of rotas) {
      expect(ler(arquivo)).toContain(`<link rel="canonical" href="${canonica}">`);
    }
  });

  it("cada uma declara descrição própria", () => {
    for (const [arquivo] of rotas) {
      expect(ler(arquivo)).toMatch(/<meta name="description" content="[^"]{60,}"/);
    }
  });
});

// É este bloco que guarda `TelaDaVitrine.tsx` contra desvio: a composição de
// teste afirma a mesma ordem de seções, e aqui se confere que a página real a
// tem (design — decisão 7).
describe("cada recorte abre com as seções que o PRD-03 §5 lhe dá", () => {
  /** Só os `h2` de dentro do `<main>`: o diálogo de entrada, que o cabeçalho
   * monta, também tem um, e ele não é seção de recorte. */
  function titulos(arquivo: string): string[] {
    const principal = /<main[^>]*>([\s\S]*)<\/main>/.exec(ler(arquivo))?.[1] ?? "";
    return [...principal.matchAll(/<h2[^>]*>([^<]+)<\/h2>/g)].map((achado) => achado[1]);
  }

  it("sociedade civil traz as onze seções, na ordem (RF-03-02, RF-03-25)", () => {
    expect(titulos("index.html")).toEqual([
      "Quem somos",
      "Guerreiros e Guerreiras",
      "Portfólio de criações originais",
      "Ranking",
      "Poderes",
      "Mestres",
      "Apoiadores",
      "Comunidades Virtuais",
      "Construir sobre a API",
      "Como apoiar",
      "Contatos",
    ]);
  });

  it("pesquisadores entra pelas séries (RF-03-26)", () => {
    expect(titulos("pesquisadores.html")).toEqual([
      "Séries do território e metodologia",
      "Cobertura da Agenda 2030",
      "Solicitação do conjunto de dados",
      "Contatos",
    ]);
  });

  it("gestores públicos abre com o bloco do município (RF-03-63)", () => {
    expect(titulos("gestores-publicos.html")[0]).toBe(
      "Para que a plataforma serve ao município",
    );
  });
});

describe("a casca da comunidade indexa, e o painel não vem no documento", () => {
  it("traz nome e território, sem executar script (RF-03-15)", () => {
    const html = ler(join("comunidades", "zeferina.html"));

    expect(html).toContain("Guerreira Zeferina");
    expect(html).toContain("Cabula, Salvador");
  });

  it("não traz o painel: série e contagem chegam na visita", () => {
    const html = ler(join("comunidades", "zeferina.html"));

    expect(html).not.toContain("registros válidos");
    expect(html).not.toContain(">17<");
  });

  it("declara título e canônica próprios da comunidade", () => {
    const html = ler(join("comunidades", "zeferina.html"));

    expect(html).toContain(
      "<title>Guerreira Zeferina — território e séries | Comunidade Game",
    );
    expect(html).toContain(
      '<link rel="canonical" href="https://comunidadegame.org/comunidades/zeferina">',
    );
  });
});

describe("a página de pessoa não é indexada e não traz perfil", () => {
  it("a casca declara que não deve ser indexada (RF-03-13, RF-03-14)", () => {
    expect(ler("app.html")).toContain('<meta name="robots" content="noindex, nofollow">');
  });

  it("a casca não traz avatar, nick, badge nem desempenho no documento", () => {
    const html = ler("app.html");

    expect(html).not.toMatch(/nick/i);
    expect(html).not.toMatch(/badge/i);
    expect(html).not.toMatch(/pontos regulares/i);
  });

  it("nenhum endereço institucional ou de comunidade pede para não ser indexado", () => {
    for (const arquivo of [
      "index.html",
      "pesquisadores.html",
      "gestores-publicos.html",
      "o-que-coletamos.html",
      "quero-participar.html",
      join("comunidades", "zeferina.html"),
    ]) {
      expect(ler(arquivo)).not.toContain('name="robots"');
    }
  });
});

describe("a camada de descoberta sai publicada", () => {
  it("o sitemap lista o institucional e a comunidade do build", () => {
    const xml = ler("sitemap.xml");

    expect(xml).toContain("https://comunidadegame.org/comunidades/zeferina");
    expect(xml).toContain("https://comunidadegame.org/o-que-coletamos");
  });

  it("o sitemap não lista pessoa nem formulário", () => {
    const xml = ler("sitemap.xml");

    for (const trecho of [
      "/guerreiros/",
      "/mestres/",
      "/apoiadores/",
      "/participar",
      "/solicitar-dados",
      "/desenvolvedor",
      "/apresentar-url",
    ]) {
      expect(xml).not.toContain(trecho);
    }
  });

  it("o robots barra a casca de pessoa e aponta o sitemap", () => {
    const robots = ler("robots.txt");

    expect(robots).toContain("Disallow: /guerreiros/");
    expect(robots).toContain("Disallow: /app.html");
    expect(robots).toContain("Sitemap: https://comunidadegame.org/sitemap.xml");
  });
});

describe("a moldura da Arena sai em toda tela pública", () => {
  const todas = [
    "index.html",
    "pesquisadores.html",
    "gestores-publicos.html",
    "o-que-coletamos.html",
    "quero-participar.html",
    "participar.html",
    "solicitar-dados.html",
    "desenvolvedor.html",
    "apresentar-url.html",
    "app.html",
    join("comunidades", "zeferina.html"),
  ];

  it("toda rota traz a moldura de fundo de comunidade (documento 15 §6.3)", () => {
    for (const arquivo of todas) {
      expect(ler(arquivo), arquivo).toContain("cg-fundo-de-comunidade");
    }
  });

  it("sem foto escolhida, nenhuma imagem de fundo é buscada", () => {
    // `imagem={null}` enquanto `ComunidadeVirtual` não tiver campo de foto
    // (pendência do documento 09): só a cor chapada, e a tela é a mesma.
    for (const arquivo of todas) {
      expect(ler(arquivo), arquivo).not.toContain("cg-fundo-de-comunidade__imagem");
    }
  });

  it("a moldura não traz recurso de terceiro (RF-03-51)", () => {
    for (const arquivo of ["index.html", "app.html"]) {
      const html = ler(arquivo);
      const externos = [...html.matchAll(/(?:src|href)="(https?:\/\/[^"]+)"/g)].map(
        (achado) => achado[1],
      );
      expect(externos.filter((url) => !url.startsWith("https://comunidadegame.org"))).toEqual(
        [],
      );
    }
  });

  it("o estilo do palco e da moldura chega ao documento", () => {
    // Nada de `@import` extra: os componentes vêm de `comum/react`, cujo
    // índice importa `estilos.css`, e o Astro recolhe a folha no build.
    const folhas = [...ler("index.html").matchAll(/href="(\/_astro\/[^"]+\.css)"/g)].map(
      (achado) => achado[1],
    );
    expect(folhas.length).toBeGreaterThan(0);
    const css = folhas.map((folha) => ler(folha.replace(/^\//, ""))).join("\n");
    expect(css).toContain("cg-fundo-de-comunidade");
  });
});

describe("nenhuma tela busca recurso de terceiro", () => {
  it("nenhum documento aponta domínio que não seja o próprio (RF-03-51)", () => {
    for (const arquivo of ["index.html", "o-que-coletamos.html", "app.html"]) {
      const html = ler(arquivo);
      const externos = [...html.matchAll(/(?:src|href)="(https?:\/\/[^"]+)"/g)].map(
        (achado) => achado[1],
      );

      expect(externos.filter((url) => !url.startsWith("https://comunidadegame.org"))).toEqual(
        [],
      );
    }
  });
});

describe("o herói sai no documento servido da abertura", () => {
  const ELENCO = ["susy", "otavio", "trenell", "robo-educa"];
  const DO_ELENCO = join(RAIZ, "..", "..", "comum", "marca", "elenco");

  it("a abertura traz a frase do projeto e a ação, sem executar script (RF-03-01)", () => {
    const html = ler("index.html");

    expect(html).toContain("Plataforma educacional gamificada, de código aberto");
    expect(html).toContain('href="/quero-participar"');
  });

  it("o herói vem antes da primeira seção (RF-03-01)", () => {
    const html = ler("index.html");

    expect(html.indexOf("cg-heroi")).toBeGreaterThan(-1);
    expect(html.indexOf("cg-heroi")).toBeLessThan(html.indexOf("Quem somos"));
  });

  it("a ilustração sai em AVIF com reserva WebP, fora do caminho crítico", () => {
    const html = ler("index.html");

    for (const nome of ELENCO) {
      expect(html, nome).toContain(`/elenco/${nome}.avif`);
      expect(html, nome).toContain(`/elenco/${nome}.webp`);
    }
    // Quatro figuras, todas adiadas e com o lugar reservado: a frase e a ação
    // não esperam por elas (documento 15 §1, princípio 4).
    expect([...html.matchAll(/loading="lazy"/g)]).toHaveLength(ELENCO.length);
    expect([...html.matchAll(/<img[^>]+width="\d+"[^>]+height="\d+"/g)]).toHaveLength(
      ELENCO.length,
    );
  });

  it("nenhuma requisição da ilustração sai do próprio domínio (RF-03-51)", () => {
    const html = ler("index.html");
    const heroi = /<section class="cg-heroi"[\s\S]*?<\/section>/.exec(html)?.[0] ?? "";

    expect(heroi).not.toBe("");
    // `srcset` com S maiúsculo nos bytes: o renderizador React do Astro emite
    // `srcSet`, e o analisador de HTML minúscula o nome do atributo — por isso
    // a busca aqui ignora caixa. Conferido em navegador: o Chromium pede os
    // quatro `.avif` e nem busca a reserva WebP.
    expect(
      [...heroi.matchAll(/(?:src|srcset)="([^"]+)"/gi)].map((achado) => achado[1]),
    ).toEqual(ELENCO.flatMap((nome) => [`/elenco/${nome}.avif`, `/elenco/${nome}.webp`]));
  });

  it("os oito arquivos publicados são byte a byte os de `comum/marca/elenco/`", () => {
    for (const nome of ELENCO) {
      for (const extensao of ["avif", "webp"]) {
        const arquivo = `${nome}.${extensao}`;
        expect(readFileSync(join(DIST, "elenco", arquivo)), arquivo).toEqual(
          readFileSync(join(DO_ELENCO, arquivo)),
        );
      }
    }
  });

  it("o herói é da abertura, e não dos outros recortes (RF-03-25)", () => {
    for (const arquivo of ["pesquisadores.html", "gestores-publicos.html"]) {
      expect(ler(arquivo), arquivo).not.toContain("cg-heroi");
    }
  });
});

describe("o favicon servido é o do projeto, e vem de um arquivo só", () => {
  // O favicon nasce do **símbolo**: os dois ficaram idênticos sob a forma de
  // escudo com ponta, e um arquivo só serve os dois (decisão do fundador de
  // 2026-10-02).
  const DA_MARCA = join(RAIZ, "..", "..", "comum", "marca", "simbolo.svg");

  it("o que o build publica é byte a byte o de `comum/marca/`", () => {
    expect(ler("favicon.svg")).toBe(readFileSync(DA_MARCA, "utf-8"));
  });

  it("não é mais o do Vite: sem filtro de desfoque e sem marca de terceiro", () => {
    const svg = ler("favicon.svg");
    expect(svg).not.toContain("feGaussianBlur");
    expect(svg).not.toContain("<filter");
    // A única URL é o espaço de nomes do próprio SVG (documento 15 §1, princípio 6).
    expect([...svg.matchAll(/https?:\/\/[^"'\s)]+/g)].map((achado) => achado[0])).toEqual([
      "http://www.w3.org/2000/svg",
    ]);
  });
});

// O bloco que faltava, e por cuja falta a regressão chegou a produção: os
// demais afirmam que o arquivo existe em `dist/`; este afirma por qual
// **endereço** se chega até ele (design — decisão 4).
describe("cada endereço público é servido pelo documento da própria rota", () => {
  const REPO = join(RAIZ, "..", "..");

  /** Os endereços públicos que a camada de descoberta declara, mais a página
   * de comunidade do build. Vem da própria fonte, e não de lista escrita à
   * mão: rota nova sem endereço cai aqui. */
  function enderecosPublicos(): string[] {
    return [...ENDERECOS_INDEXAVEIS, ...ENDERECOS_FORA_DO_SITEMAP, "/comunidades/zeferina"];
  }

  function servido(caminho: string) {
    const alvo = alvoDaHospedagem(REPO, "vitrine");
    return resolverEndereco(caminho, alvo, arquivosPublicados(DIST));
  }

  it("os três recortes abrem no endereço próprio (RF-03-25, RF-03-26)", () => {
    expect(servido("/")).toEqual({ tipo: "arquivo", arquivo: "/index.html" });
    expect(servido("/pesquisadores")).toEqual({
      tipo: "arquivo",
      arquivo: "/pesquisadores.html",
    });
    expect(servido("/gestores-publicos")).toEqual({
      tipo: "arquivo",
      arquivo: "/gestores-publicos.html",
    });
  });

  it("nenhum endereço público é atendido pela casca de pessoa", () => {
    for (const caminho of enderecosPublicos()) {
      const alcance = servido(caminho);
      expect(alcance.tipo, caminho).toBe("arquivo");
      expect(alcance, caminho).not.toMatchObject({ arquivo: `/${"app.html"}` });
    }
  });

  it("a página da comunidade abre no endereço que o sitemap declara (RF-03-15)", () => {
    expect(servido("/comunidades/zeferina")).toEqual({
      tipo: "arquivo",
      arquivo: "/comunidades/zeferina.html",
    });
  });

  it("todo endereço do sitemap é servido pelo documento da rota dele (PRD-03 §10)", () => {
    // É a junta exata do defeito: o sitemap convidava o buscador a dez
    // endereços que respondiam com a casca `noindex`.
    const caminhos = [...ler("sitemap.xml").matchAll(/<loc>([^<]+)<\/loc>/g)].map(
      (achado) => new URL(achado[1]).pathname,
    );

    expect(caminhos.length).toBeGreaterThan(5);
    for (const caminho of caminhos) {
      expect(servido(caminho), caminho).toMatchObject({ tipo: "arquivo" });
    }
  });

  it("o endereço público não depende da extensão do arquivo", () => {
    // `/pesquisadores.html` não é o endereço público: o `cleanUrls` devolve o
    // limpo, que é o mesmo que a canônica e o sitemap declaram.
    expect(servido("/pesquisadores.html")).toEqual({
      tipo: "redirecionamento",
      para: "/pesquisadores",
    });
    expect(servido("/index.html")).toEqual({ tipo: "redirecionamento", para: "/" });
  });

  it("os três prefixos de pessoa continuam chegando à casca (RF-03-13, RF-03-14)", () => {
    for (const prefixo of ["/guerreiros/ZeBita", "/mestres/abc", "/apoiadores/xyz"]) {
      expect(servido(prefixo), prefixo).toEqual({
        tipo: "rewrite",
        arquivo: "/app.html",
        regra: `${prefixo.replace(/\/[^/]+$/, "")}/**`,
      });
    }
  });

  it("a casca atende só o que não tem arquivo publicado", () => {
    // Endereço que não existe continua atendido pela casca, sem erro de
    // servidor — é o caso que a spec já exigia e que segue valendo.
    expect(servido("/nao-existe-em-lugar-nenhum")).toEqual({
      tipo: "rewrite",
      arquivo: "/app.html",
      regra: "**",
    });
  });

  it("a casca de pessoa é alcançável nos dois endereços, e os dois são barrados", () => {
    // O `cleanUrls` serve `app.html` também em `/app`. O `robots.txt` barra os
    // dois, e a regra de `X-Robots-Tag` casa os dois (design — decisão 3).
    expect(servido("/app")).toEqual({ tipo: "arquivo", arquivo: "/app.html" });

    const robots = ler("robots.txt");
    expect(robots).toContain("Disallow: /app");
    expect(robots).toContain("Disallow: /app.html");

    const fontes = (alvoDaHospedagem(REPO, "vitrine").headers ?? []).map(
      (cabecalho) => cabecalho.source,
    );
    expect(fontes).toContain("/app");
    expect(fontes).toContain("/app.html");
  });
});
