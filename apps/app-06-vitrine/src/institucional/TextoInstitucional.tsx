// O texto institucional é parágrafos e, no máximo, blocos com título: uma
// linha iniciada por `## ` abre um bloco. É a única marcação, e o texto entra
// na tela como texto do React, nunca como HTML (design — decisão 4).

interface Bloco {
  titulo: string | null;
  paragrafos: string[];
}

/** O `id` do bloco: o título sem acento, em minúscula e com hífen. */
export function idDoTitulo(titulo: string): string {
  return titulo
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function blocosDoTexto(texto: string): Bloco[] {
  const blocos: Bloco[] = [];
  let atual: Bloco = { titulo: null, paragrafos: [] };
  for (const paragrafo of texto.split(/\n\s*\n/)) {
    const limpo = paragrafo.trim();
    if (limpo === "") continue;
    const [primeira, ...resto] = limpo.split("\n");
    if (primeira.startsWith("## ")) {
      if (atual.titulo !== null || atual.paragrafos.length > 0) blocos.push(atual);
      atual = { titulo: primeira.slice(3).trim(), paragrafos: [] };
      if (resto.length > 0) atual.paragrafos.push(resto.join("\n"));
    } else {
      atual.paragrafos.push(limpo);
    }
  }
  if (atual.titulo !== null || atual.paragrafos.length > 0) blocos.push(atual);
  return blocos;
}

export function TextoInstitucional({ texto }: { texto: string }) {
  return (
    <>
      {blocosDoTexto(texto).map((bloco, indice) => (
        // biome-ignore lint/suspicious/noArrayIndexKey: os blocos são só de leitura e nunca reordenam.
        <div key={indice} className="cg-institucional__bloco">
          {bloco.titulo !== null && (
            <h3 id={idDoTitulo(bloco.titulo)} tabIndex={-1}>
              {bloco.titulo}
            </h3>
          )}
          {bloco.paragrafos.map((paragrafo) => (
            <p key={paragrafo} className="cg-institucional__paragrafo">
              {paragrafo}
            </p>
          ))}
        </div>
      ))}
    </>
  );
}
