// @ts-check
import react from "@astrojs/react";
import { defineConfig } from "astro/config";

/**
 * Saída **estática**, sem runtime de servidor: é o que o documento 03 §1,
 * princípio 13, exige para as oito aplicações, e o que o Firebase Hosting
 * serve. O mesmo princípio é o que põe a App 06 em Astro — ela é a única
 * indexável por buscadores (PRD-03 §10).
 *
 * Os componentes React de `comum/` e da própria App 06 continuam React: entram
 * como **ilhas**, e só as que precisam de interação recebem diretiva de
 * cliente. O que não recebe é renderizado no build e sai como HTML.
 */
export default defineConfig({
  output: "static",
  integrations: [react()],
  // O endereço da vitrine é a raiz do domínio da plataforma (documento 03
  // §1.1). Serve à canônica e ao `sitemap.xml`; a esteira o substitui pelo
  // endereço do ambiente.
  site: process.env.URL_DA_VITRINE ?? "https://comunidadegame.org",
  vite: {
    // Mantém o prefixo `VITE_` das variáveis de ambiente, que a esteira de
    // publicação já injeta e `src/api/configuracao.ts` já lê. O padrão do
    // Astro é `PUBLIC_`, e trocá-lo obrigaria a mexer no `app-06-deploy.yml`
    // e nos seis endereços do "Entrar" sem ganho nenhum.
    envPrefix: ["VITE_", "PUBLIC_"],
  },
  build: {
    // Um arquivo por rota, e não `rota/index.html`: o Firebase Hosting serve
    // arquivo real antes de aplicar `rewrite`, e o caminho direto é o que faz
    // o `rewrite` `**` sobrar só para o que não tem arquivo.
    format: "file",
  },
});
