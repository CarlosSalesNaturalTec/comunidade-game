import { chamarNucleo, configurarAcessoAoNucleo } from "comum/api";
import { CHAVE_DE_APLICACAO, URL_DO_NUCLEO } from "./configuracao";

let configurado = false;

/**
 * A App 06 é Astro, e **não tem `main.tsx`** onde configurar o acesso uma vez
 * antes de renderizar — é o que as outras sete aplicações fazem. Aqui cada
 * seção que lê dado é **ilha**, hidratada por conta própria, e a ordem entre
 * ilhas não é contratual: configurar numa delas deixaria as demais na corrida.
 *
 * Então configura-se no gargalo por onde toda leitura já passa. Idempotente: a
 * primeira leitura configura, as demais encontram feito (design — decisão 1).
 *
 * Serve ao navegador e ao `astro build`: `src/build/dados.ts` chama a mesma
 * função, para que os dois lados não tenham duas cópias que possam divergir.
 */
export function configurarAcessoUmaVez(): void {
  if (configurado) return;
  configurarAcessoAoNucleo({
    chaveDeAplicacao: CHAVE_DE_APLICACAO,
    urlDoNucleo: URL_DO_NUCLEO,
  });
  configurado = true;
}

/** Toda leitura da vitrine passa por aqui, e por aqui **nunca** passa
 * credencial de persona: a chamada leva só a chave da aplicação, e o visitante
 * segue anônimo (`RN-03-33`). */
export function lerDoNucleo<T>(caminho: string): Promise<T> {
  configurarAcessoUmaVez();
  return chamarNucleo<T>(caminho);
}
