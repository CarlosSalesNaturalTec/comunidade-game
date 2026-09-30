/**
 * A navegação programática da vitrine, agora que cada tela tem arquivo
 * próprio: trocar de tela é trocar de documento.
 *
 * Existe porque **prop de função não atravessa a fronteira do Astro**: uma
 * ilha recebe props serializadas, e nenhuma delas pode ser `irPara`. Os
 * componentes seguem aceitando `irPara` — é o que mantém os testes passando o
 * seu próprio espião —, mas o valor padrão é este, e é ele que vale quando o
 * componente é montado como ilha.
 *
 * Nada é guardado no aparelho ao navegar (`RN-03-22`).
 */
export function navegarPara(destino: string): void {
  window.location.assign(destino);
}

/** Devolve o visitante à navegação de onde ele veio. Quem abriu a tela por
 * endereço direto — sem nada antes nesta aba — não tem para onde voltar, e a
 * saída é a raiz (`RF-03-44`, `RN-03-15`).
 *
 * Com arquivo por rota o histórico do navegador é real, e `history.length`
 * deixa de ser a contagem em memória que a casca antiga precisava manter. */
export function voltarOuIrParaARaiz(): void {
  if (window.history.length > 1) {
    window.history.back();
    return;
  }
  window.location.assign("/");
}

/** O que uma seção da vitrine recebe. `irPara` é opcional porque a seção é
 * montada como ilha, e ilha não recebe prop de função: sem ela, vale
 * `navegarPara`. Os testes seguem passando o seu próprio espião. */
export interface PropsDaSecao {
  irPara?: (destino: string) => void;
}
