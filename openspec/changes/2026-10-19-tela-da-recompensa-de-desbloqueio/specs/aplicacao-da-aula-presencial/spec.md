# Spec Delta

## ADDED Requirements

### Requirement: A recompensa conquistada entra antes da próxima missão no aparelho do encontro

No caminho das trilhas e missões, alcançado o marco que concede recompensa, a aplicação SHALL
apresentar a **tela da recompensa** **antes** da próxima missão, e NEVER SHALL levar o
Guerreiro(a) direto à missão seguinte. A tela SHALL trazer, de cima para baixo: o **trio de
estrelas**, o **nome do que foi conquistado** com a quantidade, o aviso em linguagem simples de
que **a entrega é confirmada pelo Mestre** no encontro, e o controle de **avançar**, que leva à
próxima missão. (`RF-04-72`, `RF-04-73`, `RF-05-45`)

#### Scenario: A sondagem respondida no encontro apresenta a recompensa do marco

- **WHEN** o Guerreiro(a) responde no aparelho do encontro a missão de sondagem que é marco com
  recompensa declarada
- **THEN** a tela da recompensa é apresentada antes da próxima missão, com o trio de estrelas, o
  nome do recurso, a quantidade e o aviso de que o Mestre confirma a entrega

#### Scenario: O quiz que desbloqueia no encontro apresenta a recompensa do marco

- **WHEN** o Guerreiro(a) passa, no aparelho do encontro, no quiz do desbloqueio de uma missão
  que é marco com recompensa
- **THEN** a tela da recompensa é apresentada antes da missão seguinte

#### Scenario: Avançar leva à próxima missão

- **WHEN** o Guerreiro(a) aciona avançar na tela da recompensa
- **THEN** a próxima missão do percurso é apresentada

#### Scenario: Marco sem recompensa não interrompe o percurso

- **WHEN** o Guerreiro(a) desbloqueia uma missão que não tem recompensa declarada
- **THEN** nenhuma tela de recompensa é apresentada, e a próxima missão abre como já abria

#### Scenario: A tela não vende nem mostra custo

- **WHEN** a tela da recompensa é apresentada
- **THEN** nenhum caminho de adquirir a recompensa é oferecido, nenhum ponto é debitado e nenhum
  valor em moedas ou em reais aparece

### Requirement: A tela da recompensa aparece uma vez, e no prático só depois do Mestre

A tela da recompensa SHALL ser apresentada **uma vez** por recompensa conquistada: avançar
SHALL dar **ciência** dela, e a tela NEVER SHALL voltar a interromper o percurso depois disso,
ainda que a entrega siga aguardando o Mestre. A ciência dada num aparelho SHALL valer em
qualquer outro e na Área do Guerreiro(a), porque é fato do Guerreiro(a) e não do aparelho — o
aparelho do encontro é compartilhado, e NEVER SHALL guardar no próprio navegador o que já foi
avisado. Sendo o desbloqueio **desafio prático**, a tela NEVER SHALL ser apresentada antes de o
**Mestre autor** julgar que o Guerreiro(a) passou. (`RF-04-73`, `RF-05-14`, `RF-05-45`,
`RN-05-50`)

#### Scenario: Voltar à trilha não reapresenta a recompensa

- **WHEN** o Guerreiro(a) avança na tela da recompensa e volta à trilha no mesmo atendimento
- **THEN** a tela não é apresentada de novo, e o percurso abre na missão

#### Scenario: A ciência não se perde no aparelho compartilhado

- **WHEN** o Guerreiro(a) deu ciência num aparelho do encontro e abre a trilha noutro aparelho,
  ou na Área do Guerreiro(a)
- **THEN** a tela da recompensa não é apresentada de novo

#### Scenario: O prático não julgado não apresenta recompensa

- **WHEN** o Guerreiro(a) declarou no encontro ter cumprido o desafio prático de missão que é
  marco com recompensa e o Mestre autor ainda não julgou
- **THEN** nenhuma tela de recompensa é apresentada, e o percurso diz que a missão aguarda o
  Mestre

#### Scenario: Julgado o prático, a recompensa aparece na volta

- **WHEN** o Mestre autor julga que o Guerreiro(a) passou e ele volta à trilha depois, no mesmo
  encontro ou noutro
- **THEN** a tela da recompensa é apresentada antes da próxima missão

#### Scenario: Duas recompensas conquistadas saem uma por tela

- **WHEN** o Guerreiro(a) tem duas recompensas conquistadas sem ciência
- **THEN** cada uma é apresentada na sua própria tela, em sequência, e o último avançar leva à
  missão

### Requirement: Sem rede, a tela da recompensa não abre nem enfileira a ciência

O caminho das trilhas e missões já exige rede, e a tela da recompensa SHALL seguir a mesma
regra: sem rede ela NEVER SHALL ser apresentada, e a ciência NEVER SHALL ser enfileirada no
aparelho para sincronizar depois — a fila local do aparelho é da **presença**, e ciência
guardada fora do núcleo arriscaria consumir o aviso sem que a criança o tivesse visto.
(`RF-04-23`, `RF-04-72`, `RN-05-50`)

#### Scenario: Sem rede o caminho não abre

- **WHEN** a rede está fora e o Guerreiro(a) escolhe trilhas e missões
- **THEN** a aplicação diz que o caminho precisa de rede, e nenhuma tela de recompensa é
  apresentada

#### Scenario: A ciência não entra na fila local

- **WHEN** se procura no aparelho um caminho de guardar a ciência para sincronizar depois
- **THEN** nenhum existe: a fila local é da presença, e a ciência só se grava com rede
