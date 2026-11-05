import type { RefObject } from "react";

interface Props {
  /** O lugar que a tela empresta ao módulo de biometria: é `acoplarEspelho`
   * que anexa o vídeo aqui dentro. O visor nunca recebe `MediaStream`, quadro
   * nem pixel — a fronteira que guarda o invariante 12 continua de pé por
   * construção (`RF-05-95`, `RN-05-53`). */
  lugar: RefObject<HTMLDivElement | null>;
  /** O que o laço de detecção está vendo, **já em palavras**. A redação é de
   * quem usa o visor, porque o público de cada tela é outro: a tela que um
   * Mestre opera fala com quem opera, e a entrada da App 05 fala com uma
   * criança de 6 anos (PRD-05 §10, PRD-04 §10). O retorno é **abstrato** —
   * diz o que o laço vê, nunca mostra a imagem capturada (`RN-05-53`,
   * `RN-04-34`). */
  frase?: string | null;
}

// O visor da câmera das telas de reconhecimento, nas Apps 01 e 05. Fica
// sempre montado, e o CSS o esconde enquanto está vazio: assim o elemento
// existe no DOM antes de o preparo terminar, e não há corrida entre a
// renderização e o acoplamento do espelho.
export function Visor({ lugar, frase }: Props) {
  return (
    <div className="cg-visor-moldura">
      <div className="cg-visor-lugar" ref={lugar} />
      {frase && <p className="cg-visor-estado">{frase}</p>}
    </div>
  );
}
