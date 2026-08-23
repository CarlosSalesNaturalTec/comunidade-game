# area-do-mestre Specification

## Purpose

A App 09 é a casa do Mestre: é nela que ele escreve a trilha que a plataforma inteira consome,
e é dela que saem a missão, a atividade e a cadência de retomada. Esta capacidade cobre como o
Mestre entra na aplicação, o que a sessão e o papel lhe abrem, e a autoria de trilha, missão e
atividade de ponta a ponta.

## Requirements

### Requirement: A Área do Mestre é inteiramente autenticada e se identifica por chave

A App 09 SHALL apresentar a chave de aplicação dela em toda chamada ao núcleo e NEVER SHALL
expor tela de autoria a quem não tem sessão aberta. Visitante não alcança tela alguma.
(`RF-01-02`, `RN-01-32`, PRD-09 §4)

#### Scenario: Quem não tem sessão vê a entrada

- **WHEN** alguém abre qualquer endereço da aplicação sem sessão aberta
- **THEN** a aplicação apresenta a tela de entrada, e nenhuma trilha aparece

#### Scenario: A chave acompanha toda chamada

- **WHEN** a aplicação chama qualquer rota de dados do núcleo
- **THEN** a chamada leva a chave de aplicação da App 09 do ambiente em que ela roda

### Requirement: O Mestre entra por login social, e o papel vem do núcleo

A App 09 SHALL abrir sessão para o adulto que autentica pela conta social e SHALL guardar o
papel que o núcleo devolveu, que é o que governa o que ele alcança dali em diante. Conta social
sem cadastro correspondente SHALL ler a recusa com a orientação de solicitar participação pela
vitrine, sem que sessão alguma se abra. (`RF-01-09`, `RF-01-10`, `RN-01-04`, PRD-09 §4)

#### Scenario: Mestre com cadastro entra

- **WHEN** um Mestre autentica pela conta social associada ao cadastro dele
- **THEN** a aplicação abre a sessão e apresenta as telas de autoria

#### Scenario: O papel vem do núcleo, não da tela

- **WHEN** a sessão é aberta
- **THEN** o papel que governa a aplicação é o que o núcleo devolveu, e nenhuma escolha na tela
  o altera

#### Scenario: Conta social sem cadastro lê a orientação

- **WHEN** um adulto autentica com conta social que não corresponde a persona cadastrada
- **THEN** a aplicação apresenta a recusa com a orientação de solicitar participação pela
  vitrine, e nenhuma sessão é aberta

#### Scenario: Sessão expirada devolve à entrada

- **WHEN** o Mestre aciona uma tela de autoria e o núcleo recusa a sessão por expirada
- **THEN** a aplicação o devolve à tela de entrada, informando que a sessão terminou

### Requirement: O Guerreiro(a) não entra na Área do Mestre

A App 09 NEVER SHALL abrir sessão para persona de Guerreiro(a): a aplicação é de adulto, e o
Guerreiro(a) não a acessa. A recusa SHALL ser apresentada em linguagem simples, sem código de
erro cru. (PRD-09 §4)

#### Scenario: Guerreiro(a) é recusado na entrada

- **WHEN** uma credencial de Guerreiro(a) é apresentada à entrada da App 09
- **THEN** a aplicação recusa em linguagem simples e nenhuma sessão é aberta

### Requirement: O Mestre cria a trilha vinculada a um poder do catálogo

A App 09 SHALL permitir ao Mestre criar trilha informando nome, objetivo, área do conhecimento
e um **poder do catálogo**, e a trilha criada SHALL nascer em **rascunho**. O seletor SHALL
oferecer apenas poder **ativo** e de **natureza de Guerreiro(a)**; a recusa do núcleo a poder
fora dessa natureza SHALL ser apresentada em linguagem simples. (`RF-09-01`, `RN-01-43`)

#### Scenario: Mestre cria a trilha

- **WHEN** um Mestre em sessão informa nome, objetivo, área do conhecimento e um poder do
  catálogo e confirma
- **THEN** a trilha passa a existir em rascunho, com ele como autor, e a aplicação a apresenta
  entre as dele

#### Scenario: Campo obrigatório em falta

- **WHEN** o Mestre confirma a criação com nome, objetivo, área do conhecimento ou poder vazios
- **THEN** a aplicação aponta o campo em falta e nenhuma trilha passa a existir

#### Scenario: O seletor não oferece poder sem trilha

- **WHEN** o Mestre abre o seletor de poder
- **THEN** o Poder Sustentador e qualquer poder que não seja de Guerreiro(a) não lhe são
  oferecidos

