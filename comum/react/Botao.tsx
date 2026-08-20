import type { MouseEventHandler, ReactNode } from "react";

interface Props {
  children: ReactNode;
  onClick?: MouseEventHandler<HTMLButtonElement>;
  tipo?: "button" | "submit";
  variante?: "primaria" | "secundaria";
  desabilitado?: boolean;
}

// Alvo de toque de ao menos 48 px e separação de ao menos 8 px de um Botao
// vizinho são garantidos pela própria classe — quem usa não precisa lembrar
// (documento 15 §5, requisito "Todo elemento acionável cumpre o alvo de
// toque e mostra o foco").
export function Botao({
  children,
  onClick,
  tipo = "button",
  variante = "primaria",
  desabilitado = false,
}: Props) {
  return (
    <button
      type={tipo}
      onClick={onClick}
      disabled={desabilitado}
      className={`cg-botao cg-botao--${variante}`}
    >
      {children}
    </button>
  );
}
