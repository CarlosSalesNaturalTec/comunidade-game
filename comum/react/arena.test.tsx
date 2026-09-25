import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { CartaDoPersonagem, type DadosDaCarta } from "./CartaDoPersonagem";
import { FundoDeComunidade } from "./FundoDeComunidade";
import { PalcoDoPersonagem } from "./PalcoDoPersonagem";
import { RetornoDeConquista } from "./RetornoDeConquista";

const AQUI = dirname(fileURLToPath(import.meta.url));
const ESTILOS = readFileSync(join(AQUI, "estilos.css"), "utf-8");

/** O corpo da regra que abre com o seletor pedido, sem as regras seguintes. */
function corpoDaRegra(seletor: string): string {
  const inicio = ESTILOS.indexOf(`${seletor} {`);
  expect(inicio).toBeGreaterThan(-1);
  const abre = ESTILOS.indexOf("{", inicio);
  return ESTILOS.slice(abre + 1, ESTILOS.indexOf("}", abre));
}

const GUERREIRA: DadosDaCarta = {
  variante: "guerreiro",
  avatar: null,
  nick: "Zeferina",
  badges: [{ familia: "de_nivel", poder: "Poder do Território" }],
  poderes: [{ poder: "Poder do Território", nivel: 3 }],
  desempenho: "2º na comunidade, com 40 pontos",
  criacoes: ["Mapa das águas do bairro"],
};

describe("A Arena põe a ilustração em primeiro plano (documento 15 §6)", () => {
  // Cenário: A carta domina a tela da Arena
  it("a carta é o elemento maior da tela, e a tela pede uma decisão só", () => {
    const { container } = render(
      <PalcoDoPersonagem
        rotulo="Carta de Zeferina"
        decisao={<button type="button">Ver as minhas trilhas</button>}
        apoio={<p>A presença de hoje está registrada.</p>}
      >
        <CartaDoPersonagem dados={GUERREIRA} />
      </PalcoDoPersonagem>,
    );

    // A carta está no primeiro plano do palco, e não no apoio.
    const personagem = container.querySelector(".cg-palco__personagem");
    expect(personagem?.querySelector(".cg-carta")).not.toBeNull();

    // Uma decisão só: o palco tem um botão, e o apoio nenhum.
    expect(screen.getAllByRole("button")).toHaveLength(1);
    expect(container.querySelector(".cg-palco__apoio")?.querySelector("button")).toBeNull();

    // A carta ocupa a largura inteira do palco — é isso que a faz dominar,
    // e não um tamanho fixo, que quebraria no celular.
    expect(corpoDaRegra(".cg-palco__personagem .cg-carta")).toContain("width: 100%");
    // O apoio fica menor que a apresentação, nunca disputando o primeiro plano.
    expect(corpoDaRegra(".cg-palco__apoio")).toContain("font-size: var(--escala-0875)");
  });

  it("o palco não reproduz a densidade da Operação nem mexe no alvo de toque", () => {
    // Densidade baixa: o espaçamento entre as partes é o maior da escala, e
    // não o `--densidade` que só a Operação declara (invariante 24).
    const palco = corpoDaRegra(".cg-palco");
    expect(palco).toContain("gap: var(--espaco-24)");
    expect(palco).not.toContain("--densidade");

    // O alvo de toque de `48` px continua sendo o do `cg-botao`: o palco não
    // declara altura nem largura mínima que o contrarie.
    const decisao = corpoDaRegra(".cg-palco__decisao");
    expect(decisao).not.toContain("min-height");
    expect(decisao).not.toContain("--alvo-de-toque");
    expect(corpoDaRegra(".cg-botao")).toContain("min-height: var(--alvo-de-toque)");
  });
});

