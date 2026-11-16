# Tasks — Avatar na fila de entregas do encontro

## 1. Avatar na fila do encontro (`RF-09-75`, `RF-04-55`)

- [x] 1.1 Em `apps/app-01-aula-presencial/src/entregas/TelaDeEntregasDoEncontro.tsx`, trocar
      `({pendencia.guerreiro_avatar})` por `<Avatar avatar={pendencia.guerreiro_avatar}
      tamanho={32} />` antes do nick, importando de `comum/avatar` (`RF-09-75`, `RF-04-55`)
- [x] 1.2 Em `entregas.test.tsx`, o cenário de nick e avatar passa a conferir o desenho, e um
      cenário com o avatar em JSON confere que nenhum trecho dele aparece como texto
      (`RF-09-75`, `RF-04-55`)

## 2. Fechamento

- [x] 2.1 `biome format`, `biome check` e `vitest run` na App 01, uma vez
- [x] 2.2 Ao arquivar, a linha da fatia 36 do PRD-04 no `openspec/cronograma-de-fatias.md`
      passa a `implementado`