### Requirement: A aplicação apresenta ao Mestre as trilhas dele, com a situação de cada uma

A App 09 SHALL apresentar ao Mestre em sessão as trilhas de que ele é autor, com nome, poder,
área do conhecimento e **situação** — rascunho, publicada ou despublicada —, e NEVER SHALL
apresentar-lhe o rascunho de outro Mestre. Na trilha despublicada, a aplicação SHALL apresentar
o **motivo** registrado pelo Admin, para que o autor saiba o que corrigir. (`RF-09-04`,
`RF-09-10`)

#### Scenario: O Mestre lê os próprios rascunhos

- **WHEN** um Mestre em sessão abre a lista das trilhas dele
- **THEN** a aplicação apresenta as trilhas de que ele é autor, rascunhos inclusive, com a
  situação de cada uma

#### Scenario: Rascunho alheio não aparece

- **WHEN** um Mestre em sessão abre a lista das trilhas dele e outro Mestre tem trilha em
  rascunho
- **THEN** a trilha do outro Mestre não aparece na lista

#### Scenario: O motivo da despublicação aparece ao autor

- **WHEN** um Mestre em sessão abre a lista e uma trilha dele está despublicada
- **THEN** a aplicação apresenta a situação despublicada e o motivo registrado pelo Admin

### Requirement: O Mestre acrescenta missões à trilha, ordenadas e declaradas

A App 09 SHALL permitir ao Mestre autor acrescentar missão à trilha informando **título**,
**posição** na sequência, **nível de dificuldade**, a declaração de **obrigatória ou opcional**
e a **etapa do ciclo** a que ela pertence. A aplicação SHALL apresentar as missões na ordem da
posição. (`RF-09-02`, `RF-09-03`, `RF-09-80`)

#### Scenario: Mestre acrescenta missão

- **WHEN** o Mestre autor informa título, posição, dificuldade, obrigatoriedade e etapa do
  ciclo e confirma
- **THEN** a missão passa a existir naquela posição da trilha e a aplicação a apresenta na
  ordem

#### Scenario: Declaração de obrigatoriedade em falta

- **WHEN** o Mestre confirma a missão sem declarar se ela é obrigatória ou opcional
- **THEN** a aplicação aponta a declaração em falta e nenhuma missão passa a existir

#### Scenario: Missão de trilha alheia é recusada

- **WHEN** um Mestre que não é o autor tenta acrescentar missão à trilha
- **THEN** a aplicação apresenta a recusa do núcleo e a trilha permanece como estava

### Requirement: O Mestre declara a missão de sondagem que abre a trilha

A App 09 SHALL permitir ao Mestre autor marcar como **sondagem** a missão que ocupa a primeira
posição da trilha, e SHALL apresentar em linguagem simples a recusa do núcleo à sondagem fora
da primeira posição e à segunda sondagem na mesma trilha. A aplicação SHALL aceitar trilha em
rascunho **sem** sondagem — a trava é da publicação, que não é desta fatia. (`RF-09-81`)

#### Scenario: Sondagem na primeira posição

- **WHEN** o Mestre autor marca como sondagem a missão da primeira posição
- **THEN** a aplicação grava a marcação e passa a distinguir a sondagem das demais missões

#### Scenario: Segunda sondagem é recusada em linguagem simples

- **WHEN** o Mestre autor tenta marcar uma segunda missão da trilha como sondagem
- **THEN** a aplicação apresenta que a trilha já tem sondagem, sem código de erro cru, e a
  sondagem existente permanece

#### Scenario: Rascunho sem sondagem é aceito

- **WHEN** o Mestre cria a trilha e ainda não declarou a sondagem
- **THEN** a aplicação a mantém em rascunho sem cobrar a sondagem

### Requirement: O Mestre cria as atividades da missão

A App 09 SHALL permitir ao Mestre autor criar atividade dentro de uma missão informando
**título**, **descrição**, **modalidade**, **formato**, **natureza** e a **produção** esperada
do Guerreiro(a). A aplicação SHALL apresentar em linguagem simples a recusa do núcleo à
atividade sem modalidade ou sem formato. (`RF-09-69`, `RF-09-70`)

#### Scenario: Mestre cria atividade

- **WHEN** o Mestre autor informa título, descrição, modalidade, formato, natureza e produção
  esperada e confirma
- **THEN** a atividade passa a existir naquela missão e a aplicação a apresenta entre as dela

#### Scenario: Atividade sem modalidade é recusada

