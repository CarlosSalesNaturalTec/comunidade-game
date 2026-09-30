/**
 * O que a vitrine declara a buscadores. A regra é a da spec: o `sitemap.xml`
 * lista **apenas** os endereços institucionais e de comunidade, e nunca
 * endereço individual de pessoa nem de formulário (PRD-03 §10).
 *
 * A montagem mora aqui, e não no endpoint, para ser testável em unidade — o
 * `.astro` e o `.ts` de rota ficam finos de propósito (design — decisão 6).
 */

/** Os endereços fixos que entram no `sitemap.xml`: os três recortes de
 * leitura, a área detalhada de coleta e a porta do convite. */
export const ENDERECOS_INDEXAVEIS = [
  "/",
  "/pesquisadores",
  "/gestores-publicos",
  "/o-que-coletamos",
  "/quero-participar",
] as const;

/** Formulário e Área do Apoiador Desenvolvedor: ficam de fora do
 * `sitemap.xml`. Não é o que se busca, e o assistente consome modelo pago a
 * cada pergunta (`RN-03-38`). */
export const ENDERECOS_FORA_DO_SITEMAP = [
  "/participar",
  "/solicitar-dados",
  "/desenvolvedor",
  "/apresentar-url",
] as const;

/** Os prefixos das páginas de pessoa. Nunca entram no `sitemap.xml`, e o
 * `robots.txt` barra a casca que os serve (`RF-03-13`, `RF-03-14`). */
export const PREFIXOS_DE_PESSOA = ["/guerreiros/", "/mestres/", "/apoiadores/"] as const;

/** A casca de cliente das páginas de pessoa, destino dos `rewrite` do
 * `firebase.json`. Barrada no `robots.txt` para não ser indexada por si. */
export const CASCA_DE_PESSOA = "/app.html";

function escaparXml(texto: string): string {
  return texto
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

/** Monta o `sitemap.xml` com os endereços fixos e a página de cada comunidade
 * publicada no build. */
export function montarSitemap(site: string, idsDeComunidade: string[]): string {
  const base = site.replace(/\/$/, "");
  const caminhos = [
    ...ENDERECOS_INDEXAVEIS,
    ...idsDeComunidade.map((id) => `/comunidades/${encodeURIComponent(id)}`),
  ];
  const linhas = caminhos.map(
    (caminho) => `  <url><loc>${escaparXml(`${base}${caminho}`)}</loc></url>`,
  );
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...linhas,
    "</urlset>",
    "",
  ].join("\n");
}

/** Monta o `robots.txt`. Barra a casca de pessoa e os três prefixos, e aponta
 * o `sitemap.xml`. Nenhuma requisição a terceiro e nenhuma medição de
 * audiência: é arquivo do próprio domínio (`RF-03-51`, `RN-03-22`). */
export function montarRobots(site: string): string {
  const base = site.replace(/\/$/, "");
  return [
    "User-agent: *",
    ...PREFIXOS_DE_PESSOA.map((prefixo) => `Disallow: ${prefixo}`),
    `Disallow: ${CASCA_DE_PESSOA}`,
    ...ENDERECOS_FORA_DO_SITEMAP.map((caminho) => `Disallow: ${caminho}`),
    "Allow: /",
    "",
    `Sitemap: ${base}/sitemap.xml`,
    "",
  ].join("\n");
}
