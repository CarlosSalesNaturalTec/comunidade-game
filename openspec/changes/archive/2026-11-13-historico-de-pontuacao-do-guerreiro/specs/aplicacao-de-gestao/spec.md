## ADDED Requirements

### Requirement: O Admin abre a ficha do Guerreiro(a) com o histórico de pontuação

A lista de Guerreiros e Guerreiras da App 03 SHALL abrir a **ficha** de cada um, com os
**saldos** — o regular de cada trilha ou poder e as duas contas de ponto extra, separadas e
rotuladas — e o **histórico de pontuação** do mais recente ao mais antigo: data, origem em
linguagem simples, valor com sinal, conta, trilha ou poder e, na ocorrência de conduta, o
motivo. Ponto regular e ponto extra SHALL aparecer cada um com o seu glifo, ficha e rótulo, e a
lista SHALL carregar mais lançamentos sob pedido. (`RF-02-116`, `RN-01-68`, documento 15 §9,
invariante 24)

#### Scenario: A lista leva à ficha

- **WHEN** o Admin escolhe um Guerreiro(a) na lista de Guerreiros e Guerreiras
- **THEN** a App 03 abre a ficha dele, com os saldos e o histórico de pontuação

#### Scenario: O histórico traz troca e estorno

- **WHEN** o histórico traz uma troca por recompensa avulsa e um estorno de presença
- **THEN** cada linha mostra a data, a origem e o valor negativo na conta que se moveu

#### Scenario: Ficha sem pontuação

- **WHEN** a ficha de um Guerreiro(a) que nunca pontuou é aberta
- **THEN** a App 03 mostra os saldos em zero e o aviso de que ainda não há lançamento
