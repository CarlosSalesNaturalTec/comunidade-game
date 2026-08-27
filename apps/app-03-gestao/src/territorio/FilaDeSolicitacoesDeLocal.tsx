import { Aviso, EstadoDaLista } from "comum/react";
import "./Territorio.css";
import { AvaliacaoDeSolicitacaoDeLocal } from "./AvaliacaoDeSolicitacaoDeLocal";
import type { DesafioPublicadoDaLista, LocalDaLista, SolicitacaoDeLocalDaLista } from "./api";
import { ROTULO_DO_NIVEL } from "./FormularioDeLocal";

interface GuerreiroResumo {
  nick: string;
}

interface Props {
  solicitacoes: SolicitacaoDeLocalDaLista[] | null;
  locais: LocalDaLista[];
  guerreiroPorId: Map<string, GuerreiroResumo>;
  desafioPorId: Map<string, DesafioPublicadoDaLista>;
  podeAvaliar: boolean;
  onAvaliada: () => void;
}

// Alerta enquanto houver solicitação sem desfecho — some quando a fila
// esvazia (`RF-02-21`, `RN-02-22`). Solicitante por nick, nunca por imagem
// real (invariante 12 do documento 99 §6).
export function FilaDeSolicitacoesDeLocal({
  solicitacoes,
  locais,
  guerreiroPorId,
  desafioPorId,
  podeAvaliar,
  onAvaliada,
}: Props) {
  if (solicitacoes === null) {
    return <EstadoDaLista>Carregando as solicitações de novo local…</EstadoDaLista>;
  }

  return (
    <div>
      {solicitacoes.length > 0 && (
        <Aviso tipo="atencao">
          Há {solicitacoes.length} solicitação(ões) de novo local aguardando avaliação.
        </Aviso>
      )}

      {solicitacoes.length === 0 ? (
        <EstadoDaLista>Nenhuma solicitação de novo local em aberto.</EstadoDaLista>
      ) : (
        <ul className="fila-de-solicitacoes-de-local" aria-label="Solicitações de novo local">
          {solicitacoes.map((solicitacao) => {
            const solicitante = guerreiroPorId.get(solicitacao.solicitante_id);
            const desafio = desafioPorId.get(solicitacao.desafio_de_coleta_id);
            return (
              <li key={solicitacao.id} className="fila-de-solicitacoes-de-local__item">
                <div className="fila-de-solicitacoes-de-local__linha">
                  <span className="fila-de-solicitacoes-de-local__solicitante">
                    {solicitante ? solicitante.nick : "Guerreiro(a)"}
                  </span>
                  <span>Avatar definido</span>
                  <span>{ROTULO_DO_NIVEL[solicitacao.nivel_pretendido]}</span>
                  <span>{solicitacao.rotulo}</span>
                  <span>{desafio ? desafio.tipo_de_coleta.nome : "Desafio de coleta"}</span>
                </div>
                <p>{solicitacao.justificativa}</p>
                {podeAvaliar && (
                  <AvaliacaoDeSolicitacaoDeLocal
                    solicitacao={solicitacao}
                    locais={locais}
                    onConcluido={onAvaliada}
                  />
                )}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
