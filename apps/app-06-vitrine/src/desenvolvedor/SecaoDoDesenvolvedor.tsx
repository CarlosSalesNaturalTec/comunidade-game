import { Botao } from "comum/react";
import { CAMINHO_DA_AREA_DO_DESENVOLVEDOR } from "../navegacao/caminhos";
import type { PropsDaSecao } from "../navegacao/navegar";
import { navegarPara } from "../navegacao/navegar";

/** A porta da área dentro da vitrine — é assim que ela é **seção**, e não uma
 * nona aplicação (`RF-03-67`, `RN-03-29`). */
export function SecaoDoDesenvolvedor({ irPara = navegarPara }: PropsDaSecao) {
  return (
    <>
      <p>
        Quer construir um jogo ou uma aplicação sobre a API? A área reúne o assistente que
        explica a arquitetura, a documentação, o repositório e o formulário para pedir a sua
        chave.
      </p>
      <Botao onClick={() => irPara(CAMINHO_DA_AREA_DO_DESENVOLVEDOR)}>
        Abrir a Área do Apoiador Desenvolvedor
      </Botao>
    </>
  );
}
