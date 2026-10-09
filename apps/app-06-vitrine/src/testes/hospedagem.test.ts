import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

/**
 * O `firebase.json` é a outra metade da exclusão de indexação, e sem teste ela
 * falha calada: a etiqueta `noindex` está no `app.html`, mas quem leva
 * `/guerreiros/x` até esse arquivo é o `rewrite`, e quem responde ao agente
 * que não executa script é o `X-Robots-Tag`. Errar um prefixo aqui publica
 * página de Guerreiro(a) indexável, contra o `RF-03-14` e o invariante 12 do
 * documento 99.
 */

const PREFIXOS = ["/guerreiros/**", "/mestres/**", "/apoiadores/**"];

interface Alvo {
  target: string;
  public: string;
  cleanUrls?: boolean;
  rewrites: { source: string; destination: string }[];
  headers?: { source: string; headers: { key: string; value: string }[] }[];
}

const vitrine: Alvo = (() => {
  const bruto = JSON.parse(
    readFileSync(join(__dirname, "..", "..", "..", "..", "firebase.json"), "utf-8"),
  );
  const alvos: Alvo[] = Array.isArray(bruto.hosting) ? bruto.hosting : [bruto.hosting];
  const achado = alvos.find((alvo) => alvo.target === "vitrine");
  if (achado === undefined) throw new Error("o alvo `vitrine` sumiu do firebase.json");
  return achado;
})();

describe("a hospedagem da vitrine", () => {
  it("serve o que o Astro publicou", () => {
    expect(vitrine.public).toBe("apps/app-06-vitrine/dist");
  });

  it("declara `cleanUrls`, sem o que só a raiz é alcançável (RF-03-25, RF-03-26)", () => {
    // `build.format: "file"` emite `pesquisadores.html`, e o Firebase serve
    // arquivo real antes do `rewrite` — mas só por correspondência exata ou
    // índice de diretório. Sem `cleanUrls`, `/pesquisadores` não alcança
    // arquivo nenhum e cai no `**`, que é a casca de pessoa. Retirar esta
    // linha volta a falhar aqui, e não em produção.
    expect(vitrine.cleanUrls).toBe(true);
  });

  it("leva os três prefixos de pessoa à casca noindex (RF-03-13, RF-03-14)", () => {
    for (const prefixo of PREFIXOS) {
      const regra = vitrine.rewrites.find((rewrite) => rewrite.source === prefixo);
      expect(regra, `falta o rewrite de ${prefixo}`).toBeDefined();
      expect(regra?.destination).toBe("/app.html");
    }
  });

  it("declara X-Robots-Tag nos três prefixos e na própria casca", () => {
    for (const fonte of [...PREFIXOS, "/app.html"]) {
      const regra = vitrine.headers?.find((cabecalho) => cabecalho.source === fonte);
      expect(regra, `falta o cabeçalho de ${fonte}`).toBeDefined();
      expect(regra?.headers).toContainEqual({
        key: "X-Robots-Tag",
        value: "noindex, nofollow",
      });
    }
  });

  it("mantém o `**` como último rewrite, e nunca antes dos prefixos de pessoa", () => {
    const fontes = vitrine.rewrites.map((rewrite) => rewrite.source);

    expect(fontes[fontes.length - 1]).toBe("**");
    for (const prefixo of PREFIXOS) {
      expect(fontes.indexOf(prefixo)).toBeLessThan(fontes.indexOf("**"));
    }
  });

  it("o fallback também vai para a casca, e nunca para a abertura", () => {
    const fallback = vitrine.rewrites.find((rewrite) => rewrite.source === "**");

    // `/index.html` serviria o conteúdo da abertura no endereço de uma
    // pessoa, que é o que a fatia existe para impedir.
    expect(fallback?.destination).toBe("/app.html");
  });

  it("nenhum endereço institucional recebe X-Robots-Tag", () => {
    const fontes = (vitrine.headers ?? []).map((cabecalho) => cabecalho.source);

    for (const institucional of [
      "/",
      "/o-que-coletamos",
      "/pesquisadores",
      "/gestores-publicos",
      "/quero-participar",
      "/comunidades/**",
    ]) {
      expect(fontes).not.toContain(institucional);
    }
  });
});
