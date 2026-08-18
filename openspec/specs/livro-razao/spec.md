## Purpose

O registro contábil da plataforma: cada entrada e cada saída de recurso vira um lançamento que
nunca se apaga nem se edita, e o saldo de cada tipo de recurso em cada ponto de apoio é sempre
recontado a partir deles. É o que torna a prestação de contas auditável e o que autoriza ou
barra a atividade que precisa de lastro.

## Requirements

### Requirement: O lançamento é somente inserção

O núcleo SHALL registrar cada movimento de recurso como um **lançamento** com **natureza**
— crédito, débito ou ajuste —, **tipo de recurso**, **ponto de apoio**, **quantidade**, valor em
**moedas**, autor e data e hora com fuso. O lançamento gravado SHALL ser imutável: alterar
qualquer atributo dele SHALL ser recusado com **405**, e remover um lançamento SHALL ser
recusado por qualquer via, dentro ou fora do ORM. A quantidade e as moedas SHALL ser guardadas
em decimal exato de duas casas. (`RF-07-19`, `RN-07-15`, `RN-07-04`, `RF-01-03`, `RF-01-27`,
PRD-07 §8)

#### Scenario: Lançamento nasce com autoria e momento

- **WHEN** o núcleo registra um lançamento a partir de um aporte homologado
- **THEN** o lançamento guarda natureza, tipo de recurso, ponto de apoio, quantidade, moedas,
  o autor da operação e a data e hora com fuso

#### Scenario: Edição de lançamento é recusada

- **WHEN** chega uma tentativa de alterar um lançamento já gravado
- **THEN** o núcleo responde 405 e o lançamento permanece exatamente como estava

#### Scenario: Remoção de lançamento é recusada fora do ORM

- **WHEN** uma remoção de lançamento é tentada diretamente no banco, sem passar pelo núcleo
- **THEN** o banco recusa a operação e o lançamento permanece gravado

### Requirement: A correção se faz por lançamento de ajuste

O núcleo SHALL corrigir erro de lançamento apenas por **lançamento de ajuste**, que SHALL
referenciar o lançamento original e SHALL guardar **motivo** e **autor**. Lançar ajuste SHALL
exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL receber **403**.
Ajuste sem motivo SHALL ser recusado com **422**, e ajuste que referencie lançamento inexistente
SHALL ser recusado com **422**. O lançamento original SHALL permanecer intacto após o ajuste.
(`RF-07-19`, `RN-07-15`, `RF-01-16`, `RF-01-03`, PRD-07 §9)

#### Scenario: Admin lança ajuste sobre um lançamento errado

- **WHEN** um Admin em sessão lança um ajuste referenciando um lançamento existente, com motivo
- **THEN** o núcleo grava o ajuste com a referência, o motivo, o autor e o momento, e o
  lançamento original segue gravado sem alteração

#### Scenario: Ajuste sem motivo é recusado

- **WHEN** chega um ajuste sem motivo
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Mestre não lança ajuste

- **WHEN** um Mestre em sessão tenta lançar um ajuste
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O saldo é derivado por tipo de recurso e ponto de apoio

O núcleo SHALL manter o **saldo de cada tipo de recurso em cada ponto de apoio** como valor
**derivado dos lançamentos**, nunca como número editável. O saldo SHALL somar os créditos,
subtrair os débitos e aplicar os ajustes daquele par tipo/ponto de apoio, e recontar os
lançamentos SHALL devolver o mesmo número. Lançamento creditado a um ponto de apoio NÃO SHALL
compor o saldo de outro ponto de apoio.

O núcleo SHALL distinguir, sobre esse saldo, a **quantidade reservada** — comprometida por
reservas ainda no estado reservada — e a **quantidade disponível**, que é o saldo menos a
reservada. A reserva NÃO SHALL alterar o saldo derivado: só o lançamento o move, e o débito da
baixa é o que faz o saldo cair quando o recurso é de fato consumido. (`RF-07-07`, `RN-07-36`,
`RF-07-08`, `RF-07-09`, PRD-07 §§8, 10, 12)

#### Scenario: Saldo soma os lançamentos do par tipo e ponto de apoio

- **WHEN** dois aportes do mesmo tipo entram no mesmo ponto de apoio, com quantidades 3 e 2
- **THEN** o saldo daquele tipo naquele ponto de apoio é 5

#### Scenario: Ponto de apoio não empresta saldo a outro

- **WHEN** um aporte de um tipo entra no ponto de apoio A e nenhum entra no ponto de apoio B
- **THEN** o saldo daquele tipo no ponto de apoio B é zero, e o do ponto de apoio A é o
  aportado

#### Scenario: Recontagem devolve o mesmo saldo

- **WHEN** o saldo de um par tipo/ponto de apoio é recalculado a partir dos lançamentos
- **THEN** o número devolvido é igual ao anterior, sem depender de estado guardado à parte

#### Scenario: Ajuste entra na conta do saldo

- **WHEN** um ajuste é lançado sobre um crédito de quantidade 3, corrigindo-o em -1
- **THEN** o saldo daquele tipo naquele ponto de apoio passa a 2

#### Scenario: Reserva reduz a disponível e não o saldo

- **WHEN** uma aula reserva 4 de um tipo cujo saldo no ponto de apoio é 10
- **THEN** o saldo segue 10 e a quantidade disponível é 6

#### Scenario: A baixa é o que faz o saldo cair

- **WHEN** a atividade realizada é lançada e a reserva de 4 vira débito
- **THEN** o saldo passa a 6 e a quantidade reservada volta a zero

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
