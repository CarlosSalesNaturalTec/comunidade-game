## Purpose

O desafio de coleta é o que o Mestre declara dentro da própria trilha para que o Guerreiro(a)
abra depois uma série e passe a medir o território: o tipo do catálogo, a cadência, a vigência, a
granularidade exigida e quantos registros do mesmo período pontuam. É o elo entre a trilha, que
já existe, e a série, que vem da fatia seguinte.

## Requirements

### Requirement: O desafio de coleta é criado pelo Mestre autor, preso a uma missão da sua trilha

O núcleo SHALL permitir que o **Mestre autor da trilha** crie desafio de coleta vinculado a uma
**missão daquela trilha** — a mesma posse já aplicada à trilha e à etiqueta ODS, conferida pela
trilha alcançada a partir de `missão.trilha_id`: uma missão de trilha que o operador não é autor
SHALL ser recusada com **403**, o mesmo status de qualquer outro Mestre que não é o autor. Missão
**inexistente** SHALL ser recusada com **422**. Toda escrita SHALL gravar autoria, data e hora.
(`RF-08-06`, `RF-01-03`, `RF-01-16`, PRD-08 §§4, 5.2)

#### Scenario: Mestre autor cria o desafio na própria trilha

- **WHEN** o Mestre autor da trilha cria um desafio de coleta vinculado a uma missão dela
- **THEN** o núcleo grava o desafio com o autor, a data e a hora com fuso

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor da trilha tenta criar desafio de coleta nela, apontando uma
  missão que pertence a essa trilha de outro autor
- **THEN** o núcleo responde 403 e nenhum desafio é criado

#### Scenario: Missão inexistente é recusada

- **WHEN** chega um desafio de coleta apontando um `missao_id` que não existe
- **THEN** o núcleo responde 422 e nenhum desafio é criado

### Requirement: O desafio declara tipo, cadência, vigência, granularidade e registros que pontuam

O núcleo SHALL exigir do desafio de coleta: o **tipo** escolhido no catálogo, a **cadência** —
uma entre **diária**, **semanal** e **mensal** —, a **vigência** com data de início e data de
fim, a **granularidade exigida** e **quantos registros do mesmo período de cadência pontuam**,
que SHALL ser inteiro maior ou igual a 1. Desafio sem qualquer um desses atributos SHALL ser
recusado com **422**, apontando o campo em falta; cadência fora das três, vigência cujo fim
precede o início, ou quantidade menor que 1 SHALL ser recusada com **422**. (`RF-08-06`,
`RN-08-06`, PRD-08 §§5.2, 8, 02 §1)

#### Scenario: Desafio completo é aceito

- **WHEN** o Mestre autor declara tipo, cadência semanal, vigência do ciclo, granularidade `rua`
  e um registro que pontua por período
- **THEN** o núcleo grava o desafio com os cinco atributos

#### Scenario: Desafio sem cadência é recusado

- **WHEN** chega um desafio de coleta sem cadência declarada
- **THEN** o núcleo responde 422 apontando o campo em falta e nada é gravado

#### Scenario: Cadência fora das três é recusada

- **WHEN** chega um desafio com cadência `anual`
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Vigência invertida é recusada

- **WHEN** chega um desafio cuja data de fim da vigência precede a data de início
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Quantidade de registros que pontuam menor que 1 é recusada

- **WHEN** chega um desafio declarando que zero registros do período pontuam
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A granularidade exigida é declarada livremente no desafio

O núcleo SHALL aceitar como granularidade exigida qualquer um dos seis níveis da hierarquia do
território — **comunidade**, **bairro**, **rua**, **condomínio**, **bloco** e **quadra** — sem
conferi-la contra a granularidade máxima de comunidade alguma. A trilha publicada alcança todas
as comunidades, e cada uma declara a sua granularidade máxima, de modo que não há comunidade
única contra a qual conferir o teto na criação do desafio. O teto SHALL ser conferido **na
abertura da série**, contra a comunidade do Guerreiro(a) — comportamento de `RF-08-07`, fora
desta capacidade. Nível fora dos seis SHALL ser recusado com **422**. (`RN-08-25`, `RF-08-06`,
02 §1)

#### Scenario: Granularidade mais fina que a de uma comunidade é aceita

- **WHEN** o Mestre declara granularidade `quadra` num desafio, e existe comunidade cuja
  granularidade máxima é `rua`
- **THEN** o núcleo grava o desafio, sem consultar comunidade alguma

#### Scenario: A criação do desafio não consulta comunidade

- **WHEN** um desafio de coleta é criado
- **THEN** nenhuma Comunidade Virtual é lida para validar a granularidade exigida

#### Scenario: Nível fora da hierarquia é recusado

- **WHEN** chega um desafio com granularidade exigida `município`
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A trilha sem desafio de coleta não é recusada nesta capacidade

O núcleo NEVER SHALL recusar a criação ou a alteração de trilha ou de missão por ainda não haver
desafio de coleta vinculado. `RN-08-14` exige ao menos um desafio por trilha, e a trava mora na
**publicação da trilha**, que é do PRD-09 — mesmo precedente da sondagem, cuja recusa de publicar
é `RF-09-82`. Aqui o desafio nasce; quem o exige é quem publica. (`RN-08-14`, PRD-08 §5.2)

#### Scenario: Trilha em rascunho sem desafio de coleta é aceita

- **WHEN** um Mestre autor grava uma trilha em rascunho sem nenhum desafio de coleta vinculado
- **THEN** o núcleo aceita a trilha, porque a trava é conferida na publicação
