import type { APIRoute } from "astro";
import { montarRobots } from "../descoberta/enderecos";

/** O `robots.txt`, do próprio domínio. */
export const GET: APIRoute = ({ site }) =>
  new Response(montarRobots(site?.href ?? "https://comunidadegame.org"), {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
