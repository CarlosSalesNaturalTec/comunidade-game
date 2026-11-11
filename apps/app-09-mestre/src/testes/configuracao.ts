import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";
import "@testing-library/jest-dom/vitest";
// O `Dialogo` da imagem ampliada da moldura fixa abre por `showModal`, que o
// jsdom não tem (decisão do fundador de 2026-11-11).
import "comum/testes/polyfill-do-dialogo";

afterEach(() => {
  cleanup();
});
