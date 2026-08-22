import { EstadoDaLista } from "comum/react";
import "./ListaDePontosDeApoio.css";
import type { PontoDeApoioDaLista } from "./api";
import { MudarSituacaoDoPontoDeApoio } from "./MudarSituacaoDoPontoDeApoio";

interface Props {
  pontosDeApoio: PontoDeApoioDaLista[] | null;
  podeGerenciar: boolean;
  aoMudarSituacao: () => void;
  aoIrParaTransferencia: (pontoDeApoio: PontoDeApoioDaLista) => void;
}

// O ponto de apoio sem responsável designado é informação, nunca pendência
// a resolver — a designação é ato posterior (`RF-07-49`, `RN-07-34`). O
// inativo continua na lista, distinguido do ativo por rótulo textual, nunca
// só por cor (`RN-02-09`, `RN-02-21`). Lista densa do temperamento Operação
// (documento 15 §6).
export function ListaDePontosDeApoio({
  pontosDeApoio,
  podeGerenciar,
  aoMudarSituacao,
  aoIrParaTransferencia,
}: Props) {
  if (pontosDeApoio === null) {
    return <EstadoDaLista>Carregando pontos de apoio…</EstadoDaLista>;
  }

  if (pontosDeApoio.length === 0) {
    return <EstadoDaLista>Nenhum ponto de apoio cadastrado ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-pontos-de-apoio" aria-label="Pontos de Apoio">
      {pontosDeApoio.map((pontoDeApoio) => (
        <li key={pontoDeApoio.id} className="lista-de-pontos-de-apoio__item">
          <div className="lista-de-pontos-de-apoio__linha">
            <span className="lista-de-pontos-de-apoio__nome">{pontoDeApoio.nome}</span>
            <span
              className={`lista-de-pontos-de-apoio__situacao lista-de-pontos-de-apoio__situacao--${
                pontoDeApoio.ativo ? "ativo" : "inativo"
              }`}
            >
              {pontoDeApoio.ativo ? "Ativo" : "Inativo"}
            </span>
            {pontoDeApoio.responsavel_id === null ? (
              <EstadoDaLista>Sem responsável designado.</EstadoDaLista>
            ) : (
              <span className="lista-de-pontos-de-apoio__responsavel">
                Responsável designado
              </span>
            )}
          </div>

          {podeGerenciar && (
            <MudarSituacaoDoPontoDeApoio
              idDoPontoDeApoio={pontoDeApoio.id}
              ativo={pontoDeApoio.ativo}
              onConcluido={aoMudarSituacao}
              onIrParaTransferencia={() => aoIrParaTransferencia(pontoDeApoio)}
            />
          )}
        </li>
      ))}
    </ul>
  );
}
