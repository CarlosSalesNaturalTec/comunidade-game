import { chamarNucleo, lerArquivoDoNucleo } from "comum/api";
import type { ComprovacaoEntregue } from "../trilhas/api";

export interface RecursoFaltante {
  tipo_de_recurso_id: string;
  quantidade_declarada: string;
  quantidade_disponivel: string;
}

export interface AulaDaTurma {
  id: string;
  comunidade_virtual_id: string;
  ponto_de_apoio_id: string;
  inicio_em: string;
  fim_em: string;
  situacao: string;
  cancelamento_motivo: string | null;
  recursos_faltantes: RecursoFaltante[];
}

export type FormatoDaAtividade = "presencial" | "on_line_assincrona";

export interface AtividadeDoMestre {
  id: string;
  missao_id: string;
  titulo: string;
  formato: FormatoDaAtividade;
  modalidade: string;
  // A aula que a atividade presencial declarou, ou `null` quando ainda não
  // vinculada a encontro algum (`RF-09-42`, `RF-09-73`).
  aula_id: string | null;
}

export interface MinhasTurmas {
  itens: AulaDaTurma[];
  proximo_cursor: string | null;
  atividades_presenciais: AtividadeDoMestre[];
  atividades_on_line: AtividadeDoMestre[];
}

// Aulas das comunidades do Mestre em sessão e as atividades de que é autor,
// já separadas por formato — presencial do encontro e on-line entre
// encontros (`RF-09-42`, `RF-09-73`).
export function listarMinhasTurmas(token: string): Promise<MinhasTurmas> {
  return chamarNucleo<MinhasTurmas>("/v1/minhas-turmas", { token });
}

export type DesfechoDoResultado =
  | "realizada"
  | "realizada_com_merito"
  | "merito_extra_por_auxilio";

// As seis formas do comprovante do Resultado — a produção do Guerreiro(a)
// (`RF-09-149`, `RN-09-64`). Texto e link vão no lançamento; as quatro de
// mídia sobem antes, pelo envio retomável.
export type FormaDoComprovante =
  | "texto"
  | "imagem"
  | "audio"
  | "video"
  | "arquivo"
  | "link_externo";

export const FORMAS_EM_TEXTO: FormaDoComprovante[] = ["texto", "link_externo"];

export interface ComprovanteDoLancamento {
  tipo: FormaDoComprovante;
  texto?: string;
  envio_id?: string;
}

export interface JulgamentoNoLancamento {
  cumpriu: boolean;
  publicavel: boolean;
  motivo: string | null;
}

export interface ParticipanteDoLancamento {
  guerreiro_id: string;
  momento_do_fato: string;
  comprovante: ComprovanteDoLancamento;
  desfecho: DesfechoDoResultado;
  julgamento_do_pratico?: JulgamentoNoLancamento;
}

export interface Resultado {
  id: string;
  guerreiro_id: string;
  atividade_id: string;
  aula_id: string;
  momento_do_fato: string;
  producao: string | null;
  comprovante_tipo: FormaDoComprovante;
  desfecho: string;
}

interface LancamentoDaAtividade {
  resultados: Resultado[];
  fora_por_falta_de_presenca: string[];
}

// Um Guerreiro(a) por envio na App 09 (`RF-09-148`); a API segue aceitando a
// lista, que a App 03 usa.
export async function lancarResultadoDaAtividade(
  idDaAtividade: string,
  aulaId: string,
  participante: ParticipanteDoLancamento,
  token: string,
): Promise<Resultado> {
  const lancamento = await chamarNucleo<LancamentoDaAtividade>(
    `/v1/atividades/${idDaAtividade}/lancamentos`,
    { metodo: "POST", corpo: { aula_id: aulaId, participantes: [participante] }, token },
  );
  return lancamento.resultados[0];
}

interface EnvioDoComprovante {
  envio_id: string;
  endereco_da_sessao: string;
}

// Abre o envio do comprovante em mídia **antes** do lançamento — a lista e o
// teto são conferidos aqui, antes de qualquer byte (`RF-09-149`).
export function abrirEnvioDoComprovante(
  idDaAtividade: string,
  tipo: FormaDoComprovante,
  tipoMime: string,
  tamanhoDeclarado: number,
  token: string,
): Promise<EnvioDoComprovante> {
  return chamarNucleo<EnvioDoComprovante>(
    `/v1/atividades/${idDaAtividade}/lancamentos/comprovantes`,
    {
      metodo: "POST",
      corpo: { tipo, tipo_mime: tipoMime, tamanho_declarado: tamanhoDeclarado },
      token,
    },
  );
}

