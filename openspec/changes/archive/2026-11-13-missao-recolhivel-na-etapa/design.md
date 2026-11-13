# Design

## Context

O padrão já está consolidado: `BlocoRecolhivel` (`comum/react`), sobre `details`/`summary`,
nasce fechado a cada montagem e leva título e resumo em texto (documento 15 §6.1; requisito
"A App 09 monta o desafio de desbloqueio da missão" em `openspec/specs/area-do-mestre`).
`TelaDaTrilha` já entrega a `ListaDeMissoes` só as missões da etapa aberta (`RF-09-03`), de modo
que "mais de uma missão na etapa" é `missoes.length > 1` dentro da lista.

## Decisions

1. **Reusar `BlocoRecolhivel`, sem variante nova.** Título `"{posição}. {título}"`; resumo com
   "Sondagem" (quando for), "Obrigatória"/"Opcional" e "Dificuldade N", separados por " · ". A
   etapa sai do resumo: é a página aberta. Descartado: componente próprio de missão recolhível
   — duplicaria teclado e `aria-expanded` que o `details` já entrega.
2. **Tudo da missão vai para dentro do bloco**, inclusive "Corrigir missão", "Subir" e "Descer":
   `summary` não pode conter controle interativo. Descartado: atos fora do bloco — a linha
   fechada deixaria de ser uma linha.
3. **Condição na lista, não na tela**: `ListaDeMissoes` extrai o corpo da missão para uma função
   e o envolve no bloco só quando recebe mais de uma. Com uma, o JSX fica idêntico ao de hoje.
4. **Estado aberto/fechado continua interno ao bloco**, chaveado pelo `id` da missão: subir e
   descer preservam o que estava aberto; trocar de etapa remonta e fecha tudo, como o
   documento 15 §6.1 pede.

## Risks / Trade-offs

- Passar de uma para duas missões na etapa (ou o inverso) troca o envoltório e remonta a
  missão que já estava ali: formulário aberto e não gravado dentro dela se perde. Aceito — a
  nova missão nasce pelo formulário do topo da tela, fora da missão existente.
- Bloco recolhível dentro de bloco recolhível: a borda externa abraça as internas. Se a leitura
  pedir, um ajuste de espaçamento em `index.css` da App 09, sem tocar `comum/react`.