- **WHEN** o Mestre confirma a atividade sem declarar a modalidade
- **THEN** a aplicação aponta o campo em falta e nenhuma atividade passa a existir

#### Scenario: A natureza aceita valor novo

- **WHEN** o Mestre informa natureza que não está entre as do Ciclo 01
- **THEN** a aplicação a aceita, porque a natureza é lista aberta

### Requirement: O Mestre declara a cadência de retomada da missão

A App 09 SHALL permitir ao Mestre autor declarar a **cadência de retomada** de uma missão e
SHALL permitir deixá-la **sem retomada**. A cadência declarada é a do Mestre; a sugestão de 2,
7 e 21 dias é do _template_ de missão, que não é desta fatia. (`RF-09-83`, `RF-09-101`)

#### Scenario: Mestre declara a cadência

- **WHEN** o Mestre autor declara a cadência de retomada de uma missão dele
- **THEN** a aplicação a grava na missão e a apresenta junto dela

#### Scenario: Missão sem retomada é aceita

- **WHEN** o Mestre autor deixa a missão sem cadência de retomada
- **THEN** a aplicação a aceita, e a missão fica sem retomada declarada

### Requirement: A autoria não exige do Mestre conhecimento técnico

A App 09 NEVER SHALL exigir do Mestre escrever código, HTML ou configuração técnica em campo
algum da autoria, e SHALL apresentar toda recusa do núcleo em linguagem simples, sem jargão de
TI e sem código de erro cru. (`RF-09-12`, PRD-09 §10)

#### Scenario: Nenhum campo pede código

- **WHEN** o Mestre percorre a criação de trilha, missão e atividade
- **THEN** nenhum campo lhe pede código, marcação ou configuração técnica

#### Scenario: A recusa do núcleo é traduzida

- **WHEN** o núcleo recusa uma escrita da autoria
- **THEN** a aplicação apresenta o que falta em linguagem simples, sem expor o código do erro

### Requirement: O Mestre declara a culminância da trilha

A App 09 SHALL oferecer ao Mestre autor, dentro da trilha, a declaração da **culminância** —
descrição da criação original esperada, modalidade individual ou em equipe, e critério de
validação. A aplicação SHALL apresentar a culminância já declarada e permitir substituí-la, e
NEVER SHALL oferecer a declaração em trilha de outro Mestre. (`RF-09-29`, `RF-09-30`)

#### Scenario: Mestre declara a culminância

- **WHEN** o Mestre autor preenche descrição, modalidade e critério e confirma
- **THEN** a aplicação grava a culminância no núcleo e passa a apresentá-la na trilha

#### Scenario: Campo obrigatório em falta

- **WHEN** o Mestre confirma sem o critério de validação
- **THEN** a aplicação apresenta a recusa em linguagem simples e nada é gravado

#### Scenario: A declaração substitui a culminância anterior

- **WHEN** o Mestre autor declara a culminância de uma trilha que já tem uma
- **THEN** a aplicação apresenta os novos valores no lugar dos anteriores

### Requirement: O Mestre publica a própria trilha e lê o que falta quando é recusado

A App 09 SHALL oferecer ao Mestre autor a **publicação** da própria trilha, em rascunho ou
despublicada, sem passar por aprovação. Recusada a publicação, a aplicação SHALL apresentar,
em linguagem simples e sem jargão, **exatamente o que falta** — a missão de sondagem, o
desafio de coleta, a culminância, ou mais de uma delas —, e NEVER SHALL apresentar código de
erro nem mensagem técnica. (`RF-09-05`, `RF-09-08`, `RF-09-12`, `RF-09-82`)

#### Scenario: Trilha completa é publicada

- **WHEN** o Mestre autor publica trilha que atende às três travas
- **THEN** a aplicação apresenta a trilha como publicada

#### Scenario: A recusa diz em linguagem simples o que falta

- **WHEN** a publicação é recusada por faltar a culminância
- **THEN** a aplicação apresenta que falta a culminância, em linguagem simples

#### Scenario: A recusa lista todas as travas que faltam

- **WHEN** a publicação é recusada por faltarem as três travas
- **THEN** a aplicação apresenta as três, e não apenas uma

#### Scenario: O Mestre republica a trilha corrigida

- **WHEN** o Mestre autor corrige a trilha despublicada e publica de novo
- **THEN** a aplicação apresenta a trilha como publicada e deixa de apresentar o motivo

#### Scenario: A publicação não é oferecida em trilha alheia

- **WHEN** um Mestre abre uma trilha de que não é autor
- **THEN** a aplicação não oferece a ação de publicar

