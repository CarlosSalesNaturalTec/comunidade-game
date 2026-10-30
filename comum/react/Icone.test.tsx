import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { BadgeDaFamilia, type FamiliaDeBadge } from "./BadgeDaFamilia";
import { CAMINHO_DA_ESTRELA, Icone, type NomeDeGlifo } from "./Icone";

const ARQUIVO = readFileSync(
  join(dirname(fileURLToPath(import.meta.url)), "Icone.tsx"),
  "utf-8",
);

const GLIFOS: NomeDeGlifo[] = [
  "onboarding",
  "presenca",
  "equipes",
  "quiz",
  "medicao",
  "troca",
  "som",
  "som-desligado",
  "encerrar",
  "momento-de-troca",
  "entregas",
  "medalha",
  "pincel",
  "ponto-extra",
];

function desenhar(glifo: NomeDeGlifo): SVGSVGElement {
  const { container } = render(<Icone glifo={glifo} />);
  const svg = container.querySelector("svg");
  expect(svg).not.toBeNull();
  return svg as SVGSVGElement;
}

describe("Icone — nenhum ícone vem de fora (documento 15 §11.1, princípio 6)", () => {
  it("desenha os glifos embutidos, sem pedir nada a domínio algum", () => {
    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      // SVG embutido: o desenho está no próprio documento, não numa imagem
      // buscada. Nada de `<img>`, `<use>` nem `url(...)` — nenhum pedido sai.
      expect(svg.querySelector("img, image, use")).toBeNull();
      expect(svg.innerHTML).not.toContain("url(");
      expect(svg.innerHTML).not.toContain("http");
      expect(svg.querySelector("path, circle")).not.toBeNull();
    }
  });

  it("o desenho vive no pacote da aplicação, sem endereço de terceiro no arquivo", () => {
    expect(ARQUIVO).not.toMatch(/https?:\/\/(?!www\.w3\.org)/);
  });
});

describe("Icone — o ícone acompanha o tema (documento 15 §§11.1, 12)", () => {
  it("herda a cor do texto por currentColor, e não preenche", () => {
    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      expect(svg.getAttribute("stroke")).toBe("currentColor");
      expect(svg.getAttribute("fill")).toBe("none");
    }
  });

  it("nenhum arquivo de glifo guarda valor de cor", () => {
    // Nem hexadecimal, nem `rgb()`, nem nome de cor em atributo de traço ou
    // preenchimento: trocar o tema troca o ícone junto.
    expect(ARQUIVO).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    expect(ARQUIVO).not.toMatch(/\brgba?\(/);
    expect(ARQUIVO).not.toMatch(/\bhsla?\(/);

    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      for (const forma of svg.querySelectorAll("*")) {
        expect(forma.getAttribute("fill")).toBeNull();
        expect(forma.getAttribute("stroke")).toBeNull();
      }
    }
  });

  it("desenha na grade de 24 px, com traço de 2 px de ponta e junta arredondadas", () => {
    const svg = desenhar("presenca");
    expect(svg.getAttribute("viewBox")).toBe("0 0 24 24");
    expect(svg.getAttribute("stroke-width")).toBe("2");
    expect(svg.getAttribute("stroke-linecap")).toBe("round");
    expect(svg.getAttribute("stroke-linejoin")).toBe("round");
  });

  it("aceita os quatro tamanhos do documento 15 §11.1, e usa 24 por padrão", () => {
    expect(desenhar("presenca").getAttribute("width")).toBe("24");
    for (const tamanho of [16, 24, 32, 48] as const) {
      const { container } = render(<Icone glifo="presenca" tamanho={tamanho} />);
      const svg = container.querySelector("svg") as SVGSVGElement;
      expect(svg.getAttribute("width")).toBe(String(tamanho));
      expect(svg.getAttribute("height")).toBe(String(tamanho));
    }
  });
});

