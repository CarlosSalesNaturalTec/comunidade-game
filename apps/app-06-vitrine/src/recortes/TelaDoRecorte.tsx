import { Moldura } from "comum/react";
import type { Recorte } from "../navegacao/recortes";

interface Props {
  recorte: Recorte;
}

// Esqueleto do recorte: as seções na ordem daquele recorte, cada uma dizendo em
// linguagem simples o que ainda vai chegar (PRD-03 §10). Nenhum espaço é
// reservado a publicidade ou patrocínio, aqui nem em lugar nenhum do layout
// (`RF-03-50`, `RN-03-21`).
export function TelaDoRecorte({ recorte }: Props) {
  return (
    <Moldura>
      <div className="cg-vitrine">
        {recorte.secoes.map((secao) => (
          <section key={secao.titulo}>
            <h2>{secao.titulo}</h2>
            <p className="cg-secao__pendente">{secao.pendente}</p>
          </section>
        ))}
      </div>
    </Moldura>
  );
}
