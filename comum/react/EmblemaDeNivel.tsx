import { GlifoDePoder } from "./GlifoDePoder";

// O emblema de nível do documento 15 §8.2: o nível aparece como **número de
// marcas na moldura, igual ao nível** — uma no 1, cinco no 5 —, para que uma
// criança de 6 anos possa **contá-lo**, e legível sem depender de cor, porque
// a marca é forma e não tinta.
//
// No nível 5 a moldura **fecha**: é a marca de **Mestre Aprendiz**, e vem com
// o rótulo em texto, porque o documento 15 §5 proíbe significado só por forma
// como proíbe só por cor — moldura fechada sem rótulo seria decoração.
//
// O emblema é sempre **de uma trilha ou de um poder, nunca global**
// (`RN-05-03`), e a moldura carrega o nome do poder: é o `poder` obrigatório
// aqui. As marcas ficam `aria-hidden` porque quem lê por voz alcança o numeral
// e o nome, que dizem a mesma coisa sem contar traço.

/** O nível em que a moldura fecha — Mestre Aprendiz (documento 15 §8.2). */
export const NIVEL_DE_MESTRE_APRENDIZ = 5;

/** As cinco marcas possíveis, nomeadas: a moldura leva as primeiras `nivel`
 * delas, e o nome de cada uma é a chave estável da lista. */
const MARCAS = ["um", "dois", "tres", "quatro", "cinco"] as const;

interface Props {
  nivel: number;
  /** O nome do poder — ou da trilha — a que o nível pertence. Emblema sem ele
   * seria emblema global, que o documento 15 §8.2 proíbe. */
  poder: string;
}

export function EmblemaDeNivel({ nivel, poder }: Props) {
  const marcas = Math.max(0, Math.min(Math.trunc(nivel), NIVEL_DE_MESTRE_APRENDIZ));
  const fechada = marcas >= NIVEL_DE_MESTRE_APRENDIZ;

  return (
    <span
      className={`cg-emblema-de-nivel${fechada ? " cg-emblema-de-nivel--fechada" : ""}`}
      data-nivel={marcas}
    >
      <span className="cg-emblema-de-nivel__marcas" aria-hidden="true">
        {MARCAS.slice(0, marcas).map((marca) => (
          <span key={marca} className="cg-emblema-de-nivel__marca" data-marca="" />
        ))}
      </span>
      <span className="cg-emblema-de-nivel__numeral">Nível {marcas}</span>
      <GlifoDePoder poder={poder} tamanho={16} />
      {fechada && <span className="cg-emblema-de-nivel__mestre">Mestre Aprendiz</span>}
    </span>
  );
}
