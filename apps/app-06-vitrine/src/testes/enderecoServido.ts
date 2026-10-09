import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative, sep } from "node:path";

/**
 * Qual arquivo o Firebase Hosting serve para um endereço pedido.
 *
 * Existe porque nenhum teste cruzava **arquivo emitido × caminho servido**, e
 * foi por essa junta que a regressão passou: `saidaDoBuild` afirmava que
 * `dist/pesquisadores.html` existe, com título, canônica e seções corretos —
 * tudo verdade — e nunca perguntava por qual endereço se chega até ele. Em
 * produção, `/pesquisadores` não chegava: caía no `rewrite` `**` e era atendido
 * pela casca de pessoa (design — decisão 4).
 *
 * Aplica a **precedência documentada** do Firebase Hosting, sem esperteza:
 *
 *   1. arquivo exato
 *   2. `cleanUrls` — `/x` serve `x.html`, e `/x.html` redireciona para `/x`
 *   3. índice de diretório — `/x/` serve `x/index.html`
 *   4. `rewrites`, na ordem declarada
 *   5. não encontrado
 *
 * É alimentado pelo `firebase.json` **real** e pela árvore **real** de `dist/`,
 * e não por fixture: é isso que o faz falhar quando a configuração muda, quando
 * o `build.format` muda e quando uma rota nova nasce sem endereço — os três
 * jeitos de a regressão voltar.
 */

export interface AlvoDeHospedagem {
  target: string;
  public: string;
  cleanUrls?: boolean;
  rewrites?: { source: string; destination: string }[];
  headers?: { source: string; headers: { key: string; value: string }[] }[];
}

export type EnderecoServido =
  /** Arquivo servido diretamente, pelo nome exato ou pelo `cleanUrls`. */
  | { tipo: "arquivo"; arquivo: string }
  /** `cleanUrls` devolve o endereço sem a extensão. */
  | { tipo: "redirecionamento"; para: string }
  /** Nenhum arquivo correspondeu: um `rewrite` atendeu. */
  | { tipo: "rewrite"; arquivo: string; regra: string }
  | { tipo: "nao-encontrado" };

/** Lê o alvo pedido do `firebase.json`. */
export function alvoDaHospedagem(raizDoRepo: string, target: string): AlvoDeHospedagem {
  const bruto = JSON.parse(readFileSync(join(raizDoRepo, "firebase.json"), "utf-8"));
  const alvos: AlvoDeHospedagem[] = Array.isArray(bruto.hosting)
    ? bruto.hosting
    : [bruto.hosting];
  const achado = alvos.find((alvo) => alvo.target === target);
  if (achado === undefined) throw new Error(`o alvo \`${target}\` sumiu do firebase.json`);
  return achado;
}

/** Os caminhos de todo arquivo publicado, relativos à raiz do site e com `/`
 * à frente — do jeito que o Firebase os endereça. */
export function arquivosPublicados(dist: string): Set<string> {
  const encontrados = new Set<string>();
  function descer(pasta: string): void {
    for (const entrada of readdirSync(pasta)) {
      const caminho = join(pasta, entrada);
      if (statSync(caminho).isDirectory()) {
        descer(caminho);
        continue;
      }
      encontrados.add(`/${relative(dist, caminho).split(sep).join("/")}`);
    }
  }
  descer(dist);
  return encontrados;
}

/** Um `source` de `rewrite` do Firebase: `**` atravessa separador, `*` não.
 * Parte-se em `**` primeiro, para que o `*` de dentro de cada pedaço não
 * precise de sentinela para se distinguir do duplo. */
function casa(fonte: string, caminho: string): boolean {
  const padrao = fonte
    .split("**")
    .map((pedaco) => pedaco.replace(/[.+^${}()|[\]\\]/g, "\\$&").replace(/\*/g, "[^/]*"))
    .join(".*");
  return new RegExp(`^${padrao}$`).test(caminho);
}

export function resolverEndereco(
  caminho: string,
  alvo: AlvoDeHospedagem,
  publicados: Set<string>,
): EnderecoServido {
  // 1. Arquivo exato. A raiz pede o índice dela.
  const exato = caminho === "/" ? "/index.html" : caminho;
  if (publicados.has(exato)) {
    // 2. Com `cleanUrls`, o endereço com `.html` não é o endereço público:
    // responde redirecionando para o limpo. A raiz é a exceção — `/` já é o
    // endereço público de `index.html`.
    if (alvo.cleanUrls === true && caminho.endsWith(".html")) {
      return { tipo: "redirecionamento", para: caminho.replace(/(index)?\.html$/, "") || "/" };
    }
    return { tipo: "arquivo", arquivo: exato };
  }

  // 2. `cleanUrls`: `/x` serve `x.html`.
  if (alvo.cleanUrls === true && !caminho.endsWith("/")) {
    const comExtensao = `${caminho}.html`;
    if (publicados.has(comExtensao)) return { tipo: "arquivo", arquivo: comExtensao };
  }

  // 3. Índice de diretório.
  const indice = `${caminho.replace(/\/$/, "")}/index.html`;
  if (publicados.has(indice)) return { tipo: "arquivo", arquivo: indice };

  // 4. `rewrites`, na ordem declarada.
  for (const regra of alvo.rewrites ?? []) {
    if (!casa(regra.source, caminho)) continue;
    return { tipo: "rewrite", arquivo: regra.destination, regra: regra.source };
  }

  return { tipo: "nao-encontrado" };
}
