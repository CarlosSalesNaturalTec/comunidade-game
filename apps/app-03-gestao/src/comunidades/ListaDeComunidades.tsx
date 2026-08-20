import { EstadoDaLista } from "comum/react";
import "./ListaDeComunidades.css";
import type { ComunidadeDaLista } from "./api";

interface Props {
  comunidades: ComunidadeDaLista[] | null;
}

// Comunidade abaixo do piso de coletores aparece sem os indicadores do
// território, e a ausência deles nunca é apresentada como falha
// (`RF-08-30`, `RF-08-31`, `RN-08-28`). Lista densa do temperamento
// Operação (documento 15 §6).
export function ListaDeComunidades({ comunidades }: Props) {
  if (comunidades === null) {
    return <EstadoDaLista>Carregando comunidades…</EstadoDaLista>;
  }

  if (comunidades.length === 0) {
    return <EstadoDaLista>Nenhuma Comunidade Virtual cadastrada ainda.</EstadoDaLista>;
  }

  return (
    <ul className="lista-de-comunidades" aria-label="Comunidades Virtuais">
      {comunidades.map((comunidade) => (
        <li key={comunidade.id} className="lista-de-comunidades__item">
          <span className="lista-de-comunidades__nome">{comunidade.nome}</span>
          <span className="lista-de-comunidades__localizacao">{comunidade.localizacao}</span>
          {comunidade.registros_validos === null ? (
            <EstadoDaLista>Ainda sem indicadores do território.</EstadoDaLista>
          ) : (
            <span className="lista-de-comunidades__indicadores">
              {comunidade.series_ativas} séries ativas · {comunidade.registros_validos}{" "}
              registros válidos
            </span>
          )}
        </li>
      ))}
    </ul>
  );
}
