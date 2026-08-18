## MODIFIED Requirements

### Requirement: O aporte declarado no pré-cadastro só credita ao ser registrado

O núcleo SHALL guardar em cada aporte a **origem do registro** — gestão ou pré-cadastro — e,
quando a origem for o pré-cadastro, a **solicitação de participação de origem** que o declarou.
O aporte declarado numa solicitação de participação NÃO SHALL creditar moeda alguma enquanto
existir apenas como declaração; o crédito SHALL nascer somente do registro do aporte por um
Admin, que é o ato de **homologação** e que converte o valor em moedas pela vigência da data.
Registrar mais de um aporte apontando a **mesma** solicitação de origem SHALL ser recusado com
**422**, para que a mesma declaração não credite duas vezes. (`RF-07-29`, `RF-07-30`,
`RN-07-21`, `RF-07-05`, PRD-07 §8)

#### Scenario: Declaração no pré-cadastro não credita

- **WHEN** uma solicitação de participação é registrada com aporte declarado e comprovante
- **THEN** nenhum lançamento é gerado e o saldo de todo tipo de recurso permanece como estava

#### Scenario: Registro pelo Admin homologa e credita

- **WHEN** um Admin registra o aporte apontando a solicitação de participação de origem
- **THEN** o núcleo grava o aporte com origem "pré-cadastro", converte em moedas pela vigência
  da data do aporte e gera o lançamento de crédito

#### Scenario: Mesma solicitação não credita duas vezes

- **WHEN** um segundo aporte é registrado apontando uma solicitação de origem já homologada
- **THEN** o núcleo responde 422 e nada é gravado
