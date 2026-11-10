import { Botao } from "comum/react";
import { CAMINHO_DO_CONVITE } from "../navegacao/caminhos";
import { navegarPara } from "../navegacao/navegar";

interface Props {
  irPara?: (destino: string) => void;
}

/** A chamada "Quero apoiar", que **toda página individual** traz e que leva à
 * porta do convite (`RF-03-39`). A vitrine não oferece ação de acompanhar nem de
 * favoritar (decisão do fundador de 2026-11-10).
 *
 * A chamada é **do projeto**: não oferece apoiar, apadrinhar ou favorecer quem
 * está na tela, e nada de quem está sendo visto é passado adiante — o componente
 * recebe só `irPara`, e o endereço da porta não tem parâmetro (`RF-03-41`,
 * `RN-03-25`; design — decisão 3). Favoritar é função de Apoiador cadastrado, na
 * App 08, e a vitrine não guarda favorito nenhum (`RF-03-38`, `RN-03-15`,
 * `RN-03-16`). */
export function ChamadaDeParticipacao({ irPara = navegarPara }: Props) {
  return (
    <section className="cg-chamada" aria-label="Quero apoiar">
      <p>
        Gostou do que a comunidade construiu? Você pode sustentar o projeto — e não uma pessoa:
        o apoio é do Comunidade Game inteiro.
      </p>
      <Botao onClick={() => irPara(CAMINHO_DO_CONVITE)}>Quero apoiar</Botao>
    </section>
  );
}
