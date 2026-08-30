import { chamarNucleo } from "comum/api";

export interface IntegranteDaEquipe {
  avatar: string | null;
  nick: string;
  papel: string | null;
}

export interface Equipe {
  id: string;
  aula_id: string | null;
  trilha_id: string | null;
  homologado_por_id: string | null;
  homologado_em: string | null;
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

// `RF-04-61`: a equipe da trilha — sujeito da criação original que encerra
// a trilha (documento 02 §5). O Guerreiro(a) cria e entra como primeiro
// integrante, sem aprovação de terceiro.
export function criarEquipeDaTrilha(
  trilhaId: string,
  papel: string | null,
  token: string,
): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/trilhas/${trilhaId}/equipes`, {
    metodo: "POST",
    corpo: { papel },
    token,
  });
}

// A equipe da trilha de que o Guerreiro(a) em sessão já integra, se houver
// — 404 vira `ErroDaApi`, tratado por quem chama como "ainda não formou"
// (`RN-05-12`).
export function obterMinhaEquipeDaTrilha(trilhaId: string, token: string): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/eu/trilhas/${trilhaId}/equipe`, { token });
}

interface HomologacaoDaEquipe {
  equipe_id: string;
  homologado_por_id: string;
  homologado_em: string;
}

// `RF-04-62`: só o Mestre, sob a sessão de trabalho do aparelho — o
// `tokenDeTrabalho`, nunca o do Guerreiro(a) (`RN-04-18`).
export function homologarEquipeDaTrilha(
  equipeId: string,
  tokenDeTrabalho: string,
): Promise<HomologacaoDaEquipe> {
  return chamarNucleo<HomologacaoDaEquipe>(`/v1/equipes/${equipeId}/homologacao`, {
    metodo: "POST",
    token: tokenDeTrabalho,
  });
}
