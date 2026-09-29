import { Aviso, Botao, EstadoDaLista, Moldura } from "comum/react";
import { useState } from "react";
import { URL_DA_APP_08_APOIADOR } from "../api/configuracao";
import { TextoInstitucional } from "../institucional/TextoInstitucional";
import { useConteudoInstitucional } from "../institucional/useConteudoInstitucional";
import { CAMINHO_DA_PARTICIPACAO } from "../navegacao/caminhos";
import { ListaDeNecessidades } from "../necessidades/ListaDeNecessidades";
import { MODALIDADES, type Modalidade } from "./modalidades";

interface Props {
  irPara: (destino: string) => void;
  voltar: () => void;
}

/** A porta do convite (`RF-03-42` a `RF-03-44`). É **tela da vitrine**, e não a
 * porta da App 08: é o que põe a chave PIX e as necessidades em aberto dentro
 * dela, como o `RF-03-43` exige (decisão do fundador, 2026-09-29; design —
 * decisão 1).
 *
 * O componente **não tem propriedade de origem** e o endereço não tem
 * parâmetro: nada de quem estava sendo visto chega aqui, por construção
 * (`RF-03-41`, `RN-03-25`). A modalidade escolhida vive no estado deste
 * componente e morre com ele — nada vai ao aparelho (`RF-03-38`, `RN-03-15`). */
export function PortaDoConvite({ irPara, voltar }: Props) {
  const [escolhida, definirEscolhida] = useState<string | null>(null);
  const modalidade = MODALIDADES.find((candidata) => candidata.chave === escolhida);

  return (
    <Moldura>
      <div className="cg-vitrine cg-convite">
        <h2>Quero participar</h2>
        <p>
          O apoio é ao projeto, nunca a uma pessoa: nada aqui vincula o que você traz a um
          Guerreiro, a uma Guerreira ou a uma comunidade que você viu.
        </p>

        <section>
          <h3>O que é ser Apoiador</h3>
          <p>
            O Apoiador sustenta o que a comunidade faz: <strong>aporta</strong> o que falta às
            atividades, <strong>propõe desafios extras</strong> para os Guerreiros e as
            Guerreiras e <strong>acompanha os favoritos</strong> dentro da Área do Apoiador.
          </p>
          <Aviso tipo="atencao">
            Nada aqui cria cadastro nem acesso. Quem cadastra Apoiador é um Admin, que confere
            o comprovante, em até 7 dias. A vitrine não pede senha, documento nem login.
          </Aviso>
        </section>

        <section>
          <h3>O que você traz?</h3>
          {modalidade === undefined ? (
            <ul className="cg-convite__modalidades">
              {MODALIDADES.map((candidata) => (
                <li key={candidata.chave}>
                  <Botao
                    variante="secundaria"
                    onClick={() => definirEscolhida(candidata.chave)}
                  >
                    {candidata.rotulo}
                  </Botao>
                </li>
              ))}
            </ul>
          ) : (
            <DestinoDaModalidade
              modalidade={modalidade}
              irPara={irPara}
              aoVoltar={() => definirEscolhida(null)}
            />
          )}
        </section>

        <section>
          <h3>Doar sem se cadastrar</h3>
          <ChavePix />
        </section>

        <section>
          <h3>Necessidades de recurso em aberto</h3>
          <ListaDeNecessidades />
        </section>

        <Botao variante="secundaria" onClick={voltar}>
          Não quero agora, voltar à vitrine
        </Botao>
      </div>
    </Moldura>
  );
}

/** O encaminhamento de uma modalidade: o comprobatório que ela pede e o destino
 * que já existe (`RF-03-42`). Endereço vazio da App 08 é caso previsto — o
 * destino é nomeado em texto, sem link quebrado, como no "Entrar". */
function DestinoDaModalidade({
  modalidade,
  irPara,
  aoVoltar,
}: {
  modalidade: Modalidade;
  irPara: (destino: string) => void;
  aoVoltar: () => void;
}) {
  return (
    <div className="cg-convite__destino">
      <p>
        <strong>{modalidade.rotulo}</strong> — o que comprova: {modalidade.comprobatorio}.
      </p>
      {modalidade.destino === "pre-cadastro" ? (
        <>
          <p>
            Quem aporta em dinheiro faz o pré-cadastro na Área do Apoiador, onde declara o
            aporte e anexa o comprovante. Um Admin confere, em até 7 dias.
          </p>
          {URL_DA_APP_08_APOIADOR ? (
            <p>
              <a href={URL_DA_APP_08_APOIADOR}>Ir ao pré-cadastro da Área do Apoiador</a>
            </p>
          ) : (
            <p>O endereço da Área do Apoiador ainda não foi publicado.</p>
          )}
        </>
      ) : (
        <>
          <p>
            Esse apoio entra pelo formulário de participação da vitrine, com o comprobatório
            descrito ali. Um Admin avalia, em até 7 dias.
          </p>
          <Botao onClick={() => irPara(CAMINHO_DA_PARTICIPACAO)}>
            Abrir o formulário de participação
          </Botao>
        </>
      )}
      <Botao variante="secundaria" onClick={aoVoltar}>
        Trago outra coisa
      </Botao>
    </div>
  );
}

/** A chave PIX vem do "Como apoiar" que o Admin publicou, pela leitura
 * institucional já memorizada: **nenhum valor fica escrito aqui** (`RF-03-43`,
 * `RF-03-46`; design — decisão 5). */
function ChavePix() {
  const estado = useConteudoInstitucional("como-apoiar");

  if (estado.situacao === "carregando") return <EstadoDaLista>Carregando…</EstadoDaLista>;
  if (estado.situacao === "falhou") {
    return <Aviso tipo="erro">Não foi possível carregar os canais de doação agora.</Aviso>;
  }
  if (estado.dado.texto === null) {
    return <EstadoDaLista>Os canais de doação ainda não foram publicados.</EstadoDaLista>;
  }
  return <TextoInstitucional texto={estado.dado.texto} />;
}
