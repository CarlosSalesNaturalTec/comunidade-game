import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

// Só roda em Node — chamado pelo `vite.config.ts` de cada app, nunca
// importado do código de navegador. Por isso não entra em `indice.ts`
// (a porta para o bundle do browser) e ganha o próprio caminho de
// `exports` no `package.json` deste pacote.
const requerer = createRequire(import.meta.url);

// Os únicos cinco modelos que `biometria.ts` habilita (`face.detector`,
// `face.mesh`, `face.description`, `face.antispoof`, `face.liveness`) —
// não o diretório inteiro de modelos da Human, que traz modelos que este
// projeto não usa.
const MODELOS_HABILITADOS = ["blazeface", "antispoof", "liveness", "faceres", "facemesh"];

interface ManifestoDePesos {
  weightsManifest: Array<{ paths: string[] }>;
}

// O pacote resolve, pelas condições de `exports`, para `dist/human.node.js`
// (mesmo ponto de partida do `alias` em cada `vite.config.ts`); os modelos
// ficam na raiz do pacote, um nível acima de `dist/`.
function diretorioDeModelosDaHuman(): string {
  const arquivoPrincipal = requerer.resolve("@vladmandic/human");
  const raizDoPacote = path.dirname(path.dirname(arquivoPrincipal));
  return path.join(raizDoPacote, "models");
}

// Copia o `.json` de cada modelo habilitado e os arquivos de peso que o
// próprio `weightsManifest` declara — nunca por nome fixo de arquivo, para
// não presumir que todo modelo tem um único `.bin` de mesmo nome
// (design.md — Decisions, Risks).
export function provisionarModelosDeBiometria(diretorioDeDestino: string): void {
  const origem = diretorioDeModelosDaHuman();
  mkdirSync(diretorioDeDestino, { recursive: true });

  for (const modelo of MODELOS_HABILITADOS) {
    const nomeDoJson = `${modelo}.json`;
    const manifesto: ManifestoDePesos = JSON.parse(
      readFileSync(path.join(origem, nomeDoJson), "utf-8"),
    );
    copyFileSync(path.join(origem, nomeDoJson), path.join(diretorioDeDestino, nomeDoJson));

    for (const grupo of manifesto.weightsManifest) {
      for (const nomeDoPeso of grupo.paths) {
        copyFileSync(path.join(origem, nomeDoPeso), path.join(diretorioDeDestino, nomeDoPeso));
      }
    }
  }
}
