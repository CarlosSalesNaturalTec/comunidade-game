## ADDED Requirements

### Requirement: As necessidades em aberto trazem a da recompensa com a trilha

A lista de necessidades em aberto da App 08 SHALL apresentar também a necessidade da
**recompensa de marco**, com a **trilha** no lugar da data e do horário da aula, o ponto de
apoio, a comunidade e o que falta em moedas, na ordem em que o núcleo a devolve. (`RF-14-24`,
`RF-07-54`, `RN-14-09`)

#### Scenario: A necessidade da recompensa aparece com a trilha

- **WHEN** o Apoiador abre as necessidades em aberto e há necessidade de recompensa
- **THEN** ela aparece com o recurso, a trilha, o ponto de apoio, a comunidade e o que falta em
  moedas

### Requirement: A declaração e o pré-cadastro aceitam a necessidade da recompensa

A declaração de aporte por necessidade SHALL oferecer também as necessidades de recompensa,
identificadas pela trilha, e SHALL enviar comunidade, trilha e tipo no lugar da aula. O
pré-cadastro SHALL oferecer a necessidade da recompensa entre as necessidades publicadas,
descrevendo-a pela trilha. (`RF-14-25`, `RF-14-02`, `RF-07-54`)

#### Scenario: O Apoiador declara pela necessidade da recompensa

- **WHEN** o Apoiador escolhe uma necessidade de recompensa na declaração
- **THEN** a aplicação envia comunidade, trilha e tipo, e a declaração entra pendente

#### Scenario: O pré-cadastro descreve a necessidade da recompensa pela trilha

- **WHEN** o visitante escolhe uma necessidade de recompensa no pré-cadastro
- **THEN** a tela a descreve pela trilha e mostra o equivalente em moedas
