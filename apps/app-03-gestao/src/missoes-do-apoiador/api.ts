import { chamarNucleo } from "comum/api";

export type NivelDeNecessidade = "existir" | "acontecer" | "reconhecer" | "permanecer";
export type FamiliaDeSelo = "frente" | "modalidade" | "ato" | "multiplicacao";
export type SituacaoDaMissao = "aberta" | "concluida" | "despublicada";

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
  selo_familia: FamiliaDeSelo;
  situacao: SituacaoDaMissao;
  vencida: boolean;
}

export interface PublicarMissaoEntrada {
  aulaId: string;
  tipoDeRecursoId: string;
  nivelDeNecessidade: NivelDeNecessidade;
  titulo: string;
  oQueSePede: string;
  quantidade: string;
  prazo: string;
  seloNome: string;
  seloFamilia: FamiliaDeSelo;
}

// Publica a missão a partir de uma necessidade de recurso em aberto — só
// Admin (`RF-02-102`, `RF-02-103`, `RN-02-31`).
export function publicarMissao(
  entrada: PublicarMissaoEntrada,
  token: string,
): Promise<MissaoDoApoiador> {
  return chamarNucleo<MissaoDoApoiador>("/v1/missoes-do-apoiador", {
    metodo: "POST",
    corpo: {
      aula_id: entrada.aulaId,
      tipo_de_recurso_id: entrada.tipoDeRecursoId,
      nivel_de_necessidade: entrada.nivelDeNecessidade,
      titulo: entrada.titulo,
      o_que_se_pede: entrada.oQueSePede,
      quantidade: entrada.quantidade,
      prazo: entrada.prazo,
      selo_nome: entrada.seloNome,
      selo_familia: entrada.seloFamilia,
    },
    token,
  });
}

// As missões publicadas em qualquer situação, com o coberto, o que falta e
// a situação (`RF-02-104`).
export function listarMissoes(token: string): Promise<MissaoDoApoiador[]> {
  return chamarNucleo<MissaoDoApoiador[]>("/v1/missoes-do-apoiador", { token });
}

// Despublica a missão publicada por engano, sem estornar aporte já
// homologado (`RF-02-105`).
export function despublicarMissao(id: string, token: string): Promise<MissaoDoApoiador> {
  return chamarNucleo<MissaoDoApoiador>(`/v1/missoes-do-apoiador/${id}/despublicacao`, {
    metodo: "POST",
    token,
  });
}
