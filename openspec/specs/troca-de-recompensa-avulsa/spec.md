## Purpose

A troca de pontos extras por item do catálogo avulso: o ato do Guerreiro(a) que o Mestre
entrega no encontro, o preço cobrado na data, as recusas que protegem o lastro e o saldo, e o
histórico que guarda o que foi cobrado. É o único débito de ponto extra do Ciclo 01.

## Requirements

### Requirement: A troca é registrada pelo Mestre na aula em que entrega

O núcleo SHALL registrar a **troca** com **item do catálogo avulso**, **Guerreiro(a)**, **preço
em pontos extras cobrado**, **encontro**, **Mestre que entregou** e **data e hora com fuso**. O
encontro SHALL ser a **`Aula`**, e o núcleo NÃO SHALL verificar o estado dela nem a presença do
Guerreiro(a) nela: o momento da troca é garantia da App 01, como a janela de troca do
`RF-04-49` já é. Registrar troca SHALL exigir persona **Mestre** em sessão, vinculado à
comunidade da aula; **Admin**, **Apoiador**, **Guerreiro(a)** e **responsável** SHALL receber
**403**. Registro sem item, sem Guerreiro(a) ou sem aula SHALL ser recusado com **422**,
indicando o campo em falta. (`RF-07-35`, `RF-01-16`, `RF-01-27`, 02 §8.2, PRD-07 §§8, 9)

#### Scenario: Mestre registra a troca na aula

- **WHEN** um Mestre vinculado à comunidade da aula registra a troca de um item por um
  Guerreiro(a)
- **THEN** o núcleo grava a troca com item, Guerreiro(a), preço cobrado, aula, o Mestre que
  entregou e a data e hora com fuso

#### Scenario: O núcleo não verifica o estado da aula

- **WHEN** um Mestre registra a troca numa aula que ainda não foi lançada como realizada
- **THEN** o núcleo grava a troca, sem verificar o estado da aula

#### Scenario: O núcleo não exige presença do Guerreiro(a)

- **WHEN** um Mestre registra a troca de um Guerreiro(a) sem presença registrada naquela aula
- **THEN** o núcleo grava a troca, sem verificar a presença

#### Scenario: Mestre de outra comunidade não registra a troca

- **WHEN** um Mestre em sessão tenta registrar troca numa aula de comunidade a que não está
  vinculado
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Guerreiro(a) não registra a própria troca

- **WHEN** um Guerreiro(a) em sessão tenta registrar uma troca
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Registro sem item é recusado

- **WHEN** chega um registro de troca sem o item do catálogo
- **THEN** o núcleo responde 422 indicando o campo em falta, e nada é gravado

### Requirement: O preço cobrado é o da vigência corrente na data da troca

O núcleo SHALL cobrar o **preço de referência em pontos extras vigente na data da troca** para o
tipo de recurso do item, e SHALL **gravar esse preço na troca**, para que mudança posterior da
tabela não reescreva o histórico. O registro da troca NEVER SHALL aceitar preço informado por
quem registra: preço declarado SHALL ser recusado com **422**. Troca de item cujo tipo de
recurso não tem preço de referência vigente na data SHALL ser recusada com **422**, dizendo que
falta o preço. O preço NEVER SHALL derivar do valor em moedas nem de valor em reais.
(`RF-07-46`, `RF-07-38`, `RN-07-25`, `RN-07-29`, `RN-07-24`, invariante 23)

#### Scenario: A troca cobra o preço da vigência corrente

- **WHEN** um Mestre registra a troca de um item cujo tipo de recurso tem preço de referência
  vigente de 40 pontos extras
- **THEN** o núcleo cobra 40 e grava 40 como preço cobrado da troca

#### Scenario: Mudança posterior da tabela não altera a troca gravada

- **WHEN** o preço de referência do tipo de recurso passa de 40 para 60 depois de uma troca
  registrada por 40
- **THEN** a troca já gravada segue com preço cobrado 40

#### Scenario: Preço informado no registro é recusado

- **WHEN** chega um registro de troca declarando o preço em pontos extras
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Item de tipo sem preço vigente não é trocado

- **WHEN** um Mestre registra a troca de um item cujo tipo de recurso não tem preço de
  referência vigente na data
- **THEN** o núcleo responde 422 dizendo que falta o preço de referência, e nada é gravado

### Requirement: Quatro condições recusam a troca antes de qualquer escrita

O núcleo SHALL recusar a troca com **422**, sem gravar nada e sem mover saldo algum, quando:

1. o item estiver **inativo** ou o **lastro** não se confirmar no ato — a quantidade disponível
   do tipo de recurso do item no ponto de apoio dele for **menor que 1**;
2. o **estoque** do item for **zero**;
3. o Guerreiro(a) **não pertencer à comunidade do item**;
4. o **saldo disponível** de pontos extras do Guerreiro(a) for **menor que o preço cobrado**.

A resposta SHALL dizer qual das condições recusou. O lastro SHALL ser reverificado **no ato da
troca**, e não apenas lido da marca de ativo do item, porque o saldo pode ter caído desde a
ativação. (`RF-07-37`, `RN-07-26`, `RN-07-30`, `RN-01-40`, invariantes 9 e 23, 02 §8.2)

