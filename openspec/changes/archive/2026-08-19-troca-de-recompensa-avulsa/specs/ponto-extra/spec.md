## MODIFIED Requirements

### Requirement: Ponto extra vive em duas contas que nunca se confundem

O núcleo SHALL manter, por Guerreiro(a), duas contas de ponto extra: o **acumulado** — tudo o que
já foi ganho, que **nunca decresce** — e o **saldo disponível** — o que ainda não foi trocado, que
**nunca fica negativo**. O acumulado SHALL receber apenas crédito. O saldo disponível SHALL
receber crédito e **débito**, e o **único débito** previsto no Ciclo 01 é a **troca por
recompensa avulsa**, que debita o preço cobrado sem tocar o acumulado. Débito que deixaria o
saldo disponível negativo SHALL ser recusado, em qualquer via — inclusive fora do ORM.
(`RF-01-56`, `RN-01-39`, `RN-01-40`, `RF-07-36`, 11 §5, invariante 23)

#### Scenario: Crédito aumenta as duas contas juntas

- **WHEN** um Resultado credita ponto extra a um Guerreiro(a)
- **THEN** o núcleo aumenta o acumulado e o saldo disponível pelo mesmo valor

#### Scenario: Acumulado nunca decresce

- **WHEN** qualquer operação tenta reduzir o acumulado de pontos extras
- **THEN** o núcleo recusa a operação

#### Scenario: Saldo disponível nunca aceita valor negativo

- **WHEN** qualquer operação resultaria em saldo disponível negativo
- **THEN** o núcleo recusa a operação

#### Scenario: A troca debita só o saldo disponível

- **WHEN** uma troca por recompensa avulsa cobra 40 pontos extras de um Guerreiro(a) com
  acumulado 300 e saldo disponível 100
- **THEN** o saldo disponível passa a 60 e o acumulado permanece 300

#### Scenario: A troca não debita além do saldo disponível

- **WHEN** uma troca cobraria mais pontos extras do que o saldo disponível do Guerreiro(a)
- **THEN** o núcleo recusa o débito e o saldo permanece exatamente como estava
