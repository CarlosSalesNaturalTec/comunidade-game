import { copyFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

// Só roda em Node — chamado pelo `vite.config.ts` de cada aplicação, nunca
// importado do código de navegador. Mesmo caminho de
// `biometria/provisionamento.ts`, pelo mesmo motivo: ativo de `comum/` que
// precisa chegar ao `public/` de cada aplicação.
//
// O favicon é **um arquivo só**, nesta pasta, copiado para as sete: manter
// sete cópias versionadas à mão é como o logotipo do Vite ficou em todas sem
// ninguém notar (design — decisão 5).
//
// A origem é o **símbolo**: sob a forma de escudo com ponta, o favicon e o
// símbolo ficaram idênticos — os dois limitados pela mesma grade de 48 —, e
// dois arquivos de conteúdo igual são a duplicidade que o §7 do README proíbe
// (decisão do fundador de 2026-10-02). O nome de destino segue `favicon.svg`,
// que é o que cada `index.html` referencia.

const AQUI = path.dirname(fileURLToPath(import.meta.url));

/** Copia `simbolo.svg` para o `public/` da aplicação que chamar, com o nome
 * `favicon.svg`. */
export function provisionarFavicon(diretorioDeDestino: string): void {
  mkdirSync(diretorioDeDestino, { recursive: true });
  copyFileSync(path.join(AQUI, "simbolo.svg"), path.join(diretorioDeDestino, "favicon.svg"));
}

/** Os quatro do elenco (documento 15 §13.6), no par AVIF com reserva WebP que
 * o `README.md` §3 fixa. */
const ELENCO = ["susy", "otavio", "trenell", "robo-educa"];

/** Copia o elenco para `<destino>/elenco/`, mesmo caminho e mesmo motivo do
 * favicon: ativo de `comum/` que precisa ser servido pelo próprio domínio da
 * aplicação (documento 15 §1, princípio 6). Só a App 06 chama, porque só o
 * herói da vitrine apresenta o elenco hoje. */
export function provisionarElenco(diretorioDeDestino: string): void {
  const destino = path.join(diretorioDeDestino, "elenco");
  mkdirSync(destino, { recursive: true });
  for (const nome of ELENCO) {
    for (const extensao of ["avif", "webp"]) {
      const arquivo = `${nome}.${extensao}`;
      copyFileSync(path.join(AQUI, "elenco", arquivo), path.join(destino, arquivo));
    }
  }
}