export type EstadoDoPratico = "sem_declaracao" | "aguardando" | "nao_cumpriu" | "cumpriu";

// O que a tela precisa para saber se pede o julgamento do prático
// (`RF-09-150`, `RN-09-65`).
export interface SituacaoDoPratico {
  missao_id: string;
  tipo_do_desafio: "quiz" | "pratico" | null;
  forma_aceita: FormaDoComprovante | null;
  criterio_de_aceite: string | null;
  estado: EstadoDoPratico;
  motivo_do_julgamento: string | null;
  comprovacao_entregue: ComprovacaoEntregue | null;
  exige_julgamento: boolean;
}

export function lerSituacaoDoPratico(
  idDaMissao: string,
  idDoGuerreiro: string,
  token: string,
): Promise<SituacaoDoPratico> {
  return chamarNucleo<SituacaoDoPratico>(
    `/v1/missoes/${idDaMissao}/desbloqueios/${idDoGuerreiro}`,
    { token },
  );
}

// Os resultados lançados na aula, nas atividades do Mestre (`RF-09-151`).
export interface ResultadoDaAula {
  id: string;
  guerreiro_id: string;
  nick: string | null;
  atividade_id: string;
  atividade_titulo: string;
  momento_do_fato: string;
  desfecho: DesfechoDoResultado;
  comprovante_tipo: FormaDoComprovante;
  comprovante_texto: string | null;
  tem_arquivo: boolean;
}

export function listarResultadosDaAula(
  idDaAula: string,
  token: string,
): Promise<ResultadoDaAula[]> {
  return chamarNucleo<ResultadoDaAula[]>(`/v1/aulas/${idDaAula}/resultados`, { token });
}

// Os bytes vêm do núcleo, não de `<img src>`: toda rota sob `/v1` exige a
// chave da aplicação em cabeçalho (`RF-09-151`).
export function lerComprovanteDoResultado(
  idDoResultado: string,
  token: string,
): Promise<Blob> {
  return lerArquivoDoNucleo(`/v1/resultados/${idDoResultado}/comprovante`, { token });
}

export interface Presenca {
  id: string;
  aula_id: string;
  guerreiro_id: string;
  modo: string;
  confirmador_id: string | null;
  momento_do_fato: string;
}

// Só o modo confirmação alcança o Mestre — o reconhecimento continua
// exclusivo do App 01 (`RF-09-45`).
export function confirmarPresenca(
  idDaAula: string,
  guerreiroId: string,
  momentoDoFato: string,
  token: string,
): Promise<Presenca> {
  return chamarNucleo<Presenca>(`/v1/aulas/${idDaAula}/presencas`, {
    metodo: "POST",
    corpo: { guerreiro_id: guerreiroId, modo: "confirmacao", momento_do_fato: momentoDoFato },
    token,
  });
}

export interface PresencaDaAula {
  id: string;
  guerreiro_id: string;
  nick: string | null;
  nome: string | null;
  avatar: string | null;
  momento_do_fato: string;
  modo: string;
}

interface PresencasDaAula {
  itens: PresencaDaAula[];
  proximo_cursor: string | null;
}

// Os presentes da aula — só as presenças não anuladas, por nick e avatar,
// nunca imagem real (`RF-09-145`, `RN-09-18`).
export async function listarPresencasDaAula(
  idDaAula: string,
  token: string,
): Promise<PresencaDaAula[]> {
  const pagina = await chamarNucleo<PresencasDaAula>(`/v1/aulas/${idDaAula}/presencas`, {
    token,
  });
  return pagina.itens;
}

export interface OcorrenciaDeConduta {
  id: string;
  guerreiro_id: string;
  aula_id: string;
  atividade_id: string;
  valor: number;
  motivo: string | null;
  momento_do_fato: string;
}

// O valor nunca é enviado — é fixo no núcleo — e o lançamento já vale no
// ato, sem revisão de outro Admin (`RF-09-46`, `RN-09-09`).
export function lancarOcorrenciaDeConduta(
  guerreiroId: string,
  aulaId: string,
  atividadeId: string,
  motivo: string,
  momentoDoFato: string,
  token: string,
): Promise<OcorrenciaDeConduta> {
  return chamarNucleo<OcorrenciaDeConduta>("/v1/ocorrencias-de-conduta", {
    metodo: "POST",
    corpo: {
      guerreiro_id: guerreiroId,
      aula_id: aulaId,
      atividade_id: atividadeId,
      motivo,
      momento_do_fato: momentoDoFato,
    },
    token,
  });
}
