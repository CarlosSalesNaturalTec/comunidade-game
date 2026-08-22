export type Papel = "admin" | "mestre" | "guerreiro" | "responsavel" | "apoiador";

export interface CorpoDeErro {
  codigo: string;
  mensagem: string;
  campo?: string;
}
