import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("comum/api", async () => {
  const real = await vi.importActual<typeof import("comum/api")>("comum/api");
  return { ...real, chamarNucleo: vi.fn() };
});

import { chamarNucleo } from "comum/api";
import { listarAgenda } from "./api";

afterEach(() => {
  vi.mocked(chamarNucleo).mockReset();
});

describe("listarAgenda", () => {
  it("pede as canceladas ao núcleo só quando marcado (`RF-02-12`)", async () => {
    vi.mocked(chamarNucleo).mockResolvedValue({ itens: [], proximo_cursor: null });

    await listarAgenda("token", { comunidadeId: "c1" });
    await listarAgenda("token", { comunidadeId: "c1", incluirCanceladas: false });
    await listarAgenda("token", { comunidadeId: "c1", incluirCanceladas: true });

    const caminhos = vi.mocked(chamarNucleo).mock.calls.map(([caminho]) => caminho);
    expect(caminhos).toEqual([
      "/v1/aulas?comunidade=c1",
      "/v1/aulas?comunidade=c1",
      "/v1/aulas?comunidade=c1&incluir_canceladas=true",
    ]);
  });
});
