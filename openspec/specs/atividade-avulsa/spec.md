## Purpose

A atividade **fora de trilha**, cadastrada pela gestão: o único cadastro de atividade que cabe
ao Admin, classificada pelos mesmos três eixos da atividade de trilha e ancorada no **poder**
que ela desenvolve, que é onde o ponto regular dela pousa.

## Requirements

### Requirement: A atividade avulsa é cadastrada por Admin, fora de trilha e sem missão

O núcleo SHALL registrar a **atividade avulsa** com **título**, **descrição**, **modalidade**,
**formato**, **natureza**, **produção esperada** e o **poder** que ela desenvolve, **sem missão**
— é o que a distingue da atividade de trilha, que sempre pertence a uma. Cadastrar atividade
avulsa SHALL exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL receber
**403**, inclusive o Mestre, cuja bancada de autoria é a App 09.

Cadastro sem título, sem modalidade, sem formato, sem natureza, sem produção esperada ou sem
poder SHALL ser recusado com **422**, indicando o campo em falta. Modalidade e formato SHALL
ficar fechados nos valores do documento 11 §4, e valor fora deles SHALL ser recusado com **422**;
a natureza SHALL seguir aberta, como na atividade de trilha. A escrita SHALL gravar autoria,
data e hora com fuso. (`RF-02-29`, `RF-01-16`, `RF-01-03`, `RF-01-27`, documento 11 §4,
PRD-02 §3.2)

#### Scenario: Admin cadastra a atividade avulsa

- **WHEN** um Admin em sessão cadastra uma atividade com título, modalidade, formato, natureza,
  produção esperada e poder
- **THEN** o núcleo grava a atividade sem missão, com autor, data e hora com fuso

#### Scenario: Mestre não cadastra atividade avulsa

- **WHEN** um Mestre em sessão tenta cadastrar uma atividade avulsa
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Cadastro sem produção esperada é recusado

- **WHEN** chega um cadastro de atividade avulsa sem a produção esperada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Modalidade fora dos valores previstos é recusada

- **WHEN** chega um cadastro de atividade avulsa com modalidade que não é nenhum dos valores do
  documento 11 §4
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: Toda atividade tem missão ou poder, nunca as duas nem nenhuma

O núcleo SHALL exigir de toda atividade **exatamente uma** âncora de progressão: a **missão**, na
atividade de trilha, ou o **poder**, na avulsa. Atividade sem nenhuma das duas SHALL ser recusada
com **422**, e atividade que declare as duas SHALL ser recusada com **422** — é a mesma regra que
o ponto regular já aplica ao creditar por trilha ou por poder, nunca global.

O poder declarado SHALL existir no catálogo da gestão; poder inexistente SHALL ser recusado com
**422**. A atividade de trilha SHALL continuar sem declarar poder: o dela vem da trilha.
(`RF-02-29`, `RF-01-20`, `RF-01-21`, documento 11 §§5, 6)

#### Scenario: Atividade avulsa sem poder é recusada

- **WHEN** chega um cadastro de atividade avulsa sem poder declarado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Atividade que declara missão e poder é recusada

- **WHEN** chega um cadastro de atividade declarando ao mesmo tempo a missão e o poder
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Poder fora do catálogo é recusado

- **WHEN** chega um cadastro de atividade avulsa cujo poder não existe no catálogo
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A pontuação da atividade avulsa vem do motor e credita no poder declarado

O núcleo SHALL derivar o valor do Resultado de atividade avulsa do **motor de pontuação** do
documento 11 §5, pela **modalidade** da atividade e pelo **desfecho** lançado — a mesma régua da
atividade de trilha. NENHUM campo do cadastro SHALL aceitar valor de pontuação: ninguém arbitra
valor no cadastro.

O ponto regular apurado SHALL ser creditado no **poder declarado** pela atividade, e NUNCA numa
trilha. **Nível** e **badge de valores e temas transversais** SHALL permanecer percurso de
trilha e NÃO SHALL se mover pelo Resultado de atividade avulsa, que não pertence a missão
alguma. (`RF-02-29`, `RF-01-20`, `RF-01-21`, documento 11 §§5, 6, 7)

#### Scenario: A atividade avulsa em equipe com familiar vale o dobro da base

- **WHEN** o Admin lança o desfecho "realizada" para uma atividade avulsa de modalidade em
  equipe com familiar
- **THEN** o Guerreiro(a) recebe 20 pontos regulares no poder declarado pela atividade

#### Scenario: O crédito não pousa em trilha alguma

- **WHEN** um Resultado de atividade avulsa é lançado para um Guerreiro(a) inscrito numa trilha
- **THEN** o saldo daquela trilha permanece como estava e o do poder declarado sobe

#### Scenario: O nível da trilha não se move pela atividade avulsa

- **WHEN** um Resultado de atividade avulsa é lançado
- **THEN** nenhum nível de trilha é certificado por esse lançamento

#### Scenario: O cadastro não aceita valor de pontuação

- **WHEN** chega um cadastro de atividade avulsa declarando um valor de pontuação
- **THEN** o núcleo recusa o campo e nada é gravado com valor arbitrado

### Requirement: A atividade avulsa não declara recurso — quem declara é a aula

A atividade avulsa NÃO SHALL declarar tipo de recurso nem quantidade: **a aula** é que declara o
que consome e em que ponto de apoio, e é o agendamento dela que reserva. NENHUM campo do cadastro
de atividade avulsa SHALL receber recurso, e a atividade avulsa NÃO SHALL, por si, gerar reserva,
necessidade de recurso nem situação de pendente de lastro. (`RF-02-29`, `RF-02-31`, `RF-02-32`,
documento 04 §1)

#### Scenario: O cadastro não recebe recurso

- **WHEN** chega um cadastro de atividade avulsa declarando um tipo de recurso e uma quantidade
- **THEN** o núcleo recusa o campo e nenhuma reserva é gravada

#### Scenario: Cadastrar atividade avulsa não cria necessidade

- **WHEN** um Admin cadastra uma atividade avulsa
- **THEN** nenhuma necessidade de recurso passa a existir e nenhuma aula muda de situação
