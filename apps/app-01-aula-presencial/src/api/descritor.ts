import { chamarNucleo } from "comum/api";

export interface DescritorGravado {
  guerreiro_id: string;
  gravado_em: string;
}

interface GravarDescritorEntrada {
  descritor: number[];
}

// Só o descritor viaja — nunca a fotografia (`RF-04-14`, `RF-04-48`,
// `RN-04-12`, documento 03 §3.3). Recusada sem consentimento de biometria
// vigente: o núcleo responde 422 (`RN-01-17`).
export function enviarDescritor(
  guerreiroId: string,
  entrada: GravarDescritorEntrada,
  tokenDeTrabalho: string,
): Promise<DescritorGravado> {
  return chamarNucleo<DescritorGravado>(`/v1/guerreiros/${guerreiroId}/descritor`, {
    metodo: "POST",
    corpo: entrada,
    token: tokenDeTrabalho,
  });
}
