import { chamarNucleo } from "../api/cliente";
import type { Papel } from "../api/tipos";

interface AberturaDeSessao {
  token: string;
  expira_em: string;
  papel: Papel;
}

export function loginSocial(idToken: string): Promise<AberturaDeSessao> {
  return chamarNucleo<AberturaDeSessao>("/v1/sessoes/social", {
    metodo: "POST",
    corpo: { id_token: idToken },
  });
}

export function encerrarSessao(token: string): Promise<void> {
  return chamarNucleo<void>("/v1/sessoes/atual", { metodo: "DELETE", token });
}

export interface Eu {
  persona_id: string;
  papel: Papel;
  permissoes: Record<string, string[]>;
}

export function eu(token: string): Promise<Eu> {
  return chamarNucleo<Eu>("/v1/eu", { token });
}
