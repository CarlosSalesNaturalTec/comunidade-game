import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

// As regras do §7 de `marca/README.md`, que valem para todo arquivo da pasta,
// conferidas sobre os arquivos de verdade: nenhuma cor fora da paleta do
// documento 15 §3, nenhuma referência a terceiro, nenhum texto em `<text>` e o
// peso dentro do orçamento que o manifesto declara.
//
// O teste mora aqui, e não em `marca/`, porque `marca/**` está fora do alcance
// do Biome — a pasta guarda ativo estático, e um `.ts` ali ficaria sem lint.

const PASTA = join(dirname(fileURLToPath(import.meta.url)), "marca");

/** Os orçamentos dos §§1 e 2 do manifesto, em KB. */
const ORCAMENTO: Record<string, number> = {
  "marca-horizontal.svg": 10,
  "marca-horizontal-mono.svg": 10,
  "marca-empilhada.svg": 10,
  "simbolo.svg": 3,
  "simbolo-mono.svg": 3,
  "favicon.svg": 2,
  "submarca-robroders.svg": 5,
  "submarca-robroders-mono.svg": 5,
  "submarca-robo-educa.svg": 5,
  "submarca-robo-educa-mono.svg": 5,
};

/** A paleta do documento 15 §3, em maiúsculas — a única fonte de cor permitida. */
const PALETA = new Set([
  "#10141F",
  "#1C2333",
  "#2E3850",
  "#5C6885",
  "#A8B2C6",
  "#CFD6E3",
  "#E7EBF2",
  "#F7F5F0",
  "#FFFFFF",
  "#B33C00",
  "#C94800",
  "#F25C05",
  "#FF7A2E",
  "#FFE3D1",
  "#123E8A",
  "#1750AE",
  "#1D63D1",
  "#5B93EA",
  "#DCE8FB",
  "#7A5500",
  "#996B00",
  "#F2B705",
  "#FFCE3D",
  "#FFF1CC",
  "#0B5D57",
  "#0E7A72",
  "#12A093",
  "#3FC7B9",
  "#D3F1EE",
  "#1B7A3D",
  "#4ECB80",
  "#8A5A00",
  "#E8A93B",
  "#C02626",
  "#F27A7A",
]);

const arquivos = readdirSync(PASTA)
  .filter((nome) => nome.endsWith(".svg"))
  .sort();

const conteudo = (nome: string) => readFileSync(join(PASTA, nome), "utf-8");
const cores = (svg: string) =>
  [...svg.matchAll(/#[0-9A-Fa-f]{6}/g)].map((achado) => achado[0].toUpperCase());

describe("comum/marca — o manifesto é cumprido pelos arquivos (README §7)", () => {
  it("entrega exatamente os dez arquivos que os §§1 e 2 declaram", () => {
    expect(arquivos).toEqual(Object.keys(ORCAMENTO).sort());
  });

  it.each(arquivos)("%s não busca nada de terceiro nem traz texto vivo", (nome) => {
    const svg = conteudo(nome);
    expect(svg).not.toContain("<text");
    expect(svg).not.toContain("<script");
    expect(svg).not.toContain("<image");
    expect(svg).not.toContain("<filter");
    expect(svg).not.toContain("<style");
    // A única URL permitida é o espaço de nomes do próprio SVG.
    const enderecos = [...svg.matchAll(/https?:\/\/[^"'\s)]+/g)].map((a) => a[0]);
    expect(enderecos).toEqual(["http://www.w3.org/2000/svg"]);
  });

  it.each(arquivos)("%s não usa cor fora da paleta do documento 15 §3", (nome) => {
    expect(cores(conteudo(nome)).filter((cor) => !PALETA.has(cor))).toEqual([]);
  });

  it.each(arquivos.filter((nome) => nome.includes("-mono")))(
    "%s não declara cor nenhuma: herda do texto por currentColor",
    (nome) => {
      const svg = conteudo(nome);
      expect(cores(svg)).toEqual([]);
      expect(svg).toContain("currentColor");
    },
  );

  it.each(arquivos)("%s cabe no orçamento de peso do manifesto", (nome) => {
    expect(statSync(join(PASTA, nome)).size).toBeLessThanOrEqual(ORCAMENTO[nome] * 1024);
  });
});

// A marca não basta existir: ela precisa **alcançar** toda aplicação. Estes
// casos conferem a montagem pelo arquivo de configuração e pelo ponto de
// entrada de cada uma — é o que faz uma aplicação nova nascer sem o símbolo
// ser percebido antes de ir ao ar.

const APPS = join(dirname(fileURLToPath(import.meta.url)), "..", "apps");
const aplicacoes = readdirSync(APPS).filter((nome) => nome.startsWith("app-"));

describe("a marca alcança todas as aplicações", () => {
  it("há aplicação para conferir", () => {
    expect(aplicacoes.length).toBeGreaterThan(0);
  });

  it.each(aplicacoes)("%s provisiona o favicon do arquivo único da camada comum", (app) => {
    const config = ["vite.config.ts", "astro.config.mjs"]
      .map((nome) => join(APPS, app, nome))
      .find((caminho) => existsSync(caminho));
    expect(config).toBeDefined();

    const texto = readFileSync(config as string, "utf-8");
    expect(texto).toContain("provisionarFavicon");
    // Do arquivo único: a cópia em `public/` nasce do plugin e não é versionada,
    // o que `.gitignore` garante e esta asserção não pode conferir sozinha.
    expect(texto).toMatch(/provisionarFavicon\(\s*path\.join/);
  });

  it.each(aplicacoes)("%s monta a marca uma vez, no ponto de entrada", (app) => {
    const entrada = ["src/main.tsx", "src/layouts/Vitrine.astro"]
      .map((caminho) => join(APPS, app, caminho))
      .find((caminho) => existsSync(caminho));
    expect(entrada).toBeDefined();

    const texto = readFileSync(entrada as string, "utf-8");
    expect(texto).toContain("MarcaDoProjeto");
    // Uma vez: a marca é do topo da aplicação, nunca de cada tela.
    expect([...texto.matchAll(/<MarcaDoProjeto\b/g)]).toHaveLength(1);
  });
});
