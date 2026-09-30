import { describe, expect, it } from "vitest";
import {
  ENDERECOS_FORA_DO_SITEMAP,
  montarRobots,
  montarSitemap,
  PREFIXOS_DE_PESSOA,
} from "../descoberta/enderecos";

const SITE = "https://comunidadegame.org";

describe("a montagem do sitemap.xml", () => {
  it("lista os endereços institucionais e uma linha por comunidade (PRD-03 §10)", () => {
    const xml = montarSitemap(SITE, ["zeferina", "outra"]);

    expect(xml).toContain("<loc>https://comunidadegame.org/</loc>");
    expect(xml).toContain("<loc>https://comunidadegame.org/pesquisadores</loc>");
    expect(xml).toContain("<loc>https://comunidadegame.org/gestores-publicos</loc>");
    expect(xml).toContain("<loc>https://comunidadegame.org/o-que-coletamos</loc>");
    expect(xml).toContain("<loc>https://comunidadegame.org/quero-participar</loc>");
    expect(xml).toContain("<loc>https://comunidadegame.org/comunidades/zeferina</loc>");
    expect(xml).toContain("<loc>https://comunidadegame.org/comunidades/outra</loc>");
  });

  it("nunca lista endereço individual de pessoa (RF-03-13, RF-03-14)", () => {
    const xml = montarSitemap(SITE, ["zeferina"]);

    for (const prefixo of PREFIXOS_DE_PESSOA) {
      expect(xml).not.toContain(prefixo);
    }
  });

  it("nunca lista endereço de formulário nem a área do Desenvolvedor", () => {
    const xml = montarSitemap(SITE, []);

    for (const caminho of ENDERECOS_FORA_DO_SITEMAP) {
      expect(xml).not.toContain(`<loc>${SITE}${caminho}</loc>`);
    }
  });

  it("não quebra o XML com o que o identificador da comunidade trouxer", () => {
    const xml = montarSitemap(SITE, ['a&b<c>"d']);

    // `encodeURIComponent` já resolve no caminho, e o escape de XML é a
    // segunda trava: nem `<`, nem `>`, nem aspas escapam do `<loc>`.
    const locs = [...xml.matchAll(/<loc>(.*?)<\/loc>/g)].map((achado) => achado[1]);
    const loc = locs[locs.length - 1];
    expect(loc).not.toMatch(/[<>"]/);
    expect(loc).toContain("%26");
  });

  it("não duplica a barra quando o site vem com barra no fim", () => {
    expect(montarSitemap("https://comunidadegame.org/", [])).toContain(
      "<loc>https://comunidadegame.org/</loc>",
    );
    expect(montarSitemap("https://comunidadegame.org/", [])).not.toContain(
      "comunidadegame.org//",
    );
  });
});

describe("a montagem do robots.txt", () => {
  it("barra os três prefixos de pessoa e a casca que os serve", () => {
    const robots = montarRobots(SITE);

    expect(robots).toContain("Disallow: /guerreiros/");
    expect(robots).toContain("Disallow: /mestres/");
    expect(robots).toContain("Disallow: /apoiadores/");
    expect(robots).toContain("Disallow: /app.html");
  });

  it("barra os formulários e a área do Desenvolvedor", () => {
    const robots = montarRobots(SITE);

    for (const caminho of ENDERECOS_FORA_DO_SITEMAP) {
      expect(robots).toContain(`Disallow: ${caminho}`);
    }
  });

  it("aponta o sitemap e libera o resto", () => {
    const robots = montarRobots(SITE);

    expect(robots).toContain("Sitemap: https://comunidadegame.org/sitemap.xml");
    expect(robots).toContain("Allow: /");
  });

  it("não aponta domínio de terceiro nem pede medição (RF-03-51, RN-03-22)", () => {
    const robots = montarRobots(SITE);
    const enderecos = robots.match(/https?:\/\/[^\s]+/g) ?? [];

    expect(enderecos.every((endereco) => endereco.startsWith(SITE))).toBe(true);
  });
});
