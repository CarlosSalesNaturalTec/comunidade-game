import { EstadoDaLista } from "comum/react";
import type { NecessidadeDeRecurso } from "./api";

interface Props {
  necessidades: NecessidadeDeRecurso[] | null;
  nomeDoTipoDeRecurso: (id: string) => string;
  nomeDaComunidade: (id: string) => string;
  nomeDoPontoDeApoio: (id: string) => string;
}

function formatarHorario(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// A lista vem do núcleo já derivada — nunca soma, ordena por saldo nem
// recalcula a falta (`RF-02-58`, `RN-02-19`).
export function ListaDeNecessidades({
  necessidades,
  nomeDoTipoDeRecurso,
  nomeDaComunidade,
  nomeDoPontoDeApoio,
}: Props) {
  if (necessidades === null) {
    return <EstadoDaLista>Carregando as necessidades…</EstadoDaLista>;
  }

  if (necessidades.length === 0) {
    return <EstadoDaLista>Não há necessidade de recurso em aberto.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-necessidades" aria-label="Necessidades de recurso em aberto">
      {necessidades.map((necessidade) => (
        <li
          key={`${necessidade.aula_id}-${necessidade.tipo_de_recurso_id}`}
          className="lista-de-necessidades__item"
        >
          <span className="lista-de-necessidades__tipo">
            {nomeDoTipoDeRecurso(necessidade.tipo_de_recurso_id)}
          </span>
          <span className="lista-de-necessidades__quantidade">
            Falta: {necessidade.quantidade_faltante}
          </span>
          <span className="lista-de-necessidades__valor">
            {necessidade.valor_em_moedas !== null
              ? `${necessidade.valor_em_moedas} moedas`
              : "Sem valor de referência vigente"}
          </span>
          <span className="lista-de-necessidades__comunidade">
            {nomeDaComunidade(necessidade.comunidade_virtual_id)}
          </span>
          <span className="lista-de-necessidades__ponto-de-apoio">
            {nomeDoPontoDeApoio(necessidade.ponto_de_apoio_id)}
          </span>
          <span className="lista-de-necessidades__horario">
            {formatarHorario(necessidade.inicio_em)} – {formatarHorario(necessidade.fim_em)}
          </span>
        </li>
      ))}
    </ul>
  );
}
