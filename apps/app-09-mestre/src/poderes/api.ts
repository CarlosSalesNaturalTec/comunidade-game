import { chamarNucleo } from "comum/api";

export type NaturezaDoPoder = "de_guerreiro" | "derivado_do_aporte";

export interface PoderDoCatalogo {
  id: string;
  nome: string;
  descricao: string;
  natureza: NaturezaDoPoder;
  vigencia: string;
  papel: string | null;
  ativo: boolean;
}

interface PaginaDePoderes {
  itens: PoderDoCatalogo[];
  proximo_cursor: string | null;
}

// Só para alimentar o seletor de poder da criação de trilha — a gestão
// completa do catálogo é da App 03 (`RF-09-01`).
export function listarPoderes(token: string): Promise<PaginaDePoderes> {
  return chamarNucleo<PaginaDePoderes>("/v1/poderes", { token });
}
