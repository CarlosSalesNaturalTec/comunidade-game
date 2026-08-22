import { EstadoDaLista } from "comum/react";
import "./ListaDeFilas.css";
import type { SolicitacaoDeParticipacao } from "./api";

const ROTULO_DA_PRETENSAO: Record<SolicitacaoDeParticipacao["pretensao"], string> = {
  mestre: "Mestre",
  apoiador: "Apoiador",
};

const ROTULO_DA_SITUACAO: Record<SolicitacaoDeParticipacao["situacao"], string> = {
  recebida: "Recebida",
  em_avaliacao: "Em avaliação",
  aceita: "Aceita",
  recusada: "Recusada",
};

function formatarPrazo(valorComFuso: string): string {
  const data = new Date(valorComFuso);
  if (Number.isNaN(data.getTime())) return valorComFuso;
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

interface Props {
  solicitacoes: SolicitacaoDeParticipacao[] | null;
  aoSelecionar: (solicitacao: SolicitacaoDeParticipacao) => void;
}

// A situação e o atraso se distinguem por rótulo textual, nunca só por cor
// (documento 15 §5). Lista densa do temperamento Operação (documento 15 §6).
export function ListaDeFilas({ solicitacoes, aoSelecionar }: Props) {
  if (solicitacoes === null) {
    return <EstadoDaLista>Carregando a fila…</EstadoDaLista>;
  }

  if (solicitacoes.length === 0) {
    return <EstadoDaLista>Nenhuma solicitação de participação por enquanto.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-filas" aria-label="Fila de avaliação">
      {solicitacoes.map((solicitacao) => (
        <li key={solicitacao.id} className="lista-de-filas__item">
          <button
            type="button"
            className="lista-de-filas__botao"
            onClick={() => aoSelecionar(solicitacao)}
          >
            <span className="lista-de-filas__quem">{solicitacao.nome_ou_razao_social}</span>
            <span className="lista-de-filas__pretensao">
              {ROTULO_DA_PRETENSAO[solicitacao.pretensao]}
            </span>
            <span className="lista-de-filas__situacao">
              {ROTULO_DA_SITUACAO[solicitacao.situacao]}
            </span>
            {solicitacao.em_atraso && (
              <span className="lista-de-filas__atraso">Em atraso</span>
            )}
            <span>Prazo: {formatarPrazo(solicitacao.prazo)}</span>
          </button>
        </li>
      ))}
    </ul>
  );
}
