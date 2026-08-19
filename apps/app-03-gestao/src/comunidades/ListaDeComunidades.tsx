import type { ComunidadeDaLista } from "./api";

interface Props {
  comunidades: ComunidadeDaLista[] | null;
}

// Comunidade abaixo do piso de coletores aparece sem os indicadores do
// território, e a ausência deles nunca é apresentada como falha
// (`RF-08-30`, `RF-08-31`, `RN-08-28`).
export function ListaDeComunidades({ comunidades }: Props) {
  if (comunidades === null) {
    return <p>Carregando comunidades…</p>;
  }

  if (comunidades.length === 0) {
    return <p>Nenhuma Comunidade Virtual cadastrada ainda.</p>;
  }

  return (
    <ul aria-label="Comunidades Virtuais">
      {comunidades.map((comunidade) => (
        <li key={comunidade.id}>
          <span>{comunidade.nome}</span> — <span>{comunidade.localizacao}</span>
          {comunidade.registros_validos === null ? (
            <p>Ainda sem indicadores do território.</p>
          ) : (
            <p>
              {comunidade.series_ativas} séries ativas · {comunidade.registros_validos}{" "}
              registros válidos
            </p>
          )}
        </li>
      ))}
    </ul>
  );
}
