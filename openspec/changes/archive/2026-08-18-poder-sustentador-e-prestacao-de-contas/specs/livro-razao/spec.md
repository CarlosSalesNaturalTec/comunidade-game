## ADDED Requirements

### Requirement: O débito da baixa declara a aula que o consumiu

O núcleo SHALL gravar, no **lançamento de débito emitido pela baixa da reserva**, a **aula** que
consumiu o recurso — o atributo que o PRD-07 §8 define para `Lancamento` ao lado da natureza, do
tipo de recurso e do ponto de apoio. É o que torna o consumo por aula derivável do próprio
livro-razão, sem revalorar o consumo pela tabela de referência corrente.

A aula SHALL ser gravada **no ato** da baixa e SHALL seguir a imutabilidade que esta capacidade
já exige de todo atributo de lançamento: alterá-la depois SHALL ser recusado com **405**.
Lançamento de **crédito** NÃO SHALL declarar aula — ele vem de um aporte, e o caminho até o
provedor é o próprio aporte. Lançamento de **ajuste** NÃO SHALL declarar aula — ele referencia o
lançamento original. (`RF-07-16`, `RF-07-09`, `RN-07-15`, `RN-07-36`, PRD-07 §8)

#### Scenario: A baixa grava a aula no débito

- **WHEN** a atividade realizada é lançada e uma reserva vira baixa
- **THEN** o débito emitido guarda a aula que consumiu o recurso, junto do tipo de recurso, do
  ponto de apoio, da quantidade e das moedas

#### Scenario: O crédito do aporte não declara aula

- **WHEN** um aporte homologado gera o lançamento de crédito
- **THEN** o crédito é gravado sem aula, e o provedor dele segue alcançável pelo aporte

#### Scenario: A aula do lançamento não muda depois

- **WHEN** chega uma tentativa de alterar a aula de um débito já gravado
- **THEN** o núcleo responde 405 e o lançamento permanece exatamente como estava

#### Scenario: O consumo da aula é derivável do ledger

- **WHEN** uma aula deu baixa em dois tipos de recurso, em dois débitos
- **THEN** somar os débitos daquela aula devolve o consumo dela em moedas, pelo valor que cada
  débito gravou
