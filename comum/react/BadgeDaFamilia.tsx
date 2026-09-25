import type { ReactElement } from "react";
import { glifoDoPoder } from "./GlifoDePoder";
import { Icone } from "./Icone";

// As seis silhuetas de badge do documento 15 §8.3 — uma por família —,
// desenhadas na grade de `24` px do sistema de ícone da §11.1 e legíveis nesse
// tamanho **sem depender de cor**, porque o que as separa é a forma.
//
// A silhueta diz a **família**, nunca o poder: dois badges de nível são ambos
// escudo, e o que os distingue é o **glifo do poder** dentro deles (§8.4). Por
// isso o glifo entra na silhueta, e o rótulo em texto acompanha as duas coisas
// — forma sozinha não carrega significado (§5).
//
// As seis são desenhadas de uma vez, e **duas ainda não têm dado**: o
// `TipoDeBadge` do núcleo tem quatro valores, e as famílias **de conquista** e
// **de território** seguem como pendência no documento 09 §1. Desenhá-las
// agora custa o mesmo e evita voltar aqui quando o núcleo as tiver.

/** As seis famílias do documento 15 §8.3. Os quatro primeiros valores são os
 * do `TipoDeBadge` do núcleo; `de_conquista` e `de_territorio` são as duas que
 * o documento declara e o núcleo ainda não emite (documento 09 §1). */
export type FamiliaDeBadge =
  | "de_nivel"
  | "de_conquista"
  | "de_valores_e_causas"
  | "de_territorio"
  | "de_autoria"
  | "de_protagonismo";

interface Silhueta {
  /** O nome da forma, como o documento 15 §8.3 a chama. */
  forma: string;
  rotulo: string;
  desenho: ReactElement;
}

const SILHUETAS: Record<FamiliaDeBadge, Silhueta> = {
  de_nivel: {
    forma: "escudo",
    rotulo: "Badge de nível",
    desenho: (
      <path d="M12 2.5l7.5 2.5v6.5c0 4.7-3.2 8.2-7.5 10.5-4.3-2.3-7.5-5.8-7.5-10.5V5Z" />
    ),
  },
  de_conquista: {
    forma: "estrela",
    rotulo: "Badge de conquista",
    desenho: (
      <path d="m12 2.5 2.9 6 6.6.9-4.8 4.6 1.2 6.5-5.9-3.2-5.9 3.2 1.2-6.5-4.8-4.6 6.6-.9Z" />
    ),
  },
  de_valores_e_causas: {
    forma: "coracao",
    rotulo: "Badge de valores e causas",
    desenho: (
      <path d="M12 20.8C8 18 4 14.4 4 10.3A4.3 4.3 0 0 1 12 7.4a4.3 4.3 0 0 1 8 2.9c0 4.1-4 7.7-8 10.5Z" />
    ),
  },
  de_territorio: {
    forma: "gota",
    rotulo: "Badge de território",
    desenho: <path d="M12 2.5c3.7 4.4 6 7.6 6 10.5a6 6 0 0 1-12 0c0-2.9 2.3-6.1 6-10.5Z" />,
  },
  de_autoria: {
    forma: "folha-com-canto-dobrado",
    rotulo: "Badge de autoria",
    desenho: (
      <>
        <path d="M5 3.5h9l5 5v12H5Z" />
        <path d="M14 3.5v5h5" />
      </>
    ),
  },
  de_protagonismo: {
    forma: "hexagono",
    rotulo: "Badge de protagonismo",
    desenho: <path d="M12 2.5l8.2 4.7v9.6L12 21.5 3.8 16.8V7.2Z" />,
  },
};

interface Props {
  familia: FamiliaDeBadge;
  /** O poder do badge, quando houver: o glifo dele entra na silhueta e é o que
   * separa dois badges da mesma família (documento 15 §§8.3, 8.4). O badge de
   * protagonismo é global por exceção (`RN-01-50`) e não tem poder. */
  poder?: string;
}

export function BadgeDaFamilia({ familia, poder }: Props) {
  const silhueta = SILHUETAS[familia];

  return (
    <span className="cg-badge">
      <span className="cg-badge__silhueta">
        <svg
          className="cg-badge__forma"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
          focusable="false"
          data-silhueta={silhueta.forma}
        >
          {silhueta.desenho}
        </svg>
        {poder !== undefined && (
          <span className="cg-badge__glifo">
            <Icone glifo={glifoDoPoder(poder)} tamanho={16} />
          </span>
        )}
      </span>
      {/* O nome do poder acompanha o glifo que está na silhueta, no rótulo do
       * badge: dentro da moldura de `24` px não cabe texto, e glifo sem nome é
       * o que o documento 15 §8.4 proíbe. */}
      <span className="cg-badge__rotulo">
        {silhueta.rotulo}
        {poder !== undefined && ` — ${poder}`}
      </span>
    </span>
  );
}
