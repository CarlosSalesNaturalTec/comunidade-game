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
