import { Botao, EstadoDaLista } from "comum/react";
import { useState } from "react";
import "./Acervo.css";
import { AnotacaoNaFichaDeVida } from "./AnotacaoNaFichaDeVida";
import type { ItemPatrimonialDaLista } from "./api";
import { FichaDeVida } from "./FichaDeVida";

interface Props {
  itens: ItemPatrimonialDaLista[] | null;
  pontoDeApoioPorId: Map<string, string>;
  nomePorId: Map<string, string>;
  podeAnotar: boolean;
  onAnotado: () => void;
}

interface PropsDoItem {
  item: ItemPatrimonialDaLista;
  nomeDoPontoDeApoio: string;
  nomeDoResponsavel: string | null;
  nomePorId: Map<string, string>;
  podeAnotar: boolean;
  onAnotado: () => void;
}

// A ficha de vida é seção do próprio exemplar, aberta e fechada por item —
// não uma tela à parte, porque `GET /v1/itens-patrimoniais` já a devolve
// inteira (`RF-02-53`; design — decisão 2).
function ItemDoAcervo({
  item,
  nomeDoPontoDeApoio,
  nomeDoResponsavel,
  nomePorId,
  podeAnotar,
  onAnotado,
}: PropsDoItem) {
  const [aberto, definirAberto] = useState(false);

  return (
    <li className="lista-do-acervo__item">
      <div className="lista-do-acervo__linha">
        <span className="lista-do-acervo__titulo">{item.titulo}</span>
        <span>Tombo {item.numero_de_tombo}</span>
        <span>{nomeDoPontoDeApoio}</span>
        <span>{item.estado_de_conservacao}</span>
        {nomeDoResponsavel === null ? (
          <EstadoDaLista>Sem responsável designado.</EstadoDaLista>
        ) : (
          <span className="lista-do-acervo__responsavel">{nomeDoResponsavel}</span>
        )}
      </div>

      <Botao variante="secundaria" onClick={() => definirAberto((atual) => !atual)}>
        {aberto ? "Ocultar ficha de vida" : "Ver ficha de vida"}
      </Botao>

      {aberto && (
        <div className="lista-do-acervo__ficha">
          <FichaDeVida anotacoes={item.ficha_de_vida} nomePorId={nomePorId} />
          {podeAnotar && <AnotacaoNaFichaDeVida idDoItem={item.id} onAnotado={onAnotado} />}
        </div>
      )}
    </li>
  );
}

// Lista densa do temperamento Operação (documento 15 §6): título, número de
// tombo, ponto de apoio, estado de conservação corrente e o responsável
// derivado, sem valor em reais e sem caminho de retirada, empréstimo,
// devolução ou transferência (`RF-02-52`, `RN-02-18`, `RN-02-19`).
export function ListaDoAcervo({
  itens,
  pontoDeApoioPorId,
  nomePorId,
  podeAnotar,
  onAnotado,
}: Props) {
  if (itens === null) {
    return <EstadoDaLista>Carregando o acervo…</EstadoDaLista>;
  }

  if (itens.length === 0) {
    return <EstadoDaLista>Nenhum exemplar tombado nesta comunidade.</EstadoDaLista>;
  }

  return (
    <ul className="lista-do-acervo" aria-label="Acervo">
      {itens.map((item) => (
        <ItemDoAcervo
          key={item.id}
          item={item}
          nomeDoPontoDeApoio={
            pontoDeApoioPorId.get(item.ponto_de_apoio_id) ?? item.ponto_de_apoio_id
          }
          nomeDoResponsavel={
            item.responsavel_id === null
              ? null
              : (nomePorId.get(item.responsavel_id) ?? item.responsavel_id)
          }
          nomePorId={nomePorId}
          podeAnotar={podeAnotar}
          onAnotado={onAnotado}
        />
      ))}
    </ul>
  );
}
