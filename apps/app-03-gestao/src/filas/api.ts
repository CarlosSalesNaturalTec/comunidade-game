import { chamarNucleo } from "comum/api";

export type PretensaoDeParticipacao = "mestre" | "apoiador";

export interface SolicitacaoDeParticipacao {
  id: string;
  nome_ou_razao_social: string;
  email: string;
  whatsapp: string;
  pretensao: PretensaoDeParticipacao;
  apresentacao: string;
  instituicao: string | null;
  links: string | null;
  situacao: "recebida" | "em_avaliacao" | "aceita" | "recusada";
  prazo: string;
  em_atraso: boolean;
  avaliado_por_id: string | null;
  parecer: string | null;
  decidido_em: string | null;
  nick: string | null;
  aporte_declarado: string | null;
  comprovante_anexado: boolean;
}

interface ListaDeSolicitacoesDeParticipacao {
  itens: SolicitacaoDeParticipacao[];
  proximo_cursor: string | null;
}

export function listarSolicitacoesDeParticipacao(
  token: string,
): Promise<ListaDeSolicitacoesDeParticipacao> {
  return chamarNucleo<ListaDeSolicitacoesDeParticipacao>("/v1/solicitacoes-de-participacao", {
    token,
  });
}

export interface AvaliarSolicitacaoDeParticipacaoEntrada {
  situacao: "aceita" | "recusada";
  parecer?: string;
}

export function avaliarSolicitacaoDeParticipacao(
  idDaSolicitacao: string,
  entrada: AvaliarSolicitacaoDeParticipacaoEntrada,
  token: string,
): Promise<SolicitacaoDeParticipacao> {
  return chamarNucleo<SolicitacaoDeParticipacao>(
    `/v1/solicitacoes-de-participacao/${idDaSolicitacao}/avaliacao`,
    { metodo: "POST", corpo: entrada, token },
  );
}

export interface SolicitacaoDeDados {
  id: string;
  solicitante: string;
  instituicao: string;
  finalidade_declarada: string;
  recorte_pedido: string;
  situacao: "recebida" | "em_avaliacao" | "aceita" | "recusada";
  prazo: string;
  em_atraso: boolean;
  avaliado_por_id: string | null;
  parecer: string | null;
  decidido_em: string | null;
  entregue: string | null;
}

interface ListaDeSolicitacoesDeDados {
  itens: SolicitacaoDeDados[];
  proximo_cursor: string | null;
}

export function listarSolicitacoesDeDados(token: string): Promise<ListaDeSolicitacoesDeDados> {
  return chamarNucleo<ListaDeSolicitacoesDeDados>("/v1/solicitacoes-de-dados", { token });
}

export interface AvaliarSolicitacaoDeDadosEntrada {
  situacao: "aceita" | "recusada";
  parecer: string;
  compromisso_de_nao_reidentificar?: boolean;
  entregue?: string;
}

export function avaliarSolicitacaoDeDados(
  idDaSolicitacao: string,
  entrada: AvaliarSolicitacaoDeDadosEntrada,
  token: string,
): Promise<SolicitacaoDeDados> {
  return chamarNucleo<SolicitacaoDeDados>(
    `/v1/solicitacoes-de-dados/${idDaSolicitacao}/avaliacao`,
    { metodo: "POST", corpo: entrada, token },
  );
}

export interface SolicitacaoDeChave {
  id: string;
  solicitante: string;
  contato: string;
  instituicao: string | null;
  o_que_pretende_construir: string;
  situacao: "recebida" | "em_avaliacao" | "aceita" | "recusada";
  prazo: string;
  em_atraso: boolean;
  avaliado_por_id: string | null;
  parecer: string | null;
  decidido_em: string | null;
  chave_emitida: boolean;
}

interface ListaDeSolicitacoesDeChave {
  itens: SolicitacaoDeChave[];
  proximo_cursor: string | null;
}

export function listarSolicitacoesDeChave(token: string): Promise<ListaDeSolicitacoesDeChave> {
  return chamarNucleo<ListaDeSolicitacoesDeChave>("/v1/solicitacoes-de-chave", { token });
}

export interface AvaliarSolicitacaoDeChaveEntrada {
  situacao: "aceita" | "recusada";
  parecer?: string;
}

export function avaliarSolicitacaoDeChave(
  idDaSolicitacao: string,
  entrada: AvaliarSolicitacaoDeChaveEntrada,
  token: string,
): Promise<SolicitacaoDeChave> {
  return chamarNucleo<SolicitacaoDeChave>(
    `/v1/solicitacoes-de-chave/${idDaSolicitacao}/avaliacao`,
    { metodo: "POST", corpo: entrada, token },
  );
}

export type TipoDeSolicitacaoDoResponsavel =
  | "acesso"
  | "correcao"
  | "exclusao"
  | "esclarecimento";

export interface SolicitacaoDoResponsavel {
  id: string;
  responsavel_id: string;
  nick_do_responsavel: string | null;
  guerreiro_id: string;
  nick_do_guerreiro: string | null;
  tipo: TipoDeSolicitacaoDoResponsavel;
  texto: string;
  situacao: "recebida" | "em_avaliacao" | "aceita" | "recusada";
  prazo: string;
  em_atraso: boolean;
  tratado_por_id: string | null;
  desfecho: string | null;
  tratado_em: string | null;
}

