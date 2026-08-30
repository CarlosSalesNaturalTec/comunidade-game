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
SHALL permitir deixá-la **sem retomada**. A cadência declarada é sempre a do Mestre: a de 2, 7 e
21 dias que o _template_ de missão propõe é **sugestão**, apresentada já preenchida no campo e
alterável à vontade, e NEVER SHALL ser gravada sem ele confirmar. (`RF-09-83`, `RF-09-116`,
`RF-09-101`)

#### Scenario: Mestre declara a cadência

- **WHEN** o Mestre autor declara a cadência de retomada de uma missão dele
- **THEN** a aplicação a grava na missão e a apresenta junto dela

#### Scenario: Missão sem retomada é aceita

- **WHEN** o Mestre autor deixa a missão sem cadência de retomada
- **THEN** a aplicação a aceita, e a missão fica sem retomada declarada

#### Scenario: A sugestão do template vem preenchida e alterável

- **WHEN** o Mestre autor recebe a estrutura sugerida de uma missão
- **THEN** a cadência de 2, 7 e 21 dias aparece preenchida como proposta, e ele a altera ou a
  descarta antes de qualquer gravação

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

### Requirement: A App 09 monta o desafio de desbloqueio da missão

A aplicação SHALL permitir ao **Mestre autor** montar o **desafio de desbloqueio** de cada
missão da trilha que ele autora, escolhendo entre **quiz** e **desafio prático**. A tela SHALL
dizer que é esse desafio que **abre a missão seguinte** para o Guerreiro(a). Missão que ainda
**não tem** desafio declarado SHALL ser sinalizada na bancada, sem impedir a publicação da
trilha. Trilha de outro Mestre NEVER SHALL ser oferecida para edição. (`RF-09-26`)

#### Scenario: O Mestre autor monta o desafio da sua missão

- **WHEN** o Mestre autor abre uma missão da sua trilha e monta o desafio de desbloqueio
- **THEN** a aplicação grava o desafio e a missão passa a exibi-lo

#### Scenario: A bancada sinaliza a missão sem desafio

- **WHEN** o Mestre autor abre uma trilha com missão que ainda não declarou desafio
- **THEN** a missão vem sinalizada como sem desafio, e a trilha segue publicável

#### Scenario: Trilha de outro Mestre não é editável

- **WHEN** o Mestre abre uma trilha de que não é autor
- **THEN** nenhuma ação de montar ou alterar o desafio de desbloqueio é oferecida

### Requirement: A App 09 mostra ao Mestre autor os desafios práticos a julgar

A aplicação SHALL listar ao **Mestre autor** os **desafios práticos declarados como cumpridos**
pelos Guerreiros e Guerreiras das suas trilhas e ainda **não julgados**, cada um com o
Guerreiro(a), a missão e quando foi declarado. O Mestre SHALL poder **julgar se passou** por
Guerreiro(a). A tela SHALL dizer que o julgamento **abre a missão seguinte** para aquele
Guerreiro(a) e que **não passar não o elimina**. Declaração de trilha de outro Mestre NEVER
SHALL aparecer nesta lista. (`RF-09-26`, `RF-05-13`, `RF-05-14`)

#### Scenario: A lista traz o que espera julgamento

- **WHEN** o Mestre autor abre a bancada dos desafios práticos
- **THEN** vê as declarações ainda não julgadas das suas trilhas, com Guerreiro(a), missão e
  data

#### Scenario: Julgar abre a missão seguinte para aquele Guerreiro(a)

- **WHEN** o Mestre autor julga que um Guerreiro(a) passou no desafio prático
- **THEN** a declaração sai da lista e a missão seguinte abre para aquele Guerreiro(a)

#### Scenario: Declaração de trilha alheia não aparece

- **WHEN** o Mestre abre a bancada dos desafios práticos
- **THEN** nenhuma declaração de trilha de que ele não é autor é listada

### Requirement: A App 09 mostra ao Mestre autor as criações originais a validar

A App 09 SHALL apresentar ao Mestre em sessão as criações originais **entregues** nas trilhas de
que ele é **autor**, cada uma com a **trilha**, o **critério de validação** que ele mesmo
declarou na culminância, a **produção entregue** e a **autoria creditada**. Na modalidade de
equipe, a lista SHALL trazer **cada integrante com o papel** que teve na entrega. A lista NEVER
SHALL alcançar criação de trilha de outro Mestre. (`RF-09-31`, `RF-09-32`)

#### Scenario: A fila traz as criações entregues das trilhas do Mestre autor

- **WHEN** o Mestre autor abre as criações originais a validar
- **THEN** a tela lista as entregues nas trilhas dele, com a produção e a autoria de cada uma

#### Scenario: A fila mostra o critério que o próprio Mestre declarou

- **WHEN** o Mestre autor abre uma criação a validar
- **THEN** a tela mostra o critério de validação declarado por ele na culminância daquela trilha

#### Scenario: Criação em equipe traz o papel de cada integrante

- **WHEN** a criação a validar foi entregue por uma equipe da trilha
- **THEN** a tela traz cada integrante creditado com o papel que teve

#### Scenario: Criação de trilha de outro Mestre não aparece

- **WHEN** existe criação original entregue numa trilha de que o Mestre não é autor
- **THEN** ela não aparece na fila dele

### Requirement: O Mestre autor valida a criação, creditando autoria e badge

A App 09 SHALL permitir ao Mestre autor **validar** a criação original entregue. Validada, a
tela SHALL informar que a autoria foi creditada e o **badge de autoria** liberado a cada
creditado, e a criação SHALL sair da fila. A App 09 NEVER SHALL oferecer ao Mestre editar a
produção entregue nem reatribuir a autoria. (`RF-09-31`, `RN-09-04`)

#### Scenario: Validação credita a autoria e libera o badge

- **WHEN** o Mestre autor valida uma criação original entregue
- **THEN** a tela confirma que a autoria foi creditada e o badge de autoria liberado, e a criação
  sai da fila

#### Scenario: A App 09 não edita a produção nem a autoria

