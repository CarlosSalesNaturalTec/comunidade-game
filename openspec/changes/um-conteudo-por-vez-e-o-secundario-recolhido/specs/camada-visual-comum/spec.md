# Spec Delta

## RENAMED Requirements

- FROM: `### Requirement: A camada comum entrega o bloco recolhível das telas da Operação`
- TO: `### Requirement: A camada comum entrega o bloco recolhível, com um uso em cada temperamento`

## MODIFIED Requirements

### Requirement: A camada comum entrega o bloco recolhível, com um uso em cada temperamento

A camada comum SHALL entregar um bloco recolhível para as telas do temperamento Operação que
reúnem muitos blocos de declaração. O bloco SHALL nascer **fechado** e SHALL apresentar, na
linha fechada, o **resumo do estado** que quem o monta declara — quantos itens ele guarda, ou
que não guarda nenhum —, para a existência de cada parte ficar visível sem o peso do conteúdo
de todas. O controle de abrir e fechar SHALL ser botão com rótulo textual e SHALL declarar se
o bloco está aberto ou fechado a quem navega por leitor de tela. O bloco NEVER SHALL animar a
abertura, e NEVER SHALL comunicar seu estado apenas por cor ou apenas por ícone.
(PRD-02 §10, documento 15 §§5, 6.1, decisão do fundador de 2026-09-07)

Nas telas do temperamento **Arena** o mesmo bloco SHALL servir a **outro uso, e só a ele**:
tirar do fluxo de leitura o que é **secundário** — metadado da obra, e o que adianta o que a
pessoa ainda não alcançou —, sem apagá-lo da tela. Ali o resumo da linha fechada SHALL ser
**neutro**: SHALL nomear o que o bloco guarda e NEVER SHALL repetir o conteúdo recolhido, sob
pena de o recolhimento não recolher nada. **Empilhar blocos de declaração** na mesma tela
NEVER SHALL acontecer na Arena, que põe uma decisão por tela. (documento 15 §§6.1, 6.4,
decisão do fundador de 2026-09-26)

O que o bloco recolhe SHALL continuar **alcançável** em qualquer temperamento: recolher NEVER
SHALL equivaler a suprimir, e nenhuma informação que um requisito manda apresentar SHALL
deixar de existir na tela por estar dentro de um bloco fechado.

#### Scenario: Tela que reúne muitos blocos abre com todos fechados

- **WHEN** o operador abre uma tela da Operação montada com blocos recolhíveis
- **THEN** todos os blocos aparecem fechados, e cada linha fechada apresenta o resumo do
  estado do seu bloco

#### Scenario: Bloco sem conteúdo declara que está vazio

- **WHEN** um bloco recolhível não guarda item nenhum
- **THEN** a linha fechada diz que não há nenhum, e o bloco continua visível e alcançável

#### Scenario: Operador abre e fecha um bloco

- **WHEN** o operador aciona o controle de um bloco fechado
- **THEN** o conteúdo do bloco passa a ser apresentado sem animação de altura, o controle
  informa que o bloco está aberto, e acioná-lo de novo o fecha

#### Scenario: Quem navega por leitor de tela alcança o bloco

- **WHEN** um leitor de tela percorre a tela
- **THEN** o controle de cada bloco é anunciado com rótulo textual e com o estado de aberto
  ou fechado, sem depender de cor nem de ícone

#### Scenario: Na Arena, o resumo neutro não entrega o que o bloco guarda

- **WHEN** uma tela da Arena recolhe num bloco o que é secundário à leitura
- **THEN** a linha fechada nomeia o que está ali sem repetir o conteúdo recolhido, e o bloco
  abre ao ser acionado

#### Scenario: O recolhido continua alcançável

- **WHEN** uma informação que um requisito manda apresentar é posta dentro de um bloco
  recolhível
- **THEN** ela continua presente na tela e alcançável pelo controle do bloco, inclusive por
  leitor de tela
