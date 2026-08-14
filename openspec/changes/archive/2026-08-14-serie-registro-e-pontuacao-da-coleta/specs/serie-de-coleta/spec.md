## Purpose

A série de coleta é o compromisso individual do Guerreiro(a) com um desafio num ponto do
território: é ela que dá endereço à medição, herda a cadência do desafio e sustenta a
progressão do Poder do Território enquanto estiver viva.

## ADDED Requirements

### Requirement: O Guerreiro(a) abre a série sobre um desafio e um local da sua comunidade

O núcleo SHALL abrir a série de coleta a pedido de um **Guerreiro(a) em sessão**, sobre um
**desafio de coleta** vigente e um **local** cadastrado na Comunidade Virtual a que ele está
vinculado. A série SHALL nascer com a **cadência herdada do desafio** e no estado **`ativa`**.
Persona de outro papel SHALL receber **403**. Local de outra comunidade SHALL ser recusado com
**403**, e desafio fora da vigência SHALL ser recusado com **422**. (`RF-08-07`, `RN-08-02`,
PRD-08 §§4, 5.3, 9)

#### Scenario: Guerreiro(a) abre a série sobre desafio vigente e local da sua comunidade

- **WHEN** um Guerreiro(a) em sessão abre série sobre um desafio vigente, escolhendo um local
  cadastrado na comunidade a que está vinculado
- **THEN** o núcleo grava a série no estado `ativa`, com a cadência do desafio, o coletor da
  sessão e o local escolhido

#### Scenario: Local de outra comunidade é recusado

- **WHEN** um Guerreiro(a) vinculado à comunidade A tenta abrir série sobre um local da
  comunidade B
- **THEN** o núcleo responde 403 e nenhuma série é gravada

#### Scenario: Desafio fora da vigência é recusado

- **WHEN** um Guerreiro(a) tenta abrir série sobre um desafio cuja vigência já terminou
- **THEN** o núcleo responde 422 e nenhuma série é gravada

#### Scenario: Mestre não abre série

- **WHEN** um Mestre em sessão tenta abrir uma série
- **THEN** o núcleo responde 403 e nenhuma série é gravada

### Requirement: A abertura da série confere o teto de granularidade da comunidade

O núcleo SHALL conferir, **na abertura da série**, a **granularidade exigida pelo desafio**
contra a **granularidade máxima da Comunidade Virtual** do Guerreiro(a), e SHALL recusar com
**422** a abertura cuja granularidade exigida seja mais fina que o teto daquela comunidade. O
**nível do local escolhido** SHALL corresponder à granularidade exigida pelo desafio; nível
diferente SHALL ser recusado com **422**. É aqui — e não na criação do desafio — que o teto é
conferido. (`RN-08-25`, `RF-08-07`, 02 §1)

#### Scenario: Granularidade exigida mais fina que o teto da comunidade é recusada

- **WHEN** um Guerreiro(a) de comunidade cuja granularidade máxima é `rua` tenta abrir série
  sobre desafio que exige granularidade `quadra`
- **THEN** o núcleo responde 422 e nenhuma série é gravada

#### Scenario: Granularidade exigida dentro do teto é aceita

- **WHEN** um Guerreiro(a) de comunidade cuja granularidade máxima é `quadra` abre série sobre
  desafio que exige granularidade `rua`, escolhendo um local de nível `rua`
- **THEN** o núcleo grava a série

#### Scenario: Local de nível diferente da granularidade exigida é recusado

- **WHEN** o desafio exige granularidade `rua` e o Guerreiro(a) escolhe um local de nível
  `bairro`
- **THEN** o núcleo responde 422 e nenhuma série é gravada

### Requirement: A série é individual e pertence a quem está na sessão

O núcleo SHALL manter **um único coletor por série** e SHALL atribuí-la ao **Guerreiro(a) da
sessão**, nunca ao aparelho de onde veio a chamada — o ponto de apoio usa aparelho
compartilhado. O núcleo SHALL recusar com **409** a abertura de uma segunda série do mesmo
Guerreiro(a) sobre o mesmo par de desafio e local, e NEVER SHALL aceitar coletor informado no
corpo da requisição. (`RN-08-04`, PRD-08 §§8, 10)

#### Scenario: A série é do Guerreiro(a) da sessão

- **WHEN** um Guerreiro(a) abre série informando no corpo o identificador de outro Guerreiro(a)
  como coletor
- **THEN** o núcleo ignora o coletor informado e grava a série em nome do Guerreiro(a) da sessão

#### Scenario: Série duplicada do mesmo par de desafio e local é recusada

- **WHEN** um Guerreiro(a) que já tem série sobre um desafio e um local tenta abrir outra sobre
  o mesmo par
- **THEN** o núcleo responde 409 e nenhuma série nova é gravada

#### Scenario: Dois Guerreiros abrem série sobre o mesmo desafio e local

- **WHEN** dois Guerreiros e Guerreiras da mesma comunidade abrem série sobre o mesmo desafio e
  o mesmo local
- **THEN** o núcleo grava duas séries independentes, uma para cada coletor

### Requirement: A série nasce ativa e nesta entrega não muda de estado

O núcleo SHALL abrir a série no estado **`ativa`** e, nesta entrega, NEVER SHALL transitá-la
para `interrompida`, `encerrada` ou qualquer outro estado. A interrupção por dois períodos de
cadência sem registro, a retomada pelo registro seguinte e o encerramento pelo fim da vigência
do desafio SHALL ser comportamento de entrega posterior — `RF-08-10` e `RF-08-11` —, e a sua
ausência aqui NEVER SHALL impedir a abertura da série nem a gravação de registros. A série SHALL
guardar a **data da última medição válida**, que é o insumo daquela transição. (`RF-08-07`,
PRD-08 §8)

#### Scenario: Série recém-aberta aparece como ativa

- **WHEN** uma série é aberta
- **THEN** o núcleo a devolve no estado `ativa`, com a data de abertura gravada

#### Scenario: Série sem registro por dois períodos permanece ativa nesta entrega

- **WHEN** uma série de cadência semanal passa duas semanas sem nenhum registro
- **THEN** o núcleo a mantém no estado `ativa`, porque a transição para `interrompida` é de
  entrega posterior

#### Scenario: A data da última medição válida acompanha a série

- **WHEN** um registro válido é gravado numa série
- **THEN** o núcleo atualiza na série a data da última medição válida
