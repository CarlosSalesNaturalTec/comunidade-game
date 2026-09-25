import type { ReactNode } from "react";

// O **palco da Arena** (documento 15 §6): onde uma tela da Arena apresenta
// personagem, a apresentação — a carta, quando a tela tem carta — é o
// **elemento maior da tela**, e a tela pede **uma decisão só**. É a densidade
// baixa que o §6 atribui à Arena, e o contrário da densidade da Operação, cuja
// tabela, lote e painel são da outra família (invariante 24).
//
// A única decisão é um campo próprio, e não `children`, justamente para que a
// tela não possa empilhar duas sem que se note: quem precisar de duas decisões
// está escrevendo uma tela da Operação. Voltar não conta — é saída, e mora na
// ação do `Cabecalho`.
//
// O `apoio` é o que a tela ainda comunica depois da decisão: fica **abaixo** e
// **menor** que a apresentação, nunca disputando o primeiro plano com ela.

interface Props {
  /** A apresentação do personagem — a carta, no caso das telas que a têm. */
  children: ReactNode;
  /** A **única** decisão da tela. Ausente, a tela é só leitura. */
  decisao?: ReactNode;
  /** O que a tela ainda comunica, abaixo e menor que a apresentação. */
  apoio?: ReactNode;
  /** O rótulo acessível da região, já que o palco é uma seção própria. */
  rotulo: string;
}

export function PalcoDoPersonagem({ children, decisao, apoio, rotulo }: Props) {
  return (
    <section className="cg-palco" aria-label={rotulo}>
      <div className="cg-palco__personagem">{children}</div>
      {decisao && <div className="cg-palco__decisao">{decisao}</div>}
      {apoio && <div className="cg-palco__apoio">{apoio}</div>}
    </section>
  );
}
