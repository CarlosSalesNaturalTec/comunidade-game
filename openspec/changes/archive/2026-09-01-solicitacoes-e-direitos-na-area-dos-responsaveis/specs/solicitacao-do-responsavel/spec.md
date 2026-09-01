## MODIFIED Requirements

### Requirement: O desfecho registra o tratamento e não executa o pedido por si

O desfecho gravado nesta fila SHALL ser **registro do tratamento**, e NEVER SHALL, por si só,
apagar, despersonalizar ou alterar dado do Guerreiro(a) — **com uma exceção**: o desfecho
**aceito** de uma solicitação do tipo **exclusão** SHALL marcar o _template_ biométrico daquele
Guerreiro(a) para apagamento em **5 dias** (`RF-13-43`, `RN-13-22`). É a única execução que o
desfecho dispara, e ela alcança apenas o _template_.

A **despersonalização do registro de dado do território** (`RN-13-12`) NEVER SHALL ser presumida
como efeito do desfecho: ela é o **limite declarado** que a App 07 apresenta antes do aceite, e a
sua execução ficou para o Ciclo 02 (decisão do fundador, 2026-09-01, documento 09 §1). Desfecho
**recusado**, e desfecho aceito de qualquer outro tipo, NEVER SHALL marcar apagamento algum.
(`RF-02-24`, `RF-13-43`, `RN-13-12`, `RN-13-22`)

#### Scenario: Desfecho aceito de exclusão marca o _template_

- **WHEN** o Admin registra o desfecho aceito de uma solicitação de exclusão de um Guerreiro(a)
  com _template_ gravado
- **THEN** o núcleo grava o desfecho e o _template_ fica marcado para apagamento em 5 dias

#### Scenario: Desfecho de exclusão não apaga nada por si

- **WHEN** o Admin registra o desfecho aceito de uma solicitação de exclusão
- **THEN** nenhum registro de território é apagado nem despersonalizado, e nenhum outro dado do
  Guerreiro(a) é alterado por esse ato

#### Scenario: Desfecho recusado não marca nada

- **WHEN** o Admin registra o desfecho recusado de uma solicitação de exclusão
- **THEN** o desfecho é gravado e nenhum _template_ é marcado para apagamento

#### Scenario: Desfecho de outro tipo não marca nada

- **WHEN** o Admin aceita uma solicitação de acesso, correção ou esclarecimento
- **THEN** o desfecho é gravado e nenhum _template_ é marcado para apagamento
