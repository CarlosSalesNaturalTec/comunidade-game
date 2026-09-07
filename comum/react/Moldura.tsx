import type { ElementType, ReactNode } from "react";

interface Props {
  children: ReactNode;
  as?: ElementType;
  /** `leitura` (padrão) é a largura de 64 caracteres do texto corrido;
   * `densa` é a largura de área densa, para tela com tabela ou painel
   * (documento 15 §4, design — decisão 5). */
  variante?: "leitura" | "densa";
}

// Limita a linha de texto corrido à largura de leitura do documento 15 §4
// (requisito "O texto respeita a largura de leitura e o corpo mínimo"); a
// variante `densa` troca essa largura pela de área densa.
export function Moldura({ children, as: Tag = "main", variante = "leitura" }: Props) {
  return <Tag className={`cg-moldura cg-moldura--${variante}`}>{children}</Tag>;
}
