import { chamarNucleo } from "comum/api";

export interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

export type NivelDoLocal = "comunidade" | "bairro" | "rua" | "condominio" | "bloco" | "quadra";

export const NIVEIS_DO_LOCAL: NivelDoLocal[] = [
  "comunidade",
  "bairro",
  "rua",
  "condominio",
  "bloco",
  "quadra",
];

export interface LocalDaLista {
  id: string;
  comunidade_virtual_id: string;
  nivel: NivelDoLocal;
  rotulo: string;
  local_pai_id: string | null;
}

// A hierarquia e o seletor de local pai exigem a comunidade inteira — a
// primeira leitura da App 03 a seguir o `proximo_cursor` até o fim, em vez
// de ler só a primeira página (design — decisão 7, riscos).
export async function listarTodosOsLocais(comunidadeId: string): Promise<LocalDaLista[]> {
  const locais: LocalDaLista[] = [];
  let cursor: string | null = null;
  do {
    const consulta = new URLSearchParams({ comunidade: comunidadeId });
    if (cursor) consulta.set("cursor", cursor);
    const pagina: Pagina<LocalDaLista> = await chamarNucleo<Pagina<LocalDaLista>>(
      `/v1/locais?${consulta.toString()}`,
    );
    locais.push(...pagina.itens);
    cursor = pagina.proximo_cursor;
  } while (cursor);
  return locais;
}

export interface CadastrarLocalEntrada {
  comunidade_id: string;
  nivel: NivelDoLocal;
  rotulo: string;
  local_pai_id?: string;
}

export function cadastrarLocal(
  entrada: CadastrarLocalEntrada,
  token: string,
): Promise<LocalDaLista> {
  return chamarNucleo<LocalDaLista>("/v1/locais", { metodo: "POST", corpo: entrada, token });
}

export type SituacaoDaSolicitacaoDeLocal = "recebida" | "aprovada" | "recusada";

export interface SolicitacaoDeLocalDaLista {
  id: string;
  solicitante_id: string;
  comunidade_virtual_id: string;
  desafio_de_coleta_id: string;
  nivel_pretendido: NivelDoLocal;
  rotulo: string;
  justificativa: string;
  situacao: SituacaoDaSolicitacaoDeLocal;
  avaliador_id: string | null;
  motivo_da_recusa: string | null;
  local_criado_id: string | null;
  avaliado_em: string | null;
  registrado_em: string;
}

export function listarSolicitacoesDeLocalAbertas(
  comunidadeId: string,
  token: string,
): Promise<Pagina<SolicitacaoDeLocalDaLista>> {
  const consulta = new URLSearchParams({ comunidade: comunidadeId });
  return chamarNucleo<Pagina<SolicitacaoDeLocalDaLista>>(
    `/v1/solicitacoes-de-local/abertas?${consulta.toString()}`,
    { token },
  );
}

export interface AvaliarSolicitacaoDeLocalEntrada {
  situacao: "aprovada" | "recusada";
  local_pai_id?: string;
  motivo?: string;
}

export function avaliarSolicitacaoDeLocal(
  idDaSolicitacao: string,
  entrada: AvaliarSolicitacaoDeLocalEntrada,
  token: string,
): Promise<SolicitacaoDeLocalDaLista> {
  return chamarNucleo<SolicitacaoDeLocalDaLista>(
    `/v1/solicitacoes-de-local/${idDaSolicitacao}/avaliacao`,
    { metodo: "POST", corpo: entrada, token },
  );
}

export interface TipoDeColetaResumo {
  nome: string;
  forma_de_registro: "numero" | "foto" | "video";
  unidade: string | null;
}

export interface DesafioPublicadoDaLista {
  id: string;
  missao_id: string;
  trilha_id: string;
  tipo_de_coleta: TipoDeColetaResumo;
  cadencia: "diaria" | "semanal" | "mensal";
  vigencia_inicio: string;
  vigencia_fim: string;
  granularidade_exigida: NivelDoLocal;
  quantidade_de_series_ativas: number;
}

export function listarDesafiosDeColetaPublicados(
  token: string,
): Promise<Pagina<DesafioPublicadoDaLista>> {
  return chamarNucleo<Pagina<DesafioPublicadoDaLista>>("/v1/desafios-de-coleta", { token });
}
