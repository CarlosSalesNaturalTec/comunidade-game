import type { EstadoDaVivacidade } from "comum/biometria";
import type { RefObject } from "react";

// O retorno a quem opera é **abstrato**: diz o que o laço de detecção está
// vendo, nunca mostra a imagem capturada (`RF-04-64`, `RN-04-34`, documento 03
// §3.3, documento 99 §6 invariante 12).
const FRASE_DO_LACO: Record<EstadoDaVivacidade, string> = {
  procurando_rosto: "Procurando um rosto…",
  rosto_encontrado: "Rosto encontrado. Confirmando que há uma pessoa…",
  vivacidade_confirmada: "Pessoa confirmada.",
};

interface Props {
  /** O lugar que a tela empresta ao módulo de biometria: é `acoplarEspelho`
   * que anexa o vídeo aqui dentro. A tela nunca recebe `MediaStream`, quadro
   * nem pixel (design — decisão 2). */
  lugar: RefObject<HTMLDivElement | null>;
  estado: EstadoDaVivacidade | null;
}

// O visor fica sempre montado, e o CSS o esconde enquanto está vazio: assim o
// elemento existe no DOM antes de o preparo terminar, e não há corrida entre
// a renderização e o acoplamento do espelho.
export function Visor({ lugar, estado }: Props) {
  return (
    <div className="cg-visor-moldura">
      <div className="cg-visor-lugar" ref={lugar} />
      {estado && <p className="cg-visor-estado">{FRASE_DO_LACO[estado]}</p>}
    </div>
  );
}
