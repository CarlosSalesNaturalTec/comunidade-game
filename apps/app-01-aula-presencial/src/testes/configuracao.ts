import { cleanup } from "@testing-library/react";
import * as biometria from "comum/biometria";
import { afterEach, beforeEach, vi } from "vitest";
import "@testing-library/jest-dom/vitest";

// O jsdom não tem câmera: preparar a captura e acoplar o espelho falhariam em
// toda tela que abre a câmera, por fato do ambiente e não por escolha do
// teste. Ficam dublados aqui, e o teste que precisa da falha de preparo
// sobrescreve o dublê (`RF-04-64`, `RF-04-65`).
beforeEach(() => {
  vi.spyOn(biometria, "prepararCaptura").mockResolvedValue(undefined);
  vi.spyOn(biometria, "acoplarEspelho").mockImplementation(() => {});
});

afterEach(() => {
  cleanup();
});
