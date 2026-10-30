import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { BadgeDaFamilia, type FamiliaDeBadge } from "./BadgeDaFamilia";
import { CartaDoPersonagem, cartaEstaCompleta, type DadosDaCarta } from "./CartaDoPersonagem";
import { EmblemaDeNivel } from "./EmblemaDeNivel";
import { GLIFO_GENERICO_DE_PODER, GlifoDePoder, glifoDoPoder } from "./GlifoDePoder";
import { TerritorioDaComunidade } from "./TerritorioDaComunidade";

const AQUI = dirname(fileURLToPath(import.meta.url));
const ESTILOS = readFileSync(join(AQUI, "estilos.css"), "utf-8");
const ARQUIVO_DO_GLIFO = readFileSync(join(AQUI, "GlifoDePoder.tsx"), "utf-8");
const ARQUIVO_DO_BADGE = readFileSync(join(AQUI, "BadgeDaFamilia.tsx"), "utf-8");

/** O corpo da regra que abre com o seletor pedido, sem as regras seguintes. */
function corpoDaRegra(seletor: string): string {
  // Ancorado na abertura de linha: um seletor curto também casa com o
  // descendente que termina nele, e o descendente pode vir antes no arquivo.
  const inicio = ESTILOS.indexOf(`\n${seletor} {`);
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
  ["de_nivel", "losango"],
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

  it("nenhuma silhueta é o escudo, que passou a ser a forma da marca", () => {
    const { container } = render(
      <div>
        {FAMILIAS.map(([familia]) => (
          <BadgeDaFamilia key={familia} familia={familia} />
        ))}
      </div>,
    );

    const formas = [...container.querySelectorAll("[data-silhueta]")].map((forma) =>
      forma.getAttribute("data-silhueta"),
    );
    expect(formas).not.toContain("escudo");
    // E as seis continuam distintas entre si, que é o que a §8.3 exige.
    expect(new Set(formas).size).toBe(FAMILIAS.length);
  });

  it("dois badges da mesma família se distinguem pelo poder", () => {
    const { container } = render(
      <>
        <BadgeDaFamilia familia="de_nivel" poder="Poder da IA e Robótica" />
        <BadgeDaFamilia familia="de_nivel" poder="Poder do Território" />
      </>,
    );

    const silhuetas = [...container.querySelectorAll("[data-silhueta]")];
    // Ambos losango: a silhueta diz a família, nunca o poder.
    expect(silhuetas.map((forma) => forma.getAttribute("data-silhueta"))).toEqual([
      "losango",
      "losango",
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

const COMUNIDADE_COMPLETA: DadosDaCarta = {
  variante: "comunidade-virtual",
  nome: "Guerreira Zeferina",
  territorio: "Salvador, Bahia",
  seriesAtivas: 4,
  seriesAbertas: 6,
  vinculados: 23,
  camadas: [
    { tipo: "Temperatura", registrosValidos: 30, ativo: true },
    { tipo: "Resíduos", registrosValidos: 10, ativo: false },
  ],
  bairrosPublicados: 2,
};

describe("CartaDoPersonagem — a variante Comunidade Virtual do documento 11 §8.2", () => {
  it("a carta da comunidade traz os cinco campos da variante", () => {
    render(<CartaDoPersonagem dados={COMUNIDADE_COMPLETA} />);

    expect(screen.getByText("Guerreira Zeferina")).toBeInTheDocument();
    expect(screen.getByText("Salvador, Bahia")).toBeInTheDocument();
    expect(screen.getByText("Séries ativas")).toBeInTheDocument();
    expect(screen.getByText("4")).toBeInTheDocument();
    expect(screen.getByText("Guerreiros e Guerreiras vinculados")).toBeInTheDocument();
    expect(screen.getByText("23")).toBeInTheDocument();
    expect(
      screen.getByRole("img", { name: /Território de Guerreira Zeferina/ }),
    ).toBeVisible();
  });

  it("a carta da comunidade não desce abaixo do bairro nem identifica coletor", () => {
    const { container } = render(<CartaDoPersonagem dados={COMUNIDADE_COMPLETA} />);
    const texto = container.textContent ?? "";

    for (const proibido of ["Rua", "Condomínio", "Bloco", "Quadra", "nick", "coletor"]) {
      expect(texto).not.toContain(proibido);
    }
    expect(container.querySelector(".cg-carta__avatar")).toBeNull();
  });

  it("comunidade sem os indicadores não vira carta incompleta", () => {
    // O que a lista devolve para a comunidade abaixo do piso: nome e
    // localização, com os quatro indicadores nulos (`RN-08-28`).
    const abaixoDoPiso: DadosDaCarta = {
      ...COMUNIDADE_COMPLETA,
      seriesAtivas: null,
      seriesAbertas: null,
    };
    expect(cartaEstaCompleta(abaixoDoPiso)).toBe(false);
    const { container } = render(<CartaDoPersonagem dados={abaixoDoPiso} />);
    expect(container.querySelector(".cg-carta")).toBeNull();
  });
});

describe("TerritorioDaComunidade — a representação visual do documento 11 §8.3", () => {
  it("comunidade recém-criada aparece como território vazio", () => {
    const { container } = render(<TerritorioDaComunidade nome="Nova" />);

    expect(screen.getByRole("img", { name: /Território de Nova, ainda vazio/ })).toBeVisible();
    expect(screen.getByText(/Território ainda vazio/)).toBeInTheDocument();
    expect(container.querySelectorAll(".cg-territorio__camada")).toHaveLength(0);
    expect(container.querySelector(".cg-territorio__contorno")).not.toBeNull();
  });

  it("o desenho cresce e ganha detalhe conforme os registros e os bairros", () => {
    const pequena = render(
      <TerritorioDaComunidade
        nome="Zeferina"
        bairrosPublicados={1}
        camadas={[{ tipo: "Temperatura", registrosValidos: 3, ativo: true }]}
        seriesAbertas={2}
        seriesAtivas={1}
      />,
    );
    const ladosAntes = ladosDoContorno(pequena.container);
    const aneisAntes = pequena.container.querySelectorAll(".cg-territorio__camada").length;
    pequena.unmount();

    const crescida = render(
      <TerritorioDaComunidade
        nome="Zeferina"
        bairrosPublicados={5}
        camadas={[
          { tipo: "Temperatura", registrosValidos: 30, ativo: true },
          { tipo: "Resíduos", registrosValidos: 12, ativo: true },
        ]}
        seriesAbertas={2}
        seriesAtivas={2}
      />,
    );

    expect(ladosDoContorno(crescida.container)).toBeGreaterThan(ladosAntes);
    expect(
      crescida.container.querySelectorAll(".cg-territorio__camada").length,
    ).toBeGreaterThan(aneisAntes);
    // O anel do tipo com mais registros é o maior — a medida é a participação
    // dele nos registros válidos publicados, nunca um número de estilo.
    const raios = [...crescida.container.querySelectorAll(".cg-territorio__camada")].map(
      (anel) => Number(anel.getAttribute("r")),
    );
    expect(raios[0]).toBeGreaterThan(raios[1]);
  });

  it("a camada de recorte inativo permanece, marcada e legível sem cor", () => {
    const { container } = render(
      <TerritorioDaComunidade
        nome="Zeferina"
        bairrosPublicados={2}
        camadas={[{ tipo: "Resíduos", registrosValidos: 8, ativo: false }]}
      />,
    );

    const camada = container.querySelector(".cg-territorio__camada");
    expect(camada).not.toBeNull();
    expect(camada?.getAttribute("data-ativo")).toBe("nao");
    expect(screen.getByText(/série inativa/)).toBeInTheDocument();
  });

  it("nenhum elemento visual aparece sem fato que o sustente", () => {
    const { container } = render(<TerritorioDaComunidade nome="Nova" bairrosPublicados={0} />);
    expect(container.querySelectorAll(".cg-territorio__camada")).toHaveLength(0);
  });
});

function ladosDoContorno(container: HTMLElement): number {
  const pontos =
    container.querySelector(".cg-territorio__contorno")?.getAttribute("points") ?? "";
  return pontos.trim().split(/\s+/).length;
}

describe("as variantes Mestre e Apoiador da carta (documento 11 §8.2)", () => {
  const MESTRE: DadosDaCarta = {
    variante: "mestre",
    avatar: "avatar-do-mestre",
    identificacao: { valor: "mestra_ana", tipo: "nick" },
    areasDeHabilidade: ["Artes", "Tecnologia"],
    artefatos: [{ endereco: "https://exemplo.org/cv", rotulo: "Currículo" }],
    trilhasDeAutoria: ["Robótica de sucata"],
    absorcoes: 2,
  };

  const APOIADOR: DadosDaCarta = {
    variante: "apoiador",
    avatar: "logo-propria",
    identificacao: { valor: "apoia_norte", tipo: "nick" },
    totalEmMoedas: "42.00",
    avatarPadrao: false,
    nivelDeSustento: 2,
    nomeDoNivel: "Quem faz acontecer",
    selos: ["Primeiro aporte"],
    desafiosPropostos: [
      {
        trilha: "Trilha da Água",
        periodoInicio: "2026-03-01",
        periodoFim: "2026-04-30",
        concluiram: 3,
        direcionado: false,
      },
    ],
    artefatos: [{ endereco: "https://exemplo.org/portfolio", rotulo: "Portfólio" }],
  };

  it("a carta do Mestre traz os seis campos da variante", () => {
    render(<CartaDoPersonagem dados={MESTRE} />);
    expect(screen.getByText("mestra_ana")).toBeTruthy();
    expect(screen.getByText("Tecnologia")).toBeTruthy();
    expect(screen.getByText("Robótica de sucata")).toBeTruthy();
    expect(screen.getByText("Currículo")).toBeTruthy();
    expect(screen.getByText("2 vezes")).toBeTruthy();
  });

  it("sem nick, a carta apresenta o nome, declarado como nome", () => {
    render(
      <CartaDoPersonagem
        dados={{ ...MESTRE, identificacao: { valor: "Ana Clara", tipo: "nome" } }}
      />,
    );
    const identificacao = screen.getByText("Ana Clara");
    expect(identificacao.getAttribute("data-tipo")).toBe("nome");
  });

  it("com nick, a carta o declara como nick", () => {
    render(<CartaDoPersonagem dados={MESTRE} />);
    expect(screen.getByText("mestra_ana").getAttribute("data-tipo")).toBe("nick");
  });

  it("a prova do Mestre sai como link com rótulo, nunca como anexo", () => {
    render(<CartaDoPersonagem dados={MESTRE} />);
    const link = screen.getByText("Currículo") as HTMLAnchorElement;
    expect(link.tagName).toBe("A");
    expect(link.href).toContain("https://exemplo.org/cv");
  });

  it("a carta do Apoiador traz o total em moedas e nunca reais", () => {
    const { container } = render(<CartaDoPersonagem dados={APOIADOR} />);
    expect(screen.getByText("42.00 moedas")).toBeTruthy();
    expect(container.textContent).not.toContain("R$");
  });

  it("abaixo do piso a carta usa o avatar padrão, sem outra marca de diferença", () => {
    const { container } = render(
      <CartaDoPersonagem
        dados={{ ...APOIADOR, avatar: null, avatarPadrao: true, totalEmMoedas: "5.00" }}
      />,
    );
    const carta = container.querySelector(".cg-carta") as HTMLElement;
    expect(carta.getAttribute("data-avatar-padrao")).toBe("sim");
    // A moldura e o conteúdo são os mesmos: nick e total seguem lá.
    expect(screen.getByText("apoia_norte")).toBeTruthy();
    expect(screen.getByText("5.00 moedas")).toBeTruthy();
  });

  it("logomarcas de proporções diferentes ocupam a mesma moldura", () => {
    const { container: primeira } = render(<CartaDoPersonagem dados={APOIADOR} />);
    const { container: segunda } = render(
      <CartaDoPersonagem dados={{ ...APOIADOR, avatar: "outra-logo-bem-maior" }} />,
    );
    const classe = (raiz: HTMLElement) =>
      (raiz.querySelector(".cg-carta") as HTMLElement).className;
    expect(classe(primeira)).toBe(classe(segunda));
  });

  it("a efetividade na carta não alcança quem concluiu", () => {
    const { container } = render(<CartaDoPersonagem dados={APOIADOR} />);
    expect(container.textContent).toContain("Trilha da Água");
    expect(container.textContent).toContain("3 concluíram");
    expect(container.querySelector(".cg-carta__desafios a")).toBeNull();
  });

  it("variante incompleta não vira carta pela metade", () => {
    expect(cartaEstaCompleta({ ...MESTRE, areasDeHabilidade: undefined })).toBe(false);
    expect(cartaEstaCompleta({ ...APOIADOR, totalEmMoedas: undefined })).toBe(false);
    expect(cartaEstaCompleta({ ...MESTRE, identificacao: undefined })).toBe(false);
    const { container } = render(
      <CartaDoPersonagem dados={{ ...MESTRE, artefatos: undefined }} />,
    );
    expect(container.querySelector(".cg-carta")).toBeNull();
  });

  it("as duas variantes completas se apresentam", () => {
    expect(cartaEstaCompleta(MESTRE)).toBe(true);
    expect(cartaEstaCompleta(APOIADOR)).toBe(true);
  });
});

const SALDO_PARA_TROCAR = 40;

/** A mesma carta, como a tela logada a monta: com o saldo que dá para trocar. */
const GUERREIRA_EM_SESSAO: DadosDaCarta = {
  ...GUERREIRA_COMPLETA,
  saldoParaTrocar: SALDO_PARA_TROCAR,
};

const MESTRE_COMPLETO: DadosDaCarta = {
  variante: "mestre",
  avatar: "avatar-do-mestre",
  identificacao: { valor: "mestra_ana", tipo: "nick" },
  areasDeHabilidade: ["Artes"],
  artefatos: [],
  trilhasDeAutoria: ["Robótica de sucata"],
  absorcoes: 2,
};

const APOIADOR_COMPLETO: DadosDaCarta = {
  variante: "apoiador",
  avatar: "logo-propria",
  identificacao: { valor: "apoia_norte", tipo: "nick" },
  totalEmMoedas: "42.00",
  avatarPadrao: false,
  nivelDeSustento: 2,
  nomeDoNivel: "Quem faz acontecer",
  selos: [],
  desafiosPropostos: [],
  artefatos: [],
};

/** O bloco `@media` que alcança o seletor pedido. */
function media(seletor: string): string {
  const blocos = [...ESTILOS.matchAll(/@media \(min-width: 768px\) \{([\s\S]*?)\n\}/g)].map(
    (m) => m[1],
  );
  const bloco = blocos.find((candidato) => candidato.includes(seletor));
  expect(bloco).toBeDefined();
  return bloco as string;
}

describe("CartaDoPersonagem — a identidade é centralizada (documento 15 §8.1)", () => {
  it("o avatar da moldura comum se centraliza, como o documento 11 §8.2 exige", () => {
    // O §8.2 manda "avatar centralizado em proporção fixa" na carta do
    // Apoiador desde sempre, e o CSS não cumpria: a largura de metade sem
    // margem automática encostava o avatar à esquerda, nas quatro variantes.
    expect(corpoDaRegra(".cg-carta__avatar")).toContain("margin-inline: auto;");
    expect(corpoDaRegra(".cg-carta__identidade")).toContain("text-align: center;");
    expect(corpoDaRegra(".cg-territorio__desenho")).toContain("margin-inline: auto;");
  });

  it("as quatro variantes trazem a identidade no mesmo bloco", () => {
    for (const dados of [
      GUERREIRA_COMPLETA,
      COMUNIDADE_COMPLETA,
      MESTRE_COMPLETO,
      APOIADOR_COMPLETO,
    ]) {
      const { container } = render(<CartaDoPersonagem dados={dados} />);
      const identidade = container.querySelector(".cg-carta__identidade");
      expect(identidade).not.toBeNull();
      expect(identidade?.querySelector(".cg-carta__nick")).not.toBeNull();
    }
  });

  it("só a variante Guerreiro(a) ganha colunas", () => {
    for (const dados of [COMUNIDADE_COMPLETA, MESTRE_COMPLETO, APOIADOR_COMPLETO]) {
      const { container } = render(<CartaDoPersonagem dados={dados} />);
      expect(container.querySelector(".cg-carta__colunas")).toBeNull();
    }
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_COMPLETA} />);
    expect(container.querySelector(".cg-carta__colunas")).not.toBeNull();
  });
});

describe("CartaDoPersonagem — as seções em colunas (documento 15 §§4, 8.1)", () => {
  it("cada coluna traz o símbolo acima do rótulo", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_EM_SESSAO} />);
    const colunas = [...container.querySelectorAll(".cg-carta__coluna")];
    expect(colunas).toHaveLength(4);

    for (const coluna of colunas) {
      // Primeiro o símbolo, depois o rótulo: o desenho encabeça a coluna e
      // nunca aparece sozinho (documento 15 §5).
      expect(coluna.children[0]?.tagName.toLowerCase()).toBe("svg");
      expect(coluna.children[1]?.classList.contains("cg-carta__rotulo")).toBe(true);
      expect(coluna.children[1]?.textContent?.trim().length).toBeGreaterThan(0);
    }

    expect(colunas.map((coluna) => coluna.children[1]?.textContent)).toEqual([
      "Poderes",
      "Badges",
      "Criações originais",
      "Para trocar",
    ]);
  });

  it("são duas por linha no celular e todas em linha a partir do marco", () => {
    const celular = corpoDaRegra(".cg-carta__colunas");
    expect(celular).toContain("display: grid;");
    expect(celular).toContain("grid-template-columns: repeat(2, minmax(0, 1fr));");
    // Alinhadas pelo topo: coluna curta fica curta.
    expect(celular).toContain("align-items: start;");

    // Na linha larga o CSS não fixa o número de trilhas: o arranjo acompanha
    // o número de seções, que é três na carta pública.
    const largo = media(".cg-carta__colunas");
    expect(largo).toContain("grid-auto-flow: column;");
    expect(largo).not.toMatch(/grid-template-columns: repeat\(4/);
  });

  it("sem o saldo, o arranjo se fecha em três colunas", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_COMPLETA} />);
    const colunas = [...container.querySelectorAll(".cg-carta__coluna")];

    expect(colunas).toHaveLength(3);
    expect(colunas.map((coluna) => coluna.children[1]?.textContent)).toEqual([
      "Poderes",
      "Badges",
      "Criações originais",
    ]);
  });
});

