import { chamarNucleo } from "comum/api";

export interface GuerreiroVinculado {
  id: string;
  nick: string;
  avatar: string;
  grau_de_parentesco: string;
}

// Só os vinculados por vínculo vigente, cada um com o grau de parentesco
// declarado naquele vínculo — nunca uma criança de terceiro, nem por busca
// (`RF-13-04`, `RF-13-05`, `RN-13-04`).
export function listarMeusGuerreiros(token: string): Promise<GuerreiroVinculado[]> {
  return chamarNucleo<GuerreiroVinculado[]>("/v1/eu/guerreiros", { token });
}
