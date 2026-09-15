## MODIFIED Requirements

### Requirement: O Mestre escreve o conteúdo da missão

A App 09 SHALL oferecer ao Mestre autor, dentro da missão, a escrita do **conteúdo**: texto
formatado com imagens, link para vídeo hospedado fora da plataforma, e o envio de vídeo e de
arquivo de apoio. A aplicação SHALL apresentar o conteúdo já escrito na ordem declarada e
permitir reordená-lo, alterá-lo e removê-lo antes de publicar. Nenhum campo SHALL pedir código,
HTML, marcação ou configuração técnica, e NEVER SHALL oferecer a escrita em missão de trilha de
outro Mestre. A aplicação SHALL salvar o rascunho do texto automaticamente, de modo que queda de
rede NEVER SHALL perder o que já foi escrito. (`RF-09-14`, `RF-09-15`, `RF-09-24`, `RN-09-16`,
PRD-09 §10)

A aplicação SHALL apresentar o conteúdo já gravado toda vez que o Mestre autor volta à missão,
em sessão nova inclusive, e não apenas dentro da sessão em que foi escrito: a lista de
conteúdo NEVER SHALL aparecer vazia quando a missão tem conteúdo gravado. (`RF-09-14`,
`RF-09-15`)

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

#### Scenario: O conteúdo gravado reabre em sessão nova

- **WHEN** o Mestre autor anexou uma imagem como conteúdo da missão, saiu da aplicação e volta
  à mesma missão
- **THEN** a tela apresenta a imagem já gravada na lista de conteúdo, e não uma lista vazia

#### Scenario: Vários conteúdos de tipos diferentes reabrem juntos

- **WHEN** o Mestre autor declarou texto, imagem e vídeo na mesma missão e volta a ela em
  sessão nova
- **THEN** a tela apresenta os três, na ordem em que foram declarados

### Requirement: O Mestre declara a bibliografia da missão

A App 09 SHALL oferecer ao Mestre autor, dentro da missão, a declaração da **bibliografia** —
título e capítulo em texto — e, **opcionalmente**, o apontamento de um **exemplar do acervo**
escolhido de uma lista, nunca digitado como identificador. A aplicação SHALL apresentar as
entradas já declaradas e permitir acrescentar e remover. Havendo vínculo, a aplicação SHALL
apresentar ao Mestre a disponibilidade do exemplar e o Apoiador creditado; não havendo, NEVER
SHALL apresentar nem pedir nenhum dos dois. (`RF-09-21`, `RF-09-22`, `RF-09-23`)

A aplicação SHALL apresentar as entradas de bibliografia já gravadas toda vez que o Mestre
autor volta à missão, em sessão nova inclusive, e não apenas dentro da sessão em que foram
declaradas. (`RF-09-21`)

#### Scenario: Mestre declara bibliografia sem apontar exemplar

- **WHEN** o Mestre autor informa título e capítulo e confirma sem escolher exemplar
- **THEN** a aplicação grava a entrada e a apresenta sem disponibilidade nem crédito

#### Scenario: Mestre aponta o exemplar do acervo

- **WHEN** o Mestre autor escolhe um exemplar da lista do acervo e confirma
- **THEN** a aplicação grava a entrada com o vínculo e passa a apresentar a disponibilidade

#### Scenario: O Apoiador creditado não é digitado

- **WHEN** o Mestre autor declara bibliografia vinculada a exemplar
- **THEN** a aplicação apresenta o Apoiador que o núcleo devolveu, e não oferece campo para digitá-lo

#### Scenario: A bibliografia gravada reabre em sessão nova

- **WHEN** o Mestre autor declarou duas entradas de bibliografia numa missão, saiu da
  aplicação e volta a ela
- **THEN** a tela apresenta as duas entradas já declaradas, e não uma lista vazia

### Requirement: O Mestre pré-visualiza a missão como o Guerreiro(a) a verá

A App 09 SHALL oferecer ao Mestre autor a **pré-visualização** da missão, apresentando o
conteúdo e a bibliografia na ordem e na forma em que o Guerreiro(a) os encontrará, antes de a
trilha ser publicada. A pré-visualização NEVER SHALL gravar coisa alguma e NEVER SHALL alterar
a situação da trilha. A pré-visualização SHALL refletir o conteúdo e a bibliografia gravados
em qualquer sessão anterior, não só os declarados na sessão corrente. (`RF-09-25`)

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
