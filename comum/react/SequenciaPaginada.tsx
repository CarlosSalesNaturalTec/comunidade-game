import { type ReactNode, useState } from "react";
import { Botao } from "./Botao";

interface Props<Item> {
  itens: Item[];
  /** O que renderizar para o item da vez. O paginador não sabe o que ele é
   * (design — decisão 2). */
  children: (item: Item, indice: number) => ReactNode;
  /** Nomeia o que se percorre, para a posição não sair só em número:
   * `"Conteúdo"` vira "Conteúdo 1 de 4". */
  nome?: string;
  rotuloDeAvancar?: string;
  /** Ausente, não há retorno ao item anterior — é o caso do conteúdo da
   * missão, que não tem o que corrigir (design — decisão 3). */
  rotuloDeVoltar?: string;
  /** Posição comandada de fora. Ausente, o paginador guarda a sua em
   * `useState` (design — decisão 7); presente, quem monta manda — é como o
   * desafio leva o Guerreiro(a) até a pergunta que falta. */
  indice?: number;
  aoIrPara?: (indice: number) => void;
}

// Percorre uma sequência um item por vez, com controle de avançar e a
// posição declarada em texto. Um item só não ganha moldura de paginação, e
// o último não oferece avançar para lugar nenhum (documento 15 §6.4).
export function SequenciaPaginada<Item>({
  itens,
  children,
  nome,
  rotuloDeAvancar = "Avançar",
  rotuloDeVoltar,
  indice: indiceDeFora,
  aoIrPara,
}: Props<Item>) {
  const [indiceLocal, definirIndiceLocal] = useState(0);

  if (itens.length === 0) return null;

  const comandadaDeFora = indiceDeFora !== undefined;
  const bruto = comandadaDeFora ? indiceDeFora : indiceLocal;
  const indice = Math.min(Math.max(bruto, 0), itens.length - 1);
  const posicao = nome
    ? `${nome} ${indice + 1} de ${itens.length}`
    : `${indice + 1} de ${itens.length}`;

  function irPara(destino: number) {
    if (!comandadaDeFora) definirIndiceLocal(destino);
    aoIrPara?.(destino);
  }

  return (
    <div className="cg-sequencia">
      <div className="cg-sequencia__item">{children(itens[indice], indice)}</div>
      {itens.length > 1 && (
        <div className="cg-sequencia__controles">
          <p className="cg-sequencia__posicao" aria-live="polite">
            {posicao}
          </p>
          {rotuloDeVoltar !== undefined && indice > 0 && (
            <Botao variante="secundaria" onClick={() => irPara(indice - 1)}>
              {rotuloDeVoltar}
            </Botao>
          )}
          {indice < itens.length - 1 && (
            <Botao variante="secundaria" onClick={() => irPara(indice + 1)}>
              {rotuloDeAvancar}
            </Botao>
          )}
        </div>
      )}
    </div>
  );
}
