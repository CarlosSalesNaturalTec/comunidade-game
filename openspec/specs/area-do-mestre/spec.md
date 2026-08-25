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

### Requirement: A aplicação apresenta ao Mestre as suas turmas, separadas por formato

A App 09 SHALL apresentar ao Mestre em sessão a área **Minhas turmas**, com as aulas das
comunidades dele e as atividades de que é autor, **separadas pelo formato** — as presenciais do
encontro e as on-line entre encontros. A área NEVER SHALL exibir turma de outra comunidade nem
atividade de outro Mestre.

Nenhuma tela desta área SHALL exibir imagem real de Guerreiro(a): o Guerreiro(a) aparece por
**nick e avatar** (`RN-09-18`). (`RF-09-42`, `RF-09-73`, `RN-09-08`)

#### Scenario: A área lista as turmas do Mestre em sessão

- **WHEN** o Mestre abre Minhas turmas
- **THEN** a aplicação lista as aulas das comunidades dele com as atividades de que é autor

#### Scenario: As atividades presenciais e on-line aparecem separadas

- **WHEN** a turma tem atividades dos dois formatos
- **THEN** a aplicação as apresenta separadas, presenciais de um lado e on-line do outro

#### Scenario: A área não exibe imagem real de criança

- **WHEN** a aplicação apresenta os Guerreiros e Guerreiras de uma turma
- **THEN** cada um aparece por nick e avatar, e nenhuma imagem real é exibida

### Requirement: Minhas turmas leva o Mestre ao painel do dia da sua aula

A App 09 SHALL oferecer, em **Minhas turmas**, o caminho para o **painel do dia** da aula do
Mestre. O painel é operado na **App 03** (`RN-02-20`), e a App 09 NEVER SHALL reconstruí-lo:
ela apenas leva o Mestre até lá, na aula que ele abriu.

O caminho SHALL aparecer apenas na aula **em andamento** — aquela cuja janela de data e horários
contém o instante da consulta. Aula futura, já realizada ou cancelada NEVER SHALL oferecê-lo,
porque não há encontro a acompanhar. (`RF-09-50`, `RF-09-42`, `RN-02-20`, PRD-09 §6.6)

#### Scenario: A aula em andamento oferece o caminho do painel

- **WHEN** o Mestre abre Minhas turmas durante a janela de uma aula dele
- **THEN** aquela aula apresenta o caminho para o painel do dia dela, na App 03

#### Scenario: Aula fora da janela não oferece o caminho

- **WHEN** a turma listada é de uma aula futura ou já realizada
- **THEN** o caminho para o painel do dia não é oferecido naquela aula

#### Scenario: A App 09 não reconstrói o painel

- **WHEN** o Mestre segue o caminho do painel do dia
- **THEN** ele chega ao painel operado na App 03, e a App 09 não apresenta cópia própria dele

### Requirement: O Mestre lança a atividade que propôs pela aplicação

A App 09 SHALL permitir ao Mestre lançar uma atividade sua, escolhendo a aula, os participantes
e o **desfecho** de cada um entre os três valores — realizada, com mérito ou mérito extra por
auxílio aos colegas. A tela SHALL permitir lançar **vários participantes de uma vez**, o que
serve a equipe inteira sem repetir o lançamento por integrante.

Recusa do núcleo SHALL ser apresentada em **linguagem simples, sem jargão de TI**
(`RN-09-16`). (`RF-09-43`, `RF-09-44`, `RF-09-74`, `RF-09-49`)

#### Scenario: O Mestre lança a equipe inteira num envio

- **WHEN** o Mestre seleciona os integrantes de uma equipe e atribui o desfecho de cada um
- **THEN** a aplicação envia o lançamento num só ato e confirma o registro dos participantes

#### Scenario: A recusa chega em linguagem simples

- **WHEN** o núcleo recusa o lançamento
- **THEN** a aplicação mostra o que impediu em linguagem simples, sem código nem jargão

