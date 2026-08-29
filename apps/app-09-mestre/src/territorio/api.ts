import { chamarNucleo } from "comum/api";

export interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

export interface ComunidadeDaLista {
  id: string;
  nome: string;
}

interface ListaDeComunidades {
  itens: ComunidadeDaLista[];
  proximo_cursor: string | null;
  ciclo_rotulo: string;
}

// Pública, a mesma leitura que a vitrine já usa — a trilha do Mestre é bem
// comum e atravessa todas as comunidades, sem seletor (`RN-01-42`, design —
// decisão 4).
export function listarComunidades(): Promise<ListaDeComunidades> {
  return chamarNucleo<ListaDeComunidades>("/v1/comunidades");
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

// A hierarquia da comunidade inteira, para o seletor do local pai da
// aprovação — a primeira leitura a seguir o `proximo_cursor` até o fim, no
// mesmo molde da App 03.
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

// O núcleo já recorta pelas trilhas do Mestre em sessão — o que sai daqui é
// só das trilhas dele, nunca de trilha alheia (`RF-08-23`, design — decisão
// 4).
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

interface SolicitacoesPorComunidade {
  comunidade: ComunidadeDaLista;
  solicitacoes: SolicitacaoDeLocalDaLista[];
}

// A varredura do alerta (`RF-09-54`): sem comunidade a filtrar — a trilha é
// bem comum —, a App 09 lê a lista pública de comunidades e soma as em
// aberto de cada uma; a primeira página de cada comunidade já basta no
// Ciclo 01 (design — Risks). Usada tanto pelo alerta na navegação quanto
// pela área de território, para as duas nunca divergirem.
export async function listarSolicitacoesAbertasDeTodasAsComunidades(
  token: string,
): Promise<SolicitacoesPorComunidade[]> {
  const { itens: comunidades } = await listarComunidades();
  const porComunidade = await Promise.all(
    comunidades.map(async (comunidade) => {
      const pagina = await listarSolicitacoesDeLocalAbertas(comunidade.id, token);
      return { comunidade, solicitacoes: pagina.itens };
    }),
  );
  return porComunidade.filter((entrada) => entrada.solicitacoes.length > 0);
}
