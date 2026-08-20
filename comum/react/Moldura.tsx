import type { ElementType, ReactNode } from "react";

interface Props {
  children: ReactNode;
  as?: ElementType;
}

// Limita a linha de texto corrido à largura de leitura do documento 15 §4
// (requisito "O texto respeita a largura de leitura e o corpo mínimo").
export function Moldura({ children, as: Tag = "main" }: Props) {
  return <Tag className="cg-moldura">{children}</Tag>;
}
