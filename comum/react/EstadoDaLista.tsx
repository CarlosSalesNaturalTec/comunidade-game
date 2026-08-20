import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

// O estado vazio, o de carregamento e a ausência de indicadores do
// território são informação, nunca erro (`RF-08-30`, `RF-08-31`,
// `RN-08-28`) — por isso `role="status"`, nunca `role="alert"`.
export function EstadoDaLista({ children }: Props) {
  return (
    <p role="status" className="cg-estado-da-lista">
      {children}
    </p>
  );
}
