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
  it("entrega exatamente os nove arquivos que os §§1 e 2 declaram", () => {
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

// A forma do escudo é **uma**, em escalas diferentes. Antes desta change ela
// estava escrita à mão em seis arquivos, e a medição mostrou que eram
// escalamento puro — raio e contorno na mesma razão com a largura, sem
// correção óptica a preservar. Estes casos impedem que as cinco voltem a
// divergir sem ninguém notar (documento 15 §§13.1, 13.3; README §7).

/** As peças que carregam o escudo. As submarcas não: o escudo significa a
 * plataforma, e por isso só a palavra entra nelas (documento 15 §13.1). */
const COM_ESCUDO = [
  "simbolo.svg",
  "simbolo-mono.svg",
  "marca-horizontal.svg",
  "marca-horizontal-mono.svg",
  "marca-empilhada.svg",
];

/** Razões de contorno do desenho original, preservadas na mudança de forma:
 * a colorida a `1.5/42` da largura do escudo, a monocromática a `2.5/42`. */
const RAZAO_DE_CONTORNO = { colorida: 1.5 / 42, mono: 2.5 / 42 };

/** O escudo é o **primeiro** `<path>` de cada peça. O traçado dele usa só `M`
 * e `C`, então todo número é coordenada e os pares nunca escorregam. */
function escudo(nome: string) {
  const svg = conteudo(nome);
  const elemento = svg.match(/<path\b[^>]*?\/>/s)?.[0] ?? "";
  const d = elemento.match(/d="([^"]+)"/)?.[1] ?? "";
  const grade = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  return {
    numeros: [...d.matchAll(/-?\d*\.?\d+/g)].map((achado) => Number(achado[0])),
    contorno: Number(elemento.match(/stroke-width="([\d.]+)"/)?.[1]),
    juncao: elemento.includes('stroke-linejoin="round"'),
    grade: [Number(grade?.[1]), Number(grade?.[2])] as [number, number],
  };
}

const eixo = (numeros: number[], resto: number) => numeros.filter((_, i) => i % 2 === resto);

/** O contorno em fração da largura do escudo, com origem no canto da caixa
 * dele: duas peças da mesma forma coincidem, qualquer que seja a escala. */
function normalizado(numeros: number[]): number[] {
  const x0 = Math.min(...eixo(numeros, 0));
  const y0 = Math.min(...eixo(numeros, 1));
  const largura = Math.max(...eixo(numeros, 0)) - x0;
  return numeros.map((v, i) => (i % 2 === 0 ? v - x0 : v - y0) / largura);
}

/** O contorno do escudo em pontos: cada cúbica amostrada, para dar um polígono
 * com que se pergunta se um ponto está dentro. */
function amostrado(numeros: number[]): Array<[number, number]> {
  const pt = (i: number): [number, number] => [numeros[i * 2], numeros[i * 2 + 1]];
  const saida: Array<[number, number]> = [];
  for (let c = 0; c < 4; c += 1) {
    const [p0, p1, p2, p3] = [pt(c * 3), pt(c * 3 + 1), pt(c * 3 + 2), pt(c * 3 + 3)];
    for (let k = 0; k < 40; k += 1) {
      const t = k / 40;
      const u = 1 - t;
      saida.push([
        u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
        u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1],
      ]);
    }
  }
  return saida;
}

/** Ponto dentro do polígono, pela regra do raio que cruza as arestas. */
function dentro([x, y]: [number, number], poligono: Array<[number, number]>): boolean {
  let sim = false;
  for (let i = 0, j = poligono.length - 1; i < poligono.length; j = i, i += 1) {
    const [xi, yi] = poligono[i];
    const [xj, yj] = poligono[j];
    if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) sim = !sim;
  }
  return sim;
}

