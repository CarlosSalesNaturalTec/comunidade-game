import { chamarNucleo } from "comum/api";

/** Toda leitura da vitrine passa por aqui, e por aqui **nunca** passa
 * credencial de persona: a chamada leva só a chave da aplicação, e o visitante
 * segue anônimo (`RN-03-33`). Nenhuma tela desta fatia lê dado — a função
 * existe para que as fatias seguintes não tenham onde inventar um token. */
export function lerDoNucleo<T>(caminho: string): Promise<T> {
  return chamarNucleo<T>(caminho);
}
