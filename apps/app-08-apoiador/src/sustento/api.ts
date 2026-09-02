import { chamarNucleo } from "comum/api";

export type FamiliaDeSelo = "frente" | "modalidade" | "ato" | "multiplicacao";

export interface SeloDoApoiador {
  selo_nome: string;
  missao_do_apoiador_id: string;
  creditado_em: string;
}

export type SelosPorFamilia = Record<FamiliaDeSelo, SeloDoApoiador[]>;

export interface SustentoDoApoiador {
  nivel: number;
  nome_do_nivel: string;
  frente_que_falta: string;
  selos: SelosPorFamilia;
}

export const FAMILIAS_DE_SELO: FamiliaDeSelo[] = [
  "frente",
  "modalidade",
  "ato",
  "multiplicacao",
];

// O próprio nível de sustento, os selos agrupados por família e a frente
// que falta para o próximo nível — nunca de outro Apoiador (`RF-14-67`,
// `RF-14-68`, `RN-14-38`).
export function consultarMeuSustento(token: string): Promise<SustentoDoApoiador> {
  return chamarNucleo<SustentoDoApoiador>("/v1/eu/apoiador/sustento", { token });
}
