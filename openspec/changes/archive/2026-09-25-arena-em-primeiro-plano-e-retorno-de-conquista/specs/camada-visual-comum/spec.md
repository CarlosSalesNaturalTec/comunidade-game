# Spec Delta

## ADDED Requirements

### Requirement: A Arena põe a ilustração em primeiro plano e devolve progresso e conquista

Nas aplicações do temperamento **Arena**, a camada comum SHALL apresentar a **ilustração em primeiro
plano**, com a **carta dominando a tela** e **uma decisão por tela** — a densidade baixa que o
documento 15 §6 atribui à Arena. NEVER SHALL reproduzir na Arena a densidade da Operação: tabela,
lote e painel são da outra família. (documento 15 §6, invariante 24)

A camada comum SHALL admitir **imagem de comunidade ao fundo** nas telas da Arena, atrás da cor
chapada. A imagem NEVER SHALL carregar significado sozinha, NEVER SHALL ser a única via a informação
alguma, e NEVER SHALL reduzir o contraste do texto e dos componentes que ficam sobre ela abaixo dos
pisos medidos — `4,5:1` em texto e `3:1` em componente, borda que informa e estado de foco.
(documento 15 §§3.3, 5, 6, princípio 3)

A camada comum SHALL apresentar, na Arena, **retorno de progresso e conquista**, com duração de
`300` ms e `ease-in-out`. O retorno SHALL acompanhar **fato real** — progresso alcançado, conquista
certificada — e NEVER SHALL existir sem fato que o justifique: movimento que não informa é o
movimento decorativo que esta camada já proíbe. (documento 15 §§5, 6, princípio 2)

O retorno SHALL ser **suprimido por completo** quando o aparelho declara preferir menos movimento, e
o fato que ele anuncia SHALL continuar legível sem ele — em texto, numeral ou forma. NEVER SHALL
haver conquista que só o movimento comunique. (documento 15 §5)

#### Scenario: A carta domina a tela da Arena

- **WHEN** uma tela da Arena apresenta personagem
- **THEN** a carta é o elemento maior da tela, e a tela pede uma decisão só

#### Scenario: A imagem de fundo não come o contraste

- **WHEN** uma tela da Arena apresenta imagem de comunidade ao fundo
- **THEN** o texto, os componentes, as bordas que informam e o estado de foco sobre ela continuam
  cumprindo os pisos de contraste medidos

#### Scenario: A imagem de fundo não carrega informação

- **WHEN** a imagem de fundo não é carregada, por rede ou por preferência do aparelho
- **THEN** nada do que a tela comunica se perde

#### Scenario: A conquista devolve retorno, e o fato fica legível sem ele

- **WHEN** uma conquista é certificada numa aplicação da Arena
- **THEN** o retorno acontece em `300` ms, e a conquista também aparece em texto, numeral ou forma

#### Scenario: Menos movimento suprime o retorno sem esconder o fato

- **WHEN** o aparelho declara preferir menos movimento e uma conquista é certificada
- **THEN** nenhum movimento acontece, e a conquista continua anunciada

#### Scenario: Não há retorno sem fato

- **WHEN** uma tela da Arena é apresentada sem progresso nem conquista nova
- **THEN** nenhum movimento acontece
