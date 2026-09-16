## MODIFIED Requirements

### Requirement: O Mestre declara a culminância da trilha

A App 09 SHALL oferecer ao Mestre autor, dentro da trilha, a declaração da **culminância** —
descrição da criação original esperada, modalidade individual ou em equipe, e critério de
validação. A aplicação SHALL apresentar a culminância já declarada e permitir substituí-la, e
NEVER SHALL oferecer a declaração em trilha de outro Mestre.

A culminância apresentada SHALL ser a **gravada no núcleo**, não apenas a declarada na sessão
corrente: ao reabrir a trilha em sessão nova, a aplicação SHALL apresentar a descrição, a
modalidade e o critério de validação já gravados, e o formulário de substituição SHALL nascer
**preenchido** com eles. A aplicação NEVER SHALL afirmar que a trilha não tem culminância
quando ela existe no núcleo, e NEVER SHALL oferecer a declaração como se fosse a primeira
quando há uma a substituir — declarar de novo substitui a anterior, e um formulário vazio faria
o Mestre perder o critério que já escreveu. (`RF-09-29`, `RF-09-30`)

#### Scenario: Mestre declara a culminância

- **WHEN** o Mestre autor preenche descrição, modalidade e critério e confirma
- **THEN** a aplicação grava a culminância no núcleo e passa a apresentá-la na trilha

#### Scenario: Campo obrigatório em falta

- **WHEN** o Mestre confirma sem o critério de validação
- **THEN** a aplicação apresenta a recusa em linguagem simples e nada é gravado

#### Scenario: A declaração substitui a culminância anterior

- **WHEN** o Mestre autor declara a culminância de uma trilha que já tem uma
- **THEN** a aplicação apresenta os novos valores no lugar dos anteriores

#### Scenario: A culminância reabre em sessão nova

- **WHEN** o Mestre autor declarou a culminância numa sessão anterior e abre a trilha em sessão
  nova, sem declarar nada antes
- **THEN** a aplicação apresenta a culminância gravada, e não a mensagem de que a trilha ainda
  não tem culminância declarada

#### Scenario: O formulário de substituição nasce preenchido

- **WHEN** o Mestre autor abre a alteração da culminância de uma trilha que já tem uma
- **THEN** a descrição, a modalidade e o critério de validação gravados já estão no formulário

### Requirement: O Mestre pré-visualiza a missão como o Guerreiro(a) a verá

A App 09 SHALL oferecer ao Mestre autor a **pré-visualização** da missão, apresentando-a na
ordem e na forma em que o Guerreiro(a) a encontrará, antes de a trilha ser publicada. A
pré-visualização NEVER SHALL gravar coisa alguma e NEVER SHALL alterar a situação da trilha. A
pré-visualização SHALL refletir o que foi gravado em **qualquer sessão anterior**, não só o
declarado na sessão corrente.

A pré-visualização SHALL apresentar: o **título** da missão; se ela é **opcional**, no mesmo
aviso que o Guerreiro(a) recebe; o **conteúdo** na ordem disposta, com o texto legível e a
imagem e o vídeo **exibidos** — nunca descritos por frase nem pela referência do armazenamento
—; o **crédito ao autor** e a **licença**; a **bibliografia**, com título e capítulo; as
**atividades** declaradas, que é por elas que o Guerreiro(a) entrega a produção; e o **desafio
de desbloqueio**, ou a **sondagem**, em leitura. Conteúdo cujo envio não foi concluído SHALL
ser dito pendente, nunca apresentado como quebrado. A pré-visualização NEVER SHALL apresentar
menos do que o Guerreiro(a) verá naquela missão. (`RF-09-25`, `RF-09-14`, `RF-09-15`,
`RF-09-21`, `RF-09-26`, `RF-09-81`)

#### Scenario: Mestre pré-visualiza antes de publicar

- **WHEN** o Mestre autor abre a pré-visualização de uma missão de trilha em rascunho
- **THEN** a aplicação apresenta o conteúdo e a bibliografia como o Guerreiro(a) os verá

#### Scenario: A pré-visualização não grava nada

- **WHEN** o Mestre autor fecha a pré-visualização
- **THEN** nada foi gravado e a situação da trilha permanece inalterada

#### Scenario: A pré-visualização reflete conteúdo gravado em sessão anterior

- **WHEN** o Mestre autor declarou conteúdo numa sessão anterior e abre a pré-visualização em
  sessão nova, sem declarar nada antes
- **THEN** a pré-visualização apresenta o conteúdo já gravado, e não a mensagem de que a missão
  ainda não tem conteúdo

#### Scenario: A pré-visualização apresenta as atividades declaradas

- **WHEN** o Mestre autor abre a pré-visualização de uma missão que tem atividades declaradas
- **THEN** as atividades aparecem, como o Guerreiro(a) as encontrará ao entregar a produção

#### Scenario: A imagem enviada aparece como imagem

- **WHEN** o Mestre autor abre a pré-visualização de uma missão cujo conteúdo tem imagem com
  envio confirmado
- **THEN** a imagem é exibida, e nenhuma referência de armazenamento nem frase a substitui

#### Scenario: Envio não concluído é dito pendente

- **WHEN** a missão tem conteúdo de arquivo cujo envio nunca foi confirmado
- **THEN** a pré-visualização diz que o envio está pendente, sem apresentar arquivo quebrado

#### Scenario: A pré-visualização apresenta o desbloqueio e a obrigatoriedade

- **WHEN** o Mestre autor abre a pré-visualização de uma missão opcional com desafio de
  desbloqueio declarado
- **THEN** o aviso de missão opcional e o desafio de desbloqueio aparecem, em leitura
