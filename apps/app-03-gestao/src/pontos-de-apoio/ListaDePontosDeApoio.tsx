import { EstadoDaLista } from "comum/react";
import "./ListaDePontosDeApoio.css";
import type { PontoDeApoioDaLista } from "./api";

interface Props {
  pontosDeApoio: PontoDeApoioDaLista[] | null;
}

// O ponto de apoio sem responsável designado é informação, nunca pendência
// a resolver — a designação é ato posterior (`RF-07-49`, `RN-07-34`).
// Lista densa do temperamento Operação (documento 15 §6).
export function ListaDePontosDeApoio({ pontosDeApoio }: Props) {
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
          <span className="lista-de-pontos-de-apoio__nome">{pontoDeApoio.nome}</span>
          {pontoDeApoio.responsavel_id === null ? (
            <EstadoDaLista>Sem responsável designado.</EstadoDaLista>
          ) : (
            <span className="lista-de-pontos-de-apoio__responsavel">
              Responsável designado
            </span>
          )}
        </li>
      ))}
    </ul>
  );
}
