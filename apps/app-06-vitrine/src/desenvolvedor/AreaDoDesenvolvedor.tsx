import { Aviso, Botao, Moldura } from "comum/react";
import { CAMINHO_DA_APRESENTACAO_DA_URL } from "../navegacao/caminhos";
import { ChatDoDesenvolvedor } from "./ChatDoDesenvolvedor";
import { URL_DA_DOCUMENTACAO, URL_DO_REPOSITORIO } from "./enderecos";
import { FormularioDeChave } from "./FormularioDeChave";

interface Props {
  irPara: (destino: string) => void;
}

/** Área do Apoiador Desenvolvedor: **seção da vitrine**, pública e sem login,
 * nunca uma nona aplicação (`RN-03-29`). Reúne as quatro coisas do `RF-03-67`
 * — assistente, documentação, formulário de chave e repositório —, os dois
 * prazos (`RF-03-75`) e o que a chave é e não é (`RF-03-76`).
 *
 * As quatro partes são independentes: o assistente fora do ar não derruba
 * nenhuma das outras três (`RF-03-72`). */
export function AreaDoDesenvolvedor({ irPara }: Props) {
  return (
    <Moldura>
      <div className="cg-vitrine">
        <Botao variante="secundaria" onClick={() => irPara("/")}>
          Voltar à vitrine
        </Botao>
        <h2>Área do Apoiador Desenvolvedor</h2>
        <p>
          Quer construir um jogo ou uma aplicação sobre a API do Comunidade Game? Esta é a
          porta. Converse com o assistente, leia a documentação, veja o código e peça a sua
          chave.
        </p>

        <Aviso tipo="atencao">
          <strong>Sem chave a API não responde.</strong> E a chave não amplia direito nenhum: o
          contrato é de <strong>somente leitura</strong>, igual para toda aplicação de terceiro
          — nada que você construir escreve no domínio.
        </Aviso>

        <ChatDoDesenvolvedor />

        <section aria-labelledby="cg-portas-do-desenvolvedor">
          <h3 id="cg-portas-do-desenvolvedor">Documentação e código</h3>
          <ul>
            <li>
              <a href={URL_DA_DOCUMENTACAO} target="_blank" rel="noreferrer">
                Documentação da plataforma
              </a>
            </li>
            <li>
              <a href={URL_DO_REPOSITORIO} target="_blank" rel="noreferrer">
                Repositório no GitHub
              </a>
            </li>
          </ul>
        </section>

        <FormularioDeChave />

        <section aria-labelledby="cg-prazos-do-desenvolvedor">
          <h3 id="cg-prazos-do-desenvolvedor">Os dois prazos</h3>
          <ul>
            <li>
              <strong>7 dias</strong> para a gestão responder ao seu pedido de chave.
            </li>
            <li>
              <strong>30 dias</strong>, contados da emissão, para apresentar a URL do que você
              construiu. Sem a apresentação no prazo a chave é revogada — e pedir outra é
              sempre possível.
            </li>
          </ul>
          <Botao variante="secundaria" onClick={() => irPara(CAMINHO_DA_APRESENTACAO_DA_URL)}>
            Já tenho a chave: apresentar a URL
          </Botao>
        </section>
      </div>
    </Moldura>
  );
}
