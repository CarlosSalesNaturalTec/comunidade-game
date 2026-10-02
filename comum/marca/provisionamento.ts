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

const AQUI = path.dirname(fileURLToPath(import.meta.url));

/** Copia `favicon.svg` para o `public/` da aplicação que chamar. */
export function provisionarFavicon(diretorioDeDestino: string): void {
  mkdirSync(diretorioDeDestino, { recursive: true });
  copyFileSync(path.join(AQUI, "favicon.svg"), path.join(diretorioDeDestino, "favicon.svg"));
}
