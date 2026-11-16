# Tasks — Avatar na fila de entregas e aulas sem as canceladas

## 1. Avatar na fila de Entregas pendentes (`RF-09-75`, `RN-09-18`)

- [ ] 1.1 Em `apps/app-09-mestre/src/recompensas/FilaDeEntregasPendentes.tsx`, trocar
      `({pendencia.guerreiro_avatar})` por `<Avatar avatar={pendencia.guerreiro_avatar}
      tamanho={32} />` antes do nick, importando de `comum/avatar` (`RF-09-75`, `RN-09-18`)
- [ ] 1.2 Em `FilaDeEntregasPendentes.test.tsx`, cenário com `guerreiro_avatar` em JSON
      válido: o nick aparece e nenhum trecho do JSON (`formaDeTratamento`) está no texto da
      tela (`RF-09-75`, `RN-09-18`)

## 2. Aulas canceladas fora de Minhas turmas (`RF-09-42`)

- [ ] 2.1 Em `apps/app-09-mestre/src/turmas/TelaDeMinhasTurmas.tsx`, gravar no estado só as
      aulas com `situacao !== "cancelada"` (`RF-09-42`)
- [ ] 2.2 Em `turmas.test.tsx`: aula cancelada não aparece e a confirmada sim; só canceladas
      dá a mensagem "Nenhuma aula agendada nas suas comunidades." (`RF-09-42`). Revisar o
      teste "aula cancelada dentro da janela não oferece o caminho", que deixa de fazer
      sentido com a aula fora da lista (`RF-09-50`)

## 3. Fechamento

- [ ] 3.1 `biome format --check .`, `biome check .` e `vitest run` na App 09, uma vez
- [ ] 3.2 Ao arquivar, a linha da fatia 34 do PRD-09 no `openspec/cronograma-de-fatias.md`
      passa a `implementado`
