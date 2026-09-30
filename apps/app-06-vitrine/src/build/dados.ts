import { configurarAcessoAoNucleo } from "comum/api";
import { CHAVE_DE_APLICACAO, URL_DO_NUCLEO } from "../api/configuracao";
import {
  type ComunidadeNaLista,
  lerConteudoInstitucional,
  listarComunidades,
  type SecaoInstitucionalPublica,
} from "../api/leituras";

/**
 * O que a vitrine busca **no build**, para sair no documento servido: o
 * conteúdo institucional e a lista de comunidades (PRD-03 §10). Tudo o mais é
 * ilha, e é lido na visita.
 *
 * Roda em Node, no `astro build` — não no navegador. As leituras de
 * `../api/leituras` não dependem de API de navegador, então servem aos dois.
 *
 * **Núcleo fora do ar derruba o build** (design — decisão 4). Publicar a
 * vitrine com o institucional vazio é pior do que não publicar: a spec exige
 * que o documento servido traga o conteúdo publicado, e página indexada vazia
 * é o defeito que esta fatia existe para corrigir.
 */

let configurado = false;

function configurarUmaVez(): void {
  if (configurado) return;
  configurarAcessoAoNucleo({
    chaveDeAplicacao: CHAVE_DE_APLICACAO,
    urlDoNucleo: URL_DO_NUCLEO,
  });
  configurado = true;
}

/** Uma leitura por build, compartilhada por todas as páginas: cada página é
 * montada em sequência no mesmo processo, e repetir a chamada por página
 * cairia no freio por origem do próprio núcleo. */
function umaVezPorBuild<T>(ler: () => Promise<T>): () => Promise<T> {
  let promessa: Promise<T> | null = null;
  return () => {
    configurarUmaVez();
    if (promessa === null) {
      promessa = ler().catch((causa) => {
        promessa = null;
        throw new Error(
          "O núcleo não respondeu durante o build da vitrine. A publicação foi " +
            "interrompida de propósito: página indexada sem conteúdo é pior do que " +
            "página não publicada (design — decisão 4).",
          { cause: causa },
        );
      });
    }
    return promessa;
  };
}

export const conteudoInstitucionalDoBuild: () => Promise<SecaoInstitucionalPublica[]> =
  umaVezPorBuild(lerConteudoInstitucional);

export const comunidadesDoBuild: () => Promise<ComunidadeNaLista[]> = umaVezPorBuild(
  async () => (await listarComunidades()).itens,
);

/** A seção pedida, no formato que o componente consome. Seção que o núcleo não
 * devolveu existe sem texto, e nada é inventado no lugar dela (`RF-03-45`). */
export async function secaoInstitucionalDoBuild(
  secao: SecaoInstitucionalPublica["secao"],
): Promise<SecaoInstitucionalPublica> {
  const secoes = await conteudoInstitucionalDoBuild();
  return (
    secoes.find((item) => item.secao === secao) ?? { secao, texto: null, video_url: null }
  );
}
