import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("comum/api", async () => {
  const real = await vi.importActual<typeof import("comum/api")>("comum/api");
  return { ...real, chamarNucleo: vi.fn() };
});

import { chamarNucleo } from "comum/api";
import {
  type AdultoDaLista,
  type ArtefatoComprobatorio,
  anexarComprobatorio,
  listarComprobatoriosPendentes,
} from "./api";

// A fila do comprobatório não tem rota própria no núcleo: é derivada da
// listagem de Apoiadores, paginada por cursor (design — decisão 2). O teste de
// tela dubla o módulo inteiro, então é aqui que o filtro e o laço da paginação
// de fato rodam (`RF-02-101`).
const dublada = vi.mocked(chamarNucleo);

function artefato(sobrescreve: Partial<ArtefatoComprobatorio> = {}): ArtefatoComprobatorio {
  return {
    id: "artefato-1",
    endereco: "https://exemplo.org/termo",
    rotulo: "Termo de doação",
    publicado: false,
    ...sobrescreve,
  };
}

function apoiador(sobrescreve: Partial<AdultoDaLista> = {}): AdultoDaLista {
  return {
    id: "apoiador-1",
    nome: "Instituição de Tal",
    email: "instituicao@example.org",
    whatsapp: null,
    nick: null,
    artefatos: [artefato()],
    ...sobrescreve,
  };
}

afterEach(() => {
  vi.resetAllMocks();
});

describe("listarComprobatoriosPendentes", () => {
  it("deixa de fora o documento já publicado e identifica o Apoiador de cada pendente", async () => {
    dublada.mockResolvedValueOnce({
      itens: [
        apoiador({
          artefatos: [
            artefato({ id: "artefato-publicado", publicado: true }),
            artefato({ id: "artefato-pendente", rotulo: "Currículo", publicado: false }),
          ],
        }),
      ],
      proximo_cursor: null,
    });

    const pendentes = await listarComprobatoriosPendentes("token-do-admin");

    expect(pendentes).toEqual([
      {
        artefato_id: "artefato-pendente",
        apoiador_id: "apoiador-1",
        apoiador: "Instituição de Tal",
        endereco: "https://exemplo.org/termo",
        rotulo: "Currículo",
      },
    ]);
  });

  it("segue o cursor até o fim: pendente em página seguinte também entra na fila", async () => {
    dublada
      .mockResolvedValueOnce({
        itens: [apoiador({ artefatos: [artefato({ id: "da-primeira-pagina" })] })],
        proximo_cursor: "cursor-2",
      })
      .mockResolvedValueOnce({
        itens: [
          apoiador({
            id: "apoiador-2",
            nome: "Outra Instituição",
            artefatos: [artefato({ id: "da-segunda-pagina" })],
          }),
        ],
        proximo_cursor: null,
      });

    const pendentes = await listarComprobatoriosPendentes("token-do-admin");

    expect(pendentes.map((pendente) => pendente.artefato_id)).toEqual([
      "da-primeira-pagina",
      "da-segunda-pagina",
    ]);
    expect(dublada).toHaveBeenNthCalledWith(1, "/v1/apoiadores", { token: "token-do-admin" });
    expect(dublada).toHaveBeenNthCalledWith(2, "/v1/apoiadores?cursor=cursor-2", {
      token: "token-do-admin",
    });
  });

  it("nenhum pendente devolve fila vazia, não erro", async () => {
    dublada.mockResolvedValueOnce({
      itens: [apoiador({ artefatos: [artefato({ publicado: true })] })],
      proximo_cursor: null,
    });

    expect(await listarComprobatoriosPendentes("token-do-admin")).toEqual([]);
  });
});

describe("anexarComprobatorio", () => {
  it("posta na rota de anexação que o identificador da listagem alcança", async () => {
    dublada.mockResolvedValueOnce({
      id: "artefato-1",
      endereco: "https://exemplo.org/termo",
      rotulo: "Termo de doação",
      publicado: true,
    });

    await anexarComprobatorio("apoiador-1", "artefato-1", "token-do-admin");

    expect(dublada).toHaveBeenCalledWith(
      "/v1/apoiadores/apoiador-1/artefatos/artefato-1/anexacao",
      { metodo: "POST", token: "token-do-admin" },
    );
  });
});
