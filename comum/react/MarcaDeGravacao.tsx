interface Props {
  instante: Date | null;
}

function formatarHora(data: Date): string {
  const horas = String(data.getHours()).padStart(2, "0");
  const minutos = String(data.getMinutes()).padStart(2, "0");
  return `${horas}h${minutos}`;
}

// Apresentação pura: recebe o instante da última gravação e o formata —
// quem grava é dono do instante (design — decisão 5). Instante nulo é
// bloco que ainda não gravou nada, e não apresenta marca (documento 15
// §6.2).
export function MarcaDeGravacao({ instante }: Props) {
  if (!instante) return null;
  return <p className="cg-marca-de-gravacao">{`Salvo às ${formatarHora(instante)}`}</p>;
}
