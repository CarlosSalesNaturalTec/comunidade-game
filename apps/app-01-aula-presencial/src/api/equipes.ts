import { chamarNucleo } from "comum/api";
import type { AtividadeDoEncontro } from "./programacao";

export interface IntegranteDaEquipe {
  avatar: string | null;
  nick: string;
  papel: string | null;
}

export interface Equipe {
  id: string;
  nome: string;
  aula_id: string | null;
  trilha_id: string | null;
  homologado_por_id: string | null;
  homologado_em: string | null;
  integrantes: IntegranteDaEquipe[];
}

// `RN-04-39`: nome obrigatório, de até 20 caracteres — o campo não deixa
// passar disso, e o núcleo confere de novo, com a unicidade.
export const TETO_DO_NOME_DA_EQUIPE = 20;

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
  nome: string,
  papel: string | null,
  token: string,
): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/aulas/${aulaId}/equipes`, {
    metodo: "POST",
    corpo: { nome, papel },
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

// `RF-04-70`: qualquer integrante troca o nome, com a mesma regra da
// criação — tamanho e unicidade são conferidos pelo núcleo (`RN-04-39`).
export function renomearEquipe(
  equipeId: string,
  nome: string,
  token: string,
): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/equipes/${equipeId}`, {
    metodo: "PATCH",
    corpo: { nome },
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
  nome: string,
  papel: string | null,
  token: string,
): Promise<Equipe> {
  return chamarNucleo<Equipe>(`/v1/trilhas/${trilhaId}/equipes`, {
    metodo: "POST",
    corpo: { nome, papel },
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

export interface AtividadeDaMinhaEquipe {
  atividade: AtividadeDoEncontro;
  missao_id: string;
  missao_titulo: string;
  trilha_id: string;
  trilha_titulo: string;
  corrente: boolean;
}

export interface MinhaEquipe extends Equipe {
  meu_papel: string | null;
  atividades: AtividadeDaMinhaEquipe[];
}

// As equipes de que o Guerreiro(a) em sessão é integrante — da aula e da
// trilha —, cada uma já com as atividades dela. É esta leitura, e não
// `GET /v1/equipes/{id}/missao`, que serve o caminho das trilhas: a lista
// das equipes da aula traz integrante só com avatar, nick e papel, por
// exigência do `RN-04-14`, e por isso esta aplicação não teria como saber
// qual das equipes é a do Guerreiro(a) (`RF-04-72`, `RF-04-35`, design —
// decisão 4).
export function listarMinhasEquipes(token: string): Promise<MinhaEquipe[]> {
  return chamarNucleo<MinhaEquipe[]>("/v1/eu/equipes", { token });
}
