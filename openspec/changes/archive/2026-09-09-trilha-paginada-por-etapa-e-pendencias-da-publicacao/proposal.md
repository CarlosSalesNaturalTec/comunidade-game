# Trilha paginada por etapa e pendências da publicação

Origem: **PRD-09 — Área do Mestre**, fatia **17** do `openspec/cronograma-de-fatias.md`.
Atende `RF-09-03`, `RF-09-06` e `RF-09-07`, e aplica a ordem dos blocos da missão decidida
pelo fundador em 2026-09-09. Depende da fatia transversal do bloco recolhível, já entregue
(`2026-09-07-bloco-recolhivel-e-marca-de-gravacao`).

## Why

A tela da trilha da App 09 cresceu por acúmulo e hoje pede do Mestre três coisas que ela não
entrega:

1. **A etapa do ciclo não organiza nada.** O Mestre declara a etapa de cada missão — abertura,
   desenvolvimento, marcos, fechamento —, mas ela só vira etiqueta na linha. `RF-09-03` pede
   que a trilha seja **paginada** por etapa; hoje as missões descem numa lista única.
2. **O que falta para publicar só aparece quando a publicação é recusada.** As três travas de
   `RF-09-06`, `RF-09-07` e `RF-09-82` o núcleo já calcula e já nomeia em linguagem simples,
   mas o Mestre só as lê depois de tentar publicar e ser recusado. Ele escreve a trilha inteira
   às cegas quanto ao que ainda falta.
3. **A ordem dos nove blocos de cada missão é sedimento, não decisão.** Cada bloco foi parar no
   fim do arquivo na fatia que o entregou. O resultado lê de trás para frente — a recompensa
   antes do desbloqueio que a paga, o template que sugere os oito blocos abaixo em segundo
   lugar.

## What Changes

- **A tela da trilha pagina as missões pelas quatro etapas do ciclo** (`RF-09-03`). Dentro de
  cada etapa, a ordem da posição permanece. Etapa sem missão aparece vazia, e não some.
- **As três travas de publicação viram painel permanente** na tela da trilha (`RF-09-06`,
  `RF-09-07`), lido a qualquer momento, não só na recusa. O painel é **checklist, não porteiro**:
  quem recusa a publicação continua sendo o núcleo, e a mensagem da recusa não muda
  (`RF-09-08`, inalterado).
- **Os nove blocos recolhíveis de cada missão passam à ordem em que o Mestre a escreve** —
  template da missão, conteúdo, bibliografia, cadência de retomada, atividades, desafio de
  desbloqueio, recompensa pelo desbloqueio, desafios de coleta e ODS da missão —, com a
  pré-visualização da missão fechando o conjunto. Reordenação pura: nenhum bloco nasce, some
  ou muda de comportamento.
- **Nada muda no núcleo.** Nenhuma rota nova, nenhum campo novo, nenhuma migração.

Fora desta fatia, embora o recorte da fatia 17 no cronograma o mencione: **o tópico do template
da missão já é declarado descartável na tela** (`TemplateDaMissao.tsx`, "Este tópico não é
guardado — só o que você aceitar vira registro na missão."), atendido na fatia 12. O recorte
descreve estado já alcançado; esta change não tem tarefa para ele.

## Capabilities

### New Capabilities

Nenhuma. A fatia é da aplicação, e a `area-do-mestre` já existe.

### Modified Capabilities

- `area-do-mestre`: a apresentação das missões passa de lista única a **paginação por etapa do
  ciclo** (`RF-09-03`, requisito existente "O Mestre acrescenta missões à trilha, ordenadas e
  declaradas"); a aplicação passa a **apresentar permanentemente as travas pendentes** de
  publicação, e não só na recusa (`RF-09-06`, `RF-09-07`, requisito existente "O Mestre publica
  a própria trilha e lê o que falta quando é recusado"); e a **ordem dos blocos da missão**
  passa a ser declarada, em requisito novo dentro da mesma capability.

## Impact

- `apps/app-09-mestre/src/trilhas/TelaDaTrilha.tsx`: a paginação por etapa e o painel de
  pendências.
- `apps/app-09-mestre/src/trilhas/ListaDeMissoes.tsx`: a ordem dos nove blocos; passa a receber
  as missões de uma etapa por vez.
- `apps/app-09-mestre/src/trilhas/trilhas.test.tsx`: os testes da tela.
- **Backend: nada.** As três travas já vêm inteiras no payload de `GET /trilhas/minhas` —
  `e_sondagem` na missão, `desafios_de_coleta` aninhados e `culminancia` na trilha.
- **Documentação:** só a situação da fatia 17 no `openspec/cronograma-de-fatias.md`. Nenhum
  documento de `docs/` declara ordem de bloco, paginação de tela ou o painel; nenhuma decisão
  nova nasce aqui, e o documento 09 não muda.