describe("CartaDoPersonagem — o saldo que dá para trocar (RF-05-82, documento 15 §9)", () => {
  it("a seção traz o saldo, rotulado como o que dá para trocar", () => {
    render(<CartaDoPersonagem dados={GUERREIRA_EM_SESSAO} />);

    expect(screen.getByText("Para trocar")).toBeInTheDocument();
    expect(screen.getByText(String(SALDO_PARA_TROCAR))).toBeInTheDocument();
    // A unidade diz a grandeza: o §9 proíbe as duas contas do ponto extra
    // aparecerem sem rótulo que as separe.
    expect(screen.getByText(/pontos extras/)).toBeInTheDocument();
  });

  it("o acumulado não entra na seção, e nada é somado", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_EM_SESSAO} />);
    const coluna = [...container.querySelectorAll(".cg-carta__coluna")].at(-1);

    expect(coluna?.textContent).toContain("Para trocar");
    expect(coluna?.textContent).not.toContain("Acumulado");
    expect(coluna?.textContent).not.toContain("acumulado");
    // E o ponto regular continua só na frase de desempenho, nunca aqui.
    expect(coluna?.textContent).not.toContain("pontos regulares");
  });

  it("o numeral do saldo é o da carta: destaque em peso 700 (documento 15 §4)", () => {
    const numeral = corpoDaRegra(".cg-carta__numeral");
    expect(numeral).toContain("font-family: var(--fonte-destaque);");
    expect(numeral).toContain("font-weight: var(--peso-numeral);");
  });

  it("a falta do saldo não torna a carta incompleta", () => {
    // O campo é de tela logada, e a superfície pública não tem de onde lê-lo:
    // ausente, a carta se apresenta sem a seção (invariantes 8, 12 e 23).
    expect(cartaEstaCompleta(GUERREIRA_COMPLETA)).toBe(true);
    expect(cartaEstaCompleta(GUERREIRA_EM_SESSAO)).toBe(true);

    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_COMPLETA} />);
    expect(container.querySelector(".cg-carta")).not.toBeNull();
    expect(container.textContent).not.toContain("Para trocar");
  });
});

