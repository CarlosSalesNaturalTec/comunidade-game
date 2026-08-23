## Purpose

A ocorrência de conduta é o registro do fato de má conduta lançado pelo Mestre autor da
atividade ou pelo Admin, e a única causa de débito de ponto regular fora do estorno de coleta
invalidada. Guarda data, autor, motivo, aula, atividade e Guerreiro(a), e o motivo tem prazo de
guarda próprio, menor que o do lançamento.

## ADDED Requirements

### Requirement: A ocorrência de conduta vale 5 pontos, e ninguém arbitra o valor

O núcleo SHALL debitar **5 pontos regulares** por ocorrência de conduta. O valor vem da tabela
do documento 11 §5, **única fonte do valor**, e NEVER SHALL ser declarado por quem lança:
requisição que traga um valor SHALL ser recusada com **422**.

O débito SHALL respeitar o **teto de 10 pontos por Guerreiro(a) e por aula presencial**. A
terceira ocorrência do mesmo Guerreiro(a) na mesma aula presencial SHALL ser recusada com
**422**, dizendo que o teto da aula foi alcançado. O teto é por pessoa: a ocorrência de um
Guerreiro(a) NEVER SHALL consumir o teto de outro. (`RF-09-46`, `RF-01-57`, 11 §5)

#### Scenario: A ocorrência debita exatamente 5 pontos

- **WHEN** o Mestre autor lança uma ocorrência de conduta contra um Guerreiro(a)
- **THEN** o núcleo debita 5 pontos regulares, sem que o valor tenha sido informado

#### Scenario: Requisição que declara valor é recusada

- **WHEN** chega uma ocorrência de conduta que traz o valor do débito
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: A terceira ocorrência na mesma aula é recusada

- **WHEN** um Guerreiro(a) já tem duas ocorrências de conduta numa aula presencial e uma
  terceira é lançada
- **THEN** o núcleo responde 422 dizendo que o teto da aula foi alcançado, e nada é gravado

#### Scenario: O teto de um Guerreiro(a) não alcança o outro

- **WHEN** um Guerreiro(a) já alcançou o teto de 10 na aula e outro recebe a primeira
  ocorrência dela
- **THEN** o núcleo grava a ocorrência do segundo normalmente

### Requirement: A ocorrência declara a atividade, e é dela que vem a trilha do débito

O núcleo SHALL exigir, em toda ocorrência de conduta, a **aula** em que aconteceu e a
**atividade** a que se refere. A **trilha** que sofre o débito SHALL ser derivada de atividade →
missão → trilha, nunca declarada pelo cliente: é o que dá sentido a "pontuação negativa das
**suas atividades**" do PRD-01 §4.

Quem lança é o **Mestre autor** da trilha da atividade ou um **Admin**. Mestre que não é o autor
SHALL receber **403**, pela mesma conferência de posse que vale para o lançamento do Resultado
(`RN-09-08`). Ocorrência cuja atividade não pertence à aula declarada SHALL ser recusada com
**422**.

O **motivo** é texto livre e SHALL ser exigido: ocorrência sem motivo SHALL ser recusada com
**422**. O núcleo NEVER SHALL exigir item de catálogo do Código de Conduta nesta operação — o
item é requisito da App 03 (`RF-02-38`). O lançamento SHALL ser efetivado **no ato**, sem
revisão de terceiro (`RN-09-09`). (`RF-09-46`, `RF-01-57`, `RF-01-16`, `RN-09-08`, `RN-09-09`)

#### Scenario: O Mestre autor lança e a ocorrência vale na hora

- **WHEN** o Mestre autor da trilha lança uma ocorrência de conduta declarando a aula, a
  atividade e o motivo
- **THEN** o núcleo grava a ocorrência com a autoria dele e a efetiva no ato, sem fila de
  revisão e sem intervenção de Admin

#### Scenario: O débito vai à trilha da atividade

- **WHEN** uma ocorrência de conduta é lançada sobre uma atividade da trilha 1
- **THEN** o núcleo debita o ponto regular do Guerreiro(a) na trilha 1, e em nenhuma outra

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha da atividade tenta lançar a ocorrência
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Ocorrência sem motivo é recusada

- **WHEN** chega uma ocorrência de conduta sem motivo, ou com motivo em branco
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Atividade que não é da aula é recusada

- **WHEN** chega uma ocorrência cuja atividade não pertence à aula declarada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: A ocorrência entra na trilha de auditoria com o nome de quem lançou

- **WHEN** uma ocorrência de conduta é gravada com sucesso
- **THEN** ela aparece na trilha de auditoria com autor, papel, data e hora

### Requirement: O débito da conduta não desfaz percurso

O débito da ocorrência SHALL parar em **zero** quando for maior que o saldo da trilha — o saldo
NEVER SHALL ficar negativo. Ele NEVER SHALL derrubar **nível** já certificado nem **badge** já
concedido, e NEVER SHALL alcançar o saldo de **pontos extras**. (`RF-09-46`, `RF-01-69`,
`RN-01-55`, 11 §5)

#### Scenario: Débito maior que o saldo para em zero

- **WHEN** uma ocorrência é lançada contra um Guerreiro(a) com 3 pontos regulares na trilha
- **THEN** o núcleo deixa o saldo em zero, e ele não fica negativo

#### Scenario: O nível já alcançado permanece

- **WHEN** o débito leva o saldo do Guerreiro(a) abaixo do limiar de um nível que ele já
  alcançou
- **THEN** o nível continua certificado e os badges dele seguem concedidos

#### Scenario: A ocorrência não alcança o ponto extra

- **WHEN** uma ocorrência é lançada contra um Guerreiro(a) que tem saldo de pontos extras
- **THEN** o saldo de pontos extras permanece inalterado

### Requirement: A ocorrência é somente inserção e o motivo tem guarda pelo ciclo

O núcleo SHALL tratar a ocorrência de conduta como registro **somente inserção**: alterar ou
remover uma ocorrência gravada SHALL ser recusado. A correção se faz por ocorrência nova, nunca
por edição.

O **motivo** SHALL ter guarda limitada ao **ciclo em que a ocorrência aconteceu**, e o campo
SHALL ser anulável para que apagá-lo não apague o lançamento. Apagado o motivo, a ocorrência
SHALL permanecer consultável com **valor, data e autor**, e nenhuma rota SHALL devolver o motivo
apagado. (`RF-09-46`, `RN-01-52`, `RF-01-57`, 03 §12.2)

#### Scenario: Ocorrência gravada não se altera

- **WHEN** qualquer operação tenta alterar ou remover uma ocorrência de conduta já gravada
- **THEN** o núcleo recusa a operação

#### Scenario: Ocorrência sem motivo guardado não o devolve

- **WHEN** uma ocorrência de conduta cujo motivo já foi apagado é lida em qualquer rota
- **THEN** a saída traz valor, data e autor, e não traz o motivo

#### Scenario: Apagar o motivo não desfaz o débito

- **WHEN** o motivo de uma ocorrência de conduta é apagado
- **THEN** o saldo de ponto regular do Guerreiro(a) permanece como ficou depois do débito
