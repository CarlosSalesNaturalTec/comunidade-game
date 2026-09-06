import type { ReactNode } from "react";

export interface AreaDeNavegacao {
  chave: string;
  rotulo: string;
  /** Conteúdo extra ao lado do rótulo — o alerta de solicitação em aberto
   * da App 09, por exemplo. */
  conteudoExtra?: ReactNode;
}

interface Props {
  /** Rótulo acessível da navegação, ex.: "Áreas da gestão". */
  rotulo: string;
  areas: AreaDeNavegacao[];
  areaAtual: string;
  aoSelecionarArea: (chave: string) => void;
  aoSair: () => void;
}

// As áreas da aplicação e a saída da sessão, numa navegação só: a área
// corrente é marcada por `aria-current` e por peso de fonte e borda, sem
// depender de cor (documento 15 §5), e a saída aparece uma única vez, ao
// fim — nunca dentro de cada tela de área (documento 15 §6, design —
// decisão 4).
export function NavegacaoDeAreas({
  rotulo,
  areas,
  areaAtual,
  aoSelecionarArea,
  aoSair,
}: Props) {
  return (
    <nav className="cg-navegacao-de-areas" aria-label={rotulo}>
      <div className="cg-navegacao-de-areas__areas">
        {areas.map((area) => (
          <button
            key={area.chave}
            type="button"
            className="cg-navegacao-de-areas__item"
            aria-current={area.chave === areaAtual ? "true" : undefined}
            onClick={() => aoSelecionarArea(area.chave)}
          >
            {area.rotulo}
            {area.conteudoExtra}
          </button>
        ))}
      </div>
      <button type="button" className="cg-navegacao-de-areas__saida" onClick={aoSair}>
        Sair
      </button>
    </nav>
  );
}
