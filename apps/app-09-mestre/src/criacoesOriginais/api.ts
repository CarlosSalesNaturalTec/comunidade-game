import { chamarNucleo } from "comum/api";

export type TipoDeProducaoDaCriacaoOriginal =
  | "texto"
  | "imagem"
  | "link_externo"
  | "video"
  | "arquivo";
export type SituacaoDaCriacaoOriginal = "entregue" | "validada" | "devolvida";

export interface AutorNaFila {
  avatar: string | null;
  nick: string;
  // `null` na modalidade individual — só a equipe tem papel por
  // integrante, fixado na homologação (`RF-09-32`).
  papel: string | null;
}

export interface CriacaoNaFila {
  id: string;
  trilha_id: string;
  trilha_nome: string;
  criterio_de_validacao: string;
  tipo: TipoDeProducaoDaCriacaoOriginal;
  producao: string | null;
  referencia: string | null;
  autores: AutorNaFila[];
}

// As criações entregues nas trilhas de que o Mestre em sessão é autor —
// nunca alcança trilha de outro Mestre (`RF-09-31`, `RF-09-32`).
export function listarFilaDeCriacoes(token: string): Promise<CriacaoNaFila[]> {
  return chamarNucleo<CriacaoNaFila[]>("/v1/criacoes/fila", { token });
}

export interface CriacaoOriginal {
  id: string;
  trilha_id: string;
  equipe_id: string | null;
  guerreiro_id: string | null;
  tipo: TipoDeProducaoDaCriacaoOriginal;
  producao: string | null;
  referencia: string | null;
  tamanho: number | null;
  situacao: SituacaoDaCriacaoOriginal;
  motivo_da_devolucao: string | null;
}

// Credita a autoria e libera o badge, saindo da fila — o núcleo faz os
// dois na mesma operação (`RF-09-31`).
export function validarCriacaoOriginal(
  idDaCriacao: string,
  token: string,
): Promise<CriacaoOriginal> {
  return chamarNucleo<CriacaoOriginal>(`/v1/criacoes/${idDaCriacao}/validacao`, {
    metodo: "POST",
    token,
  });
}

// Exige o motivo em linguagem simples — o Guerreiro(a) o lerá na App 05;
// a autoria nunca muda (`RF-09-34`, `RN-09-04`).
export function devolverCriacaoOriginal(
  idDaCriacao: string,
  motivo: string,
  token: string,
): Promise<CriacaoOriginal> {
  return chamarNucleo<CriacaoOriginal>(`/v1/criacoes/${idDaCriacao}/devolucao`, {
    metodo: "POST",
    corpo: { motivo },
    token,
  });
}
