import { cleanup } from "@testing-library/react";
import * as biometria from "comum/biometria";
import { afterEach, beforeEach, vi } from "vitest";
import "@testing-library/jest-dom/vitest";

// A pré-carga busca ~10 MB de modelo assim que a entrada acha câmera: sem
// dublê, toda suíte tentaria baixá-los (`RF-05-90`). O teste que precisa do
// andamento ou da falha sobrescreve o dublê.
beforeEach(() => {
  vi.spyOn(biometria, "precarregarModelos").mockResolvedValue(true);
  vi.spyOn(biometria, "andamentoDosModelos").mockReturnValue({ carregados: 0, total: 5 });
});

afterEach(() => {
  cleanup();
});
