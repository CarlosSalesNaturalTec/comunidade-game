# Tasks

## 1. A folha de estilo de `comum/trilha`

- [x] 1.1 Criar `comum/trilha/estilos.css` e importá-la no `comum/trilha/indice.ts`, no molde
      de `comum/react/indice.ts`, com o mínimo que a fatia exige: a linha separadora e o
      espaçamento dos grupos. Verificar que as duas aplicações passam a receber a folha. Não há
      regra a mover — `comum/trilha` não tem folha alguma e as classes dos componentes
      promovidos não têm regra no repositório; `.cg-trilha__badges` fica no `index.css` da
      App 05, porque é do `Progresso.tsx` dela (design — decisão 5).

## 2. A missão, o guia e os quatro grupos em `comum/trilha`

- [x] 2.1 Tirar da `Missao` a bibliografia e o `Crédito e licença`, deixando-a com o título, o
      aviso de missão opcional, o conteúdo paginado, o aviso de espera pelo Mestre, a sondagem
      ou o desafio de desbloqueio e a entrega da produção. Verificar que o ato continua
      renderizado logo abaixo do conteúdo (`RF-04-73`, `RF-05-11`).
- [x] 2.2 Subir a chamada de `obterTrilhaPublica` da `Missao` para o `GuiaDaTrilha`, que passa
      a ser o dono do dado da trilha publicada. Verificar que a missão continua apresentando o
      conteúdo na ordem do autor e que a chamada acontece **uma vez** por trilha aberta
      (`RF-05-11`, design — decisão 1).
- [x] 2.3 Compor no `GuiaDaTrilha` os quatro grupos na ordem decidida, com `border-top` no
      grupo que vem **depois** de cada linha, sem rótulo e sem elemento anunciado. Verificar
      que grupo sem conteúdo não renderiza, levando a sua linha, e que não sobra separador
      entre dois grupos vizinhos (`RF-04-72`, `RF-05-08`, `RF-05-10`, design — decisão 2).
- [x] 2.4 Apresentar a bibliografia em `BlocoRecolhivel`, no grupo da próxima missão, com o
      resumo "Onde ler mais sobre esta missão.", e **omiti-la** quando a missão não tem
      bibliografia. Verificar que ela nasce fechada e que abre com título, capítulo e a
      disponibilidade no ponto de apoio (`RF-05-12`, design — decisão 6).
- [x] 2.5 Montar o grupo do rodapé com o caminho ao catálogo — recebido como callback, e
      apresentado só quando recebido — seguido do `Crédito e licença` recolhido, e receber as
      atividades do encontro como `ReactNode` no grupo anterior. Verificar que o guia sem os
      dois não apresenta grupo vazio nem linha (`RF-04-72`, `RF-04-74`, design — decisão 3).
- [x] 2.6 Envolver no mesmo esqueleto o caminho da trilha **sem próxima missão**, hoje de saída
      antecipada. Verificar que as atividades do encontro e o rodapé continuam na tela e que o
      crédito passa a ser apresentado ali, que hoje não acontece (`RF-04-72`, invariante 5 do
      documento 99, design — decisão 4).
- [x] 2.7 Cobrir em `comum/trilha/trilha.test.tsx` a ordem dos grupos, o ato acima da primeira
      linha, o grupo vazio que leva a linha, a bibliografia fechada e omitida, o crédito no
      rodapé e o crédito na trilha concluída — os cenários dos dois deltas de spec.

## 3. As duas aplicações

- [x] 3.1 Na `TelaDeTrilhasDoGuerreiro` da App 01, passar as atividades do encontro como slot e
      passar o callback do catálogo **somente** com uma trilha inscrita, quando a lista de
      trilhas é inalcançável. Verificar que com duas trilhas o rodapé não oferece o caminho e
      que ele segue na lista (`RF-04-72`, `RF-04-74`).
- [x] 3.2 No `Trilha.tsx` da App 05, não passar o callback do catálogo ao guia, mantendo o
      caminho na tela de trocar de trilha. Verificar que o guia não oferece escolher outro
      poder e que a tela de trocar de trilha continua oferecendo (`RF-05-08`, `RF-05-09`).
      **Não exigiu mudança de código**: o `prop` nasceu opcional e a App 05 nunca o passa —
      o que a tarefa entregou foi a verificação.
- [x] 3.3 Atualizar os testes das duas aplicações — `apps/app-01-aula-presencial/src/trilhas/`
      e `apps/app-05-guerreiro/src/trilha/` — nos pontos que afirmam a posição ou a presença da
      bibliografia, do crédito, da próxima missão e do caminho ao catálogo, cobrindo os
      cenários do delta de cada capacidade.

## 4. Documentação

- [x] 4.1 Marcar a fatia 27 como `implementado` em `openspec/cronograma-de-fatias.md` e
      escrever o slug da change na coluna Recorte. Nada muda em `docs/`: não houve decisão nova
      de regra de negócio — é apresentação, no molde das fatias 25 e 26 —, o PRD-04 segue em
      implementação em `docs/prds/index.md`, nenhuma relação entre documentos mudou e nenhum
      arquivo nasceu em `docs/`.
