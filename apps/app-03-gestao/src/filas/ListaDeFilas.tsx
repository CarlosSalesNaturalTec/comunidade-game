import { EstadoDaLista } from "comum/react";
import "./ListaDeFilas.css";

// Compartilhada pelas quatro naturezas da fila — quem chama normaliza os
// campos próprios de cada uma antes de passar aqui, para que a lista, o
// filtro e a apresentação do atraso não mudem de forma quando a natureza
// muda (design — decisão 3, `RF-02-25`, `RF-02-77`, `RF-02-87`).
export interface ItemDeFila {
  id: string;
  quem: string;
  detalhe: string;
  situacaoRotulo: string;
  em_atraso: boolean;
  prazo: string;
}

function formatarPrazo(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

interface Props {
  itens: ItemDeFila[] | null;
  mensagemVazia: string;
  aoSelecionar: (id: string) => void;
}

// A situação e o atraso se distinguem por rótulo textual, nunca só por cor
// (documento 15 §5). Lista densa do temperamento Operação (documento 15 §6).
export function ListaDeFilas({ itens, mensagemVazia, aoSelecionar }: Props) {
  if (itens === null) {
    return <EstadoDaLista>Carregando a fila…</EstadoDaLista>;
  }

  if (itens.length === 0) {
    return <EstadoDaLista>{mensagemVazia}</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-filas" aria-label="Fila de avaliação">
      {itens.map((item) => (
        <li key={item.id} className="lista-de-filas__item">
          <button
            type="button"
            className="lista-de-filas__botao"
            onClick={() => aoSelecionar(item.id)}
          >
            <span className="lista-de-filas__quem">{item.quem}</span>
            <span className="lista-de-filas__pretensao">{item.detalhe}</span>
            <span className="lista-de-filas__situacao">{item.situacaoRotulo}</span>
            {item.em_atraso && <span className="lista-de-filas__atraso">Em atraso</span>}
            <span>Prazo: {formatarPrazo(item.prazo)}</span>
          </button>
        </li>
      ))}
    </ul>
  );
}
