import { mkdtempSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { afterEach, describe, expect, it } from "vitest";
import { provisionarModelosDeBiometria } from "./provisionamento";

const MODELOS_ESPERADOS = ["blazeface", "antispoof", "liveness", "faceres", "facemesh"];

describe("provisionarModelosDeBiometria", () => {
  let destino: string;

  afterEach(() => {
    if (destino) rmSync(destino, { recursive: true, force: true });
  });

  it("copia o .json e os pesos de cada um dos cinco modelos habilitados, e nada mais", () => {
    destino = mkdtempSync(path.join(tmpdir(), "modelos-de-biometria-"));

    provisionarModelosDeBiometria(destino);

    const copiados = readdirSync(destino);
    for (const modelo of MODELOS_ESPERADOS) {
      expect(copiados).toContain(`${modelo}.json`);
      expect(
        copiados.some((arquivo) => arquivo.startsWith(modelo) && arquivo !== `${modelo}.json`),
      ).toBe(true);
    }

    const prefixosEsperados = MODELOS_ESPERADOS;
    for (const arquivo of copiados) {
      expect(prefixosEsperados.some((prefixo) => arquivo.startsWith(prefixo))).toBe(true);
    }
  });
});
