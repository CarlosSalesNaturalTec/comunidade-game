import { render } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { Avatar } from "./Avatar";
import { CAMADAS_DO_AVATAR, type NomeDeCamada } from "./catalogo";
import { AVATAR_PADRAO_DO_PROJETO, escreverAvatar, lerAvatar } from "./objeto";

// As nove camadas do documento 15 §7.1, na ordem de composição.
const CAMADAS_NA_ORDEM: NomeDeCamada[] = [
  "fundo",
  "tom",
  "cabelo",
  "cabelo_cor",
  "rosto",
  "olhos",
  "boca",
  "roupa",
  "acessorio",
];

function desenhar(avatar: Parameters<typeof Avatar>[0]["avatar"]): SVGSVGElement {
  const { container } = render(<Avatar avatar={avatar} />);
  const svg = container.querySelector("svg");
  if (!svg) throw new Error("O avatar não desenhou nenhum SVG.");
  return svg as SVGSVGElement;
}

function camadasDesenhadas(svg: SVGSVGElement): string[] {
  return [...svg.querySelectorAll("g[data-camada]")]
    .filter((grupo) => grupo.parentElement === svg)
    .map((grupo) => grupo.getAttribute("data-camada") ?? "");
}

describe("o avatar se compõe pelas nove camadas do catálogo (documento 15 §7.1)", () => {
  it("monta as nove camadas na ordem da tabela", () => {
    expect(camadasDesenhadas(desenhar(AVATAR_PADRAO_DO_PROJETO))).toEqual(CAMADAS_NA_ORDEM);
  });

  it("o catálogo tem as nove camadas, e cada escolha vem dele", () => {
    expect(CAMADAS_DO_AVATAR.map((camada) => camada.nome)).toEqual(CAMADAS_NA_ORDEM);

    for (const camada of CAMADAS_DO_AVATAR) {
      expect(camada.tracos.length).toBeGreaterThan(0);
      // O padrão da camada é traço do próprio catálogo — é nele que cai o
      // desconhecido, e é dele que o avatar padrão do projeto se compõe.
      expect(camada.tracos.map((traco) => traco.id)).toContain(camada.padrao);
    }
  });

  it("todo traço de todo camada desenha, sem quebrar nenhuma", () => {
    for (const camada of CAMADAS_DO_AVATAR) {
      for (const traco of camada.tracos) {
        const svg = desenhar({ ...AVATAR_PADRAO_DO_PROJETO, [camada.nome]: traco.id });
        expect(camadasDesenhadas(svg)).toEqual(CAMADAS_NA_ORDEM);
      }
    }
  });
});

describe("cada traço tem nome dizível (documento 15 §7, exigência 2)", () => {
  it("nenhum traço aparece como código ou número", () => {
    for (const camada of CAMADAS_DO_AVATAR) {
      expect(camada.rotulo).toMatch(/\p{L}{3}/u);
      for (const traco of camada.tracos) {
        // Nome em português simples, com palavra de verdade — nunca "modelo 7",
        // nunca dígito, nunca código.
        expect(traco.nome).toMatch(/^\p{Lu}[\p{L}\p{M} çãáéíóúâêôõ-]+$/u);
        expect(traco.nome).not.toMatch(/\d/);
        expect(traco.nome).not.toMatch(/modelo/i);
      }
    }
  });
});

describe("a escala de pele abre pelo mais retinto (documento 15 §7.1)", () => {
  it("o primeiro tom de pele é o mais retinto, e é o padrão da camada", () => {
    const tom = CAMADAS_DO_AVATAR.find((camada) => camada.nome === "tom");
    if (!tom) throw new Error("A camada de tom de pele não está no catálogo.");

    expect(tom.tracos).toHaveLength(8);
    expect(tom.padrao).toBe(tom.tracos[0].id);

    // Escala monotônica do mais retinto ao mais claro: a soma dos canais de
    // cada degrau cresce, degrau por degrau.
    const luminosidades = tom.tracos.map((traco) => {
      const hex = (traco.cor ?? "").replace("#", "");
      return Number.parseInt(hex.slice(0, 2), 16) + Number.parseInt(hex.slice(2, 4), 16);
    });
    expect(luminosidades).toEqual([...luminosidades].sort((a, b) => a - b));
    expect(luminosidades[0]).toBeLessThan(luminosidades[7]);
  });

  it("as texturas de cabelo crespo vêm antes das lisas", () => {
    const cabelo = CAMADAS_DO_AVATAR.find((camada) => camada.nome === "cabelo");
    if (!cabelo) throw new Error("A camada de cabelo não está no catálogo.");

    const ordem = cabelo.tracos.map((traco) => traco.id);
    for (const crespa of ["black-power", "crespo-curto", "trancas", "dreads"]) {
      expect(ordem.indexOf(crespa)).toBeGreaterThanOrEqual(0);
      expect(ordem.indexOf(crespa)).toBeLessThan(ordem.indexOf("liso"));
    }
  });
});

describe("nenhum item é de um gênero (documento 15 §7, exigência 4)", () => {
  it("todos os traços de todas as camadas são oferecidos, sem depender da forma de tratamento", () => {
    for (const camada of CAMADAS_DO_AVATAR) {
      for (const traco of camada.tracos) {
        expect(traco).not.toHaveProperty("formaDeTratamento");
        expect(traco).not.toHaveProperty("genero");
        expect(traco.nome).not.toMatch(/menin[oa]|masculin|feminin|guerreir[oa]\b/i);
      }
    }
    // O catálogo é uma lista só por camada: não há recorte por persona a
    // aplicar, e portanto não há como restringi-lo pela forma de tratamento.
    expect(Object.keys(CAMADAS_DO_AVATAR[0])).toEqual(["nome", "rotulo", "padrao", "tracos"]);
  });
});

