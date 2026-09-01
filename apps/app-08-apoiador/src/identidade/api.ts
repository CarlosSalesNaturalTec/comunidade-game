import { chamarNucleo } from "comum/api";

export interface IdentidadeDoApoiador {
  nick: string | null;
  avatar: string | null;
  moedas_acumuladas: string;
  avatar_proprio_liberado: boolean;
  moedas_faltantes_para_avatar_proprio: string | null;
}

export interface DisponibilidadeDeNick {
  disponivel: boolean;
  sugestoes: string[];
}

// A leitura da própria identidade — nick, avatar, moedas acumuladas e o que
// falta para o avatar próprio, sem valor em reais (`RF-14-15`, `RF-14-16`).
export function lerMinhaIdentidade(token: string): Promise<IdentidadeDoApoiador> {
  return chamarNucleo<IdentidadeDoApoiador>("/v1/eu/apoiador/identidade", { token });
}

export interface GravarIdentidadeEntrada {
  nick?: string;
  avatar?: string;
}

// Nick e avatar, cada um opcional, gravados juntos ou em separado a
// qualquer tempo (`RF-14-12`, `RF-14-14`, `RF-14-17`).
export function gravarMinhaIdentidade(
  entrada: GravarIdentidadeEntrada,
  token: string,
): Promise<IdentidadeDoApoiador> {
  return chamarNucleo<IdentidadeDoApoiador>("/v1/eu/apoiador/identidade", {
    metodo: "PUT",
    corpo: entrada,
    token,
  });
}

// A mesma conferência pública do pré-cadastro, restrita a nick de adulto,
// com as sugestões de variação quando já está em uso (`RF-14-13`).
export function conferirDisponibilidadeDeNick(nick: string): Promise<DisponibilidadeDeNick> {
  return chamarNucleo<DisponibilidadeDeNick>(
    `/v1/nicks/disponibilidade?nick=${encodeURIComponent(nick)}`,
  );
}
