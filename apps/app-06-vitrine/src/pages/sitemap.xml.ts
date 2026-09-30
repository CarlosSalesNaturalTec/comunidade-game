import type { APIRoute } from "astro";
import { comunidadesDoBuild } from "../build/dados";
import { montarSitemap } from "../descoberta/enderecos";

/** O `sitemap.xml`, escrito à mão: a regra de excluir pessoa e formulário e
 * incluir a comunidade do build é lógica própria de qualquer jeito, e uma
 * dependência a mais para gerar vinte linhas de XML não se paga (design —
 * decisão 5). */
export const GET: APIRoute = async ({ site }) => {
  const comunidades = await comunidadesDoBuild();
  const corpo = montarSitemap(
    site?.href ?? "https://comunidadegame.org",
    comunidades.map((comunidade) => comunidade.id),
  );
  return new Response(corpo, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
