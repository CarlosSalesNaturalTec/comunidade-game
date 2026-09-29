import { chamarNucleo } from "comum/api";

/** O que o núcleo devolve ao registrar: só o protocolo e o prazo — nunca
 * dado, arquivo, chave ou acesso (`RF-03-34`, `RN-03-13`). */
export interface RegistroDaSolicitacao {
  id: string;
  prazo: string;
}

export type Pretensao = "mestre" | "apoiador";

export interface DadosDeParticipacao {
  nome_ou_razao_social: string;
  email: string;
  whatsapp: string;
  pretensao: Pretensao;
  apresentacao: string;
  instituicao?: string;
  links?: string;
}

export interface DadosDeSolicitacaoDeDados {
  solicitante: string;
  instituicao: string;
  email: string;
  finalidade_declarada: string;
  recorte_pedido: string;
}

/** Sem credencial de persona: a chamada leva só a chave da aplicação
 * (`RN-03-33`). O envio de participação é multipart, como o núcleo pede. */
export function enviarParticipacao(
  dados: DadosDeParticipacao,
): Promise<RegistroDaSolicitacao> {
  const formulario = new FormData();
  for (const [campo, valor] of Object.entries(dados)) {
    if (valor !== undefined && valor !== "") formulario.append(campo, valor);
  }
  return chamarNucleo<RegistroDaSolicitacao>("/v1/solicitacoes-de-participacao", {
    metodo: "POST",
    formulario,
  });
}

export function enviarSolicitacaoDeDados(
  dados: DadosDeSolicitacaoDeDados,
): Promise<RegistroDaSolicitacao> {
  return chamarNucleo<RegistroDaSolicitacao>("/v1/solicitacoes-de-dados", {
    metodo: "POST",
    corpo: dados,
  });
}
