import type { ReactNode } from "react";

export type TipoDeAviso = "erro" | "atencao" | "sucesso" | "andamento";

interface Props {
  tipo: TipoDeAviso;
  children: ReactNode;
}

const ROTULO: Record<TipoDeAviso, string> = {
  erro: "Erro:",
  atencao: "Atenção:",
  sucesso: "Sucesso:",
  andamento: "Em andamento:",
};

// Erro e recusa interrompem (`role="alert"`); andamento e sucesso apenas
// informam (`role="status"`) — cada aviso leva rótulo textual que o
// identifica sem depender da cor (documento 15 §5, requisitos "Nenhum
// estado se comunica apenas por cor").
const PAPEL: Record<TipoDeAviso, "alert" | "status"> = {
  erro: "alert",
  atencao: "alert",
  sucesso: "status",
  andamento: "status",
};

export function Aviso({ tipo, children }: Props) {
  return (
    <p role={PAPEL[tipo]} className={`cg-aviso cg-aviso--${tipo}`}>
      <span className="cg-aviso__rotulo">{ROTULO[tipo]}</span> {children}
    </p>
  );
}