- **WHEN** o Mestre autor abre uma criação a validar
- **THEN** a tela não oferece alterar a produção entregue nem reatribuir a autoria

### Requirement: O Mestre autor devolve a criação com motivo, sem tirar a autoria

A App 09 SHALL permitir ao Mestre autor **devolver** a criação original para ajuste, exigindo o
**motivo** escrito em linguagem simples — é ele que o Guerreiro(a) lerá na App 05. Devolução sem
motivo NEVER SHALL ser aceita. A devolução NEVER SHALL alterar a autoria do registro.
(`RF-09-34`, `RF-05-42`, `RN-09-04`)

#### Scenario: Devolução exige o motivo

- **WHEN** o Mestre autor tenta devolver uma criação sem escrever o motivo
- **THEN** a tela recusa a devolução e pede o motivo

#### Scenario: Devolução com motivo preserva a autoria

- **WHEN** o Mestre autor devolve a criação escrevendo o motivo
- **THEN** a criação volta ao Guerreiro(a) com o motivo, e a autoria permanece a mesma

### Requirement: A App 09 informa que a criação validada só vai à vitrine com autorização

A App 09 SHALL informar ao Mestre, na tela da criação validada, que ela só aparece na **vitrine
pública** quando **todos os creditados** têm autorização de divulgação vigente do responsável, e
que sem ela a criação existe apenas no portfólio do Guerreiro(a). A App 09 NEVER SHALL oferecer
ao Mestre conceder, alterar ou revogar essa autorização — é ato do responsável. (`RF-09-33`,
`RN-09-19`)

#### Scenario: A tela diz o que falta para a criação ir à vitrine

- **WHEN** o Mestre valida uma criação de Guerreiro(a) sem autorização de divulgação vigente
- **THEN** a tela informa que ela não irá à vitrine enquanto faltar a autorização do responsável

#### Scenario: A App 09 não altera a autorização de divulgação

- **WHEN** o Mestre vê uma criação validada dependente de autorização
- **THEN** a tela não oferece conceder nem revogar a autorização

### Requirement: O Mestre declara o desafio de coleta da missão

A App 09 SHALL oferecer ao Mestre autor, dentro de cada missão da sua trilha, a declaração do
**desafio de coleta**, com os cinco atributos que o núcleo exige: o **tipo** escolhido no
catálogo de tipos de coleta, a **cadência** — diária, semanal ou mensal —, a **vigência** com
início e fim, a **granularidade exigida** entre os seis níveis do território e **quantos
registros do mesmo período de cadência pontuam**. (`RF-09-27`, `RF-09-28`)

O tipo SHALL ser **escolhido** na lista lida do catálogo, e a aplicação NEVER SHALL oferecer a
criação de tipo novo nem a escolha de tipo desativado — o catálogo é cadastro de Admin. A
aplicação SHALL apresentar, junto do tipo escolhido, a **forma de registro** e a **unidade**
quando houver, para que o Mestre saiba o que o Guerreiro(a) vai medir.

Recusada a declaração pelo núcleo — cadência fora das três, vigência com fim antes do início,
quantidade menor que 1, campo em falta ou tipo desativado —, a aplicação SHALL apresentar o que
está errado em **linguagem simples**, apontando o campo, e NEVER SHALL apresentar código de erro
nem mensagem técnica. (`RN-09-16`)

#### Scenario: O Mestre declara o desafio completo

- **WHEN** o Mestre autor escolhe um tipo do catálogo e declara cadência semanal, vigência,
  granularidade `rua` e um registro que pontua por período
- **THEN** a aplicação grava o desafio na missão e o apresenta entre os desafios dela

#### Scenario: O tipo vem do catálogo, e a aplicação não cria nenhum

- **WHEN** o Mestre abre a declaração do desafio de coleta
- **THEN** a aplicação apresenta os tipos ativos do catálogo para escolha, e nenhuma ação de
  criar tipo novo

#### Scenario: O tipo escolhido mostra o que se mede

- **WHEN** o Mestre escolhe um tipo cuja forma de registro é número
- **THEN** a aplicação apresenta a unidade daquele tipo junto do nome

#### Scenario: A recusa do núcleo vira mensagem simples

- **WHEN** o Mestre declara vigência cujo fim precede o início e o núcleo recusa
- **THEN** a aplicação apresenta em linguagem simples que a data de fim tem de vir depois da de
  início, apontando o campo, sem código de erro

#### Scenario: A declaração não é oferecida em trilha alheia

- **WHEN** um Mestre abre uma missão de trilha de que não é autor
- **THEN** a aplicação não oferece a declaração do desafio de coleta

### Requirement: A App 09 apresenta os desafios de coleta já declarados na trilha

A App 09 SHALL apresentar, em cada missão da trilha do Mestre autor, os **desafios de coleta já
declarados**, com tipo, cadência, vigência, granularidade exigida e quantos registros do período
pontuam — inclusive na trilha em **rascunho**, que é onde eles nascem. Missão sem desafio SHALL
ser apresentada como tal, sem erro. (`RF-09-27`, `RF-09-28`)

A aplicação NEVER SHALL oferecer a declaração da **etiqueta ODS no desafio**: ela é herdada da
missão, ou da trilha na falta dela, e o núcleo recusa desafio que a declare. (`RN-09-36`)

#### Scenario: A trilha em rascunho mostra o desafio declarado

- **WHEN** o Mestre abre uma trilha em rascunho em que já declarou um desafio de coleta
- **THEN** a aplicação apresenta o desafio na missão a que ele pertence

#### Scenario: Missão sem desafio é apresentada como tal

- **WHEN** o Mestre abre uma missão que ainda não tem desafio de coleta
- **THEN** a aplicação apresenta que não há desafio declarado, e oferece declarar um

#### Scenario: O formulário do desafio não declara etiqueta ODS

- **WHEN** o Mestre abre a declaração do desafio de coleta
- **THEN** nenhum campo de etiqueta ODS é apresentado, porque a etiqueta é herdada

