import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

// A Human é dublada por inteiro: o que este arquivo verifica é o laço de
// detecção e o desfecho do preparo, não a biblioteca (`RF-04-64`,
// `RF-04-65`). O dublê precisa existir antes do módulo ser importado, porque
// `biometria.ts` constrói a Human na avaliação dele.
const detectar = vi.fn();
const carregar = vi.fn();
const modelosCarregados = vi.fn<() => string[]>();
const configuracoesRecebidas: Array<{ backend?: string; face?: Record<string, unknown> }> = [];

vi.mock("@vladmandic/human", () => ({
  default: class HumanDublada {
    load = carregar;
    detect = detectar;
    models = { loaded: modelosCarregados };
    constructor(configuracao: { backend?: string; face?: Record<string, unknown> }) {
      configuracoesRecebidas.push(configuracao);
    }
  },
}));

const {
  acoplarEspelho,
  andamentoDosModelos,
  encerrarCaptura,
  ErroDePreparoDaCaptura,
  gerarDescritor,
  precarregarModelos,
  prepararCaptura,
  provarVivacidade,
  TOTAL_DE_MODELOS,
} = await import("./biometria");

const ROSTO_VIVO = { real: 0.9, live: 0.9, embedding: [0.1, 0.2] };

function darCamera() {
  const faixa = { stop: vi.fn() };
  vi.stubGlobal("navigator", {
    mediaDevices: { getUserMedia: vi.fn().mockResolvedValue({ getTracks: () => [faixa] }) },
  });
  HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined);
}

beforeEach(() => {
  darCamera();
  carregar.mockResolvedValue(undefined);
  modelosCarregados.mockReturnValue(["blazeface", "faceres"]);
  detectar.mockResolvedValue({ face: [ROSTO_VIVO] });
});

afterEach(() => {
  encerrarCaptura();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
  vi.useRealTimers();
});

describe("preparo da captura", () => {
  // O backend é declarado, não autosselecionado: onde `navigator.gpu` existe
  // sem adaptador disponível — Chrome em máquina sem aceleração gráfica —, a
  // autosseleção escolhe `webgpu` e o `load()` morre antes de buscar modelo
  // (`RF-04-65`, cenário "aparelho sem aceleração gráfica captura do mesmo
  // jeito"). Este é o teste que impede a omissão de voltar sem ninguém ver.
  it("declara o backend webgl em vez de deixar a biblioteca escolher", () => {
    expect(configuracoesRecebidas).toHaveLength(1);
    expect(configuracoesRecebidas[0].backend).toBe("webgl");
  });

  it("conclui quando a câmera abre e os modelos carregam", async () => {
    await expect(prepararCaptura()).resolves.toBeUndefined();
    expect(carregar).toHaveBeenCalled();
  });

  // O defeito que esta change conserta: `load()` resolvia sem buscar modelo
  // nenhum, e a tela culpava a pessoa por não estar diante da câmera.
  it("lança quando nenhum modelo foi carregado, ainda que load resolva", async () => {
    modelosCarregados.mockReturnValue([]);
    await expect(prepararCaptura()).rejects.toBeInstanceOf(ErroDePreparoDaCaptura);
  });

  it("lança quando a câmera não abre", async () => {
    vi.stubGlobal("navigator", {
      mediaDevices: { getUserMedia: vi.fn().mockRejectedValue(new Error("sem permissão")) },
    });
    await expect(prepararCaptura()).rejects.toBeInstanceOf(ErroDePreparoDaCaptura);
  });
});

