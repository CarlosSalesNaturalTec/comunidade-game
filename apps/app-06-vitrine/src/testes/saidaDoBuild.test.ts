import { execFile } from "node:child_process";
import { readFileSync } from "node:fs";
import type { Server } from "node:http";
import { join } from "node:path";
import { promisify } from "node:util";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
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