### Requirement: O Mestre avalia a solicitação de novo local dos desafios das suas trilhas

A App 09 SHALL apresentar ao Mestre as **solicitações de novo local em aberto** dos desafios das
**suas** trilhas, cada uma com o nível pretendido, o rótulo, a justificativa e o desafio de
origem, e SHALL oferecer **aprovar** ou **recusar** cada uma. A aprovação SHALL exigir o **local
pai** dentro da hierarquia da comunidade da solicitação; a recusa SHALL exigir o **motivo**, sem
o qual a aplicação NEVER SHALL enviá-la. (`RF-09-53`)

A aplicação NEVER SHALL apresentar solicitação de desafio de trilha de outro Mestre — o recorte
é do núcleo, e a tela não o alarga —, e NEVER SHALL oferecer o **cadastro direto de local** nem
a criação de Comunidade Virtual, que seguem privativos de Admin (PRD-09 §3.2). A solicitação já
avaliada SHALL sair da lista.

Recusada a avaliação pelo núcleo — hierarquia inválida, recusa sem motivo ou solicitação já
avaliada —, a aplicação SHALL apresentar o que está errado em linguagem simples, e a solicitação
SHALL continuar em aberto na tela. (`RN-09-16`)

#### Scenario: O Mestre aprova a solicitação informando o local pai

- **WHEN** o Mestre aprova uma solicitação de novo local escolhendo o local pai na hierarquia da
  comunidade
- **THEN** a aplicação apresenta a solicitação como aprovada e ela sai da lista das em aberto

#### Scenario: A recusa exige o motivo antes de enviar

- **WHEN** o Mestre recusa uma solicitação sem escrever o motivo
- **THEN** a aplicação não envia a recusa e pede o motivo

#### Scenario: A tela não alcança solicitação de trilha alheia

- **WHEN** há solicitações de desafios de trilhas de outro Mestre na mesma comunidade
- **THEN** a aplicação não as apresenta

#### Scenario: A App 09 não cadastra local nem comunidade

- **WHEN** o Mestre abre a área de território
- **THEN** nenhuma ação de cadastrar local diretamente ou de criar Comunidade Virtual é oferecida

#### Scenario: A hierarquia inválida vira mensagem simples

- **WHEN** o Mestre aprova informando local pai de nível que não é o imediatamente acima e o
  núcleo recusa
- **THEN** a aplicação apresenta em linguagem simples que o local pai precisa ser do nível acima,
  e a solicitação continua em aberto

### Requirement: A App 09 alerta enquanto houver solicitação de local sem desfecho

A App 09 SHALL apresentar **alerta** enquanto houver ao menos uma solicitação de novo local dos
desafios das trilhas do Mestre **sem desfecho**, visível fora da área de território, para que ele
não precise entrar nela para saber que há pedido parado. O alerta SHALL desaparecer quando a
última solicitação em aberto for aprovada ou recusada. (`RF-09-54`)

O alerta SHALL alcançar **todas as comunidades** em que há solicitação em aberto das trilhas do
Mestre, e NEVER SHALL depender de o Mestre escolher uma comunidade antes: a trilha é bem comum da
plataforma e alcança todas elas. (`RN-01-42`)

#### Scenario: O alerta aparece enquanto há pedido parado

- **WHEN** existe solicitação de novo local em aberto num desafio de trilha do Mestre
- **THEN** a aplicação apresenta o alerta fora da área de território

#### Scenario: O alerta some quando a última é tratada

- **WHEN** o Mestre trata a última solicitação em aberto
- **THEN** o alerta deixa de ser apresentado

#### Scenario: O alerta não depende de escolher comunidade

- **WHEN** o Mestre entra na aplicação e há solicitação em aberto em comunidade que ele não
  selecionou
- **THEN** o alerta é apresentado assim mesmo

#### Scenario: Solicitação de trilha alheia não gera alerta

- **WHEN** a única solicitação em aberto é de um desafio de trilha de outro Mestre
- **THEN** nenhum alerta é apresentado ao Mestre

### Requirement: O Mestre registra a proposta de evolução e acompanha o status

A App 09 SHALL oferecer ao Mestre o registro de **proposta de evolução da plataforma**, em
**texto**, na fila única da gestão, e SHALL apresentar as propostas que ele registrou com a
**situação**, o **prazo** e, concluídas, o **desfecho** — e, na não adotada, o **motivo do
retorno em linguagem simples**. (`RF-09-55`)

A aplicação NEVER SHALL oferecer envio de **áudio**, e NEVER SHALL apresentar proposta de outra
persona. O retorno SHALL ser lido **dentro da aplicação**: nenhuma notificação por e-mail é
construída. (`RN-09-23`)

A aplicação NEVER SHALL oferecer ao Mestre avaliar proposta alguma, a sua inclusive — a avaliação
é ato de Admin, na App 03 (PRD-09 §3.2).

#### Scenario: O Mestre registra a proposta em texto

- **WHEN** o Mestre escreve uma proposta de evolução da plataforma e a envia
- **THEN** a aplicação apresenta a proposta registrada, com a situação recebida e o prazo

#### Scenario: A aplicação não oferece áudio

- **WHEN** o Mestre abre o registro da proposta
- **THEN** nenhum campo ou botão de gravação de áudio é apresentado

#### Scenario: O Mestre acompanha o desfecho na própria aplicação

- **WHEN** uma proposta do Mestre é concluída como não adotada
- **THEN** a aplicação apresenta a situação e o motivo do retorno em linguagem simples, sem que
  nenhum e-mail seja enviado

#### Scenario: A lista não mostra proposta de outra persona

- **WHEN** há propostas de outros Mestres e de Guerreiros e Guerreiras na fila única
- **THEN** a aplicação apresenta apenas as do Mestre em sessão

#### Scenario: A avaliação não é oferecida ao Mestre

- **WHEN** o Mestre abre uma proposta que registrou
- **THEN** nenhuma ação de adotar ou não adotar é apresentada

### Requirement: A App 09 apresenta ao Mestre as necessidades de recurso das aulas dele