describe("compor e desenhar não pedem rede (documento 15 §7, princípio 6)", () => {
  it("nenhuma requisição sai do aparelho, e o desenho não referencia domínio algum", () => {
    const rede = vi.spyOn(globalThis, "fetch");
    const svg = desenhar(escreverAvatar({ cabelo: "dreads", roupa: "jaqueta" }));

    expect(rede).not.toHaveBeenCalled();
    expect(svg.querySelector("image")).toBeNull();
    expect(svg.outerHTML).not.toMatch(/https?:|url\(/);
    rede.mockRestore();
  });
});

describe("traço desconhecido cai no padrão da camada (documento 15 §7.2)", () => {
  it("a camada desconhecida cai no padrão dela e as demais escolhas ficam", () => {
    const lido = lerAvatar(
      JSON.stringify({ v: 1, cabelo: "penteado-que-nao-existe", roupa: "regata" }),
    );

    expect(lido.cabelo).toBe(AVATAR_PADRAO_DO_PROJETO.cabelo);
    expect(lido.roupa).toBe("regata");
    expect(camadasDesenhadas(desenhar(lido))).toEqual(CAMADAS_NA_ORDEM);
  });

  it("o objeto do documento 15 §7.2 renderiza como está escrito lá", () => {
    const doDocumento = {
      v: 1,
      fundo: "marca-100",
      tom: "t2",
      cabelo: "black-power",
      cabelo_cor: "c1",
      rosto: "r3",
      olhos: "o2",
      boca: "b1",
      roupa: "camisa-projeto",
      acessorio: "nenhum",
    };

    expect(lerAvatar(JSON.stringify(doDocumento))).toEqual(doDocumento);
  });

  it("o avatar gravado no formato antigo cai inteiro no padrão, sem quebrar", () => {
    // O que a App 01 gravava antes deste contrato: forma de tratamento e
    // características ditas em texto livre, sem nenhum traço do catálogo
    // (design — decisão 2).
    const antigo = JSON.stringify({
      formaDeTratamento: "guerreira",
      caracteristicasDoAvatar: "cabelo crespo curto e capa vermelha",
    });

    expect(lerAvatar(antigo)).toEqual(AVATAR_PADRAO_DO_PROJETO);
    expect(camadasDesenhadas(desenhar(antigo))).toEqual(CAMADAS_NA_ORDEM);
  });

  it("o objeto aninhado ao lado da forma de tratamento é lido do mesmo jeito", () => {
    const envelope = JSON.stringify({
      formaDeTratamento: "guerreiro",
      avatar: { v: 1, cabelo: "trancas", tom: "t5" },
    });

    const lido = lerAvatar(envelope);
    expect(lido.cabelo).toBe("trancas");
    expect(lido.tom).toBe("t5");
  });

  it("texto que não é JSON algum não quebra a renderização", () => {
    expect(lerAvatar("trança-e-capa")).toEqual(AVATAR_PADRAO_DO_PROJETO);
    expect(camadasDesenhadas(desenhar("trança-e-capa"))).toEqual(CAMADAS_NA_ORDEM);
  });
});

describe("avatar que falta usa o padrão do projeto (documento 15 §7.3)", () => {
  it("sem avatar algum, o desenho é o avatar padrão do projeto", () => {
    expect(lerAvatar(null)).toEqual(AVATAR_PADRAO_DO_PROJETO);
    expect(lerAvatar("")).toEqual(AVATAR_PADRAO_DO_PROJETO);
    expect(lerAvatar(undefined)).toEqual(AVATAR_PADRAO_DO_PROJETO);
  });

  it("o padrão do projeto sai na mesma moldura, sem marca de diferença", () => {
    const semAvatar = desenhar(null);
    const comAvatar = desenhar(escreverAvatar({ tom: "t7", cabelo: "liso" }));

    expect(semAvatar.getAttribute("class")).toBe(comAvatar.getAttribute("class"));
    expect(semAvatar.getAttribute("viewBox")).toBe(comAvatar.getAttribute("viewBox"));
    expect(semAvatar.getAttribute("width")).toBe(comAvatar.getAttribute("width"));
    expect(camadasDesenhadas(semAvatar)).toEqual(camadasDesenhadas(comAvatar));
  });

  it("o padrão do projeto é composto em cores da marca", () => {
    expect(AVATAR_PADRAO_DO_PROJETO.fundo).toBe("marca-100");
    expect(AVATAR_PADRAO_DO_PROJETO.roupa).toBe("camisa-projeto");
    expect(AVATAR_PADRAO_DO_PROJETO.v).toBe(1);
  });
});

describe("o avatar ao lado do nick é decorativo (documento 15 §5, `RN-04-14`)", () => {
  it("o desenho nunca é a identificação de ninguém — quem identifica é o nick", () => {
    const svg = desenhar(null);
    expect(svg.getAttribute("aria-hidden")).toBe("true");
    expect(svg.getAttribute("role")).toBeNull();
  });
});

describe("a escrita monta o objeto versionado (documento 15 §7.2)", () => {
  it("camada não escolhida fica no padrão dela, e a versão vai gravada", () => {
    expect(escreverAvatar({ cabelo: "coque" })).toEqual({
      ...AVATAR_PADRAO_DO_PROJETO,
      cabelo: "coque",
    });
  });

  it("escolha fora do catálogo não é gravada", () => {
    expect(escreverAvatar({ cabelo: "inventado" }).cabelo).toBe(
      AVATAR_PADRAO_DO_PROJETO.cabelo,
    );
  });
});
