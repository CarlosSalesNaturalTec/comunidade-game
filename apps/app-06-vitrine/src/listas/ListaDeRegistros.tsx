import { Avatar } from "comum/avatar";
import { Aviso, EstadoDaLista } from "comum/react";
import type { ReactNode } from "react";
import { useState } from "react";
import type { PaginaDoNucleo } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";

/** A linha de um registro: o avatar quando o registro tem um, a célula que o
 * identifica — e que abre a página individual dele — e os dados principais da
 * carta daquele papel (`RF-03-02`, documento 11 §8.2).
 *
 * `destino` ausente deixa a identificação em texto: é o caso do portfólio, em
 * que a criação original não tem página individual e são os **nicks dos
 * autores**, dentro de `dados`, que abrem página (design — decisão 3). */
export interface LinhaDeRegistro {
  avatar?: string | null;
  identificacao: string;
  destino?: string;
  dados: ReactNode;
}

/** O registro que uma página serve. A lista é genérica sobre a **página**, e
 * não sobre o item: é da página que o tipo do item se deduz, e é ela que a
 * leitura devolve — com o que a seção acrescente, como o ciclo corrente da
 * lista de comunidades. */
type ItemDa<Pagina> = Pagina extends PaginaDoNucleo<infer Item> ? Item : never;

interface Props<Pagina extends PaginaDoNucleo<unknown>> {
  /** A leitura de uma página da listagem. O cursor é opaco e vem da página
   * anterior; `null` é a primeira. */
  ler: (cursor: string | null) => Promise<Pagina>;
  /** A raiz da chave de cache. A página entra nela, e é a chave que refaz a
   * leitura (design — decisão 4). */
  chave: string;
  idDe: (item: ItemDa<Pagina>) => string;
  linhaDe: (item: ItemDa<Pagina>) => LinhaDeRegistro;
  /** O que a seção diz enquanto carrega, quando falha e quando não há
   * registro. */
  carregando: string;
  falha: string;
  vazio: string;
  /** Como a lista se chama para quem ouve a tela. */
  rotulo: string;
  /** O que a seção acrescenta **depois** da lista, a partir da mesma leitura
   * — o rótulo do ciclo corrente, na seção de comunidades. Uma página só é
   * lida, e nenhuma seção pede a leitura duas vezes. */
  depoisDaLista?: (dado: Pagina) => ReactNode;
}

/**
 * A **lista de registros** das seções de leitura da vitrine: uma linha por
 * registro, dez por página, com avançar e voltar e a posição em texto
 * (`RF-03-02`, `RF-03-82`).
 *
 * É `<ol>`, nunca `<table>`: tabela com cabeçalho de coluna é a densidade da
 * Operação, que o documento 15 §6 nega à Arena, e a página individual segue
 * sendo onde a carta domina (design — decisão 1).
 *
 * Mora na App 06 porque só ela lista personagem em linha (design — decisão 2).
 *
 * **Voltar** é pilha de cursores em memória: o núcleo pagina só para a frente,
 * e empilhar o que já se visitou dá o voltar sem mexer no contrato público.
 * A pilha se perde ao recarregar, que é o que o `RN-03-22` exige — nada da
 * navegação do visitante é gravado no aparelho.
 */
export function ListaDeRegistros<Pagina extends PaginaDoNucleo<unknown>>({
  ler,
  chave,
  idDe,
  linhaDe,
  carregando,
  falha,
  vazio,
  rotulo,
  depoisDaLista,
}: Props<Pagina>) {
  const [cursores, definirCursores] = useState<(string | null)[]>([null]);
  const pagina = cursores.length;
  const cursorDaPagina = cursores[pagina - 1];

  const estado = useLeitura(() => ler(cursorDaPagina), `${chave}#${pagina}`);
  const itens: ItemDa<Pagina>[] =
    estado.situacao === "pronta" ? (estado.dado.itens as ItemDa<Pagina>[]) : [];
  const proximoCursor = estado.situacao === "pronta" ? estado.dado.proximo_cursor : null;
  const temControles = proximoCursor !== null || pagina > 1;

  return (
    <>
      {estado.situacao === "carregando" && <EstadoDaLista>{carregando}</EstadoDaLista>}

      {estado.situacao === "falhou" && <Aviso tipo="erro">{falha}</Aviso>}

      {estado.situacao === "pronta" && itens.length === 0 && pagina === 1 && (
        <EstadoDaLista>{vazio}</EstadoDaLista>
      )}

      {itens.length > 0 && (
        <ol className="cg-lista-de-registros" aria-label={rotulo}>
          {itens.map((item) => {
            const linha = linhaDe(item);
            return (
              <li key={idDe(item)} className="cg-lista-de-registros__linha">
                {/* Avatar ausente não reserva espaço: a linha sai sem ele, e
                    nenhum vazio anuncia a falta (`RF-03-02`). */}
                {linha.avatar !== undefined && (
                  <span className="cg-lista-de-registros__avatar">
                    <Avatar avatar={linha.avatar} tamanho={40} />
                  </span>
                )}
                <span className="cg-lista-de-registros__identificacao">
                  {linha.destino === undefined ? (
                    linha.identificacao
                  ) : (
                    // `<a href>`, nunca `<button>`: o visitante abre em nova
                    // aba, copia o endereço e navega pelo teclado, e o
                    // `noindex` continua declarado no destino (design —
                    // decisão 3).
                    <a href={linha.destino}>{linha.identificacao}</a>
                  )}
                </span>
                <span className="cg-lista-de-registros__dados">{linha.dados}</span>
              </li>
            );
          })}
        </ol>
      )}

      {estado.situacao === "pronta" && depoisDaLista?.(estado.dado)}

      {temControles && (
        <div className="cg-lista-de-registros__paginacao">
          <button
            type="button"
            onClick={() => definirCursores((pilha) => pilha.slice(0, -1))}
            disabled={pagina === 1}
          >
            Página anterior
          </button>
          {/* A posição sai em **texto**, e não há "página 3 de 12": o núcleo
              pagina por cursor e não devolve total (design — decisão 4). */}
          <p className="cg-lista-de-registros__posicao" aria-live="polite">
            Página {pagina}
          </p>
          <button
            type="button"
            onClick={() =>
              definirCursores((pilha) =>
                proximoCursor === null ? pilha : [...pilha, proximoCursor],
              )
            }
            disabled={proximoCursor === null}
          >
            Próxima página
          </button>
        </div>
      )}
    </>
  );
}