A App 09 SHALL apresentar ao Mestre a lista das **necessidades de recurso** das aulas das
comunidades a que ele está vinculado, cada uma com o **tipo de recurso**, a **quantidade que
falta**, o **valor em moedas**, o **ponto de apoio** e a **data e o horário da aula**
(`RF-09-56`). A falta é o que impede a atividade de acontecer: a necessidade existe justamente
para a falta virar pedido, e não recusa silenciosa (`RN-09-12`).

A lista SHALL vir **derivada do núcleo**: a aplicação NEVER SHALL somar, reordenar por saldo nem
recalcular a falta, e NEVER SHALL apresentar necessidade de aula de comunidade a que o Mestre
não está vinculado — o recorte é do núcleo, e a tela não o alarga.

A aplicação NEVER SHALL apresentar valor **em reais** nesta lista, nem dado de pessoa: a
necessidade descreve recurso, aula e lugar. Necessidade cujo tipo de recurso esteja **sem valor
de referência vigente** SHALL continuar aparecendo, com a quantidade que falta e declarando que
não há valor de referência vigente, e a aplicação NEVER SHALL arbitrar valor nem nome no lugar
do que o núcleo não serviu.

#### Scenario: O Mestre vê a falta das aulas da comunidade dele

- **WHEN** o Mestre abre a área de recursos e há aula pendente de lastro na comunidade dele
- **THEN** a aplicação apresenta a necessidade com o tipo de recurso, a quantidade que falta, o
  valor em moedas, o ponto de apoio e a data e o horário da aula

#### Scenario: A lista não traz reais

- **WHEN** as necessidades são apresentadas
- **THEN** nenhum valor em reais aparece na lista

#### Scenario: A necessidade sem valor de referência vigente continua na lista

- **WHEN** o tipo de recurso em falta não tem valor de referência vigente
- **THEN** a aplicação apresenta a necessidade com a quantidade que falta e declara que não há
  valor de referência vigente, sem arbitrar um

#### Scenario: Sem necessidade em aberto a lista diz isso

- **WHEN** não há aula pendente de lastro na comunidade do Mestre
- **THEN** a aplicação declara que não há necessidade de recurso em aberto

### Requirement: O Mestre assume a necessidade como absorção em um ato de confirmação

A App 09 SHALL oferecer, **a partir da própria necessidade**, assumir o recurso como **aporte
por absorção**, em um **ato de confirmação** — um passo só, sem homologação de Admin
(`RF-09-57`). A absorção SHALL declarar a **aula** cuja necessidade atende, e o tipo de recurso
e o ponto de apoio SHALL ser os da necessidade de origem, nunca escolhidos à parte.

A aplicação SHALL apresentar que o aporte nasce **em nome do próprio Mestre** e **marcado como
ressarcível**, e que a aula é confirmada assim que o saldo fechar, sem intervenção de Admin
(`RF-09-58`, `RN-09-13`). Ela NEVER SHALL oferecer registrar aporte em nome de outra persona,
homologar aporte algum, nem declarar a destinação — a absorção não a escolhe.

O formulário SHALL exigir o **valor de origem em reais** quando o tipo de recurso for de
natureza **consumível, durável ou financeira**, porque houve desembolso e é esse valor que o
ressarcimento devolve, e NEVER SHALL exigi-lo na natureza **serviço**. Onde o valor em reais for
pedido, a aplicação SHALL apresentá-lo **ao lado do equivalente em moedas**. O formulário SHALL
exigir o **comprovante** quando o tipo de recurso o exigir, e NEVER SHALL aceitar arquivo que não
seja PDF, JPG ou PNG.

Quantidade **menor que a falta** SHALL ser aceita: ela credita, a necessidade reaparece com a
falta abatida e a aula segue pendente de lastro. Fechado o saldo, a necessidade SHALL sair da
lista e a aula SHALL aparecer confirmada.

Recusado o registro pelo núcleo — valor de origem em falta, comprovante exigido e ausente, tipo
que a aula não consome ou tipo sem vigência que cubra a data —, a aplicação SHALL apresentar o
que está errado em **linguagem simples**, e a necessidade SHALL continuar na lista (`RN-09-16`).

#### Scenario: O Mestre absorve a necessidade em um ato

- **WHEN** o Mestre assume uma necessidade, informa a quantidade e o valor de origem em reais e
  confirma
- **THEN** a aplicação registra o aporte em nome dele, apresenta-o como ressarcível e recarrega
  a lista de necessidades

#### Scenario: A absorção parcial abate a falta e a aula segue pendente

- **WHEN** o Mestre absorve quantidade menor do que a falta
- **THEN** a aplicação apresenta a mesma necessidade com a falta abatida

#### Scenario: A absorção que fecha o saldo tira a necessidade da lista

- **WHEN** o Mestre absorve exatamente o que faltava à aula
- **THEN** a necessidade deixa de ser apresentada e a aula aparece confirmada

#### Scenario: O valor de origem é exigido onde houve desembolso

- **WHEN** o Mestre assume uma necessidade de tipo de natureza consumível
- **THEN** a aplicação pede o valor de origem em reais, ao lado do equivalente em moedas, e não
  envia o registro sem ele

#### Scenario: A absorção de serviço não pede reais

- **WHEN** o Mestre assume uma necessidade de tipo de natureza serviço
- **THEN** nenhum campo de valor em reais é apresentado, e o registro é enviado sem ele

#### Scenario: A aplicação não oferece homologação nem provedor alheio

- **WHEN** o Mestre abre o ato de absorção
- **THEN** nenhum campo de provedor, de homologação ou de destinação é apresentado

#### Scenario: A recusa do núcleo vira mensagem simples

- **WHEN** o núcleo recusa o registro porque o tipo de recurso não tem vigência que cubra a data
  do aporte
- **THEN** a aplicação apresenta o motivo em linguagem simples e a necessidade continua na lista

### Requirement: O Mestre acompanha a situação do ressarcimento do que absorveu

