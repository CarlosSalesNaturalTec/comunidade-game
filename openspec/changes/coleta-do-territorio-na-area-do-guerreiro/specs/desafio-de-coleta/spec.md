## ADDED Requirements

### Requirement: O Guerreiro(a) lê os desafios de coleta que pode assumir

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** os desafios de coleta que ele **pode
assumir** — os **vigentes** no instante da consulta cuja **granularidade exigida** cabe no teto
de granularidade da **sua Comunidade Virtual**. As duas condições SHALL ser exatamente as que a
abertura da série já confere: a leitura NEVER SHALL declarar elegível um desafio que a abertura
recusaria, nem esconder um que ela aceitaria. (`RF-05-30`, `RN-05-24`, PRD-05 §§5.4, 6.4)

Cada desafio SHALL sair com o **tipo de coleta** — nome, forma de registro e unidade quando
houver —, a **cadência**, a **vigência**, a **granularidade exigida** e a **missão** e a
**trilha** de que ele nasce, para que a criança reconheça o que vai medir e por quê. O desafio
sobre o qual o Guerreiro(a) **já tem série aberta naquele local** SHALL sair assinalado como
tal, para que a aplicação não ofereça uma abertura que o núcleo recusaria.

A consulta SHALL ser paginada como toda listagem do núcleo e SHALL recusar com **403** a
persona de outro papel.

#### Scenario: O Guerreiro(a) vê os desafios vigentes que cabem na sua comunidade

- **WHEN** um Guerreiro(a) em sessão consulta os desafios de coleta que pode assumir
- **THEN** o núcleo devolve os desafios vigentes cuja granularidade exigida cabe no teto da
  Comunidade Virtual dele, cada um com tipo, cadência, vigência, granularidade, missão e trilha

#### Scenario: Desafio fora da vigência não aparece

- **WHEN** um desafio de coleta teve a vigência encerrada
- **THEN** ele não aparece na lista dos que o Guerreiro(a) pode assumir

#### Scenario: Desafio mais fino que o teto da comunidade não aparece

- **WHEN** um desafio exige granularidade mais fina que o teto da Comunidade Virtual do
  Guerreiro(a)
- **THEN** ele não aparece na lista, porque a abertura da série o recusaria

#### Scenario: A leitura concorda com a abertura da série

- **WHEN** o Guerreiro(a) tenta abrir série sobre um desafio que a lista trouxe, num local do
  nível exigido da sua comunidade
- **THEN** a abertura é aceita

#### Scenario: Desafio com série já aberta no local sai assinalado

- **WHEN** o Guerreiro(a) já tem série aberta sobre aquele desafio naquele local
- **THEN** o desafio sai da lista assinalado como já assumido naquele local

#### Scenario: Outro papel não lê pela porta do Guerreiro(a)

- **WHEN** um Mestre ou um Admin chama a consulta dos desafios que o Guerreiro(a) pode assumir
- **THEN** o núcleo responde 403
