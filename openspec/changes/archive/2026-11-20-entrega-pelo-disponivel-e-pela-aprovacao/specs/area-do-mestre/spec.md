## ADDED Requirements

### Requirement: A fila de entregas pendentes não pede o ponto de apoio

A fila de entregas pendentes da App 09 NEVER SHALL pedir o ponto de apoio: o núcleo tira o
recurso da aula imediatamente anterior da comunidade. A confirmação SHALL enviar só o
Guerreiro(a), e a recusa por falta de aula anterior SHALL ser dita em linguagem simples.
(`RF-09-76`, `RF-07-13`)

#### Scenario: A confirmação não tem seletor de ponto de apoio

- **WHEN** o Mestre abre a fila de entregas pendentes
- **THEN** a pendência oferece só a confirmação, sem seletor de ponto de apoio, e a confirmação
  envia apenas o Guerreiro(a)

### Requirement: A bancada de julgamento diz quando a aprovação entregou a recompensa

Julgado cumprido o prático, a bancada da App 09 SHALL dizer, quando a resposta trouxer
recompensa entregue, que a recompensa foi entregue no mesmo ato; sem recompensa entregue, SHALL
seguir como está. (`RF-09-146`, `RN-09-63`)

#### Scenario: A aprovação que entregou avisa

- **WHEN** o Mestre julga cumprido e o núcleo devolve uma recompensa entregue
- **THEN** a bancada diz que a recompensa foi entregue
