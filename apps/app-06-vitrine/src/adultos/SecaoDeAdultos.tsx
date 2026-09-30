import type { DadosDaCarta } from "comum/react";
import { Aviso, CartaDoPersonagem, cartaEstaCompleta, EstadoDaLista } from "comum/react";
import { useLeitura } from "../leitura/useLeitura";
import { navegarPara } from "../navegacao/navegar";

interface Props<Item> {
  /** A leitura da listagem e a chave de cache dela. */
  listar: () => Promise<{ itens: Item[] }>;
  chave: string;
  /** Como cada item vira carta, e como ele se chama na tela. */
  cartaDe: (item: Item) => DadosDaCarta;
  identificacaoDe: (item: Item) => string;
  idDe: (item: Item) => string;
  /** O prefixo do endereço próprio da página individual (`RF-03-03`). */
  prefixoDoCaminho: string;
  vazio: string;
  irPara?: (destino: string) => void;
}

/** A seção de cards de um papel adulto. As duas variantes — Mestre e
 * Apoiador — têm a mesma mecânica: carta por item, carta pela metade cai em
 * outra forma, e cada card abre a página individual em endereço próprio
 * (`RF-03-02`, `RF-03-03`, documento 11 §8.2).
 *
 * **Sem rotação**: os 5 segundos do `RF-03-04` são dos Guerreiros e
 * Guerreiras, e nenhum requisito os estende a estas duas seções. */
export function SecaoDeAdultos<Item>({
  listar,
  chave,
  cartaDe,
  identificacaoDe,
  idDe,
  prefixoDoCaminho,
  vazio,
  irPara = navegarPara,
}: Props<Item>) {
  const estado = useLeitura(listar, chave);
  const itens = estado.situacao === "pronta" ? estado.dado.itens : [];

  return (
    <>
      {estado.situacao === "carregando" && <EstadoDaLista>Carregando os cards…</EstadoDaLista>}

      {estado.situacao === "falhou" && (
        <Aviso tipo="erro">Não foi possível carregar os cards agora. Tente de novo.</Aviso>
      )}

      {estado.situacao === "pronta" && itens.length === 0 && (
        <EstadoDaLista>{vazio}</EstadoDaLista>
      )}

      {itens.length > 0 && (
        <ul className="cg-cards-de-adultos">
          {itens.map((item) => {
            const dados = cartaDe(item);
            const nome = identificacaoDe(item);
            return (
              <li key={idDe(item)}>
                {cartaEstaCompleta(dados) ? (
                  <CartaDoPersonagem dados={dados} />
                ) : (
                  <EstadoDaLista>
                    A leitura de {nome} veio incompleta — a carta não é apresentada.
                  </EstadoDaLista>
                )}
                <button
                  type="button"
                  className="cg-card-do-guerreiro__abrir"
                  onClick={() =>
                    irPara(`${prefixoDoCaminho}${encodeURIComponent(idDe(item))}`)
                  }
                >
                  Abrir a página de {nome}
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </>
  );
}
