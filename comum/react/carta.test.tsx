import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { BadgeDaFamilia, type FamiliaDeBadge } from "./BadgeDaFamilia";
import { CartaDoPersonagem, cartaEstaCompleta, type DadosDaCarta } from "./CartaDoPersonagem";
import { EmblemaDeNivel } from "./EmblemaDeNivel";
import { GLIFO_GENERICO_DE_PODER, GlifoDePoder, glifoDoPoder } from "./GlifoDePoder";

const AQUI = dirname(fileURLToPath(import.meta.url));
const ESTILOS = readFileSync(join(AQUI, "estilos.css"), "utf-8");
const ARQUIVO_DO_GLIFO = readFileSync(join(AQUI, "GlifoDePoder.tsx"), "utf-8");
const ARQUIVO_DO_BADGE = readFileSync(join(AQUI, "BadgeDaFamilia.tsx"), "utf-8");

/** O corpo da regra que abre com o seletor pedido, sem as regras seguintes. */
function corpoDaRegra(seletor: string): string {
  const inicio = ESTILOS.indexOf(`${seletor} {`);
  expect(inicio).toBeGreaterThan(-1);
  const abre = ESTILOS.indexOf("{", inicio);
  return ESTILOS.slice(abre + 1, ESTILOS.indexOf("}", abre));
}

const GUERREIRA_COMPLETA: DadosDaCarta = {
  variante: "guerreiro",
  avatar: null,
  nick: "Zeferina",
  badges: [
    { familia: "de_nivel", poder: "Poder da IA e Robótica" },
    { familia: "de_autoria", poder: "Poder do Território" },
  ],
  poderes: [{ poder: "Poder da IA e Robótica", nivel: 3 }],
  desempenho: "12º lugar, com 40 pontos",
  criacoes: ["Robô de reuso da praça"],
};

describe("CartaDoPersonagem — os valores do documento 15 §8.1", () => {
  it("a carta se monta com os valores do documento 15", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_COMPLETA} />);
    const carta = container.querySelector(".cg-carta");
    expect(carta).not.toBeNull();

    // O avatar é quadrado, recortado em círculo e ocupa metade da largura.
    const avatar = corpoDaRegra(".cg-carta__avatar");
    expect(avatar).toContain("width: 50%;");
    expect(avatar).toContain("aspect-ratio: 1;");
    expect(avatar).toContain("border-radius: var(--raio-ficha);");
    expect(carta?.querySelector(".cg-carta__avatar svg")).not.toBeNull();

    // O nick na família de destaque, em `1,125` rem.
    const nick = corpoDaRegra(".cg-carta__nick");
    expect(nick).toContain("font-family: var(--fonte-destaque);");
    expect(nick).toContain("font-size: var(--escala-1125);");
    expect(screen.getByText("Zeferina")).toBeInTheDocument();

    // Superfície, borda de 1 px e o raio que o temperamento declara — a carta
    // lê o token, nunca o número.
    const moldura = corpoDaRegra(".cg-carta");
    expect(moldura).toContain("background: var(--cor-superficie);");
    expect(moldura).toContain("border: 1px solid var(--cor-borda);");
    expect(moldura).toContain("border-radius: var(--raio-carta);");
  });

  it("a carta do Guerreiro(a) não expõe o que é vedado", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_COMPLETA} />);

    // O que o documento 11 §8.2 manda exibir está lá.
    expect(screen.getByText("Zeferina")).toBeInTheDocument();
    expect(screen.getByText("12º lugar, com 40 pontos")).toBeInTheDocument();
    expect(screen.getByText(/Badge de nível/)).toBeInTheDocument();
    expect(screen.getByText(/Nível 3/)).toBeInTheDocument();
    expect(screen.getByText("Robô de reuso da praça")).toBeInTheDocument();

    // O que ela nunca exibe: imagem real, nome civil, rede social, canal de
    // contato. O avatar é SVG composto no aparelho — não há imagem alguma —, e
    // nenhum endereço externo sai da carta (invariantes 9 e 10).
    expect(container.querySelector("img, picture, video")).toBeNull();
    expect(container.querySelector("a[href]")).toBeNull();
    expect(container.textContent).not.toMatch(/@|https?:\/\/|\(\d{2}\)/);
  });

  it("sem o dado que a variante exige, não se usa carta", () => {
    const semDesempenho: DadosDaCarta = { ...GUERREIRA_COMPLETA, desempenho: undefined };
    const semBadges: DadosDaCarta = { ...GUERREIRA_COMPLETA, badges: undefined };
    const semNick: DadosDaCarta = { ...GUERREIRA_COMPLETA, nick: "  " };

    for (const incompleta of [semDesempenho, semBadges, semNick]) {
      expect(cartaEstaCompleta(incompleta)).toBe(false);
      const { container } = render(<CartaDoPersonagem dados={incompleta} />);
      // Nenhuma carta pela metade é apresentada: quem monta a tela é que
      // escolhe a outra forma.
      expect(container.querySelector(".cg-carta")).toBeNull();
    }

    // Avatar que falta não torna a carta incompleta: o documento 15 §7.3 manda
    // desenhar o avatar padrão do projeto.
    expect(cartaEstaCompleta({ ...GUERREIRA_COMPLETA, avatar: undefined })).toBe(true);
    // Lista vazia é "ainda nenhum", não falta de dado.
    expect(cartaEstaCompleta({ ...GUERREIRA_COMPLETA, badges: [], criacoes: [] })).toBe(true);
  });
});

