import { chamarNucleo } from "comum/api";

export interface AtividadeDoEncontro {
  id: string;
  missao_id: string;
  titulo: string;
  descricao: string | null;
  modalidade: string;
  formato: string;
  natureza: string;
  producao_esperada: string;
  aula_id: string | null;
}

export type TipoDeConteudo = "texto" | "imagem" | "link_externo" | "video" | "arquivo";
export type AutoriaDoConteudo = "propria" | "terceiro";

export interface ConteudoDaMissao {
  id: string;
  missao_id: string;
  ordem: number;
  tipo: TipoDeConteudo;
  corpo: string | null;
  endereco: string | null;
  referencia: string | null;
  tamanho: number | null;
  autoria: AutoriaDoConteudo;
  fonte: string | null;
}

export interface BibliografiaDaMissao {
  id: string;
  missao_id: string;
  titulo: string;
  capitulo: string;
  disponivel: boolean | null;
  apoiador_nome: string | null;
}

export interface ItemDaProgramacao {
  atividade: AtividadeDoEncontro;
  missao_id: string;
  missao_titulo: string;
  trilha_id: string;
  trilha_titulo: string;
  conteudos: ConteudoDaMissao[];
  bibliografia: BibliografiaDaMissao[];
  corrente: boolean;
}

// A programação do encontro da aula da equipe — missão, conteúdo e
// bibliografia de cada atividade presencial declarada, com a escolha
// corrente já marcada (`RF-04-35`, `RF-02-42`). Lista vazia é encontro sem
// programação declarada, nunca erro (documento 05 §4).
export function obterProgramacaoDoEncontro(
  equipeId: string,
  token: string,
): Promise<ItemDaProgramacao[]> {
  return chamarNucleo<ItemDaProgramacao[]>(`/v1/equipes/${equipeId}/missao`, { token });
}

interface EscolhaDaEquipe {
  equipe_id: string;
  atividade_corrente_id: string;
}

// Declara ao núcleo a atividade da programação que a equipe escolheu —
// substitui a escolha corrente, sem acumular histórico (`RF-04-35`,
// `RF-02-42`).
export function declararEscolhaDaEquipe(
  equipeId: string,
  atividadeId: string,
  token: string,
): Promise<EscolhaDaEquipe> {
  return chamarNucleo<EscolhaDaEquipe>(`/v1/equipes/${equipeId}/atividade-corrente`, {
    metodo: "POST",
    corpo: { atividade_id: atividadeId },
    token,
  });
}