#### Scenario: Item inativo não é trocado

- **WHEN** um Mestre registra a troca de um item marcado inativo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Lastro é reverificado no ato

- **WHEN** um Mestre registra a troca de um item ativo cujo saldo disponível do tipo no ponto de
  apoio do item caiu a zero desde a ativação
- **THEN** o núcleo responde 422 dizendo que falta lastro, e nada é gravado

#### Scenario: Item sem estoque não é trocado

- **WHEN** um Mestre registra a troca de um item cujo estoque é zero
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Guerreiro(a) de outra comunidade não troca

- **WHEN** um Mestre registra a troca de um item por um Guerreiro(a) de comunidade diferente da
  do item
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Saldo de pontos extras menor que o preço recusa a troca

- **WHEN** um Mestre registra a troca de um item de 40 pontos extras por um Guerreiro(a) cujo
  saldo disponível é 25
- **THEN** o núcleo responde 422 dizendo que falta saldo, e nem o estoque nem o saldo mudam

#### Scenario: Recusa não move nada

- **WHEN** qualquer das quatro condições recusa a troca
- **THEN** nenhuma troca é gravada, nenhum lançamento é emitido, o estoque do item segue como
  estava e o saldo de pontos extras do Guerreiro(a) segue como estava

### Requirement: A entrega é imediata e acontece numa operação só

O núcleo SHALL executar, numa **única operação atômica**, a gravação da troca, o **débito do
saldo disponível** de pontos extras do Guerreiro(a) pelo preço cobrado, o **decremento de uma
unidade** no estoque do item e o **lançamento de débito** de **uma unidade** do tipo de recurso
do item no **ponto de apoio do item**, valorado em moedas pela vigência do valor de referência
na data. Falhando qualquer parte, nenhuma SHALL persistir. O **acumulado** de pontos extras
NEVER SHALL ser tocado. NÃO SHALL existir estado intermediário entre a escolha e a entrega: a
troca NEVER SHALL reservar item entre encontros. (`RF-07-36`, `RN-07-27`, `RF-01-56`,
`RN-01-39`, `RN-01-40`, `RN-07-36`, invariante 23, 02 §8.2)

#### Scenario: A troca move as quatro coisas juntas

- **WHEN** uma troca de 40 pontos extras é registrada para um item de estoque 5, num ponto de
  apoio cujo saldo do tipo é 5, para um Guerreiro(a) de saldo disponível 100 e acumulado 300
- **THEN** o núcleo grava a troca, o saldo disponível passa a 60, o estoque do item passa a 4, o
  saldo do tipo naquele ponto de apoio passa a 4 e o acumulado segue 300

#### Scenario: O acumulado não decresce na troca

- **WHEN** uma troca debita o saldo disponível de pontos extras de um Guerreiro(a)
- **THEN** o acumulado dele permanece exatamente como estava

#### Scenario: Falha em qualquer parte desfaz tudo

- **WHEN** o lançamento de débito no livro-razão falha durante o registro da troca
- **THEN** a troca não é gravada, o estoque não decresce e o saldo de pontos extras não muda

#### Scenario: A troca não reserva item

- **WHEN** uma troca é registrada
- **THEN** nenhuma reserva de item é criada, e o item segue disponível a outro Guerreiro(a) até
  o estoque acabar

### Requirement: O histórico da troca é lido sem moedas e sem reais

O núcleo SHALL devolver o histórico de trocas com item, Guerreiro(a), **preço cobrado em pontos
extras**, aula, Mestre que entregou e data. A leitura SHALL exigir persona em sessão:
**Guerreiro(a)** SHALL ler apenas as **próprias** trocas, **Mestre** as das comunidades a que
está vinculado e **Admin** as de qualquer comunidade; **Apoiador** e **responsável** SHALL
receber **403**. NEVER SHALL a resposta trazer valor em moedas nem em reais — o custo real fica
no livro-razão, invisível para a criança. (`RF-07-35`, `RF-07-46`, `RN-07-24`, `RN-07-13`,
invariante 23, 02 §8.2)

#### Scenario: Guerreiro(a) lê as próprias trocas

- **WHEN** um Guerreiro(a) em sessão consulta o histórico de trocas
- **THEN** o núcleo devolve apenas as trocas dele, com item, preço cobrado em pontos extras,
  aula e data

#### Scenario: Troca de outro Guerreiro(a) não aparece

- **WHEN** um Guerreiro(a) em sessão consulta o histórico de trocas e há trocas de outros
- **THEN** as trocas dos outros NEVER aparecem na resposta

#### Scenario: Mestre lê as trocas das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade consulta o histórico de trocas
- **THEN** o núcleo devolve as trocas daquela comunidade, e nenhuma de comunidade a que ele não
  está vinculado

#### Scenario: Nenhuma leitura da troca devolve moedas nem reais

- **WHEN** o histórico de trocas é consultado por qualquer persona
- **THEN** a resposta traz o preço em pontos extras, e NEVER traz valor em moedas nem em reais

#### Scenario: Apoiador não lê trocas

- **WHEN** um Apoiador em sessão consulta o histórico de trocas
- **THEN** o núcleo responde 403
