## MODIFIED Requirements

### Requirement: O desfecho do Resultado é lançado pela gestão, em três valores fechados

O núcleo SHALL exigir, em todo Resultado, um **desfecho** entre exatamente três valores:
**realizada**, **realizada com mérito** ou **mérito extra por auxílio aos colegas** (11 §4).
Quem lança o desfecho é o **Mestre autor** da trilha a que a atividade pertence, ou um **Admin**
— a mesma matriz de posse que já vale para a trilha, a missão e a atividade (`RF-01-16`). Mestre
que não é o autor SHALL receber **403**. O desfecho SHALL ser gravado com a autoria de quem
lançou (`RN-01-13`).

Na **atividade avulsa**, que não pertence a missão nem a trilha, NÃO há posse de Mestre a
conferir: o lançamento SHALL ser restrito ao **Admin**, e Mestre em sessão SHALL receber **403**
qualquer que seja a trilha de que ele é autor. O crédito do ponto regular SHALL seguir o **poder
declarado** pela atividade, e não uma trilha. (`RF-01-20`, `RF-01-16`, `RF-01-03`, `RF-02-29`,
`RF-02-33`, 11 §4)

#### Scenario: Mestre autor lança desfecho "realizada com mérito"

- **WHEN** o Mestre autor da trilha lança o desfecho "realizada com mérito" para um Resultado
- **THEN** o núcleo grava o desfecho com a autoria, data e hora de quem lançou

#### Scenario: Desfecho fora dos três valores é recusado

- **WHEN** chega um Resultado com desfecho que não é nenhum dos três valores fechados
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta lançar o desfecho de um Resultado dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Admin lança o desfecho da atividade avulsa

- **WHEN** um Admin lança o desfecho de um Resultado de atividade avulsa
- **THEN** o núcleo grava o Resultado e credita o ponto regular no poder declarado pela
  atividade

#### Scenario: Mestre não lança atividade avulsa

- **WHEN** um Mestre em sessão tenta lançar o desfecho de um Resultado de atividade avulsa
- **THEN** o núcleo responde 403 e nada é gravado