describe("EmblemaDeNivel — a marca é contável (documento 15 §8.2)", () => {
  it("o nível se conta na moldura", () => {
    const { container } = render(<EmblemaDeNivel nivel={3} poder="Poder da IA e Robótica" />);
    expect(container.querySelectorAll("[data-marca]")).toHaveLength(3);
    expect(container.querySelector(".cg-emblema-de-nivel--fechada")).toBeNull();

    // Uma marca no nível 1, cinco no 5 — a contagem é a do nível.
    for (const nivel of [1, 2, 4, 5]) {
      const { container: outro } = render(
        <EmblemaDeNivel nivel={nivel} poder="Poder da Rima" />,
      );
      expect(outro.querySelectorAll("[data-marca]")).toHaveLength(nivel);
    }

    // Legível sem depender de cor: a marca é forma, e herda a cor do texto.
    const marca = corpoDaRegra(".cg-emblema-de-nivel__marca");
    expect(marca).toContain("background: currentColor;");
    expect(marca).not.toMatch(/var\(--cor-/);
    expect(corpoDaRegra(".cg-emblema-de-nivel")).toContain("1px dashed currentColor");
  });

  it("o nível 5 fecha a moldura", () => {
    const { container } = render(<EmblemaDeNivel nivel={5} poder="Poder da IA e Robótica" />);
    expect(container.querySelectorAll("[data-marca]")).toHaveLength(5);
    expect(container.querySelector(".cg-emblema-de-nivel--fechada")).not.toBeNull();
    expect(corpoDaRegra(".cg-emblema-de-nivel--fechada")).toContain("border-style: solid;");
    // A moldura fechada não fica só na forma: leva o rótulo, como o §5 exige.
    expect(screen.getByText("Mestre Aprendiz")).toBeInTheDocument();
  });

  it("não há emblema global", () => {
    render(<EmblemaDeNivel nivel={2} poder="Poder do Território" />);
    // O emblema é de uma trilha ou de um poder, e a moldura carrega o nome —
    // o tipo exige `poder`, e não há como montar emblema sem ele.
    expect(screen.getByText("Poder do Território")).toBeInTheDocument();
    expect(screen.getByText("Nível 2")).toBeInTheDocument();
  });
});

const FAMILIAS: [FamiliaDeBadge, string][] = [
  ["de_nivel", "escudo"],
  ["de_conquista", "estrela"],
  ["de_valores_e_causas", "coracao"],
  ["de_territorio", "gota"],
  ["de_autoria", "folha-com-canto-dobrado"],
  ["de_protagonismo", "hexagono"],
];

describe("BadgeDaFamilia — uma silhueta por família (documento 15 §8.3)", () => {
  it("a família se reconhece pela forma", () => {
    const { container } = render(
      <div>
        {FAMILIAS.map(([familia]) => (
          <BadgeDaFamilia key={familia} familia={familia} />
        ))}
      </div>,
    );

    const silhuetas = [...container.querySelectorAll("[data-silhueta]")];
    expect(silhuetas.map((forma) => forma.getAttribute("data-silhueta"))).toEqual(
      FAMILIAS.map(([, forma]) => forma),
    );

    for (const forma of silhuetas) {
      // Legível a `24` px, em traço, sem cor própria.
      expect(forma.getAttribute("viewBox")).toBe("0 0 24 24");
      expect(forma.getAttribute("stroke")).toBe("currentColor");
      expect(forma.getAttribute("fill")).toBe("none");
      expect(forma.getAttribute("aria-hidden")).toBe("true");
    }
    expect(corpoDaRegra(".cg-badge__forma")).toContain("width: var(--espaco-24);");
    expect(ARQUIVO_DO_BADGE).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);

    // A forma não carrega o significado sozinha: cada badge leva rótulo (§5).
    for (const [, forma] of FAMILIAS) expect(forma).not.toBe("");
    expect(screen.getByText("Badge de território")).toBeInTheDocument();
    expect(screen.getByText("Badge de protagonismo")).toBeInTheDocument();
  });

  it("dois badges da mesma família se distinguem pelo poder", () => {
    const { container } = render(
      <>
        <BadgeDaFamilia familia="de_nivel" poder="Poder da IA e Robótica" />
        <BadgeDaFamilia familia="de_nivel" poder="Poder do Território" />
      </>,
    );

    const silhuetas = [...container.querySelectorAll("[data-silhueta]")];
    // Ambos escudo: a silhueta diz a família, nunca o poder.
    expect(silhuetas.map((forma) => forma.getAttribute("data-silhueta"))).toEqual([
      "escudo",
      "escudo",
    ]);

    // O que os separa é o glifo do poder, dentro da silhueta.
    const glifos = [...container.querySelectorAll(".cg-badge__glifo svg")];
    expect(glifos).toHaveLength(2);
    expect(glifos[0].innerHTML).not.toBe(glifos[1].innerHTML);
    expect(screen.getByText(/Poder da IA e Robótica/)).toBeInTheDocument();
    expect(screen.getByText(/Poder do Território/)).toBeInTheDocument();
  });
});

