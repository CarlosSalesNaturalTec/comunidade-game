## ADDED Requirements

### Requirement: O Admin lê os aportes, o Poder Sustentador e as declarações pendentes de um provedor

O núcleo SHALL responder `GET /provedores/{id}/aportes` **somente ao Admin** em sessão; qualquer
outro papel SHALL ser recusado. A resposta SHALL trazer, do provedor:

- os **aportes homologados**, do mais recente ao mais antigo, cada um com a data, o nome e a
  unidade do tipo de recurso, a quantidade, o valor **em moedas**, o ponto de apoio, a forma, a
  destinação, a marca de **tem comprovante** e o **valor de origem em reais** quando registrado;
- o **Poder Sustentador** em moedas, pela mesma derivação da leitura pública;
- as **declarações pendentes** feitas pela App 08, cada uma com a data, o valor declarado e a
  origem da escolha.

A resposta NEVER SHALL trazer o comprovante, o endereço dele no armazenamento nem dado
bancário. A declaração homologada ou recusada NÃO SHALL aparecer entre as pendentes, e a
pendente NÃO SHALL somar no Poder Sustentador. A rota SHALL responder **404** para persona de
Guerreiro(a) ou de responsável e para identificador inexistente, com a mesma recusa nos dois
casos. A rota é só de leitura. (`RF-02-120`, `RN-02-36`, `RF-07-17`, `RN-07-06`, `RN-07-22`,
`RN-14-07`, PRD-07 §11)

#### Scenario: O Admin lê os aportes de um Apoiador

- **WHEN** um Admin em sessão consulta os aportes de um Apoiador com dois aportes homologados
- **THEN** o núcleo devolve os dois, do mais recente ao mais antigo, com os campos de cada um, e
  o Poder Sustentador dele em moedas

#### Scenario: O valor de origem em reais sai ao Admin

- **WHEN** o aporte consultado tem valor de origem em reais registrado
- **THEN** a resposta ao Admin traz esse valor ao lado do valor em moedas

#### Scenario: O comprovante aparece só como marca

- **WHEN** o aporte consultado tem comprovante anexado
- **THEN** a resposta diz que há comprovante e não traz o arquivo nem o endereço dele

#### Scenario: A declaração pendente sai separada

- **WHEN** o Apoiador tem uma declaração pendente, uma recusada e um aporte homologado
- **THEN** a resposta traz a pendente na lista das declarações, deixa a recusada de fora, e o
  Poder Sustentador não soma a pendente

#### Scenario: O Mestre provedor também é lido

- **WHEN** um Admin consulta um Mestre que registrou aporte por absorção
- **THEN** o núcleo devolve esse aporte, com forma absorção, e o Poder Sustentador dele

#### Scenario: Outro papel é recusado

- **WHEN** um Mestre ou um Apoiador em sessão consulta os aportes de um provedor
- **THEN** o núcleo recusa, e nada do provedor é devolvido

#### Scenario: A rota não serve Guerreiro(a)

- **WHEN** um Admin consulta pelo identificador de uma persona de Guerreiro(a)
- **THEN** o núcleo responde 404, com a mesma recusa que daria a um identificador inexistente
