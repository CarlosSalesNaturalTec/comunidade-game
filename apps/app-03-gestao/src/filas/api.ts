import { chamarNucleo } from "../api/cliente";

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
