# Spec Delta

## ADDED Requirements

### Requirement: A App 09 declara a forma, o critério e o título curto do prático

Escolhido o tipo **desafio prático**, a tela SHALL pedir ao Mestre autor, ao lado do
enunciado, a **forma de comprovação aceita** — uma entre as seis —, o **critério de aceite** e
o **título curto**. Os três SHALL aparecer **somente** no prático: escolhido o quiz, a tela
NEVER SHALL apresentá-los nem mandá-los ao núcleo. (`RF-09-129` a `RF-09-131`, `RN-09-50`)

#### Scenario: Os três campos aparecem ao escolher o prático

- **WHEN** o Mestre autor abre o bloco do desafio de desbloqueio de uma missão sua e escolhe
  desafio prático
- **THEN** a tela apresenta o enunciado, a escolha da forma de comprovação, o critério de
  aceite e o título curto

#### Scenario: Ao escolher o quiz os três campos saem da tela

- **WHEN** o Mestre autor troca o tipo do desafio de prático para quiz
- **THEN** a tela deixa de apresentar os três campos e grava o quiz sem eles

#### Scenario: A sondagem não apresenta os campos do prático

- **WHEN** o Mestre autor abre o bloco da missão marcada como sondagem
- **THEN** a tela segue sem a escolha entre quiz e prático, e sem nenhum dos três campos,
  porque a sondagem é na forma de quiz (`RF-09-81`)

### Requirement: A tela diz ao Mestre para que serve cada um dos três campos

A tela SHALL dizer, em linguagem do Mestre, que a **forma de comprovação** é o que o
Guerreiro(a) vai poder entregar, que o **critério de aceite** é lido por ele na hora da
entrega e é o que o Mestre vai julgar, e que o **título curto** é o que aparece **na vitrine,
ao lado do nick**. A tela SHALL apresentar as seis formas pelo nome, para escolha, e NEVER
SHALL exigir que o Mestre digite o nome de uma delas. (`RF-09-129` a `RF-09-131`)

#### Scenario: A escolha da forma é por nome, entre as seis

- **WHEN** o Mestre autor escolhe a forma de comprovação do prático
- **THEN** a tela oferece texto, imagem, áudio, vídeo, arquivo e link externo pelo nome, e ele
  escolhe uma

#### Scenario: A tela diz onde o título curto vai aparecer

- **WHEN** o Mestre autor preenche o título curto
- **THEN** a tela diz que é esse título que a vitrine exibe ao lado do nick do Guerreiro(a)

### Requirement: A App 09 reabre os três campos do prático já declarado

A tela SHALL **reabrir** a forma de comprovação, o critério de aceite e o título curto toda vez
que o Mestre autor volta à missão, em sessão nova inclusive, pela mesma leitura que já reabre o
tipo e o enunciado. Prático declarado **antes** desta regra SHALL abrir com os três campos
**vazios** e NEVER SHALL ser apresentado como "sem desafio". (`RF-09-129` a `RF-09-131`,
`RN-09-50`)

#### Scenario: O Mestre autor volta à missão e encontra o que declarou

- **WHEN** o Mestre autor sai da trilha e volta à missão cujo prático ele declarou
- **THEN** a tela apresenta a forma escolhida, o critério de aceite e o título curto como ele
  os gravou

#### Scenario: Prático incompleto abre para ser completado

- **WHEN** o Mestre autor abre a missão de um prático declarado antes desta regra
- **THEN** a tela apresenta o enunciado que existe, os três campos vazios e o desafio como
  prático declarado

### Requirement: A recusa dos campos do prático chega ao Mestre com o motivo

A recusa de qualquer um dos três campos SHALL ser mostrada **no bloco do desafio**, com o
**motivo** que o núcleo deu — o campo que falta ou o teto do título —, nunca como falha
genérica, e NEVER SHALL apagar o que o Mestre já escreveu nos outros campos nem nas perguntas.
A tela SHALL dizer o **teto de 60 caracteres** do título curto antes do envio. (`RF-09-131`,
`RN-09-50`, `RN-09-51`)

#### Scenario: Campo em falta é dito pelo nome

- **WHEN** o Mestre autor grava o prático sem o critério de aceite
- **THEN** a tela diz que falta o critério de aceite, e o enunciado, a forma e o título que ele
  escreveu continuam na tela

#### Scenario: O teto do título é dito antes do envio

- **WHEN** o Mestre autor preenche o título curto do prático
- **THEN** a tela diz o teto de 60 caracteres, antes de ele tentar gravar

### Requirement: A pré-visualização da missão mostra o prático como o Guerreiro(a) o verá

A pré-visualização da missão SHALL apresentar, no desbloqueio prático, a **forma de
comprovação aceita** e o **critério de aceite** ao lado do enunciado — é o que o Guerreiro(a)
lê na hora de entregar. (`RF-09-25`, `RF-09-129`, `RF-09-130`)

#### Scenario: A pré-visualização traz a forma e o critério

- **WHEN** o Mestre autor pré-visualiza uma missão cujo desbloqueio é prático declarado
- **THEN** a pré-visualização mostra o enunciado, a forma de comprovação aceita e o critério de
  aceite