A App 09 SHALL apresentar ao Mestre as absorções **dele mesmo**, cada uma com o **tipo de
recurso**, a **quantidade**, o **ponto de apoio**, o **valor em moedas**, a **data** e a
**situação de ressarcimento** — em aberto, ressarcido ou não se aplica (`RF-09-59`).

A leitura SHALL ser **somente leitura**: a aplicação NEVER SHALL oferecer exigir, apressar,
reordenar ou cancelar ressarcimento, e NEVER SHALL apresentar absorção de outra persona.

A aplicação SHALL apresentar a situação **não se aplica** como o que ela é — absorção de
serviço, em que quem absorve dá tempo e não há desembolso a devolver — e NEVER SHALL apresentá-la
como pendência.

#### Scenario: O Mestre vê o que absorveu e a situação de cada aporte

- **WHEN** o Mestre abre o acompanhamento e absorveu recursos antes
- **THEN** a aplicação apresenta cada aporte com tipo, quantidade, ponto de apoio, moedas, data e
  a situação de ressarcimento

#### Scenario: A tela não oferece apressar o ressarcimento

- **WHEN** o Mestre abre um aporte com ressarcimento em aberto
- **THEN** nenhuma ação de exigir, apressar, reordenar ou cancelar é apresentada

#### Scenario: A absorção de outro Mestre não aparece

- **WHEN** há absorções em aberto de outro Mestre
- **THEN** elas não são apresentadas

#### Scenario: A absorção de serviço não aparece como pendência

- **WHEN** o Mestre absorveu um serviço
- **THEN** a aplicação apresenta a situação como não se aplica, e não como ressarcimento em
  aberto

### Requirement: A App 09 não coleta nem exibe dado bancário

A App 09 NEVER SHALL apresentar campo que colete **chave PIX, banco ou conta**, e NEVER SHALL
exibir dado bancário de ninguém: a plataforma não o guarda, e do trâmite ela retém apenas o
**comprovante da transferência**, anexado pelo Admin ao registrar o ressarcimento (`RF-09-60`).

Onde o Mestre acompanha o que absorveu, a aplicação SHALL declarar que o ressarcimento ocorre
havendo receita destinada a ele e que, nessa etapa, a **chave PIX é enviada por e-mail ao
Admin** — o único retorno por e-mail do Ciclo 01, e ato da pessoa, fora da plataforma. A
aplicação NEVER SHALL enviar e-mail, nem construir notificação por e-mail (`RN-09-23`).

#### Scenario: Nenhum campo pede dado bancário

- **WHEN** o Mestre percorre a área de recursos, do ato de absorção ao acompanhamento
- **THEN** nenhum campo de chave PIX, banco ou conta é apresentado

#### Scenario: A tela orienta o envio da chave por e-mail ao Admin

- **WHEN** o Mestre abre o acompanhamento do que absorveu
- **THEN** a aplicação declara que a plataforma não guarda dado bancário e que a chave PIX é
  enviada por e-mail ao Admin quando houver receita destinada

#### Scenario: A aplicação não envia e-mail

- **WHEN** um aporte do Mestre passa a ressarcido
- **THEN** a situação é lida dentro da aplicação, sem que nenhum e-mail seja enviado por ela

### Requirement: O Mestre cadastra o responsável que se apresentou no encontro

A App 09 SHALL oferecer ao Mestre em sessão o cadastro da persona de **responsável**, com o
**nome** dela. A tela SHALL declarar que o cadastro pressupõe que o responsável **se apresentou
pessoalmente**, e a aplicação NEVER SHALL oferecer caminho de cadastro à distância — solicitação,
convite ou autocadastro do responsável. A tela NEVER SHALL exigir e-mail, documento ou
digitalização do termo: são atos da gestão, na App 03. O responsável SHALL ser a **única**
persona que a App 09 cadastra. (`RF-09-62`, `RN-09-15`, invariante 3 do documento 99 §6)

#### Scenario: O Mestre cadastra o responsável

- **WHEN** o Mestre informa o nome do responsável apresentado no encontro e confirma
- **THEN** a aplicação cadastra a persona de responsável e segue para o vínculo

#### Scenario: A tela declara a apresentação presencial

- **WHEN** o Mestre abre o cadastro de responsável
- **THEN** a tela declara que o cadastro pressupõe a apresentação pessoal do responsável

#### Scenario: Cadastro sem nome é recusado em linguagem simples

- **WHEN** o Mestre confirma o cadastro sem informar o nome
- **THEN** a aplicação aponta o campo em falta, em linguagem simples, e nada é cadastrado

#### Scenario: A App 09 não cadastra outra persona

- **WHEN** o Mestre percorre a área de responsáveis
- **THEN** não lhe é oferecido cadastrar Guerreiro(a), Mestre, Apoiador nem Admin

### Requirement: O Mestre vincula os Guerreiros e Guerreiras declarando o parentesco

A App 09 SHALL permitir que o Mestre vincule ao responsável recém-cadastrado os Guerreiros e
Guerreiras **já ativos** que ele pode alcançar, escolhidos numa lista servida pelo núcleo e
apresentada por **nick e avatar**. Cada vínculo SHALL exigir o **grau de parentesco em texto
livre**, e o grau SHALL ser declarado **por vínculo**, ainda que o mesmo responsável seja
vinculado a mais de uma criança. A aplicação NEVER SHALL exibir imagem real de Guerreiro(a) nem
oferecer caminho para criar a persona da criança a partir daqui. (`RF-09-62`, `RF-09-63`,
`RN-09-18`, invariante 12 do documento 99 §6)

#### Scenario: O vínculo é criado com o grau declarado

- **WHEN** o Mestre escolhe um Guerreiro(a) da lista e informa o grau de parentesco
- **THEN** a aplicação cria o vínculo com aquele grau e o apresenta entre os já criados

#### Scenario: Cada vínculo tem o seu grau

- **WHEN** o Mestre vincula o mesmo responsável a dois Guerreiros e Guerreiras
- **THEN** cada vínculo pede e guarda o seu grau, sem que um herde o do outro

