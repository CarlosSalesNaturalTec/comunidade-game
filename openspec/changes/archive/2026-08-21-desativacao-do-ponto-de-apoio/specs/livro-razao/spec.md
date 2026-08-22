## ADDED Requirements

### Requirement: A transferência entre pontos de apoio é par de lançamentos

O núcleo SHALL expor a **transferência de recurso entre pontos de apoio** como operação de
**Admin** que grava, em uma única operação, um lançamento de **débito** no ponto de apoio de
origem e um lançamento de **crédito** no de destino, ambos com o mesmo **tipo de recurso**, a
mesma **quantidade**, as mesmas **moedas**, o mesmo **motivo** e a mesma autoria e momento. Os
dois lançamentos SHALL referenciar-se, de modo que a transferência seja legível como um fato
só.

A transferência NEVER SHALL usar a natureza **ajuste**, que é para corrigir erro de lançamento
e referencia o lançamento original: transferir não corrige nada, move recurso que existe. A
transferência SHALL ser recusada com **422** quando origem e destino forem o mesmo ponto de
apoio, quando a quantidade for menor ou igual a zero, quando o saldo do tipo na origem não
cobrir a quantidade, ou quando o ponto de apoio de destino estiver **inativo**. Como todo
lançamento, os dois são **somente inserção** e não se editam nem se apagam. (`RF-07-19`,
`RN-07-15`, `RN-07-04`, `RN-07-33`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Admin transfere recurso entre dois pontos de apoio

- **WHEN** um Admin em sessão transfere 5 unidades de um tipo de recurso de um ponto de apoio
  para outro, com motivo
- **THEN** o núcleo grava um débito de 5 na origem e um crédito de 5 no destino, com o mesmo
  motivo, o mesmo autor e o mesmo momento

#### Scenario: O saldo dos dois pontos acompanha a transferência

- **WHEN** o saldo de um tipo é 10 na origem e 2 no destino, e 4 unidades são transferidas
- **THEN** o saldo passa a 6 na origem e a 6 no destino

#### Scenario: Transferir mais do que há é recusado

- **WHEN** um Admin transfere quantidade maior que o saldo do tipo na origem
- **THEN** o núcleo responde 422 e nenhum dos dois lançamentos é gravado

#### Scenario: Origem igual ao destino é recusada

- **WHEN** chega uma transferência cuja origem e cujo destino são o mesmo ponto de apoio
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Destino inativo é recusado

- **WHEN** chega uma transferência cujo ponto de apoio de destino está inativo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre não transfere

- **WHEN** um Mestre em sessão tenta transferir recurso entre pontos de apoio
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A transferência não usa ajuste

- **WHEN** uma transferência é gravada
- **THEN** os dois lançamentos têm natureza débito e crédito, e nenhum deles é ajuste
