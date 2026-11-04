# Spec Delta

## ADDED Requirements

### Requirement: A mídia da criação original pública é servida sob o mesmo portão da listagem

O núcleo SHALL servir, **sem sessão**, os bytes da mídia de uma criação original que satisfaça
o **mesmo portão** do portfólio público: situação **validada** e **todos** os creditados com
autorização vigente. Criação que não o satisfaça SHALL responder **404**, nunca 403.
(`RF-01-81`, `RN-01-63`, `RN-01-13`, `RN-03-02`, `RF-03-08`)

#### Scenario: A mídia da criação pública é servida sem sessão

- **WHEN** um visitante sem sessão pede a mídia de uma criação original validada cujos
  creditados têm autorização vigente
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: Criação com creditado sem autorização responde 404

- **WHEN** um visitante pede a mídia de uma criação original cujos creditados não têm todos
  autorização vigente
- **THEN** o núcleo responde 404, e nenhum byte é servido

#### Scenario: Criação ainda não validada responde 404

- **WHEN** um visitante pede a mídia de uma criação original entregue ou devolvida
- **THEN** o núcleo responde 404

#### Scenario: A recusa não distingue o inexistente do não autorizado

- **WHEN** um visitante pede a mídia de uma criação que não existe e a de uma que existe e não
  passa no portão
- **THEN** as duas respostas são indistinguíveis no corpo e no código

#### Scenario: A autorização revogada tira a mídia do ar na leitura seguinte

- **WHEN** a autorização de um creditado é revogada e a mídia da criação é pedida de novo
- **THEN** o núcleo responde 404, sem depender de nenhum ato de limpeza
