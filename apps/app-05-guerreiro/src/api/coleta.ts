import { chamarNucleo } from "comum/api";

export interface Pagina<T> {
  itens: T[];
  proximo_cursor: string | null;
}

export interface TipoDeColetaResumo {
  nome: string;
  forma_de_registro: "numero" | "foto" | "video";
  unidade: string | null;
}

export type EstadoDaSerie = "ativa" | "interrompida" | "encerrada";

export interface SerieDoGuerreiro {
  id: string;
  desafio_de_coleta_id: string;
  local_id: string;
  comunidade_virtual_id: string;
  cadencia: "diaria" | "semanal" | "mensal";
  estado: EstadoDaSerie;
  pontos: number;
  proxima_medicao: string | null;
  tipo_de_coleta: TipoDeColetaResumo;
}

export interface SerieAberta {
  id: string;
  desafio_de_coleta_id: string;
  coletor_id: string;
  local_id: string;
  cadencia: string;
  estado: EstadoDaSerie;
  aberta_em: string;
  ultima_medicao_valida_em: string | null;
}

export interface RegistroDoHistorico {
  id: string;
  momento_do_fato: string;
  valor: number | null;
  unidade: string | null;
  midia_referencia: string | null;
  origem: "manual" | "voz" | "sensor";
  situacao: "valida" | "invalidada";
  a_conferir: boolean;
  pontos_creditados: number;
  motivo_da_invalidacao: string | null;
}

export interface DesafioDisponivel {
  id: string;
  tipo_de_coleta: TipoDeColetaResumo;
  cadencia: "diaria" | "semanal" | "mensal";
  vigencia_inicio: string;
  vigencia_fim: string;
  granularidade_exigida: string;
  missao_id: string;
  trilha_id: string;
  ja_assumido: boolean;
  comunidade_virtual_id: string;
}

export interface Local {
  id: string;
  comunidade_virtual_id: string;
  nivel: string;
  rotulo: string;
  local_pai_id: string | null;
}

export type SituacaoDaSolicitacao = "recebida" | "aprovada" | "recusada";

export interface SolicitacaoDeLocal {
  id: string;
  solicitante_id: string;
  comunidade_virtual_id: string;
  desafio_de_coleta_id: string;
  nivel_pretendido: string;
  rotulo: string;
  justificativa: string;
  situacao: SituacaoDaSolicitacao;
  avaliador_id: string | null;
  motivo_da_recusa: string | null;
  local_criado_id: string | null;
  avaliado_em: string | null;
  registrado_em: string;
}

export interface RegistroGravado {
  id: string;
  serie_de_coleta_id: string;
  valor: number | null;
  unidade: string | null;
  origem: string;
  situacao: "valida" | "invalidada";
  a_conferir: boolean;
  comunidade_virtual_id: string;
  pontos_creditados: number;
  pontuou: boolean;
  momento_do_fato: string;
  momento_do_registro: string;
}

function comCursor(caminho: string, cursor?: string | null): string {
  return cursor ? `${caminho}?cursor=${encodeURIComponent(cursor)}` : caminho;
}

export function listarMinhasSeries(
  token: string,
  cursor?: string | null,
): Promise<Pagina<SerieDoGuerreiro>> {
  return chamarNucleo<Pagina<SerieDoGuerreiro>>(
    comCursor("/v1/series-de-coleta/minhas", cursor),
    {
      token,
    },
  );
}

export function listarHistoricoDaSerie(
  serieId: string,
  token: string,
  cursor?: string | null,
): Promise<Pagina<RegistroDoHistorico>> {
  return chamarNucleo<Pagina<RegistroDoHistorico>>(
    comCursor(`/v1/series-de-coleta/${serieId}/registros`, cursor),
    { token },
  );
}

export function listarDesafiosDisponiveis(
  token: string,
  cursor?: string | null,
): Promise<Pagina<DesafioDisponivel>> {
  return chamarNucleo<Pagina<DesafioDisponivel>>(
    comCursor("/v1/desafios-de-coleta/disponiveis", cursor),
    { token },
  );
}

// Leitura pública — sem `token` (documento 03: locais não exigem credencial
// de persona, só a chave de aplicação, que `chamarNucleo` já anexa).
export function listarLocaisDaComunidade(
  comunidadeId: string,
  cursor?: string | null,
): Promise<Pagina<Local>> {
  const base = `/v1/locais?comunidade=${encodeURIComponent(comunidadeId)}`;
  return chamarNucleo<Pagina<Local>>(
    cursor ? `${base}&cursor=${encodeURIComponent(cursor)}` : base,
  );
}

interface AbrirSerieEntrada {
  desafioDeColetaId: string;
  localId: string;
}

export function abrirSerie(entrada: AbrirSerieEntrada, token: string): Promise<SerieAberta> {
  return chamarNucleo<SerieAberta>("/v1/series-de-coleta", {
    metodo: "POST",
    corpo: {
      desafio_de_coleta_id: entrada.desafioDeColetaId,
      local_id: entrada.localId,
    },
    token,
  });
}

interface SolicitarLocalEntrada {
  comunidadeId: string;
  desafioDeColetaId: string;
  nivel: string;
  rotulo: string;
  justificativa: string;
}

export function solicitarLocal(
  entrada: SolicitarLocalEntrada,
  token: string,
): Promise<SolicitacaoDeLocal> {
  return chamarNucleo<SolicitacaoDeLocal>("/v1/solicitacoes-de-local", {
    metodo: "POST",
    corpo: {
      comunidade_id: entrada.comunidadeId,
      desafio_de_coleta_id: entrada.desafioDeColetaId,
      nivel: entrada.nivel,
      rotulo: entrada.rotulo,
      justificativa: entrada.justificativa,
    },
    token,
  });
}

export function listarMinhasSolicitacoes(
  token: string,
  cursor?: string | null,
): Promise<Pagina<SolicitacaoDeLocal>> {
  return chamarNucleo<Pagina<SolicitacaoDeLocal>>(
    comCursor("/v1/solicitacoes-de-local/minhas", cursor),
    { token },
  );
}

interface RegistrarMedicaoEntrada {
  serieId: string;
  momentoDoFato: string;
  origem: "manual" | "voz";
  valor?: number;
  unidade?: string;
  midia?: File | Blob;
}

// Sempre `multipart/form-data`: a forma `foto`/`video` do tipo de coleta
// exige a mídia como o próprio registro (`RF-05-33`, PRD-08 §9).
export function registrarMedicao(
  entrada: RegistrarMedicaoEntrada,
  token: string,
): Promise<RegistroGravado> {
  const formulario = new FormData();
  formulario.set("serie_de_coleta_id", entrada.serieId);
  formulario.set("momento_do_fato", entrada.momentoDoFato);
  formulario.set("origem", entrada.origem);
  if (entrada.valor !== undefined) formulario.set("valor", String(entrada.valor));
  if (entrada.unidade !== undefined) formulario.set("unidade", entrada.unidade);
  if (entrada.midia !== undefined) formulario.set("midia", entrada.midia);

  return chamarNucleo<RegistroGravado>("/v1/registros-de-coleta", {
    metodo: "POST",
    formulario,
    token,
  });
}