#### Scenario: Vínculo sem grau de parentesco é recusado

- **WHEN** o Mestre tenta vincular sem informar o grau de parentesco
- **THEN** a aplicação aponta o campo em falta e nenhum vínculo é criado

#### Scenario: A escolha do Guerreiro(a) é por nick e avatar

- **WHEN** o Mestre abre a lista de quem pode vincular
- **THEN** vê nick e avatar de cada Guerreiro(a), e nenhuma imagem real

### Requirement: O quarto vínculo é recusado em linguagem simples

A App 09 SHALL apresentar a recusa do **quarto** vínculo de responsável ao mesmo Guerreiro(a)
como o que é — o teto de três por criança —, em linguagem simples, sem código nem jargão. A
aplicação NEVER SHALL contar os vínculos por conta própria para bloquear a tela antes de tentar:
o teto é conferido pelo núcleo. Os três vínculos vigentes SHALL continuar válidos depois da
recusa, e o vínculo recusado NEVER SHALL desfazer o cadastro do responsável já criado.
(`RF-09-64`, `RN-09-15`, PRD-09 §12)

#### Scenario: O quarto vínculo é recusado com a razão dita

- **WHEN** o Mestre tenta vincular um responsável a um Guerreiro(a) que já tem três vínculos
  vigentes
- **THEN** a aplicação informa que a criança já tem o teto de três responsáveis, e o vínculo não
  é criado

#### Scenario: A recusa não perde o que já foi feito

- **WHEN** o quarto vínculo é recusado depois de o responsável já ter sido cadastrado
- **THEN** o responsável cadastrado permanece, os vínculos já criados permanecem, e o Mestre
  segue de onde estava

### Requirement: O Mestre cria a credencial provisória do responsável sem conta Google

A App 09 SHALL permitir que o Mestre crie, para o responsável que acabou de cadastrar, a
**credencial de usuário e senha provisória** destinada a quem não tem conta Google. A aplicação
SHALL exibir a senha provisória **uma única vez**, para entrega em mãos, SHALL avisar que ela não
volta a aparecer e NEVER SHALL oferecer caminho para recuperá-la ou reexibi-la. A aplicação NEVER
SHALL enviar a credencial por e-mail nem por mensageria. O caminho SHALL ser **opcional**: o
responsável com conta Google é cadastrado e vinculado sem credencial alguma. (`RF-09-65`,
`RN-09-23`, documento 03 §1.1)

#### Scenario: A senha provisória aparece uma vez

- **WHEN** o Mestre cria a credencial informando o usuário do responsável
- **THEN** a aplicação mostra a senha provisória com o aviso de que ela não aparece de novo

#### Scenario: A senha não se recupera

- **WHEN** o Mestre sai da tela depois de ver a senha provisória
- **THEN** não lhe é oferecido caminho algum para reexibir ou recuperar aquela senha

#### Scenario: O responsável com conta Google dispensa a credencial

- **WHEN** o Mestre conclui o cadastro e o vínculo sem criar credencial
- **THEN** a aplicação encerra o fluxo normalmente, sem exigir usuário nem senha

### Requirement: O Mestre publica a prova da própria habilidade

A App 09 SHALL oferecer ao Mestre em sessão a área do **próprio perfil**, onde ele publica
**currículo, portfólio, redes sociais e artefatos comprobatórios** da sua habilidade. Cada um
SHALL ser declarado como **endereço e rótulo** — link, nunca upload de arquivo —, e a aplicação
NEVER SHALL oferecer campo de anexo nesta área. A área SHALL apresentar os artefatos declarados
por Admin no cadastro dele em **leitura**, marcados como tais, e SHALL oferecer a remoção apenas
dos que o próprio Mestre publicou. (`RF-09-66`, `RN-02-01`, documento 02 §1)

#### Scenario: O Mestre publica o currículo

- **WHEN** o Mestre acrescenta ao perfil um artefato com endereço e rótulo
- **THEN** a aplicação o publica e ele passa a constar da prova de habilidade dele

#### Scenario: A área não aceita arquivo

- **WHEN** o Mestre abre a área do próprio perfil
- **THEN** só lhe são oferecidos os campos de endereço e rótulo, e nenhum campo de anexo

#### Scenario: O artefato do cadastro fica, marcado

- **WHEN** o perfil traz artefatos declarados por Admin no cadastro do Mestre
- **THEN** eles aparecem marcados como declarados no cadastro, sem caminho de remoção

#### Scenario: O Mestre remove o que ele mesmo publicou

- **WHEN** o Mestre remove um artefato que ele publicou
- **THEN** ele deixa de constar do perfil, e os demais permanecem

### Requirement: A App 09 não cadastra Mestre nem cria acesso de Mestre

A App 09 NEVER SHALL oferecer caminho para **cadastrar Mestre**, criar acesso de Mestre,
convidar outro Mestre ou alterar o papel de qualquer persona. A área do perfil SHALL declarar
que o cadastro de Mestre é ato exclusivo de Admin, com habilidade comprovada, e que a
aplicação alcança apenas a prova de habilidade e a identidade do próprio Mestre. A aplicação
NEVER SHALL oferecer ao Mestre a edição do próprio nome, e-mail ou papel. (`RF-09-67`,
`RN-09-14`, invariante 3 do documento 99 §6)

#### Scenario: Não há caminho para cadastrar Mestre

- **WHEN** o Mestre percorre todas as áreas da App 09
- **THEN** em nenhuma delas lhe é oferecido cadastrar Mestre ou criar acesso de Mestre

#### Scenario: O perfil declara de quem é o cadastro

- **WHEN** o Mestre abre a área do próprio perfil
- **THEN** lê que o cadastro de Mestre é exclusivo de Admin, com habilidade comprovada

#### Scenario: O Mestre não edita o próprio cadastro

- **WHEN** o Mestre percorre a área do próprio perfil
- **THEN** não lhe é oferecido campo algum para alterar nome, e-mail ou papel — a área só
  alcança os artefatos comprobatórios

