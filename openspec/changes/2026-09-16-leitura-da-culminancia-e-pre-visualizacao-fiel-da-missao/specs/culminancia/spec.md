## ADDED Requirements

### Requirement: A culminância declarada volta ao Mestre autor

A culminância gravada SHALL ser legível pelo **Mestre autor** da trilha, em qualquer situação
dela — rascunho, publicada ou despublicada —, pela leitura das trilhas próprias de que trata
`trilha-e-missao`. A leitura SHALL trazer a **descrição**, a **modalidade** e o **critério de
validação** tais como gravados, para que o autor possa relê-los e substituí-los sem
redigitá-los. Trilha sem culminância SHALL ser distinguível de trilha cuja culminância não foi
lida: a ausência SHALL ser dita, nunca suposta. A declaração continua privativa do Mestre
autor, e a leitura NEVER SHALL alcançar a culminância de trilha de outro Mestre. (`RF-09-29`,
`RF-09-30`, `RF-09-04`)

#### Scenario: O autor relê a culminância em sessão nova

- **WHEN** o Mestre autor declarou a culminância de uma trilha e volta a ela em sessão nova
- **THEN** a descrição, a modalidade e o critério de validação gravados chegam a ele

#### Scenario: A culminância de trilha em rascunho é legível pelo autor

- **WHEN** o Mestre autor lê uma trilha em rascunho que tem culminância declarada
- **THEN** a culminância chega a ele, ainda que a leitura pública nunca sirva essa trilha

#### Scenario: A culminância de outro Mestre não sai

- **WHEN** um Mestre lê as próprias trilhas e outro Mestre tem trilha com culminância
  declarada
- **THEN** a culminância do outro Mestre não é devolvida

#### Scenario: Trilha sem culminância diz que não tem

- **WHEN** o Mestre autor lê uma trilha que nunca teve culminância declarada
- **THEN** a leitura afirma a ausência da culminância, e não a omite nem responde erro
