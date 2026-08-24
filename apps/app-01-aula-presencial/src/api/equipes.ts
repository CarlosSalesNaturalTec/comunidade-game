import { chamarNucleo } from "comum/api";

export interface IntegranteDaEquipe {
  avatar: string | null;
  nick: string;
  papel: string | null;
}

export interface Equipe {
  id: string;
  aula_id: string | null;
  integrantes: IntegranteDaEquipe[];
}

interface PaginaDeEquipes {
  itens: Equipe[];
  proximo_cursor: string | null;
}

// As quatro rotas do PRD-04 §9, todas sob a sessão do Guerreiro(a)
// (`RF-04-30` a `RF-04-34`, `RF-04-59`).

export function listarEquipesDaAula(aulaId: string, token: string): Promise<PaginaDeEquipes> {
  return chamarNucleo<PaginaDeEquipes>(`/v1/aulas/${aulaId}/equipes`, { token });
}

export function criarEquipe(
  aulaId: string,
  papel: string | null,
  token: string,
): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/aulas/${aulaId}/equipes`, {
    metodo: "POST",
    corpo: { papel },
    token,
  });
}

export function entrarNaEquipe(
  equipeId: string,
  papel: string | null,
  token: string,
): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/equipes/${equipeId}/integrantes`, {
    metodo: "POST",
    corpo: { papel },
    token,
  });
}

export function sairDaEquipe(equipeId: string, token: string): Promise<void> {
  return chamarNucleo<void>(`/v1/equipes/${equipeId}/integrantes/eu`, {
    metodo: "DELETE",
    token,
  });
}
