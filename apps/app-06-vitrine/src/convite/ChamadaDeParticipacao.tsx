import { Botao } from "comum/react";
import { CAMINHO_DO_CONVITE } from "../navegacao/caminhos";
import { navegarPara } from "../navegacao/navegar";

interface Props {
  irPara?: (destino: string) => void;
}

/** A chamada "Quero participar" e a ação de acompanhar, que **toda página
 * individual** traz e que levam à **mesma porta** (`RF-03-39`, `RF-03-40`).
 *
 * A chamada é **do projeto**: não oferece apoiar, apadrinhar ou favorecer quem
 * está na tela, e nada de quem está sendo visto é passado adiante — o componente
 * recebe só `irPara`, e o endereço da porta não tem parâmetro (`RF-03-41`,
 * `RN-03-25`; design — decisão 3). Favoritar é função de Apoiador cadastrado, na
 * App 08, e a vitrine não guarda favorito nenhum (`RF-03-38`, `RN-03-15`,
 * `RN-03-16`). */
export function ChamadaDeParticipacao({ irPara = navegarPara }: Props) {
  return (
    <section className="cg-chamada" aria-label="Quero participar">
      <p>
        Gostou do que a comunidade construiu? Você pode sustentar o projeto — e não uma pessoa:
        o apoio é do Comunidade Game inteiro.
      </p>
      <Botao onClick={() => irPara(CAMINHO_DO_CONVITE)}>Quero participar</Botao>
      <Botao variante="secundaria" onClick={() => irPara(CAMINHO_DO_CONVITE)}>
        Quero acompanhar
      </Botao>
      <p className="cg-chamada__ajuda">
        Acompanhar favoritos é coisa de Apoiador cadastrado, na Área do Apoiador. A vitrine não
        guarda favoritos.
      </p>
    </section>
  );
}