describe("A imagem de comunidade ao fundo (documento 15 §6.3)", () => {
  // Cenário: A imagem de fundo não come o contraste
  it("texto e componentes se apoiam em cor chapada, nunca na fotografia", () => {
    const { container } = render(
      <FundoDeComunidade imagem="https://nucleo.exemplo/comunidade.jpg">
        <PalcoDoPersonagem rotulo="Carta de Zeferina">
          <CartaDoPersonagem dados={GUERREIRA} />
        </PalcoDoPersonagem>
      </FundoDeComunidade>,
    );

    // A foto fica atrás de tudo.
    const imagem = container.querySelector(".cg-fundo-de-comunidade__imagem");
    expect(imagem).not.toBeNull();
    expect(corpoDaRegra(".cg-fundo-de-comunidade__imagem")).toContain("z-index: -1");

    // Havendo foto, quem carrega texto, componente, borda que informa e
    // estado de foco ganha cor chapada opaca — é sobre ela, e não sobre a
    // fotografia, que os pisos do documento 15 §3.3 são medidos.
    const sobreAFoto = corpoDaRegra(
      ".cg-fundo-de-comunidade .cg-palco__personagem,\n.cg-fundo-de-comunidade .cg-palco__decisao,\n.cg-fundo-de-comunidade .cg-palco__apoio",
    );
    expect(sobreAFoto).toContain("background: var(--cor-fundo)");

    // E nenhuma transparência entra no caminho: opacidade parcial devolveria
    // a medida do contraste à fotografia, que muda a cada comunidade.
    expect(ESTILOS).not.toMatch(/\.cg-fundo-de-comunidade[^{]*\{[^}]*opacity/);
  });

  // Cenário: A imagem de fundo não carrega informação
  it("nada do que a tela comunica se perde quando a imagem não carrega", () => {
    const comFoto = render(
      <FundoDeComunidade imagem="https://nucleo.exemplo/comunidade.jpg">
        <p>A presença de hoje está registrada.</p>
      </FundoDeComunidade>,
    );
    const textoComFoto = comFoto.container.textContent;
    // A foto não entra na árvore de acessibilidade: não é conteúdo.
    expect(comFoto.container.querySelector("img")?.getAttribute("alt")).toBe("");
    expect(comFoto.container.querySelector("img")?.getAttribute("aria-hidden")).toBe("true");
    comFoto.unmount();

    // Sem foto — rede fora, ou comunidade que não escolheu nenhuma — a tela é
    // exatamente a mesma, e nenhuma imagem sequer é pedida.
    const semFoto = render(
      <FundoDeComunidade imagem={null}>
        <p>A presença de hoje está registrada.</p>
      </FundoDeComunidade>,
    );
    expect(semFoto.container.querySelector("img")).toBeNull();
    expect(semFoto.container.textContent).toBe(textoComFoto);
  });
});

describe("O retorno de progresso e conquista (documento 15 §6, documento 11 §8.5)", () => {
  // Cenário: A conquista devolve retorno, e o fato fica legível sem ele
  it("o retorno acompanha o fato, e a conquista também aparece em texto", () => {
    const { container } = render(
      <RetornoDeConquista fato="badge_certificado">
        <p>Badge do Poder do Território</p>
      </RetornoDeConquista>,
    );

    const retorno = container.querySelector(".cg-retorno-de-conquista");
    expect(retorno?.getAttribute("data-fato")).toBe("badge_certificado");
    expect(retorno?.getAttribute("data-retornando")).toBe("sim");
    // A conquista é anunciada sem depender de movimento.
    expect(screen.getByRole("status")).toHaveTextContent("Badge do Poder do Território");

    // `300` ms com `ease-in-out`, pela duração do temperamento.
    const animado = corpoDaRegra('.cg-retorno-de-conquista[data-retornando="sim"]');
    expect(animado).toContain("var(--duracao, 0ms)");
    expect(animado).toContain("ease-in-out");
  });

  // Cenário: Não há retorno sem fato
  it("tela apresentada sem progresso nem conquista nova não anima nada", () => {
    const { container } = render(
      <RetornoDeConquista fato={null}>
        <p>Nível 3</p>
      </RetornoDeConquista>,
    );

    // Sem fato não há sequer elemento animável — e o conteúdo segue inteiro.
    expect(container.querySelector(".cg-retorno-de-conquista")).toBeNull();
    expect(container.textContent).toBe("Nível 3");
  });

  // Cenário: Menos movimento suprime o retorno sem esconder o fato
  it("menos movimento desliga a animação, e o fato continua anunciado", () => {
    render(
      <RetornoDeConquista fato="nivel_que_subiu">
        <p>Nível 4</p>
      </RetornoDeConquista>,
    );
    // O fato continua na tela e continua anunciado, com ou sem movimento.
    expect(screen.getByRole("status")).toHaveTextContent("Nível 4");

    // A preferência do aparelho desliga a animação de vez — não resta nem o
    // quadro inicial (documento 15 §5).
    const reduzido = ESTILOS.slice(ESTILOS.indexOf("@media (prefers-reduced-motion: reduce)"));
    expect(reduzido).toContain(".cg-retorno-de-conquista");
    expect(reduzido).toContain("animation: none");
  });
});
