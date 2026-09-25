import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";

const TOKENS = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "tokens.css"),
  "utf-8",
);

describe("tokens.css — marcos de largura e grade de colunas (documento 15 §4)", () => {
  it("declara os três marcos do documento 15 §4, e nenhum outro", () => {
    expect(TOKENS).toContain("--marco-768: 768px;");
    expect(TOKENS).toContain("--marco-1024: 1024px;");
    expect(TOKENS).toContain("--marco-1280: 1280px;");

    const marcosDeclarados = [...TOKENS.matchAll(/--marco-(\d+):/g)].map((m) => m[1]);
    expect(new Set(marcosDeclarados)).toEqual(new Set(["768", "1024", "1280"]));
  });

  it("declara a grade de colunas do documento 15 §4", () => {
    expect(TOKENS).toContain("--colunas-celular: 4;");
    expect(TOKENS).toContain("--colunas-tablet: 8;");
    expect(TOKENS).toContain("--colunas-computador: 12;");
    expect(TOKENS).toContain("--calha: 16px;");
  });

  it("a largura de leitura permanece intacta, ao lado da largura de área densa", () => {
    expect(TOKENS).toContain("--largura-de-leitura: 64ch;");
    expect(TOKENS).toContain("--largura-de-area-densa: var(--marco-1280);");
  });

  it("a densidade progressiva da Operação só muda a partir do marco de 768 px", () => {
    const blocoDeOperacao = TOKENS.slice(TOKENS.indexOf('[data-temperamento="operacao"]'));
    expect(blocoDeOperacao).toMatch(/@media \(min-width: 768px\)/);
  });
});

/** O corpo da regra que abre com o seletor pedido, sem as regras seguintes. */
function corpoDaRegra(seletor: string): string {
  const inicio = TOKENS.indexOf(seletor);
  expect(inicio).toBeGreaterThan(-1);
  const abre = TOKENS.indexOf("{", inicio);
  const fecha = TOKENS.indexOf("}", abre);
  return TOKENS.slice(abre + 1, fecha);
}

describe("tokens.css — a camada de tema dos dois temperamentos (documento 15 §6)", () => {
  it("a Arena tem camada de tema própria, com o raio de carta e a duração do documento 15", () => {
    const arena = corpoDaRegra(':root[data-temperamento="arena"]');
    expect(arena).toContain("--raio-carta: 12px;");
    expect(arena).toContain("--duracao: 300ms;");
  });

  it("a Arena não declara densidade, que o documento 15 §6 não fixa em número", () => {
    const arena = corpoDaRegra(':root[data-temperamento="arena"]');
    expect(arena).not.toContain("--densidade");

    // E a densidade progressiva da Operação não alcança a Arena: na Arena a
    // densidade não muda com a largura (documento 15 §6).
    const marcos = [...TOKENS.matchAll(/@media \(min-width: 768px\) \{[^}]*\}/g)].map(
      (m) => m[0],
    );
    for (const marco of marcos) expect(marco).not.toContain("arena");
  });

  it("as aplicações da Operação seguem como estão", () => {
    const operacao = corpoDaRegra(':root[data-temperamento="operacao"]');
    expect(operacao).toContain("--densidade: var(--espaco-8);");
    expect(operacao).toContain("--raio-carta: var(--raio-campo);");
    expect(operacao).toContain("--duracao: 200ms;");
  });

  it("os dois temperamentos são os únicos declarados", () => {
    const declarados = [...TOKENS.matchAll(/\[data-temperamento="(\w+)"\]/g)].map((m) => m[1]);
    expect(new Set(declarados)).toEqual(new Set(["operacao", "arena"]));
  });

  it("menos movimento vence o temperamento, nos dois", () => {
    // O seletor de tema é mais específico que `:root`, então a preferência
    // só vence se a regra alcançar os dois temperamentos por nome.
    const reduzido = TOKENS.slice(TOKENS.indexOf("@media (prefers-reduced-motion: reduce)"));
    expect(reduzido).toContain('[data-temperamento="arena"]');
    expect(reduzido).toContain('[data-temperamento="operacao"]');
    expect(reduzido).toContain("--duracao: 0ms;");
  });
});
