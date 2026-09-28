import { Botao, Dialogo } from "comum/react";
import { useState } from "react";
import { type ChaveDePersona, PERSONAS, type Persona } from "./personas";

interface Props {
  aberto: boolean;
  aoFechar: () => void;
}

// A vitrine **encaminha, nunca autentica** (`RN-03-27`): o destino é um link
// para a aplicação da persona, e nenhuma tela daqui pede nick, imagem, senha ou
// login, nem confirma que uma conta existe (`RF-03-61`). A escolha vive no
// estado deste componente e morre com ele — nada vai para o aparelho
// (`RF-03-60`, `RN-03-22`).
export function DialogoDeEntrada({ aberto, aoFechar }: Props) {
  const [escolhida, definirEscolhida] = useState<ChaveDePersona | null>(null);
  const persona = PERSONAS.find((candidata) => candidata.chave === escolhida);

  function fechar() {
    definirEscolhida(null);
    aoFechar();
  }

  return (
    <Dialogo aberto={aberto} titulo="Quem está entrando?" aoFechar={fechar}>
      {persona ? (
        <DestinoDaPersona persona={persona} aoVoltar={() => definirEscolhida(null)} />
      ) : (
        <ul className="cg-entrada__personas">
          {PERSONAS.map((candidata) => (
            <li key={candidata.chave}>
              <Botao variante="secundaria" onClick={() => definirEscolhida(candidata.chave)}>
                {candidata.rotulo}
              </Botao>
            </li>
          ))}
        </ul>
      )}
    </Dialogo>
  );
}

function DestinoDaPersona({ persona, aoVoltar }: { persona: Persona; aoVoltar: () => void }) {
  const orientacao = persona.orientacaoSemCadastro;

  return (
    <div>
      <p>
        Quem confere a entrada é a {persona.nomeDoDestino} — a vitrine não pede nem confere
        senha, nick ou imagem.
      </p>
      {/* Endereço vazio é caso previsto: em vez de link quebrado, o destino é
          nomeado em texto (design — decisão 4). */}
      {persona.url ? (
        <p>
          <a href={persona.url}>Ir para a {persona.nomeDoDestino}</a>
        </p>
      ) : (
        <p>O endereço da {persona.nomeDoDestino} ainda não foi publicado.</p>
      )}
      {orientacao && (
        <div className="cg-entrada__orientacao">
          <h3>Ainda não tenho cadastro</h3>
          <p>{orientacao.texto}</p>
          {orientacao.url && orientacao.rotuloDoLink && (
            <p>
              <a href={orientacao.url}>{orientacao.rotuloDoLink}</a>
            </p>
          )}
        </div>
      )}
      <Botao variante="secundaria" onClick={aoVoltar}>
        Escolher outra pessoa
      </Botao>
    </div>
  );
}
