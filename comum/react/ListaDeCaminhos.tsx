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

/** A disposição decide **junto** o arranjo da lista e o lugar do glifo: na
 * coluna ele fica ao lado do rótulo, na grade acima dele. É uma escolha, e
 * não duas, porque grade com glifo ao lado é justo o arranjo que não cabe em
 * duas colunas num celular de 360 px (design — decisão 1). */
export type DisposicaoDeCaminhos = "coluna" | "grade";

interface Props {
  /** Dado, a lista é um marco de navegação com este nome; omitido, é só o
   * contêiner dos cartões. A tela inicial da App 01 é a tela inteira e não
   * declara marco; os caminhos da Área do Guerreiro(a) navegam entre os
   * blocos dela e declaram. */
  rotulo?: string;
  caminhos: CaminhoDaTela[];
  disposicao?: DisposicaoDeCaminhos;
  /** A chave do caminho aberto. Dada, o cartão dela é anunciado como o atual
   * e se distingue por peso de fonte, não por cor — é o que o
   * `NavegacaoDeAreas` já faz (documento 15 §5). Omitida, nenhum cartão é o
   * atual: a tela inicial da App 01 não tem caminho aberto. */
  caminhoAtual?: string;
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
export function ListaDeCaminhos({
  rotulo,
  caminhos,
  disposicao = "coluna",
  caminhoAtual,
  children,
}: Props) {
  const classe = `cg-caminhos${disposicao === "grade" ? " cg-caminhos--grade" : ""}`;
  const conteudo = (
    <>
      {caminhos.map((caminho) => (
        <CartaoDeCaminho
          key={caminho.chave}
          caminho={caminho}
          atual={caminho.chave === caminhoAtual}
        />
      ))}
      {children}
    </>
  );

  if (rotulo === undefined) {
    return <div className={classe}>{conteudo}</div>;
  }
  return (
    <nav className={classe} aria-label={rotulo}>
      {conteudo}
    </nav>
  );
}

interface PropsDoCartao {
  caminho: CaminhoDaTela;
  atual?: boolean;
}

// Um cartão de caminho, exposto à parte para quem monta um grupo próprio de
// caminhos — hoje, o `fieldset` de operação da App 01.
export function CartaoDeCaminho({ caminho, atual = false }: PropsDoCartao) {
  return (
    <button
      type="button"
      className="cg-caminho"
      aria-current={atual ? "true" : undefined}
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
