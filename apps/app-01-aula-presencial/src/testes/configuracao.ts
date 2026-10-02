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
  // A pré-carga busca ~10 MB de modelo: sem dublê, toda suíte tentaria
  // baixá-los (`RF-04-75`). O teste que precisa do andamento ou da falha
  // sobrescreve o dublê.
  vi.spyOn(biometria, "precarregarModelos").mockResolvedValue(true);
  vi.spyOn(biometria, "andamentoDosModelos").mockReturnValue({ carregados: 0, total: 5 });
});

afterEach(() => {
  cleanup();
});
