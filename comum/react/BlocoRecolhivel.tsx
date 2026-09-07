import { type ReactNode, useState } from "react";

interface Props {
  titulo: string;
  resumo: string;
  children: ReactNode;
}

// Sobre o elemento `details`/`summary` nativo: o navegador entrega o
// teclado e o `aria-expanded` do controle de graça — a mesma escolha do
// `Dialogo` com `dialog` (documento 15 §6.1, design — decisão 1). O estado
// aberto/fechado é interno e nasce fechado a cada montagem (design —
// decisão 3); ele também comanda o rótulo textual do controle e o
// `hidden` do conteúdo, para o bloco fechado não ficar alcançável. Sem
// `transition` de altura: abrir e fechar não anima. O resumo é dado por
// quem monta o bloco — o componente não conhece o domínio (design —
// decisão 2).
export function BlocoRecolhivel({ titulo, resumo, children }: Props) {
  const [aberto, definirAberto] = useState(false);

  return (
    <details
      className="cg-bloco-recolhivel"
      open={aberto}
      onToggle={(evento) => definirAberto(evento.currentTarget.open)}
    >
      <summary className="cg-bloco-recolhivel__controle">
        <span className="cg-bloco-recolhivel__titulo">{titulo}</span>
        <span className="cg-bloco-recolhivel__resumo">{resumo}</span>
        <span className="cg-bloco-recolhivel__estado">{aberto ? "Ocultar" : "Mostrar"}</span>
      </summary>
      <div className="cg-bloco-recolhivel__conteudo" hidden={!aberto}>
        {children}
      </div>
    </details>
  );
}