describe("pré-carga dos modelos", () => {
  // A razão de a pré-carga existir como função própria, e não como uma
  // chamada a `prepararCaptura()`: ela NUNCA abre a câmera. Câmera fora do
  // consentimento contraria o `RN-04-07`, e aqui ninguém pediu nada
  // (`RN-04-42`, design — decisão 2).
  it("carrega os modelos sem tocar a câmera", async () => {
    const pedirCamera = vi.fn();
    vi.stubGlobal("navigator", { mediaDevices: { getUserMedia: pedirCamera } });

    await expect(precarregarModelos()).resolves.toBe(true);

    expect(carregar).toHaveBeenCalled();
    expect(pedirCamera).not.toHaveBeenCalled();
  });

  // Quem chama é a abertura da sessão de trabalho, que não tem o que dizer à
  // pessoa sobre isto: a falha é informada pelo retorno, nunca por exceção
  // (`RF-04-75`).
  it("não lança quando o carregamento falha: devolve que não conseguiu", async () => {
    carregar.mockRejectedValue(new Error("rede caiu"));
    await expect(precarregarModelos()).resolves.toBe(false);
  });

  it("devolve que não conseguiu quando load resolve sem buscar modelo nenhum", async () => {
    modelosCarregados.mockReturnValue([]);
    await expect(precarregarModelos()).resolves.toBe(false);
  });

  // Idempotente: a captura continua chamando `load()`, e acha pronto o que a
  // pré-carga já trouxe. É o que deixa as duas conviverem sem coordenação.
  it("convive com o preparo da captura, que conclui depois dela", async () => {
    await precarregarModelos();
    await expect(prepararCaptura()).resolves.toBeUndefined();
  });

  it("o andamento é por modelo carregado, contra o total habilitado", () => {
    modelosCarregados.mockReturnValue(["blazeface", "faceres", "facemesh"]);
    expect(andamentoDosModelos()).toEqual({ carregados: 3, total: TOTAL_DE_MODELOS });
  });

  // O total está escrito à mão porque a biblioteca não o expõe antes de
  // carregar. Este caso o amarra à configuração que o módulo declara, para
  // ligar ou desligar um modelo não deixar o andamento mentindo.
  it("o total declarado bate com o que a configuração habilita", () => {
    const face = configuracoesRecebidas[0].face ?? {};
    // O detector sempre carrega quando `face` está ligado; os demais, só com
    // `enabled: true`. `emotion`, `iris` e `gear` ficam de fora por isso.
    const habilitados = Object.entries(face).filter(
      ([chave, valor]) =>
        chave === "detector" ||
        (chave !== "enabled" &&
          typeof valor === "object" &&
          valor !== null &&
          (valor as { enabled?: boolean }).enabled === true),
    );
    expect(habilitados).toHaveLength(TOTAL_DE_MODELOS);
  });
});

describe("espelho", () => {
  it("é anexado ao lugar que a tela empresta", async () => {
    await prepararCaptura();
    const lugar = document.createElement("div");

    acoplarEspelho(lugar);

    expect(lugar.querySelector("video")).not.toBeNull();
  });

  it("sai do documento quando a captura é encerrada", async () => {
    await prepararCaptura();
    const lugar = document.createElement("div");
    document.body.append(lugar);
    acoplarEspelho(lugar);

    encerrarCaptura();

    expect(lugar.querySelector("video")).toBeNull();
  });
});

describe("laço da vivacidade", () => {
  it("aprova depois de quadros sem rosto, sem reprovar no primeiro", async () => {
    detectar
      .mockResolvedValueOnce({ face: [] })
      .mockResolvedValueOnce({ face: [{ real: 0.1, live: 0.1 }] })
      .mockResolvedValue({ face: [ROSTO_VIVO] });
    const estados: string[] = [];

    await expect(provarVivacidade((estado) => estados.push(estado))).resolves.toBe(true);
    expect(estados).toEqual(["procurando_rosto", "rosto_encontrado", "vivacidade_confirmada"]);
    expect(detectar).toHaveBeenCalledTimes(3);
  });

  it("reprova quando o tempo se esgota sem rosto vivo", async () => {
    detectar.mockResolvedValue({ face: [] });
    vi.useFakeTimers();

    const emCurso = provarVivacidade();
    await vi.advanceTimersByTimeAsync(16_000);

    await expect(emCurso).resolves.toBe(false);
  });
});

describe("descritor", () => {
  it("devolve o embedding e encerra a câmera no mesmo ato", async () => {
    await prepararCaptura();

    await expect(gerarDescritor()).resolves.toEqual([0.1, 0.2]);
  });

  it("lança quando o quadro aprovado não produz embedding", async () => {
    detectar.mockResolvedValue({ face: [{ real: 0.9, live: 0.9 }] });
    await prepararCaptura();

    await expect(gerarDescritor()).rejects.toThrow(/descritor/i);
  });
});