### Requirement: O Mestre confirma a presença e lança a ocorrência de conduta

A App 09 SHALL permitir ao Mestre **confirmar a presença** de um Guerreiro(a) no encontro dele,
suprindo o que não foi capturado, e **lançar a ocorrência de conduta** escolhendo a atividade e
escrevendo o motivo em texto livre.

A tela da ocorrência NEVER SHALL pedir o **valor** do débito — ele é fixo na tabela do
documento 11 §5 — nem item de catálogo do Código de Conduta. Ela SHALL deixar claro que o
lançamento vale **no ato**, sem revisão de outro Admin (`RN-09-09`), e SHALL apresentar em
linguagem simples a recusa por teto da aula alcançado. (`RF-09-45`, `RF-09-46`, `RN-09-09`)

#### Scenario: O Mestre confirma a presença que faltou

- **WHEN** o Mestre confirma a presença de um Guerreiro(a) da turma dele
- **THEN** a aplicação registra a presença por confirmação e a mostra na lista do encontro

#### Scenario: O Mestre lança a ocorrência sem arbitrar valor

- **WHEN** o Mestre lança uma ocorrência de conduta escolhendo a atividade e escrevendo o motivo
- **THEN** a aplicação a registra sem pedir valor algum e confirma que o lançamento já está
  efetivado

#### Scenario: A ocorrência exige o motivo

- **WHEN** o Mestre tenta lançar a ocorrência sem escrever o motivo
- **THEN** a aplicação impede o envio e diz que o motivo é obrigatório

#### Scenario: O teto da aula é explicado em linguagem simples

- **WHEN** o núcleo recusa a ocorrência porque o Guerreiro(a) já alcançou o teto da aula
- **THEN** a aplicação diz que o limite daquele encontro foi alcançado, sem código nem jargão

### Requirement: O Mestre escreve o conteúdo da missão

A App 09 SHALL oferecer ao Mestre autor, dentro da missão, a escrita do **conteúdo**: texto
formatado com imagens, link para vídeo hospedado fora da plataforma, e o envio de vídeo e de
arquivo de apoio. A aplicação SHALL apresentar o conteúdo já escrito na ordem declarada e
permitir reordená-lo, alterá-lo e removê-lo antes de publicar. Nenhum campo SHALL pedir código,
HTML, marcação ou configuração técnica, e NEVER SHALL oferecer a escrita em missão de trilha de
outro Mestre. A aplicação SHALL salvar o rascunho do texto automaticamente, de modo que queda de
rede NEVER SHALL perder o que já foi escrito. (`RF-09-14`, `RF-09-15`, `RF-09-24`, `RN-09-16`,
PRD-09 §10)

#### Scenario: Mestre escreve o texto da missão

- **WHEN** o Mestre autor escreve o texto da missão e confirma
- **THEN** a aplicação grava o conteúdo no núcleo e passa a apresentá-lo na missão

#### Scenario: Mestre aponta vídeo hospedado fora

- **WHEN** o Mestre autor informa o endereço de um vídeo hospedado fora da plataforma
- **THEN** a aplicação grava o link como conteúdo, sem enviar arquivo algum

#### Scenario: Conteúdo de terceiro pede a fonte na própria tela

- **WHEN** o Mestre autor marca o conteúdo como de terceiro
- **THEN** a aplicação pede a fonte em campo de texto e não confirma sem ela

#### Scenario: Rascunho sobrevive à queda de rede

- **WHEN** a rede cai enquanto o Mestre autor escreve o texto da missão
- **THEN** o que foi escrito permanece, e a aplicação retoma dali quando a rede volta

#### Scenario: Nenhum campo pede jargão técnico

- **WHEN** o Mestre autor percorre a tela de conteúdo inteira
- **THEN** nenhum campo pede código, HTML, marcação nem configuração técnica

### Requirement: O Mestre envia vídeo e arquivo com progresso visível

