import { chamarNucleo } from "comum/api";

export interface IdentidadeDoMestre {
  nick: string | null;
  avatar: string | null;
}

// A leitura da própria identidade — nick e avatar vigentes, sem dado de
// moeda, que é regra de marca do Apoiador (`RF-09-114`).
export function lerIdentidade(token: string): Promise<IdentidadeDoMestre> {
  return chamarNucleo<IdentidadeDoMestre>("/v1/eu/mestre/identidade", { token });
}

export interface GravarIdentidadeEntrada {
  nick?: string;
  avatar?: string;
}

// Nick e avatar, cada um opcional, gravados juntos ou em separado a
// qualquer tempo — sem piso de moeda alguma (`RF-09-114`, `RN-14-10`).
export function gravarIdentidade(
  entrada: GravarIdentidadeEntrada,
  token: string,
): Promise<IdentidadeDoMestre> {
  return chamarNucleo<IdentidadeDoMestre>("/v1/eu/mestre/identidade", {
    metodo: "PUT",
    corpo: entrada,
    token,
  });
}

export interface DisponibilidadeDeNick {
  disponivel: boolean;
  sugestoes: string[];
}

// A mesma conferência restrita a nick de adulto que a App 08 usa
// (`RF-14-13`, `RN-01-22`).
export function conferirDisponibilidadeDeNick(nick: string): Promise<DisponibilidadeDeNick> {
  return chamarNucleo<DisponibilidadeDeNick>(
    `/v1/nicks/disponibilidade?nick=${encodeURIComponent(nick)}`,
  );
}

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

// Corrige rótulo e endereço de um artefato do próprio perfil, o declarado
// no cadastro incluído — que segue sem caminho de remoção por aqui
// (`RF-09-66`, `RN-09-14`).
export function editarArtefato(
  mestreId: string,
  artefatoId: string,
  entrada: DeclararArtefatoEntrada,
  token: string,
): Promise<ArtefatoDoMestre> {
  return chamarNucleo<ArtefatoDoMestre>(`/v1/mestres/${mestreId}/artefatos/${artefatoId}`, {
    metodo: "PATCH",
    corpo: entrada,
    token,
  });
}
