import { chamarNucleo } from "comum/api";

export interface ArtefatoDoMestre {
  id: string;
  endereco: string;
  rotulo: string;
  declarado_no_cadastro: boolean;
}

// A leitura traz também os artefatos que o Admin declarou no cadastro,
// marcados como tais — não removíveis por aqui (`RF-09-66`, `RN-09-14`).
export function listarArtefatos(mestreId: string, token: string): Promise<ArtefatoDoMestre[]> {
  return chamarNucleo<ArtefatoDoMestre[]>(`/v1/mestres/${mestreId}/artefatos`, { token });
}

export interface DeclararArtefatoEntrada {
  endereco: string;
  rotulo: string;
}

// Link declarado — currículo, portfólio, rede social ou documento externo
// —, nunca upload de arquivo (`RF-09-66`, documento 02 §1).
export function declararArtefato(
  mestreId: string,
  entrada: DeclararArtefatoEntrada,
  token: string,
): Promise<ArtefatoDoMestre> {
  return chamarNucleo<ArtefatoDoMestre>(`/v1/mestres/${mestreId}/artefatos`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Remove apenas o que o próprio Mestre publicou — o núcleo recusa a
// remoção do que veio do cadastro (`RN-09-14`).
export function removerArtefato(
  mestreId: string,
  artefatoId: string,
  token: string,
): Promise<void> {
  return chamarNucleo<void>(`/v1/mestres/${mestreId}/artefatos/${artefatoId}`, {
    metodo: "DELETE",
    token,
  });
}
