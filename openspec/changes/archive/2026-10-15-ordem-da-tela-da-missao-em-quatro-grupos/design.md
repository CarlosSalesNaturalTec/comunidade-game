# Design

## Context

Ver `proposal.md` — Why. O que o desenho precisa levar em conta é a divisão de donos que a
tela tem hoje: `TelaDeTrilhasDoGuerreiro` (App 01) monta `GuiaDaTrilha`, que monta `Missao`,
e cada um contribui uma parte contígua da tela. A ordem decidida alterna entre os três donos
— conteúdo e bibliografia são da `Missao`, a próxima missão é do `GuiaDaTrilha`, as
atividades e o caminho ao catálogo são da tela, e o crédito volta a ser o último item,
**abaixo** do que a tela contribui. Componente não se renderiza depois do próprio pai, então
a ordem não sai de ajuste local.

O requisito do percurso já está em `openspec/specs/aplicacao-da-aula-presencial/spec.md`, e o
do conteúdo e da bibliografia em `openspec/specs/area-do-guerreiro/spec.md`; os blocos
recolhíveis da Arena estão em `camada-visual-comum`. Nada disso muda de dono aqui.

## Goals / Non-Goals

**Goals:**

- Um único dono da ordem e dos separadores, para a regra de grupo vazio existir num lugar só.
- A ordem do DOM igual à ordem visual, porque é ela que o teclado e o leitor de tela seguem.
- `comum/trilha` deixar de depender da folha de estilo de uma das duas aplicações.

**Non-Goals:**

- Componente ou tipo novo em `comum/react`: o separador é borda, não peça da camada visual.
- Estilizar as demais classes `cg-trilha__*` que hoje não têm regra: é dívida da fatia 21, e
  esta fatia escreve só o que a ordem nova exige.
- Mudança de rota, de contrato ou de busca no núcleo além de **mover** a chamada existente.

## Decisions

**O `GuiaDaTrilha` passa a compor os grupos; a `Missao` fica com o conteúdo e o ato.** É o
único ponto que alcança as duas pontas da ordem. `Bibliografia` e `Crédito e licença` saem da
`Missao` e sobem com a chamada de `obterTrilhaPublica`, que hoje mora dentro dela. Isso é o
que permite ao mesmo dono saber se o grupo da próxima missão ficou vazio — a condição vem de
dois itens de componentes diferentes. Descartado: slot na `Missao`, que não alcança o rodapé
abaixo do conteúdo da aplicação; e `order` de flex, que desencontra a ordem de leitura da
ordem visual.

**O separador é `border-top` do grupo que vem depois dele.** Grupo que não renderiza leva a
sua linha embora, sem contagem de grupos nem elemento solto. Descartado: `<hr>`, que tem
`role="separator"` implícito e é anunciado por parte dos leitores, contra a linha muda que o
fundador pediu; e o par `fieldset`/`legend` das fatias 25 e 26, que existe porque a `legend`
carrega a borda — sem rótulo não há o que a carregue.

**Cada aplicação decide o que o rodapé oferece, porque cada uma conhece o seu grafo de
navegação.** `Atividades do encontro` entra como `ReactNode`; o caminho ao catálogo entra
como callback, que a App 01 passa só com uma trilha inscrita e a App 05 nunca passa. O
`GuiaDaTrilha` NEVER decide a condição: ele apresenta o que recebeu. Descartado: o
`GuiaDaTrilha` inferir a condição da ausência de `aoTrocarDeTrilha` — funciona nos três casos
de hoje, mas amarra duas decisões sem relação declarada.

**O esqueleto dos grupos envolve também o caminho da trilha sem próxima missão**, onde o
`GuiaDaTrilha` sai cedo hoje. Sem isso a App 01 perderia as atividades do encontro ali, que a
tela renderiza depois do guia. Com a busca da trilha pública subindo, o crédito passa a ser
apresentado nesse caminho — hoje não é, porque a `Missao` nunca monta.

**`comum/trilha/estilos.css` nasce e é importada pelo `indice.ts`**, no molde de
`comum/react/indice.ts` e de `comum/avatar/Avatar.tsx`. Não há regra a mover: `comum/trilha`
não tem folha alguma, e das vinte classes `cg-trilha__*` só `.cg-trilha__badges` existe no
CSS — e ela é do `Progresso.tsx` da App 05, que não é componente promovido. A folha nasce com
o **mínimo da fatia**: a linha e o espaçamento dos grupos. Descartado: escrever a regra no
`index.css` da App 01, que deixaria a App 05 sem a linha.

**O resumo do bloco da bibliografia é "Onde ler mais sobre esta missão."** — neutro e sem
repetir o conteúdo, como a Arena exige; o resumo de estado, que conta itens, é da Operação.

## Risks / Trade-offs

- **Mover as regras de estilo muda a ordem da cascata dentro da App 05** → as regras vão
  verbatim, e as telas de trilha da App 05 são conferidas à mão depois da troca.
- **Linha aparecendo antes do conteúdo do grupo, durante o carregamento** → o grupo e a sua
  linha renderizam juntos, condicionados ao conteúdo; o estado de carregamento fica no grupo
  do conteúdo, que é o primeiro e não tem linha.
- **O crédito passa a aparecer num caminho em que hoje não aparece** → é correção, não efeito
  colateral: o invariante 5 do documento 99 exige autoria creditada, e a spec declara o
  cenário.
- **Teste que afirma a posição ou a presença desses blocos quebra** → esperado; os testes das
  duas aplicações e de `comum/trilha` entram no mesmo PR.
