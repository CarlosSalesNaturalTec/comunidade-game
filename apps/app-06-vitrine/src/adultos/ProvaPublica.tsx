import { EstadoDaLista } from "comum/react";
import type { ArtefatoPublico } from "../api/leituras";

/** A prova pública do `RF-03-07` — currículo, portfólios, redes sociais e
 * comprobatórios. O artefato não tem tipo no modelo: os quatro são o mesmo
 * registro, distinguidos pelo **rótulo** que quem declarou escreveu, e a
 * prova é sempre **link declarado**, nunca anexo (`RN-02-01`). */
export function ProvaPublica({ artefatos }: { artefatos: ArtefatoPublico[] }) {
  return (
    <>
      <h3>Prova pública</h3>
      {artefatos.length === 0 ? (
        <EstadoDaLista>Nenhum comprobatório declarado ainda.</EstadoDaLista>
      ) : (
        <ul className="cg-prova-publica">
          {artefatos.map((artefato) => (
            <li key={artefato.endereco}>
              <a href={artefato.endereco} rel="noreferrer noopener" target="_blank">
                {artefato.rotulo}
              </a>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
