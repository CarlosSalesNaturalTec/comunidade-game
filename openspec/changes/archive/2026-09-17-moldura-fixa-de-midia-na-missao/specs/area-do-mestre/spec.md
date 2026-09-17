## MODIFIED Requirements

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
de desbloqueio**, ou a **sondagem**, em leitura — com a **imagem** que a pergunta do quiz tiver,
e não só o enunciado e as alternativas. Conteúdo cujo envio não foi concluído SHALL ser dito
pendente, nunca apresentado como quebrado. A pré-visualização NEVER SHALL apresentar menos do
que o Guerreiro(a) verá naquela missão. (`RF-09-25`, `RF-09-14`, `RF-09-15`, `RF-09-21`,
`RF-09-26`, `RF-09-81`, `RF-09-119`)

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

#### Scenario: A pré-visualização apresenta a imagem da pergunta do quiz

- **WHEN** o Mestre autor abre a pré-visualização de uma missão de sondagem, ou com desafio de
  desbloqueio em quiz, cuja pergunta tem imagem
- **THEN** a imagem aparece junto do enunciado daquela pergunta, como o Guerreiro(a) a verá

## ADDED Requirements

### Requirement: A mídia exibida pela App 09 usa moldura de tamanho fixo

Toda imagem e todo vídeo que a App 09 busca do núcleo em bytes — o conteúdo da missão na
pré-visualização, a imagem da pergunta do quiz na pré-visualização e a imagem da pergunta na
edição do desafio de desbloqueio — SHALL ser exibidos numa moldura de **tamanho fixo**, igual
para os três casos, sem crescer além dela: a imagem ou o vídeo inteiro cabe dentro da moldura,
sem ser cortado para preenchê-la, e o espaço que sobrar fica em branco. A moldura NEVER SHALL
oferecer ampliação nem abrir a mídia em tamanho maior. (`RF-09-25`, `RF-09-119`, decisão do
fundador de 2026-09-17)

#### Scenario: Imagem grande cabe na moldura fixa, sem cortar

- **WHEN** o Mestre autor abre a pré-visualização de uma missão cujo conteúdo tem uma foto de
  alta resolução
- **THEN** a foto aparece inteira, dentro da moldura de tamanho fixo, sem estourar o layout

#### Scenario: Vídeo usa a mesma moldura da imagem

- **WHEN** o Mestre autor abre a pré-visualização de uma missão cujo conteúdo tem vídeo
- **THEN** o vídeo aparece na mesma moldura de tamanho fixo que a imagem usa

#### Scenario: A moldura não amplia ao ser tocada

- **WHEN** o Mestre autor toca numa imagem ou num vídeo exibidos em moldura fixa
- **THEN** nada se amplia; a mídia permanece no mesmo tamanho

#### Scenario: A imagem anexada na edição do desafio usa a mesma moldura

- **WHEN** o Mestre autor abre o quiz de uma pergunta que tem imagem anexada
- **THEN** a imagem aparece na mesma moldura de tamanho fixo que a pré-visualização usa
