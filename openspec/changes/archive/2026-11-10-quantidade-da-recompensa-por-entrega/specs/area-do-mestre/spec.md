## MODIFIED Requirements

### Requirement: O Mestre declara a recompensa que o desbloqueio da missão libera

A App 09 SHALL permitir ao **Mestre autor** declarar, junto da missão, que o **desbloqueio** dela
libera **recompensa**, escolhendo o tipo de recurso e a **quantidade**, e SHALL apresentar a
recompensa declarada junto da missão na trilha. A tela SHALL dizer que a quantidade é **por
Guerreiro(a)** — o que cada um recebe na entrega —, e não o total da turma (decisão do fundador
de 2026-11-09, 02 §8.1).

A tela NEVER SHALL oferecer preço, saldo de pontos ou qualquer contrapartida do Guerreiro(a): a
recompensa de marco é conquistada, nunca comprada nem trocada. A aplicação NEVER SHALL exigir
lastro na declaração nem avisar que ele falta: a conferência acontece na entrega.
(`RF-09-84`, `RF-09-71`, `RF-09-72`, `RN-09-26`, `RN-09-27`, `RN-09-39`, invariante 23)

#### Scenario: O Mestre autor declara a recompensa do desbloqueio

- **WHEN** o Mestre autor declara que o desbloqueio de uma missão dele libera 1 unidade de um
  tipo de recurso
- **THEN** a aplicação grava a declaração e a apresenta junto da missão

#### Scenario: O campo diz que a quantidade é por Guerreiro(a)

- **WHEN** o Mestre autor abre a declaração de recompensa
- **THEN** o campo da quantidade diz que ela é por Guerreiro(a), e não o total da turma

#### Scenario: A tela não oferece preço nem troca

- **WHEN** o Mestre autor abre a declaração de recompensa
- **THEN** nenhum campo pede preço, pontos ou contrapartida do Guerreiro(a)

#### Scenario: A declaração não exige lastro

- **WHEN** o Mestre autor declara recompensa de um tipo sem saldo em ponto de apoio algum
- **THEN** a aplicação grava a declaração normalmente, sem aviso de falta de lastro

### Requirement: A App 09 apresenta ao Mestre as entregas de recompensa pendentes

A App 09 SHALL apresentar ao Mestre, em **Minhas turmas**, a fila das **entregas pendentes**: os
Guerreiros e Guerreiras da comunidade dele que alcançaram marco com recompensa declarada e ainda
não a receberam, com a trilha, o marco, o tipo de recurso e a quantidade. Confirmada a entrega
pelo Mestre, a pendência SHALL sair da fila.

Cada Guerreiro(a) SHALL aparecer por **nick e avatar**, e nenhuma imagem real SHALL ser exibida.
A fila NEVER SHALL exibir valor em moedas nem em reais. Recusada a entrega pelo núcleo, a
aplicação SHALL dizer em linguagem simples qual foi o motivo — como a falta de lastro ou o marco
não alcançado —, sem código de erro. A fila NEVER SHALL marcar uma pendência como esgotada pelas
entregas feitas a outros Guerreiros e Guerreiras (decisão do fundador de 2026-11-09). (`RF-09-75`, `RF-09-76`, `RN-09-18`,
invariantes 12 e 16, PRD-09 §12)

#### Scenario: A fila mostra quem conquistou e ainda não recebeu

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia missão com recompensa declarada
- **THEN** a aplicação passa a apresentá-lo na fila de entregas pendentes, com a trilha, o marco,
  o tipo de recurso e a quantidade

#### Scenario: A fila não marca pendência como esgotada

- **WHEN** o Mestre já entregou a recompensa a um Guerreiro(a) e outros alcançaram o mesmo marco
- **THEN** a pendência dos outros aparece sem marca de esgotada, pronta para a entrega

#### Scenario: A entrega confirmada sai da fila

- **WHEN** o Mestre confirma a entrega pela aplicação
- **THEN** a pendência deixa de aparecer na fila

#### Scenario: A recusa da entrega é traduzida

- **WHEN** o núcleo recusa a entrega por falta de lastro no ponto de apoio
- **THEN** a aplicação diz em linguagem simples que falta o recurso naquele ponto de apoio, sem
  código de erro

#### Scenario: A fila não exibe imagem real nem custo

- **WHEN** a aplicação apresenta a fila de entregas pendentes
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhum campo traz valor em moedas ou
  em reais
