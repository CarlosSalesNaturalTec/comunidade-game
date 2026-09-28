import { Moldura } from "comum/react";
import type { Recorte } from "../navegacao/recortes";

interface Props {
  recorte: Recorte;
  irPara: (destino: string) => void;
}

// As seções na ordem daquele recorte: as que já têm conteúdo o apresentam,
// e as que faltam dizem em linguagem simples o que ainda vai chegar (PRD-03
// §10). Nenhum espaço é reservado a publicidade ou patrocínio, aqui nem em
// lugar nenhum do layout (`RF-03-50`, `RN-03-21`).
export function TelaDoRecorte({ recorte, irPara }: Props) {
  return (
    <Moldura>
      <div className="cg-vitrine">
        {recorte.secoes.map((secao) => (
          <section key={secao.titulo}>
            <h2>{secao.titulo}</h2>
            {secao.Conteudo ? (
              <secao.Conteudo irPara={irPara} />
            ) : (
              <p className="cg-secao__pendente">{secao.pendente}</p>
            )}
          </section>
        ))}
      </div>
    </Moldura>
  );
}
