import { Botao } from "comum/react";
import { CAMINHO_DA_SOLICITACAO_DE_DADOS } from "../navegacao/caminhos";
import type { PropsDaSecao } from "../navegacao/navegar";
import { navegarPara } from "../navegacao/navegar";

export function SecaoDeSolicitacaoDeDados({ irPara = navegarPara }: PropsDaSecao) {
  return (
    <>
      <p>
        Precisa do conjunto completo? Peça pelo formulário: a entrega é gratuita, anonimizada e
        depende de aprovação de um Admin.
      </p>
      <Botao onClick={() => irPara(CAMINHO_DA_SOLICITACAO_DE_DADOS)}>
        Pedir o conjunto de dados
      </Botao>
    </>
  );
}
