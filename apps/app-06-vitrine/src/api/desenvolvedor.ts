import { chamarNucleo } from "comum/api";
import type { RegistroDaSolicitacao } from "./solicitacoes";

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