### Requirement: Toda tela da App 09 que grava dado pessoal avisa o que ali se coleta

A App 09 SHALL exibir um **aviso discreto** do que está sendo coletado em toda tela em que grava
dado pessoal — o cadastro do responsável e o vínculo; o perfil do próprio Mestre; o conteúdo
autoral da missão; a conferência de presença; o lançamento do desfecho da atividade; a
ocorrência de conduta; e a validação da criação original. Cada aviso SHALL nomear o dado
**daquela** tela, na linha correspondente da tabela do PRD-09 §11, e SHALL oferecer o acesso à
área detalhada de direitos. O aviso NEVER SHALL bloquear a tela, NEVER SHALL exigir confirmação
para continuar e NEVER SHALL impedir o envio do formulário. (`RF-09-68`, PRD-09 §11,
documento 03 §12)

#### Scenario: A tela de cadastro do responsável traz o aviso

- **WHEN** o Mestre abre o cadastro do responsável
- **THEN** um aviso discreto informa o que aquela tela coleta e dá acesso à área detalhada

#### Scenario: O aviso nomeia o dado daquela tela

- **WHEN** o Mestre abre a ocorrência de conduta ou o lançamento do desfecho da atividade
- **THEN** o aviso nomeia o dado daquela tela, e não o de outra

#### Scenario: O aviso não atrapalha o uso

- **WHEN** o aviso está exibido numa tela de cadastro, de lançamento ou de validação
- **THEN** o Mestre preenche e envia o formulário sem confirmar o aviso, e nada fica bloqueado

### Requirement: A App 09 abre a área Direitos e dados, em leitura

A App 09 SHALL oferecer a área **Direitos e dados**, alcançável pela navegação e por **todo**
aviso de coleta, que apresenta, para cada dado que o Mestre coleta, a **finalidade**, a **base
legal**, o **prazo de retenção** e **quem acessa**, conforme a tabela do PRD-09 §11. A área SHALL
declarar também que o Mestre **não vê imagem real de Guerreiro(a)** em tela alguma, que a criação
original só vai à vitrine com autorização do responsável, que a pontuação negativa fica restrita
à gestão e ao responsável daquele Guerreiro(a), e que o pedido de acesso, correção ou exclusão
chega pela App 07 e é tratado pela gestão. A área é de **leitura**: NEVER SHALL oferecer escrita,
exclusão ou exportação de dado. (`RF-09-68`, `RN-09-18`, `RN-09-19`, PRD-09 §11)

#### Scenario: A área apresenta o destino de cada dado

- **WHEN** o Mestre abre a área Direitos e dados
- **THEN** vê, para cada dado coletado, a finalidade, a base legal, o prazo de retenção e quem
  acessa

#### Scenario: O aviso leva à área

- **WHEN** o Mestre aciona o acesso à área detalhada a partir do aviso de uma tela que coleta
- **THEN** chega à área Direitos e dados

#### Scenario: A área é só de leitura

- **WHEN** o Mestre lê a área Direitos e dados
- **THEN** não lhe é oferecida escrita, exclusão nem exportação de dado, e o pedido de direitos
  é declarado como caminho da App 07

### Requirement: O Mestre cadastra o tópico e recebe a estrutura sugerida da missão

A App 09 SHALL oferecer, na missão de que o Mestre é autor, um campo de **texto corrente** para
ele cadastrar o **tópico que quer ensinar**, e SHALL apresentar a **estrutura sugerida** que o
núcleo devolve: as atividades propostas, com modalidade e formato, a produção que cada uma pede,
o desafio de desbloqueio, a retomada sugerida e a etiqueta ODS proposta.

O campo NEVER SHALL pedir formato, marcação, palavra-chave nem qualquer instrução técnica: o
Mestre escreve como falaria. Não vindo a sugestão do núcleo, a aplicação SHALL dizer em
linguagem simples que ela não veio e SHALL manter aberto todo o caminho de escrever a missão à
mão. (`RF-09-85`, `RF-09-91`, `RF-09-95`, `RF-09-116`, `RN-09-16`, PRD-09 §10)

#### Scenario: O Mestre escreve o tópico como falaria

- **WHEN** o Mestre autor abre o template de uma missão dele
- **THEN** encontra um campo de texto corrente para o tópico, sem pedido de formato, marcação ou
  palavra-chave

#### Scenario: A estrutura sugerida é apresentada

- **WHEN** o Mestre autor envia o tópico
- **THEN** a aplicação apresenta as atividades propostas, a retomada sugerida e a etiqueta ODS
  proposta

#### Scenario: Sugestão que não veio não trava a autoria

- **WHEN** o núcleo não consegue devolver a sugestão
- **THEN** a aplicação diz em linguagem simples que ela não veio, sem código de erro, e o Mestre
  segue escrevendo a missão à mão

### Requirement: A App 09 mostra as lacunas e não grava nada sem o Mestre confirmar

A App 09 SHALL apresentar as **lacunas** da missão em linguagem simples — sem atividade,
atividade sem produção do Guerreiro(a), retomada não declarada e, em trilha de poder técnico,
missão sem atividade desplugada — e SHALL permitir ao Mestre **aceitar, recusar ou alterar** cada
sugestão, uma a uma.

Nenhuma sugestão SHALL ser gravada na trilha sem o Mestre confirmar, e a aplicação NEVER SHALL
apresentar como já gravado o que ainda é proposta. O que ele aceita ou altera SHALL ser gravado
pelas mesmas telas e rotas de autoria que já existem, com as mesmas recusas. A App 09 NEVER
SHALL escrever o **conteúdo** da missão a partir da sugestão: o conteúdo é escrito pelo Mestre,
autor creditado. (`RF-09-86`, `RF-09-87`, `RF-09-89`, `RN-09-33`, PRD-09 §12)

#### Scenario: As lacunas aparecem em linguagem simples

- **WHEN** a missão está sem atividade e sem retomada declarada
- **THEN** a aplicação diz que falta ao menos uma atividade e que a retomada não foi declarada,
  sem jargão e sem código de erro

