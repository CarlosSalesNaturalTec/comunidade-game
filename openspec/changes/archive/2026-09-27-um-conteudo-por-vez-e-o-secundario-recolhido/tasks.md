# Tasks

## 1. O paginador na camada comum

- [x] 1.1 Criar `comum/react/SequenciaPaginada.tsx`: recebe os itens, o que renderizar para
      cada um, e o rótulo de avançar; guarda o índice em `useState`, diz a posição na
      sequência, omite o controle quando há um item só e não oferece avançar no último.
      O retorno ao item anterior é **opcional**, ligado por quem monta (design — decisões 1,
      2, 3, 7). Exportar em `comum/react/indice.ts`
- [x] 1.2 Testar `SequenciaPaginada` em `comum/react`: avança, informa a posição, não avança
      além do último, e não apresenta controle com um item só.
      `npx vitest run comum/react` verde
- [x] 1.3 Alterar a spec viva do bloco recolhível **não** é tarefa de código: confirmar que
      `BlocoRecolhivel` já atende a Arena sem prop nova — nasce fechado, controle com rótulo,
      sem animação — e registrar no PR se algum ajuste de token for preciso
      (design — decisão 6)

## 2. O conteúdo da missão, um por vez, com o crédito recolhido

- [x] 2.1 `comum/trilha/Missao.tsx`: percorrer os conteúdos ordenados com
      `SequenciaPaginada`, sem retorno, no lugar da `<ol>` (`RF-05-11`, `RF-04-73`)
- [x] 2.2 `comum/trilha/Missao.tsx`: mover crédito e licença da trilha para `BlocoRecolhivel`,
      com resumo neutro `"Crédito e licença"`. A linha `"— fonte: X"` do conteúdo de terceiro
      **fica onde está**, junto do conteúdo (`RF-05-11`, design — decisão 5)
- [x] 2.3 Testar em `comum/trilha/trilha.test.tsx`: o primeiro conteúdo aparece sozinho,
      avançar leva ao segundo, conteúdo único não pagina, e o crédito está num bloco fechado
      que abre ao ser acionado. `npx vitest run comum/trilha -t "conteúdo"` verde

## 3. O desafio de desbloqueio, uma pergunta por vez

- [x] 3.1 `comum/trilha/DesafioDeDesbloqueio.tsx`: percorrer as perguntas com
      `SequenciaPaginada`, **com retorno ligado**, mantendo as escolhas no mesmo estado local
      e a submissão única ao fim (`RF-05-13`, `RN-05-45`, design — decisão 3)
- [x] 3.2 `comum/trilha/DesafioDeDesbloqueio.tsx`: a sinalização de pergunta sem resposta
      passa a **navegar até a primeira pendente**, em vez de só contar quantas faltam
      (design — decisão 4)
- [x] 3.3 Testar em `comum/trilha/trilha.test.tsx`: uma pergunta por vez; voltar preserva a
      resposta dada e permite trocá-la; concluir com pendência leva até ela e não envia; e a
      submissão continua sendo **uma só, com todas as respostas** — este último é o teste que
      protege o `RN-05-45` e **não muda de asserção**.
      `npx vitest run comum/trilha -t "desbloqueio"` verde

## 4. A missão seguinte recolhida

- [x] 4.1 `comum/trilha/GuiaDaTrilha.tsx`: mover o aviso da missão seguinte trancada para
      `BlocoRecolhivel`, com resumo neutro `"Próxima missão"`, mantendo dentro o título e o
      motivo do bloqueio (`RF-05-08`, `RF-05-10`, `RF-04-72`)
- [x] 4.2 Confirmar que o aviso da **própria missão trancada**, dentro de `Missao.tsx`,
      **não** foi recolhido: ali o motivo é resposta à ação
- [x] 4.3 Testar em `comum/trilha/trilha.test.tsx`: a seguinte aparece em bloco fechado de
      resumo neutro e abre com o motivo; abrir uma missão trancada segue mostrando o motivo
      direto. `npx vitest run comum/trilha` verde

## 5. O conteúdo do dia da equipe, um por vez

- [x] 5.1 `apps/app-01-aula-presencial/src/trilhas/TelaDaProgramacao.tsx`: percorrer
      `item.conteudos` com `SequenciaPaginada`, sem retorno, mantendo a linha `"Fonte: X"`
      junto do conteúdo de terceiro (`RF-04-35`)
- [x] 5.2 Testar em `apps/app-01-aula-presencial/src/trilhas/trilhas.test.tsx`: o primeiro
      conteúdo do dia aparece sozinho, avançar leva ao segundo, e a fonte do conteúdo de
      terceiro aparece junto dele. `npx vitest run apps/app-01-aula-presencial` verde

## 6. Fechamento

- [x] 6.1 Corrigir a linha da fatia 22 em `openspec/cronograma-de-fatias.md`: acrescentar o
      `RF-04-35` ao recorte e a decisão do fundador de 2026-09-26 que o incluiu; marcar a
      situação como implementado
- [x] 6.2 Rodar a suíte inteira dos dois pacotes tocados, uma vez:
      `npx vitest run comum apps/app-01-aula-presencial` e
      `npx biome check comum apps/app-01-aula-presencial` verdes
- [x] 6.3 Conferir que a App 05 não regrediu: `npx vitest run apps/app-05-guerreiro` verde —
      ela consome os mesmos componentes e é onde a mudança aparece sem que o PRD-05 mude
