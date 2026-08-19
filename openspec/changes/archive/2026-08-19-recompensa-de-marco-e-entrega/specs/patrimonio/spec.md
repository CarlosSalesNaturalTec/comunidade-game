## MODIFIED Requirements

### Requirement: O saldo de natureza durável é inerte

O núcleo SHALL manter o saldo de tipo de recurso de natureza **durável** fora de toda operação
de consumo: ele NÃO SHALL ser reservável por aula, NÃO SHALL servir de lastro a item do
catálogo avulso e NÃO SHALL ser entregue como recompensa de marco. O aporte de tipo durável
SHALL creditar o Poder Sustentador do provedor como qualquer outro, e o seu único destino no
núcleo SHALL ser o **tombamento**. Nenhum lançamento de débito SHALL ser emitido por consumo de
tipo durável. (`RN-07-07`, `RF-07-11`, `RF-07-13`, PRD-07 §8, documento 04 §1, 02 §8.2)

#### Scenario: Aporte durável credita Poder Sustentador

- **WHEN** um aporte de tipo de recurso de natureza durável é registrado e homologado
- **THEN** o Poder Sustentador do provedor sobe pelo valor em moedas do aporte, como em
  qualquer outra natureza

#### Scenario: Saldo durável não é debitado por consumo

- **WHEN** um aporte de tipo durável credita saldo num ponto de apoio
- **THEN** nenhuma operação do núcleo emite lançamento de débito daquele tipo, e o saldo
  derivado permanece o creditado

#### Scenario: Durável não é entregue como recompensa de marco

- **WHEN** um Mestre confirma a entrega de uma recompensa de marco cujo tipo de recurso é de
  natureza durável
- **THEN** o núcleo recusa, nenhum débito é emitido e o saldo durável permanece o creditado
