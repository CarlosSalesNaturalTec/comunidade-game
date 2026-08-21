import { EstadoDaLista } from "comum/react";
import "./ListaDaAgenda.css";
import type { AulaDaAgenda } from "./api";
import { CancelamentoDeAula } from "./CancelamentoDeAula";

interface Props {
  aulas: AulaDaAgenda[] | null;
  nomeDaComunidade: (id: string) => string;
  nomeDoPontoDeApoio: (id: string) => string;
  podeCancelar: boolean;
  aoCancelar: (idDaAula: string, motivo: string) => Promise<void>;
}

const ROTULO_DA_SITUACAO: Record<string, string> = {
  prevista: "Prevista",
  pendente_de_lastro: "Pendente de lastro",
  confirmada: "Confirmada",
  realizada: "Realizada",
  cancelada: "Cancelada",
};

// Aula com desfecho (realizada ou cancelada) não oferece cancelamento
// (`RF-01-72`, `RN-02-20`).
const SITUACOES_COM_DESFECHO = new Set(["realizada", "cancelada"]);

function formatarHorario(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

// A situação se distingue por rótulo textual, nunca só por cor
// (`RN-02-09`, documento 15 §5). Lista densa do temperamento Operação
// (documento 15 §6).
export function ListaDaAgenda({
  aulas,
  nomeDaComunidade,
  nomeDoPontoDeApoio,
  podeCancelar,
  aoCancelar,
}: Props) {
  if (aulas === null) {
    return <EstadoDaLista>Carregando a agenda…</EstadoDaLista>;
  }

  if (aulas.length === 0) {
    return <EstadoDaLista>Nenhuma aula agendada ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-da-agenda" aria-label="Agenda de aulas">
      {aulas.map((aula) => (
        <li key={aula.id} className="lista-da-agenda__item">
          <div className="lista-da-agenda__linha">
            <span className="lista-da-agenda__comunidade">
              {nomeDaComunidade(aula.comunidade_virtual_id)}
            </span>
            <span className="lista-da-agenda__ponto-de-apoio">
              {nomeDoPontoDeApoio(aula.ponto_de_apoio_id)}
            </span>
            <span className="lista-da-agenda__horario">
              {formatarHorario(aula.inicio_em)} – {formatarHorario(aula.fim_em)}
            </span>
            <span
              className={`lista-da-agenda__situacao lista-da-agenda__situacao--${aula.situacao}`}
            >
              {ROTULO_DA_SITUACAO[aula.situacao] ?? aula.situacao}
            </span>
          </div>

          {aula.situacao === "cancelada" && aula.cancelamento_motivo && (
            <p className="lista-da-agenda__motivo">Motivo: {aula.cancelamento_motivo}</p>
          )}

          {podeCancelar && !SITUACOES_COM_DESFECHO.has(aula.situacao) && (
            <CancelamentoDeAula onConfirmar={(motivo) => aoCancelar(aula.id, motivo)} />
          )}
        </li>
      ))}
    </ul>
  );
}