describe("CartaDoPersonagem — as duas estrelas da grandeza (documento 15 §9)", () => {
  it("a frase de desempenho leva a estrela cheia, e a frase diz tudo sozinha", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_EM_SESSAO} />);
    const desempenho = container.querySelector(".cg-carta__desempenho");

    expect(desempenho?.querySelector(".cg-estrela-de-ponto")).not.toBeNull();
    // A estrela é escondida do leitor de tela: o significado é do texto (§5).
    expect(desempenho?.querySelector("svg")?.getAttribute("aria-hidden")).toBe("true");
    expect(desempenho?.textContent).toBe("12º lugar, com 40 pontos");
  });

  it("a cheia é peça preenchida e a vazada é glifo do sistema de ícone", () => {
    const { container } = render(<CartaDoPersonagem dados={GUERREIRA_EM_SESSAO} />);
    const cheia = container.querySelector(".cg-estrela-de-ponto");
    const coluna = [...container.querySelectorAll(".cg-carta__coluna")].at(-1);
    const vazada = coluna?.querySelector("svg");

    // A forma é a mesma; o que as separa é o preenchimento, e a cor sai dos
    // tokens em um caso e do texto no outro.
    expect(cheia?.querySelector("path")?.getAttribute("d")).toBe(
      vazada?.querySelector("path")?.getAttribute("d"),
    );
    expect(cheia?.getAttribute("fill")).toBeNull();
    expect(corpoDaRegra(".cg-estrela-de-ponto")).toContain("fill: var(--cor-ponto);");
    expect(vazada?.getAttribute("fill")).toBe("none");
    expect(vazada?.getAttribute("stroke")).toBe("currentColor");
  });
});