export function listarSolicitacoesDoResponsavel(
  token: string,
): Promise<SolicitacaoDoResponsavel[]> {
  return chamarNucleo<SolicitacaoDoResponsavel[]>("/v1/solicitacoes-do-responsavel", {
    token,
  });
}

export interface TratarSolicitacaoDoResponsavelEntrada {
  situacao: "aceita" | "recusada";
  desfecho?: string;
}

export function tratarSolicitacaoDoResponsavel(
  idDaSolicitacao: string,
  entrada: TratarSolicitacaoDoResponsavelEntrada,
  token: string,
): Promise<SolicitacaoDoResponsavel> {
  return chamarNucleo<SolicitacaoDoResponsavel>(
    `/v1/solicitacoes-do-responsavel/${idDaSolicitacao}/tratamento`,
    { metodo: "POST", corpo: entrada, token },
  );
}

export interface Sugestao {
  id: string;
  autor_id: string;
  papel_do_autor: string;
  alvo_tipo: "atividade" | "trilha" | "plataforma";
  alvo_id: string | null;
  texto: string;
  situacao: "recebida" | "em_avaliacao" | "adotada" | "nao_adotada";
  prazo: string;
  em_atraso: boolean;
  avaliado_por_id: string | null;
  parecer: string | null;
  motivo_do_retorno: string | null;
  decidido_em: string | null;
}

interface ListaDeSugestoes {
  itens: Sugestao[];
  proximo_cursor: string | null;
}

export function listarSugestoes(token: string): Promise<ListaDeSugestoes> {
  return chamarNucleo<ListaDeSugestoes>("/v1/sugestoes", { token });
}

export interface AvaliarSugestaoEntrada {
  situacao: "adotada" | "nao_adotada";
  parecer?: string;
  motivo_do_retorno?: string;
}

export function avaliarSugestao(
  idDaSugestao: string,
  entrada: AvaliarSugestaoEntrada,
  token: string,
): Promise<Sugestao> {
  return chamarNucleo<Sugestao>(`/v1/sugestoes/${idDaSugestao}/avaliacao`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

export type ModalidadeDoDesafioExtra = "aberto" | "direcionado";
export type FormatoDoDesafioExtra = "presencial" | "on_line";
export type CusteioDoDesafioExtra = "aporte_do_proponente" | "saldo_de_recurso";
export type SituacaoDoDesafioExtra =
  | "em_validacao_do_mestre"
  | "em_aprovacao_do_admin"
  | "publicado"
  | "recusado";

export interface DesafioExtra {
  id: string;
  trilha_id: string;
  missao_id: string | null;
  modalidade: ModalidadeDoDesafioExtra;
  nick_do_destinatario: string | null;
  justificativa_do_vinculo: string | null;
  tipo_de_recurso_id: string;
  ponto_de_apoio_id: string;
  quantidade_disponivel: number;
  quantidade_restante: number;
  criterio_de_atribuicao: string;
  pontos_extras: number;
  formato: FormatoDoDesafioExtra;
  custeio: CusteioDoDesafioExtra;
  aporte_id: string | null;
  vigencia_inicio: string;
  vigencia_fim: string;
  situacao: SituacaoDoDesafioExtra;
  motivo_da_recusa: string | null;
  lastro_provido: boolean;
  lastro_faltante: string | null;
  admin_encerrador_id: string | null;
  encerrado_em: string | null;
}

// A fila do Admin: só os desafios já validados pelo Mestre da trilha
// (`RF-02-27`, `RN-02-10`).
export function listarDesafiosExtrasPendentes(token: string): Promise<DesafioExtra[]> {
  return chamarNucleo<DesafioExtra[]>("/v1/desafios-extras/pendentes", { token });
}

// Os desafios publicados, com a quantidade restante, para o encerramento
// (`RF-02-106`).
export function listarDesafiosExtrasPublicados(token: string): Promise<DesafioExtra[]> {
  return chamarNucleo<DesafioExtra[]>("/v1/desafios-extras/publicados", { token });
}

export interface AvaliarDesafioExtraEntrada {
  situacao: "publicado" | "recusado";
  motivo?: string;
}

// A aprovação publica o desafio e reserva a recompensa; a recusa exige
// motivo e não grava reserva alguma (`RF-02-28`, `RN-02-10`, `RN-02-11`).
export function avaliarDesafioExtra(
  idDoDesafio: string,
  entrada: AvaliarDesafioExtraEntrada,
  token: string,
): Promise<DesafioExtra> {
  return chamarNucleo<DesafioExtra>(`/v1/desafios-extras/${idDoDesafio}/aprovacao`, {
    metodo: "POST",
    corpo: entrada,
    token,
  });
}

// Fecha o desafio publicado e libera a reserva da recompensa não entregue
// (`RF-02-106`, `RF-07-40`).
export function encerrarDesafioExtra(
  idDoDesafio: string,
  token: string,
): Promise<DesafioExtra> {
  return chamarNucleo<DesafioExtra>(`/v1/desafios-extras/${idDoDesafio}/encerramento`, {
    metodo: "POST",
    token,
  });
}
