import { cleanup } from "@testing-library/react";
import { afterEach, beforeEach } from "vitest";
import "@testing-library/jest-dom/vitest";

// SONDA TEMPORÁRIA — diagnóstico da falha só-no-CI do PR #282, em que
// `FormularioDeConteudo` lê `localStorage` e o recebe indefinido. Não
// reproduz em quatro execuções locais, inclusive sob Node 24, então a
// medição tem de acontecer no runner. Sai no commit seguinte.
declare const process: { stdout: { write(texto: string): void }; version: string };

function sonda(quando: string, nome?: string) {
  const tipo = typeof (globalThis as { localStorage?: unknown }).localStorage;
  if (tipo !== "object") {
    process.stdout.write(`SONDA ${quando} ls=${tipo} teste=${nome ?? "—"}\n`);
  }
}

process.stdout.write(
  `SONDA arquivo ls=${typeof (globalThis as { localStorage?: unknown }).localStorage}` +
    ` url=${globalThis.location?.href} node=${process.version}` +
    ` jsdom=${typeof globalThis.document}\n`,
);

beforeEach((ctx) => sonda("antes", ctx.task?.name));

afterEach((ctx) => {
  sonda("depois", ctx.task?.name);
  cleanup();
});
