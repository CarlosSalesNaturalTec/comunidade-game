# Tasks

## 1. A tela inicial

- [x] 1.1 Reordenar os cartões dos caminhos em `TelaInicial.tsx` para onboarding, presença,
      trilhas e missões, equipes, quiz e — condicionado a `momentoDeTrocaAberto` — troca por
      recompensa avulsa (`RF-04-01`). Verificar que o menu renderiza nessa ordem com o momento
      aberto e que nenhum `onClick`, rótulo ou glifo mudou de cartão.
- [x] 1.2 Mover o cartão da medição do limiar para dentro do `fieldset`
      `cg-caminhos__operacao`, **depois da `legend`** e antes da chave do momento de troca,
      mantendo o encerramento por último (`RF-04-63`, `RF-04-71`, `RF-04-49`, `RN-04-33`).
      Verificar na tela que a linha do separador continua acima dos três cartões — a `legend`
      flutuada é que a desenha (design — decisão 2) — e que o caminho `"medicao"` e o pedido de
      PIN que o guarda seguem intactos (`RN-04-41`).

## 2. Os testes da tela inicial

- [x] 2.1 Acrescentar a `inicio.test.tsx` o teste da ordem inteira dos cartões `.cg-caminho`
      com o momento de troca aberto, cobrindo o cenário "Os caminhos aparecem na ordem
      decidida" (`RF-04-01`). Verificar que ele falha ao se trocar dois cartões de lugar — é a
      proteção que hoje não existe, porque o teste dos glifos itera sem asserir ordem.
- [x] 2.2 Acrescentar a `inicio.test.tsx` o teste de que a medição está dentro do
      `role="group"` nomeado "Para quem opera o aparelho" e que nenhum caminho da criança vem
      depois dela, cobrindo o cenário "A medição do limiar não fica entre os caminhos da
      criança" (`RF-04-63`, `RN-04-33`). Verificar também o cenário "As ações de quem opera
      fecham a lista, com o encerramento por último" na redação nova do delta, inclusive no
      aparelho que não abre a troca (`RF-04-71`, `RF-04-49`).
- [x] 2.3 Conferir — sem reescrever — que os dois testes de cauda por índice continuam verdes:
      `cartoes[length - 2]` é a abertura da troca e `cartoes[length - 1]` é o encerramento
      (design — decisão 3). Se algum falhar, a medição entrou na posição errada dentro do
      grupo.

## 3. Documentação

- [x] 3.1 Marcar a fatia 26 como `implementado` em `openspec/cronograma-de-fatias.md`,
      mantendo o slug já escrito na coluna Recorte. Nada muda em `docs/`: não houve decisão
      nova de regra — é apresentação, no molde da fatia 25 —, o PRD-04 segue em implementação
      em `docs/prds/index.md`, nenhuma relação entre documentos mudou e nenhum arquivo nasceu.