describe("Icone — o par do alternador difere pela forma (documento 15 §5)", () => {
  it("o som ligado e o som desligado são desenhos diferentes", () => {
    const ligado = desenhar("som").innerHTML;
    const desligado = desenhar("som-desligado").innerHTML;
    // Não é o mesmo desenho em duas cores: nenhum estado se comunica por cor
    // sozinha, e aqui nenhum dos dois declara cor alguma.
    expect(ligado).not.toBe(desligado);
  });

  it("a chave do momento de troca não repete o glifo do caminho da troca", () => {
    // Com o momento aberto os dois ficam encostados na tela inicial e têm
    // funções opostas (design — decisão 6).
    expect(desenhar("momento-de-troca").innerHTML).not.toBe(desenhar("troca").innerHTML);
  });
});

describe("Icone — o ícone não aparece sozinho (documento 15 §5)", () => {
  it("é decorativo: quem navega por leitor de tela alcança o rótulo, não o desenho", () => {
    for (const glifo of GLIFOS) {
      const svg = desenhar(glifo);
      expect(svg.getAttribute("aria-hidden")).toBe("true");
      // Sem nome acessível próprio: o ícone não concorre com o rótulo.
      expect(svg.querySelector("title")).toBeNull();
      expect(svg.getAttribute("aria-label")).toBeNull();
    }
  });

  it("o elemento acionável que o leva continua identificado pelo rótulo", () => {
    render(
      <button type="button">
        <Icone glifo="presenca" />
        Presença — registrar a presença de hoje
      </button>,
    );
    const botao = screen.getByRole("button", {
      name: "Presença — registrar a presença de hoje",
    });
    // O rótulo é o nome acessível inteiro: o glifo não acrescenta nem
    // substitui palavra alguma.
    expect(botao.querySelector("svg")).not.toBeNull();
  });
});

describe("Icone — os símbolos das colunas da carta (documento 15 §§8.1, 8.3, 9)", () => {
  /** O desenho de uma silhueta de família, como `BadgeDaFamilia` a apresenta. */
  function silhueta(familia: FamiliaDeBadge): string {
    const { container } = render(<BadgeDaFamilia familia={familia} />);
    const forma = container.querySelector(".cg-badge__forma");
    expect(forma).not.toBeNull();
    return (forma as SVGSVGElement).innerHTML;
  }

  const FAMILIAS: FamiliaDeBadge[] = [
    "de_nivel",
    "de_conquista",
    "de_valores_e_causas",
    "de_territorio",
    "de_autoria",
    "de_protagonismo",
  ];

  it("medalha e pincel não repetem silhueta de família alguma", () => {
    // No cabeçalho de uma coluna, a silhueta de família afirmaria família
    // errada: o losango diria "badge de nível" (documento 15 §8.3).
    const desenhos = [desenhar("medalha").innerHTML, desenhar("pincel").innerHTML];
    for (const familia of FAMILIAS) {
      for (const desenho of desenhos) expect(desenho).not.toBe(silhueta(familia));
    }
  });

  it("nenhum símbolo de coluna é o escudo da marca nem o círculo da moeda", () => {
    // O escudo é a forma da marca (invariante 24) e o círculo é da moeda
    // (§9): nenhum dos dois pode encabeçar coluna de carta. O escudo vem do
    // próprio arquivo da marca, para que redesenhá-lo não deixe este teste
    // afirmando uma forma que a marca já não tem.
    const simbolo = readFileSync(
      join(dirname(fileURLToPath(import.meta.url)), "..", "marca", "simbolo.svg"),
      "utf-8",
    );
    const tracados = [...simbolo.matchAll(/ d="([^"]+)"/g)].map((m) => m[1]);
    expect(tracados.length).toBeGreaterThan(0);

    for (const glifo of ["medalha", "pincel", "ponto-extra"] as const) {
      const svg = desenhar(glifo);
      expect(svg.querySelector("circle")).toBeNull();
      for (const tracado of tracados) expect(svg.innerHTML).not.toContain(tracado);
    }
  });

  it("a estrela do ponto extra é a mesma forma da cheia, e sai vazada", () => {
    // Documento 15 §9: ponto regular é estrela cheia e ponto extra é vazada.
    // A forma é uma só — o que separa as duas é o preenchimento, e no sistema
    // de ícone o vazado é a regra.
    const svg = desenhar("ponto-extra");
    expect(svg.getAttribute("fill")).toBe("none");
    expect(svg.querySelector("path")?.getAttribute("d")).toBe(CAMINHO_DA_ESTRELA);
  });
});
