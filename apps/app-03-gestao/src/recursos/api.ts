import { chamarNucleo } from "comum/api";

export interface TipoDeRecurso {
  id: string;
  nome: string;
  natureza: string;
  unidade: string;
  exige_comprovante: boolean;
  valor_em_moedas: string;
  vigencia_inicio: string;
}

// Rota fora do previsto na proposal desta change (design — decisão 6):
// sem ela, a homologação do aporte não teria seletor de tipo de recurso
// (`RF-02-84`).
export function listarTiposDeRecurso(token: string): Promise<TipoDeRecurso[]> {
  return chamarNucleo<TipoDeRecurso[]>("/v1/tipos-de-recurso", { token });
}
