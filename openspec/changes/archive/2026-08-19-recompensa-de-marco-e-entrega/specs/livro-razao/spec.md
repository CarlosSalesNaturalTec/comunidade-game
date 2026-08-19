## MODIFIED Requirements

### Requirement: O débito da baixa declara a aula que o consumiu

O núcleo SHALL gravar, no **lançamento de débito emitido pela baixa da reserva**, a **aula** que
consumiu o recurso — o atributo que o PRD-07 §8 define para `Lancamento` ao lado da natureza, do
tipo de recurso e do ponto de apoio. É o que torna o consumo por aula derivável do próprio
livro-razão, sem revalorar o consumo pela tabela de referência corrente.

A aula SHALL ser gravada **no ato** da baixa e SHALL seguir a imutabilidade que esta capacidade
já exige de todo atributo de lançamento: alterá-la depois SHALL ser recusado com **405**.
Lançamento de **crédito** NÃO SHALL declarar aula — ele vem de um aporte, e o caminho até o
provedor é o próprio aporte. Lançamento de **ajuste** NÃO SHALL declarar aula — ele referencia o
lançamento original.

O débito tem **três origens**, e só a primeira declara aula. O débito emitido pela **troca por
recompensa avulsa** NÃO SHALL declarar aula, ainda que a troca guarde o encontro em que foi
entregue, e o débito emitido pela **entrega de recompensa de marco** NÃO SHALL declarar aula,
porque o marco é alcançado no percurso da trilha e não num encontro: `Lancamento.aula` significa
**a reserva daquela aula foi baixada**, e o consumo por troca e por entrega é derivável da
própria `Troca` e da própria entrega. É o que mantém `GET /prestacao-de-contas/aulas` medindo
consumo de atividade, sem somar a ele a recompensa que um Guerreiro(a) trocou nem a que ele
conquistou. O débito da troca SHALL declarar o **ponto de apoio do item** e o da entrega, o
**ponto de apoio da entrega**; ambos SHALL ser valorados em moedas pela vigência do valor de
referência na data, como o da baixa. (`RF-07-16`, `RF-07-09`, `RF-07-36`, `RF-07-13`,
`RN-07-15`, `RN-07-36`, PRD-07 §8)

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

#### Scenario: O débito da troca não declara aula

- **WHEN** uma troca por recompensa avulsa é entregue numa aula e emite o débito de uma unidade
- **THEN** o débito é gravado sem aula, no ponto de apoio do item, com a quantidade e as moedas

#### Scenario: A troca não entra no consumo por aula

- **WHEN** uma aula deu baixa numa reserva e, no mesmo encontro, uma troca foi entregue
- **THEN** o consumo daquela aula soma apenas o débito da baixa, e o débito da troca fica fora

#### Scenario: O débito da entrega de recompensa de marco não declara aula

- **WHEN** uma recompensa de marco é entregue e emite o débito da quantidade declarada
- **THEN** o débito é gravado sem aula, no ponto de apoio da entrega, com a quantidade e as
  moedas da vigência corrente

#### Scenario: A entrega não entra no consumo por aula

- **WHEN** uma aula deu baixa numa reserva e, no mesmo encontro, uma recompensa de marco foi
  entregue
- **THEN** o consumo daquela aula soma apenas o débito da baixa, e o débito da entrega fica fora