describe("GlifoDePoder — o glifo acompanha o nome (documento 15 §8.4)", () => {
  it("o glifo nunca aparece sem o nome do poder", () => {
    const { container } = render(<GlifoDePoder poder="Poder da Capoeira" />);
    expect(container.querySelector(".cg-glifo-de-poder svg")).not.toBeNull();
    expect(screen.getByText("Poder da Capoeira")).toBeInTheDocument();

    // Os seis poderes do catálogo do documento 02 §2 têm glifo próprio, e
    // nenhum deles é o genérico.
    const catalogo = [
      "Poder da IA e Robótica",
      "Poder do Território",
      "Poder Sustentador",
      "Poder da Rima",
      "Poder das Redes",
      "Poder da Capoeira",
    ];
    const glifos = catalogo.map((poder) => glifoDoPoder(poder));
    expect(new Set(glifos).size).toBe(catalogo.length);
    expect(glifos).not.toContain(GLIFO_GENERICO_DE_PODER);
  });

  it("poder sem glifo cai no genérico", () => {
    // O catálogo é dado da gestão e cresce sem passar por aqui.
    expect(glifoDoPoder("Poder da Ancestralidade")).toBe(GLIFO_GENERICO_DE_PODER);
    const { container } = render(<GlifoDePoder poder="Poder da Ancestralidade" />);
    expect(container.querySelector("svg")).not.toBeNull();
    expect(screen.getByText("Poder da Ancestralidade")).toBeInTheDocument();
  });

  it("o poder não carrega cor", () => {
    const { container } = render(
      <>
        <GlifoDePoder poder="Poder da Rima" />
        <GlifoDePoder poder="Poder das Redes" />
      </>,
    );

    for (const svg of container.querySelectorAll("svg")) {
      expect(svg.getAttribute("stroke")).toBe("currentColor");
      expect(svg.getAttribute("fill")).toBe("none");
      for (const forma of svg.querySelectorAll("*")) {
        expect(forma.getAttribute("fill")).toBeNull();
        expect(forma.getAttribute("stroke")).toBeNull();
      }
    }
    // Nem o arquivo que resolve o glifo guarda cor: cor é da grandeza e do
    // estado (documento 15 §§8.4, 9).
    expect(ARQUIVO_DO_GLIFO).not.toMatch(/#[0-9a-fA-F]{3,8}\b/);
    expect(ARQUIVO_DO_GLIFO).not.toMatch(/\brgba?\(|\bhsla?\(/);
  });
});
