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
