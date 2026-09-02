import { chamarNucleo } from "comum/api";

export type NivelDeNecessidade = "existir" | "acontecer" | "reconhecer" | "permanecer";

export interface MissaoDoApoiador {
  id: string;
  nivel_de_necessidade: NivelDeNecessidade;
  titulo: string;
  o_que_se_pede: string;
  quantidade: string;
  falta: string;
  coberto: string;
  prazo: string;
  selo_nome: string;
  selo_familia: string;
}

export type MissoesAgrupadas = Record<NivelDeNecessidade, MissaoDoApoiador[]>;

export const NIVEIS_DE_NECESSIDADE: NivelDeNecessidade[] = [
  "existir",
  "acontecer",
  "reconhecer",
  "permanecer",
];

// As missões abertas, agrupadas pelo nível de necessidade que sustentam,
// com o que falta em moedas e o coberto em quantidade — pública, sem token
// de sessão, sem identificar quem cobriu (`RF-14-60` a `RF-14-62`,
// `RF-14-71`, `RF-14-72`).
export function listarMissoesAbertas(): Promise<MissoesAgrupadas> {
  return chamarNucleo<MissoesAgrupadas>("/v1/missoes-do-apoiador");
}
