import { Botao, EstadoDaLista } from "comum/react";
import { chaveDaNecessidade, type NecessidadeDeRecurso } from "./api";

interface Props {
  necessidades: NecessidadeDeRecurso[] | null;
  nomeDoTipoDeRecurso: (id: string) => string;
  nomeDoPontoDeApoio: (id: string) => string;
  aoAbsorver: (necessidade: NecessidadeDeRecurso) => void;
}

function formatarHorario(valorComFuso: string | null): string {
  if (valorComFuso === null) return "";
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// A falta de cada aula e de cada recompensa de marco — esta com a trilha no
// lugar do horário (`RF-09-56`, `RF-07-54`) —, derivada do núcleo — nunca soma, reordena por saldo
// nem recalcula (`RF-09-56`, `RN-09-12`). Necessidade de tipo sem valor de
// referência vigente continua aparecendo, sem valor nem nome arbitrado.
export function ListaDeNecessidades({
  necessidades,
  nomeDoTipoDeRecurso,
  nomeDoPontoDeApoio,
  aoAbsorver,
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
        <li key={chaveDaNecessidade(necessidade)} className="lista-de-necessidades__item">
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
          <span className="lista-de-necessidades__ponto-de-apoio">
            {nomeDoPontoDeApoio(necessidade.ponto_de_apoio_id)}
          </span>
          {necessidade.especie === "aula" ? (
            <span className="lista-de-necessidades__horario">
              {formatarHorario(necessidade.inicio_em)} – {formatarHorario(necessidade.fim_em)}
            </span>
          ) : (
            <span className="lista-de-necessidades__trilha">
              Recompensa de marco · Trilha {necessidade.trilha_nome}
            </span>
          )}
          <Botao variante="secundaria" onClick={() => aoAbsorver(necessidade)}>
            Absorver
          </Botao>
        </li>
      ))}
    </ul>
  );
}