### Requirement: O Mestre etiqueta a trilha com os ODS que ela toca

A App 09 SHALL oferecer ao Mestre autor, dentro da trilha, a declaração das **etiquetas ODS**
da trilha — o **objetivo**, escolhido de 1 a 18, e a **meta** opcional, quando ele souber. A
aplicação SHALL apresentar as etiquetas já declaradas e permitir **acrescentar, alterar e
remover** antes de confirmar, gravando o conjunto resultante de uma vez. A aplicação NEVER
SHALL exigir que o Mestre digite código, sigla técnica ou identificador, e NEVER SHALL oferecer
a declaração em trilha de outro Mestre. (`RF-09-92`, `RF-09-12`)

#### Scenario: Mestre etiqueta a trilha

- **WHEN** o Mestre autor escolhe o objetivo 4, informa a meta "4.7" e confirma
- **THEN** a aplicação grava a etiqueta no núcleo e passa a apresentá-la na trilha

#### Scenario: Mestre etiqueta sem saber a meta

- **WHEN** o Mestre autor escolhe o objetivo 13 e confirma sem informar a meta
- **THEN** a aplicação grava a etiqueta apenas com o objetivo, e nada é recusado

#### Scenario: Mestre declara mais de um objetivo na trilha

- **WHEN** o Mestre autor acrescenta os objetivos 4 e 13 e confirma
- **THEN** a aplicação apresenta os dois objetivos na trilha

#### Scenario: O que o Mestre remove some da trilha

- **WHEN** o Mestre autor remove um dos objetivos declarados e confirma
- **THEN** a aplicação deixa de apresentar aquele objetivo na trilha

#### Scenario: O Mestre retira todas as etiquetas

- **WHEN** o Mestre autor remove todos os objetivos e confirma
- **THEN** a aplicação apresenta a trilha sem etiqueta, e a trilha segue publicável

#### Scenario: A etiquetagem não é oferecida em trilha alheia

- **WHEN** um Mestre abre uma trilha de que não é autor
- **THEN** a aplicação não oferece a ação de etiquetar

### Requirement: O Mestre etiqueta uma missão à parte quando ela toca objetivo diferente

A App 09 SHALL oferecer ao Mestre autor, dentro de cada missão, a declaração das **etiquetas
ODS da missão**, pelo mesmo caminho da trilha e igualmente opcional. A aplicação SHALL deixar
claro que a etiqueta da missão só é necessária quando ela toca objetivo **diferente** do da
trilha, e que a missão sem etiqueta própria responde pela da trilha. A confirmação na missão
NEVER SHALL alterar as etiquetas da trilha. (`RF-09-98`, `RF-09-12`)

#### Scenario: Mestre etiqueta uma missão

- **WHEN** o Mestre autor escolhe o objetivo 13 dentro de uma missão e confirma
- **THEN** a aplicação grava a etiqueta na missão e passa a apresentá-la ali

#### Scenario: Missão sem etiqueta responde pela da trilha

- **WHEN** o Mestre autor abre uma missão sem etiqueta própria numa trilha etiquetada
- **THEN** a aplicação apresenta que a missão responde pela etiqueta da trilha

#### Scenario: Etiquetar a missão não mexe na trilha

- **WHEN** o Mestre autor confirma as etiquetas de uma missão
- **THEN** a aplicação continua apresentando as etiquetas da trilha inalteradas

### Requirement: O Mestre vê a cobertura de ODS da sua trilha

A App 09 SHALL apresentar ao Mestre autor, na trilha, a **cobertura de ODS resultante** do que
ele etiquetou — os objetivos distintos da trilha e das missões dela, reunidos. A cobertura
SHALL ser apresentada como resultado agregado da trilha, e NEVER SHALL ser apresentada por
Guerreiro(a). (`RF-09-94`, `RN-01-24`)

#### Scenario: A cobertura reúne trilha e missões

- **WHEN** o Mestre autor etiquetou a trilha com o objetivo 4 e uma missão com o objetivo 13
- **THEN** a aplicação apresenta a cobertura da trilha com os objetivos 4 e 13

#### Scenario: A cobertura acompanha o que o Mestre acabou de declarar

- **WHEN** o Mestre autor acrescenta um objetivo novo e confirma
- **THEN** a aplicação apresenta a cobertura já com o objetivo novo

#### Scenario: Trilha sem etiqueta apresenta cobertura vazia

- **WHEN** a trilha e as missões dela não têm etiqueta
- **THEN** a aplicação apresenta a cobertura vazia, sem apresentar erro
