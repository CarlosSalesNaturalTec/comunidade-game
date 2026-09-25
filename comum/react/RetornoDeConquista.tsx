import { type ReactNode, useEffect, useRef, useState } from "react";

// O **retorno de progresso e conquista** da Arena (documento 15 §6, `300` ms
// com `ease-in-out`). Os quatro fatos que o merecem estão no documento 11
// §8.5, e são os únicos: fora deles **não há retorno**, porque movimento sem
// fato é a decoração que o documento 15 §5 proíbe — este componente não abre
// exceção àquela regra, ele a aplica.
//
// Três amarras, cada uma com cenário de aceite próprio:
//
// 1. **Não há retorno sem fato.** Quem monta a tela só passa `fato` quando um
//    dos quatro aconteceu — comparando o que a leitura trouxe com o que já
//    estava à vista. Sem fato, `fato` é `null` e não há elemento animado
//    nenhum: é assim que abrir a tela nunca anima. Abrir tela não é
//    conquistar, e o componente não tem como confundir os dois, porque a
//    ausência de fato não chega a produzir movimento.
// 2. **O fato fica legível sem o movimento.** O que `children` diz — texto,
//    numeral ou forma — é a **primeira** via, e o movimento é a segunda. Não
//    existe conquista que só o movimento comunique (documento 15 §5).
// 3. **Menos movimento suprime o retorno por completo.** A animação dura
//    `var(--duracao)`, que `comum/tokens.css` já derruba a `0ms` sob
//    `prefers-reduced-motion`, e o `@media` de `estilos.css` a desliga de vez.
//    O fato continua anunciado: o `role="status"` não depende de movimento.

/** Os fatos do motor que ganham retorno (documento 11 §8.5). */
export type FatoDaArena =
  | "missao_desbloqueada"
  | "badge_certificado"
  | "nivel_que_subiu"
  | "ponto_creditado";

interface Props {
  /** O fato acontecido, ou `null` quando não houve fato nenhum — e então não
   * há retorno. */
  fato: FatoDaArena | null;
  /** O fato em texto, numeral ou forma: a via que não depende de movimento. */
  children: ReactNode;
}

export function RetornoDeConquista({ fato, children }: Props) {
  // O fato pode chegar junto com a leitura que o descobriu — é o caso comum,
  // já que o progresso vem do núcleo depois da tela montar. Por isso o retorno
  // corre também na primeira apresentação do fato, e não só quando ele muda
  // com a tela aberta: o que o impede de virar animação de abertura é `fato`
  // ser `null` quando nada aconteceu.
  const fatoAnterior = useRef<FatoDaArena | null>(null);
  const [retornando, definirRetornando] = useState(fato !== null);

  useEffect(() => {
    if (fato === fatoAnterior.current) return;
    fatoAnterior.current = fato;
    if (fato === null) return;
    definirRetornando(true);
  }, [fato]);

  if (fato === null) return <>{children}</>;

  return (
    <div
      className="cg-retorno-de-conquista"
      data-fato={fato}
      data-retornando={retornando ? "sim" : undefined}
      role="status"
      onAnimationEnd={() => definirRetornando(false)}
    >
      {children}
    </div>
  );
}