#### Scenario: A sugestão fica distinta do que já está gravado

- **WHEN** a aplicação apresenta a estrutura sugerida
- **THEN** cada item vem marcado como proposta, distinto do que já está gravado na missão

#### Scenario: O Mestre aceita uma sugestão por vez

- **WHEN** o Mestre autor aceita uma das atividades sugeridas
- **THEN** só ela é gravada, pelo mesmo caminho de criação de atividade, e as demais seguem como
  proposta

#### Scenario: O Mestre altera antes de gravar

- **WHEN** o Mestre autor altera o texto de uma sugestão e a aceita
- **THEN** o que a aplicação grava é o texto dele

#### Scenario: A recusa não muda a missão

- **WHEN** o Mestre autor recusa a estrutura sugerida
- **THEN** nada é gravado e a missão permanece exatamente como estava

#### Scenario: O template não escreve o conteúdo

- **WHEN** o Mestre autor aceita tudo o que foi sugerido
- **THEN** o conteúdo da missão continua vazio até que ele o escreva

### Requirement: O Mestre declara a recompensa que o desbloqueio da missão libera

A App 09 SHALL permitir ao **Mestre autor** declarar, junto da missão, que o **desbloqueio** dela
libera **recompensa**, escolhendo o tipo de recurso e a **quantidade**, e SHALL apresentar a
recompensa declarada junto da missão na trilha.

A tela NEVER SHALL oferecer preço, saldo de pontos ou qualquer contrapartida do Guerreiro(a): a
recompensa de marco é conquistada, nunca comprada nem trocada. A aplicação NEVER SHALL exigir
lastro na declaração nem avisar que ele falta: a conferência acontece na entrega.
(`RF-09-84`, `RF-09-71`, `RF-09-72`, `RN-09-26`, `RN-09-27`, `RN-09-39`, invariante 23)

#### Scenario: O Mestre autor declara a recompensa do desbloqueio

- **WHEN** o Mestre autor declara que o desbloqueio de uma missão dele libera 30 unidades de um
  tipo de recurso
- **THEN** a aplicação grava a declaração e a apresenta junto da missão

#### Scenario: A tela não oferece preço nem troca

- **WHEN** o Mestre autor abre a declaração de recompensa
- **THEN** nenhum campo pede preço, pontos ou contrapartida do Guerreiro(a)

#### Scenario: A declaração não exige lastro

- **WHEN** o Mestre autor declara recompensa de um tipo sem saldo em ponto de apoio algum
- **THEN** a aplicação grava a declaração normalmente, sem aviso de falta de lastro

### Requirement: A App 09 apresenta ao Mestre as entregas de recompensa pendentes

A App 09 SHALL apresentar ao Mestre, em **Minhas turmas**, a fila das **entregas pendentes**: os
Guerreiros e Guerreiras da comunidade dele que alcançaram marco com recompensa declarada e ainda
não a receberam, com a trilha, o marco, o tipo de recurso e a quantidade. Confirmada a entrega
pelo Mestre, a pendência SHALL sair da fila.

Cada Guerreiro(a) SHALL aparecer por **nick e avatar**, e nenhuma imagem real SHALL ser exibida.
A fila NEVER SHALL exibir valor em moedas nem em reais. Recusada a entrega pelo núcleo, a
aplicação SHALL dizer em linguagem simples qual foi o motivo — falta de lastro, quantidade
esgotada ou marco não alcançado —, sem código de erro. (`RF-09-75`, `RF-09-76`, `RN-09-18`,
invariantes 12 e 16, PRD-09 §12)

#### Scenario: A fila mostra quem conquistou e ainda não recebeu

- **WHEN** um Guerreiro(a) da comunidade do Mestre desbloqueia missão com recompensa declarada
- **THEN** a aplicação passa a apresentá-lo na fila de entregas pendentes, com a trilha, o marco,
  o tipo de recurso e a quantidade

#### Scenario: A entrega confirmada sai da fila

- **WHEN** o Mestre confirma a entrega pela aplicação
- **THEN** a pendência deixa de aparecer na fila

#### Scenario: A recusa da entrega é traduzida

- **WHEN** o núcleo recusa a entrega por falta de lastro no ponto de apoio
- **THEN** a aplicação diz em linguagem simples que falta o recurso naquele ponto de apoio, sem
  código de erro

#### Scenario: A fila não exibe imagem real nem custo

- **WHEN** a aplicação apresenta a fila de entregas pendentes
- **THEN** cada Guerreiro(a) aparece por nick e avatar, e nenhum campo traz valor em moedas ou
  em reais

### Requirement: O Mestre duplica uma trilha pela lista de trilhas

A App 09 SHALL permitir ao Mestre **duplicar** uma trilha a partir da lista de trilhas, criando
uma trilha nova **em rascunho** sob a autoria dele, e SHALL levá-lo à trilha nova logo em
seguida, para que ele a edite.

A aplicação SHALL deixar claro, antes de duplicar, que a cópia nasce em **rascunho**, que ela
traz as missões e as atividades da origem e que **não** traz o percurso de Guerreiro(a) algum. A
trilha de origem NEVER SHALL ser apresentada como alterada pela duplicação. (`RF-09-13`,
`RF-09-04`, `RN-09-05`)

#### Scenario: O Mestre duplica e cai na trilha nova

- **WHEN** o Mestre pede a duplicação de uma trilha publicada
- **THEN** a aplicação cria a cópia em rascunho sob a autoria dele e o leva à trilha nova

#### Scenario: A aplicação diz o que a cópia traz e o que não traz

- **WHEN** o Mestre pede a duplicação
- **THEN** a aplicação avisa, antes de duplicar, que a cópia nasce em rascunho, traz missões e
  atividades e não traz percurso de Guerreiro(a) algum

#### Scenario: A trilha de origem segue como estava

- **WHEN** a duplicação termina
- **THEN** a trilha de origem continua na lista com a mesma situação e o mesmo autor
