import { URL_DO_NUCLEO } from "../api/configuracao";

/** Documentação publicada com MkDocs e repositório no GitHub — duas das
 * quatro portas da área (`RF-03-67`). Não entram por variável de ambiente como
 * os destinos do "Entrar": estes dois endereços são os mesmos em todo
 * ambiente, e são os declarados em `mkdocs.yml` (`site_url` e `repo_url`). */
export const URL_DA_DOCUMENTACAO = "https://carlossalesnaturaltec.github.io/comunidade-game/";
export const URL_DO_REPOSITORIO = "https://github.com/CarlosSalesNaturalTec/comunidade-game";

/** A interface Swagger que o núcleo publica fora de `/v1`, aberta e sem chave
 * (`RF-03-67`, documento 03 §1.1). Deriva do endereço do núcleo, que muda por
 * ambiente; sem ele declarado não há link, em vez de um `/docs` da própria
 * vitrine. */
export function urlDaDocumentacaoDaApi(urlDoNucleo: string = URL_DO_NUCLEO): string | null {
  if (!urlDoNucleo) return null;
  return `${urlDoNucleo.replace(/\/+$/, "")}/docs`;
}
