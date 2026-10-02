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
