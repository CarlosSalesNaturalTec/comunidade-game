import type { ReactNode } from "react";
import { Icone, type NomeDeGlifo } from "./Icone";

export interface CaminhoDaTela {
  chave: string;
  /** Rótulo em **frase** — é o nome acessível do cartão, e o glifo o
   * acompanha sem tomar o lugar dele (documento 15 §5). */
  rotulo: string;
  glifo: NomeDeGlifo;
  /** O que o cartão precisa dizer abaixo do rótulo — a próxima missão, no
   * caminho da trilha da App 05 (`RF-05-08`). */
  conteudoExtra?: ReactNode;
  desabilitado?: boolean;
  aoAcionar: () => void;
}

interface Props {
  /** Dado, a lista é um marco de navegação com este nome; omitido, é só o
   * contêiner dos cartões. Nenhuma das duas telas iniciais declara marco: ali
   * os caminhos **são** a tela, e o marco não distinguiria nada. */
  rotulo?: string;
  caminhos: CaminhoDaTela[];
  /** Acrescentado ao fim da lista, dentro do contêiner — o `fieldset` "para
   * quem opera o aparelho" da App 01 entra por aqui. */
  children?: ReactNode;
}

// Os caminhos de uma tela, em cartão grande: o glifo que a criança reconhece
// antes de ler a frase inteira, e o rótulo que segue sendo o nome acessível
// do botão (documento 15 §§5, 11.1).
//
// A peça nasceu na tela inicial da App 01 e subiu para cá quando a Área do
// Guerreiro(a) passou a querer o mesmo cartão (decisão do fundador de
// 2026-10-31). O que **não** subiu é o `fieldset` "para quem opera o
// aparelho": aquele grupo é só da App 01, e entra por `children`.
//
// Há **uma** disposição, a coluna, porque é onde os caminhos são a tela
// (documento 15 §6.5). A grade e o caminho corrente existiram enquanto a Área
// do Guerreiro(a) misturava menu e conteúdo na mesma tela; separados os dois
// em telas próprias, ficaram sem objeto e saíram (decisão do fundador de
// 2026-10-31). Navegação persistente com item corrente é o `NavegacaoDeAreas`.
export function ListaDeCaminhos({ rotulo, caminhos, children }: Props) {
  const conteudo = (
    <>
      {caminhos.map((caminho) => (
        <CartaoDeCaminho key={caminho.chave} caminho={caminho} />
      ))}
      {children}
    </>
  );

  if (rotulo === undefined) {
    return <div className="cg-caminhos">{conteudo}</div>;
  }
  return (
    <nav className="cg-caminhos" aria-label={rotulo}>
      {conteudo}
    </nav>
  );
}

interface PropsDoCartao {
  caminho: CaminhoDaTela;
}

// Um cartão de caminho, exposto à parte para quem monta um grupo próprio de
// caminhos — hoje, o `fieldset` de operação da App 01.
export function CartaoDeCaminho({ caminho }: PropsDoCartao) {
  return (
    <button
      type="button"
      className="cg-caminho"
      disabled={caminho.desabilitado}
      onClick={caminho.aoAcionar}
    >
      <Icone glifo={caminho.glifo} />
      {/* O rótulo e o conteúdo extra ficam em elementos irmãos, com um espaço
          literal entre eles: sem ele o nome acessível do botão sairia grudado
          — "TrilhaMissão 3" —, porque os dois são caixas em linha e o cálculo
          do nome não inventa separador. O espaço em branco sozinho não vira
          item de flex, então não aparece na tela. */}
      <span className="cg-caminho__texto">
        <span className="cg-caminho__rotulo">{caminho.rotulo}</span>
        {caminho.conteudoExtra !== undefined && (
          <>
            {" "}
            <span className="cg-caminho__extra">{caminho.conteudoExtra}</span>
          </>
        )}
      </span>
    </button>
  );
}