describe("o escudo tem uma forma só, em todas as peças da marca", () => {
  const referencia = normalizado(escudo("simbolo.svg").numeros);

  it.each(COM_ESCUDO)("%s descreve a mesma silhueta, normalizada pela largura", (nome) => {
    const atual = normalizado(escudo(nome).numeros);
    expect(atual).toHaveLength(referencia.length);
    for (const [i, v] of atual.entries()) {
      expect(v).toBeCloseTo(referencia[i], 2);
    }
  });

  it.each(COM_ESCUDO)("%s guarda a razão de contorno da sua versão", (nome) => {
    const { numeros, contorno } = escudo(nome);
    const largura = Math.max(...eixo(numeros, 0)) - Math.min(...eixo(numeros, 0));
    const esperada = nome.includes("-mono")
      ? RAZAO_DE_CONTORNO.mono
      : RAZAO_DE_CONTORNO.colorida;
    expect(contorno / largura).toBeCloseTo(esperada, 3);
  });

  it("a proporção do escudo é a do modelo — mais alto que largo", () => {
    const { numeros } = escudo("simbolo.svg");
    const largura = Math.max(...eixo(numeros, 0)) - Math.min(...eixo(numeros, 0));
    const altura = Math.max(...eixo(numeros, 1)) - Math.min(...eixo(numeros, 1));
    expect(altura / largura).toBeCloseTo(1.172, 2);
  });

  it.each(COM_ESCUDO)("%s tem a ponta no topo, e não aresta reta", (nome) => {
    const { numeros } = escudo(nome);
    const xs = eixo(numeros, 0);
    const ys = eixo(numeros, 1);
    const topo = Math.min(...ys);
    // Um só x no topo, no meio da largura. Aresta reta daria dois x distintos;
    // o ápice aparece duas vezes no traçado porque abre e fecha o caminho.
    const xsNoTopo = [...new Set(xs.filter((_, i) => ys[i] === topo))];
    expect(xsNoTopo).toHaveLength(1);
    expect(xsNoTopo[0]).toBeCloseTo((Math.min(...xs) + Math.max(...xs)) / 2, 1);
  });

  // O escudo ganhou altura e perdeu largura: o monograma não pode ter ficado
  // de fora da forma nova. Vale para o **símbolo**, cujo monograma não é
  // transformado; nos conjuntos ele reencaixa por `transform` (spec: cenário
  // "O monograma continua dentro do escudo").
  it.each(["simbolo.svg", "simbolo-mono.svg"])(
    "%s mantém o monograma dentro do escudo",
    (nome) => {
      const contorno = amostrado(escudo(nome).numeros);
      const monograma = conteudo(nome).match(/<path\b[^>]*?\/>/gs)?.[1] ?? "";
      const n = [...(monograma.match(/d="([^"]+)"/)?.[1] ?? "").matchAll(/-?\d*\.?\d+/g)].map(
        (achado) => Number(achado[0]),
      );
      const xs = eixo(n, 0);
      const ys = eixo(n, 1);
      const cantos: Array<[number, number]> = [
        [Math.min(...xs), Math.min(...ys)],
        [Math.max(...xs), Math.min(...ys)],
        [Math.min(...xs), Math.max(...ys)],
        [Math.max(...xs), Math.max(...ys)],
      ];
      for (const canto of cantos) {
        expect(dentro(canto, contorno)).toBe(true);
      }
    },
  );

  it.each(COM_ESCUDO)("%s não deixa a ponta sair cortada pela grade", (nome) => {
    const { numeros, contorno, juncao, grade } = escudo(nome);
    // Junta redonda: o traço estende metade da espessura a partir do vértice,
    // em toda direção. Em mitre estenderia mais, e a ponta sairia cortada.
    expect(juncao).toBe(true);
    const folga = contorno / 2;
    expect(Math.min(...eixo(numeros, 1)) - folga).toBeGreaterThanOrEqual(0);
    expect(Math.max(...eixo(numeros, 1)) + folga).toBeLessThanOrEqual(grade[1]);
    expect(Math.min(...eixo(numeros, 0)) - folga).toBeGreaterThanOrEqual(0);
    expect(Math.max(...eixo(numeros, 0)) + folga).toBeLessThanOrEqual(grade[0]);
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
