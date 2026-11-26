# Tasks

## 1. Lista de Guerreiros e Guerreiras (App 03)

- [x] 1.1 Em `apps/app-03-gestao/src/personas/ListaDeGuerreiros.tsx`, acrescentar a coluna
      "Nome" logo após "Nick", sem `recolhida`, renderizando `guerreiro.nome` (`RF-02-15`)
- [x] 1.2 Remover as colunas "Avatar" e "Início do vínculo" e a função `formatarData`, que fica
      sem uso; manter `comVinculo` e a coluna Comunidade (`RF-02-15`, `RN-02-06`)
- [x] 1.3 Atualizar o comentário do componente: nick e nome, sem imagem real, App 03 fora da
      superfície pública (`RN-02-22`, invariante 12)

## 2. Testes

- [x] 2.1 Em `personas.test.tsx`, o teste do vínculo deixa de esperar "Desde" e passa a
      conferir nick, nome e comunidade na linha (`RF-02-15`)
- [x] 2.2 Novo teste: a lista não tem cabeçalho "Avatar" nem "Início do vínculo", e nenhuma
      imagem aparece (`RN-02-22`)
- [x] 2.3 Rodar `biome format --write .`, `biome check .` e `vitest run` na App 03, uma vez

## 3. Cronograma

- [x] 3.1 Ao arquivar, a linha da fatia 31 do PRD-02 em `openspec/cronograma-de-fatias.md`
      vira `implementado` com o slug arquivado
