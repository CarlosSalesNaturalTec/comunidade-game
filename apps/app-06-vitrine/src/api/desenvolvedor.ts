import { chamarNucleo } from "comum/api";
import type { RegistroDaSolicitacao } from "./solicitacoes";

/** Um turno da conversa. Vive só no estado da página: não vai ao
 * `localStorage`, não vai a cookie e não é gravado no núcleo (`RN-03-15`,
 * `RN-03-22`, PRD-03 §8). */
export interface MensagemDaConversa {
  de: "visitante" | "assistente";
  texto: string;
}

export interface RespostaDoAssistente {
  desfecho: "respondida" | "fora_do_corpus";
  resposta: string;
  /** Nenhuma mensagem chega sem a pergunta de múltipla escolha do próximo
   * passo (`RF-03-69`). */
  opcoes: string[];
}

/** Quantos turnos acompanham a pergunta, para o assistente aprofundar o tópico
 * escolhido (PRD-03 §5.8). O núcleo recusa acima disso. */
export const TETO_DO_HISTORICO = 6;

export function perguntarAoAssistente(
  texto: string,
  historico: MensagemDaConversa[],
): Promise<RespostaDoAssistente> {
  return chamarNucleo<RespostaDoAssistente>("/v1/assistente-do-desenvolvedor", {
    metodo: "POST",
    corpo: { texto, historico: historico.slice(-TETO_DO_HISTORICO) },
  });
}

export interface DadosDeSolicitacaoDeChave {
  solicitante: string;
  contato: string;
  o_que_pretende_construir: string;
  instituicao?: string;
}

export function enviarSolicitacaoDeChave(
  dados: DadosDeSolicitacaoDeChave,
): Promise<RegistroDaSolicitacao> {
  return chamarNucleo<RegistroDaSolicitacao>("/v1/solicitacoes-de-chave", {
    metodo: "POST",
    corpo: dados,
  });
}

/** Apresenta a URL do que foi construído. Quem prova a titularidade é o
 * **identificador** da chave, entregue na emissão — o segredo nunca é pedido
 * aqui (`RF-03-77`, `RN-01-33`). */
export function apresentarUrlDaChave(chaveId: string, url: string): Promise<void> {
  return chamarNucleo<void>(`/v1/chaves/${encodeURIComponent(chaveId)}/url`, {
    metodo: "POST",
    corpo: { url },
  });
}