A App 09 SHALL enviar vídeo e arquivo de apoio pela **sessão retomável** que o núcleo abre,
apresentando o **progresso** do envio enquanto ele corre. Caindo a rede, a aplicação SHALL
retomar do ponto já enviado, e NEVER SHALL recomeçar do zero. A recusa por formato fora da
lista e a recusa por tamanho acima do teto SHALL ser apresentadas em **linguagem simples**,
dizendo o tamanho do arquivo e o limite do tipo, sem código de erro nem jargão. (`RF-09-16`,
`RF-09-17`, `RF-09-18`, `RF-09-19`, `RF-09-115`, PRD-09 §10)

#### Scenario: Envio mostra o progresso

- **WHEN** o Mestre autor envia um vídeo de 180 MB
- **THEN** a aplicação apresenta o progresso do envio até a confirmação

#### Scenario: Queda de rede retoma o envio

- **WHEN** a rede cai no meio do envio e volta
- **THEN** a aplicação retoma do ponto já enviado, sem recomeçar

#### Scenario: Arquivo grande demais é recusado em linguagem simples

- **WHEN** o Mestre autor escolhe um vídeo de 240 MB
- **THEN** a aplicação diz que o vídeo tem 240 MB e o limite é 200 MB, sem código de erro

#### Scenario: Formato fora da lista é recusado em linguagem simples

- **WHEN** o Mestre autor escolhe um arquivo que não está na lista aceita
- **THEN** a aplicação diz quais formatos aceita, sem jargão técnico

### Requirement: O Mestre declara a bibliografia da missão

A App 09 SHALL oferecer ao Mestre autor, dentro da missão, a declaração da **bibliografia** —
título e capítulo em texto — e, **opcionalmente**, o apontamento de um **exemplar do acervo**
escolhido de uma lista, nunca digitado como identificador. A aplicação SHALL apresentar as
entradas já declaradas e permitir acrescentar e remover. Havendo vínculo, a aplicação SHALL
apresentar ao Mestre a disponibilidade do exemplar e o Apoiador creditado; não havendo, NEVER
SHALL apresentar nem pedir nenhum dos dois. (`RF-09-21`, `RF-09-22`, `RF-09-23`)

#### Scenario: Mestre declara bibliografia sem apontar exemplar

- **WHEN** o Mestre autor informa título e capítulo e confirma sem escolher exemplar
- **THEN** a aplicação grava a entrada e a apresenta sem disponibilidade nem crédito

#### Scenario: Mestre aponta o exemplar do acervo

- **WHEN** o Mestre autor escolhe um exemplar da lista do acervo e confirma
- **THEN** a aplicação grava a entrada com o vínculo e passa a apresentar a disponibilidade

#### Scenario: O Apoiador creditado não é digitado

- **WHEN** o Mestre autor declara bibliografia vinculada a exemplar
- **THEN** a aplicação apresenta o Apoiador que o núcleo devolveu, e não oferece campo para digitá-lo

### Requirement: O Mestre pré-visualiza a missão como o Guerreiro(a) a verá

A App 09 SHALL oferecer ao Mestre autor a **pré-visualização** da missão, apresentando o
conteúdo e a bibliografia na ordem e na forma em que o Guerreiro(a) os encontrará, antes de a
trilha ser publicada. A pré-visualização NEVER SHALL gravar coisa alguma e NEVER SHALL alterar
a situação da trilha. (`RF-09-25`)

#### Scenario: Mestre pré-visualiza antes de publicar

- **WHEN** o Mestre autor abre a pré-visualização de uma missão de trilha em rascunho
- **THEN** a aplicação apresenta o conteúdo e a bibliografia como o Guerreiro(a) os verá

#### Scenario: A pré-visualização não grava nada

- **WHEN** o Mestre autor fecha a pré-visualização
- **THEN** nada foi gravado e a situação da trilha permanece inalterada
