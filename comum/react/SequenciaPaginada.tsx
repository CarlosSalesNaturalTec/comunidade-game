import { type ReactNode, useState } from "react";
import { Botao } from "./Botao";

interface Props<Item> {
  itens: Item[];
  /** O que renderizar para o item da vez. O paginador não sabe o que ele é
   * (design — decisão 2). */
  children: (item: Item, indice: number) => ReactNode;
  rotuloDeAvancar?: string;
  /** Ausente, não há retorno ao item anterior — é o caso do conteúdo da
   * missão, que não tem o que corrigir (design — decisão 3). */
  rotuloDeVoltar?: string;
  /** Posição comandada de fora. Ausente, o paginador guarda a sua em
   * `useState` (design — decisão 7); presente, quem monta manda. */
  indice?: number;
  aoIrPara?: (indice: number) => void;
  /** O que acompanha avançar e voltar na mesma linha — hoje o envio das
   * respostas do quiz, que pertence ao conjunto e não à pergunta da vez.
   * Havendo ações, a linha de controles existe **mesmo com um item só**:
   * quiz de uma pergunta perderia o botão de enviar, porque a moldura de
   * paginação não se justifica para ele (design — decisão 4). */
  acoes?: ReactNode;
  /** Trava avançar e voltar, sem travar as `acoes`, que têm condição
   * própria — é como a mídia que ainda carrega impede a troca de item
   * (design — decisão 7). */
  controlesTravados?: boolean;
}

// Percorre uma sequência um item por vez, com controle de avançar. Um item só
// não ganha moldura de paginação, e o último não oferece avançar para lugar
// nenhum (documento 15 §6.4).
//
// A **posição não é declarada** — nem escrita, nem anunciada a leitor de tela:
// numa Arena de uma decisão por tela a contagem é ruído, e o que orienta é o
// próprio item da vez (decisão do fundador de 2026-10-16). Por isso não existe
// aqui propriedade que nomeie o que se percorre: ela só servia à frase que saiu.
export function SequenciaPaginada<Item>({
  itens,
  children,
  rotuloDeAvancar = "Avançar",
  rotuloDeVoltar,
  indice: indiceDeFora,
  aoIrPara,
  acoes,
  controlesTravados = false,
}: Props<Item>) {
  const [indiceLocal, definirIndiceLocal] = useState(0);

  if (itens.length === 0) return null;

  const comandadaDeFora = indiceDeFora !== undefined;
  const bruto = comandadaDeFora ? indiceDeFora : indiceLocal;
  const indice = Math.min(Math.max(bruto, 0), itens.length - 1);
  const navega = itens.length > 1;

  function irPara(destino: number) {
    if (!comandadaDeFora) definirIndiceLocal(destino);
    aoIrPara?.(destino);
  }

  return (
    <div className="cg-sequencia">
      <div className="cg-sequencia__item">{children(itens[indice], indice)}</div>
      {(navega || acoes) && (
        <div className="cg-sequencia__controles">
          {navega && rotuloDeVoltar !== undefined && indice > 0 && (
            <Botao
              variante="secundaria"
              onClick={() => irPara(indice - 1)}
              desabilitado={controlesTravados}
            >
              {rotuloDeVoltar}
            </Botao>
          )}
          {navega && indice < itens.length - 1 && (
            <Botao
              variante="secundaria"
              onClick={() => irPara(indice + 1)}
              desabilitado={controlesTravados}
            >
              {rotuloDeAvancar}
            </Botao>
          )}
          {acoes}
        </div>
      )}
    </div>
  );
}
