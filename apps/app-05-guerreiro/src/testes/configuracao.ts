import { cleanup } from "@testing-library/react";
import * as biometria from "comum/biometria";
import { afterEach, beforeEach, vi } from "vitest";
import "@testing-library/jest-dom/vitest";

// A pré-carga busca ~10 MB de modelo assim que a entrada acha câmera: sem
// dublê, toda suíte tentaria baixá-los (`RF-05-90`). O teste que precisa do
// andamento ou da falha sobrescreve o dublê.
beforeEach(() => {
  // O jsdom não tem câmera: preparar a captura e acoplar o espelho falhariam
  // na entrada por fato do ambiente, e não por escolha do teste. Ficam
  // dublados aqui, como na App 01, e o teste que precisa da falha de preparo
  // sobrescreve o dublê (`RF-05-95`, `RN-05-48`).
  vi.spyOn(biometria, "prepararCaptura").mockResolvedValue(undefined);
  vi.spyOn(biometria, "acoplarEspelho").mockImplementation(() => {});
  vi.spyOn(biometria, "precarregarModelos").mockResolvedValue(true);
  vi.spyOn(biometria, "andamentoDosModelos").mockReturnValue({ carregados: 0, total: 5 });
});

afterEach(() => {
  cleanup();
});
