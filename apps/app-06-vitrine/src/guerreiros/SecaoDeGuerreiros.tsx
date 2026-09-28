import {
  Aviso,
  CartaDoPersonagem,
  cartaEstaCompleta,
  EstadoDaLista,
  SequenciaPaginada,
} from "comum/react";
import { useEffect, useState } from "react";
import { listarGuerreiros } from "../api/leituras";
import { useLeitura } from "../leitura/useLeitura";
import { BuscaPorNick } from "./BuscaPorNick";
import { cartaDoGuerreiro } from "./carta";

interface Props {
  irPara: (destino: string) => void;
}

const INTERVALO_DA_ROTACAO_EM_MS = 5000;

/** O aparelho que pede menos movimento não recebe rotação nenhuma
 * (documento 15 §5). Fora do navegador — em teste, por exemplo — a consulta
 * não existe e a resposta é "não pediu". */
function pediuMenosMovimento(): boolean {
  if (typeof window === "undefined" || typeof window.matchMedia !== "function") return false;
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/** A rotação **comanda** o paginador de `comum/react`; os controles dele
 * continuam ali, e é isso que faz a rotação não ser a única via ao conteúdo
 * (`RF-03-04`, documento 15 §§5, 8.1, design — decisão 5). */
function useRotacao(quantidade: number) {
  const [indice, definirIndice] = useState(0);

  useEffect(() => {
    if (quantidade < 2 || pediuMenosMovimento()) return;
    const temporizador = setInterval(() => {
      definirIndice((atual) => (atual + 1) % quantidade);
    }, INTERVALO_DA_ROTACAO_EM_MS);
    return () => clearInterval(temporizador);
  }, [quantidade]);

  return { indice: quantidade === 0 ? 0 : indice % quantidade, definirIndice };
}

export function SecaoDeGuerreiros({ irPara }: Props) {
  const estado = useLeitura(listarGuerreiros, "vitrine/guerreiros");
  const guerreiros = estado.situacao === "pronta" ? estado.dado.itens : [];
  const { indice, definirIndice } = useRotacao(guerreiros.length);

  return (
    <>
      <BuscaPorNick irPara={irPara} />

      {estado.situacao === "carregando" && <EstadoDaLista>Carregando os cards…</EstadoDaLista>}

      {estado.situacao === "falhou" && (
        <Aviso tipo="erro">Não foi possível carregar os cards agora. Tente de novo.</Aviso>
      )}

      {estado.situacao === "pronta" && guerreiros.length === 0 && (
        <EstadoDaLista>
          Nenhum Guerreiro ou Guerreira com divulgação autorizada por enquanto.
        </EstadoDaLista>
      )}

      {guerreiros.length > 0 && (
        <SequenciaPaginada
          itens={guerreiros}
          nome="Card"
          rotuloDeAvancar="Próximo card"
          rotuloDeVoltar="Card anterior"
          indice={indice}
          aoIrPara={definirIndice}
        >
          {(guerreiro) => {
            const dados = cartaDoGuerreiro(guerreiro);
            // Carta pela metade não se apresenta (documento 11 §8.2): a tela
            // diz em uma frase o que tem, e segue oferecendo a página.
            return (
              <div className="cg-card-do-guerreiro">
                {cartaEstaCompleta(dados) ? (
                  <CartaDoPersonagem dados={dados} />
                ) : (
                  <EstadoDaLista>
                    A leitura de {guerreiro.nick} veio incompleta — a carta não é apresentada.
                  </EstadoDaLista>
                )}
                <button
                  type="button"
                  className="cg-card-do-guerreiro__abrir"
                  onClick={() => irPara(`/guerreiros/${encodeURIComponent(guerreiro.nick)}`)}
                >
                  Abrir a página de {guerreiro.nick}
                </button>
              </div>
            );
          }}
        </SequenciaPaginada>
      )}
    </>
  );
}
