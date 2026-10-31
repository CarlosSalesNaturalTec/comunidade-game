# Spec Delta

## ADDED Requirements

### Requirement: A camada comum entrega a lista de caminhos em cartão

A camada comum SHALL entregar um componente de **lista de caminhos** que apresenta cada caminho
como **cartão** com glifo e **rótulo em frase**, em duas disposições: **coluna**, com o glifo ao
lado do rótulo, e **grade**, com o glifo **acima** dele — duas colunas até o marco de largura e
quatro a partir dele. (`RF-05-08`, PRD-05 §10, documento 15 §§5, 11.1, decisão do fundador de
2026-10-31)

#### Scenario: A grade dobra no marco de largura

- **WHEN** a lista de caminhos é apresentada em grade num aparelho abaixo do marco de largura
- **THEN** os cartões aparecem em duas colunas, com o glifo acima do rótulo
- **AND** a partir do marco de largura os mesmos cartões aparecem em quatro colunas

#### Scenario: A coluna mantém o glifo ao lado do rótulo

- **WHEN** a lista de caminhos é apresentada em coluna
- **THEN** cada cartão traz o glifo ao lado do rótulo, e não acima dele

#### Scenario: O cartão alcança o alvo de toque

- **WHEN** um cartão de caminho é apresentado em qualquer das duas disposições
- **THEN** ele cumpre o alvo de toque e a separação do vizinho que a camada comum exige

#### Scenario: O glifo não substitui o rótulo

- **WHEN** um cartão de caminho é apresentado
- **THEN** o rótulo em frase continua sendo o nome acessível do cartão, e o glifo o acompanha
  sem tomar o lugar dele

### Requirement: A lista de caminhos marca o caminho corrente sem depender de cor

Havendo caminho corrente declarado, a lista SHALL anunciá-lo como o atual e distingui-lo por
outro sinal além da cor. Sem caminho corrente declarado, nenhum cartão SHALL ser anunciado como
atual. (`RF-05-08`, documento 15 §5)

#### Scenario: O caminho corrente é reconhecível sem cor

- **WHEN** a lista é apresentada com um caminho corrente declarado
- **THEN** o cartão daquele caminho é anunciado como o atual e se distingue por outro sinal além
  da cor

#### Scenario: Sem caminho corrente, nenhum cartão é o atual

- **WHEN** a lista é apresentada sem caminho corrente declarado
- **THEN** nenhum cartão é anunciado como atual

### Requirement: O glifo do caminho não invade o que a marca e as grandezas reservam

O glifo que acompanha um cartão de caminho SHALL ser desenhado no sistema de ícone do documento
15 §11.1 e NEVER SHALL ser uma das silhuetas de família de badge da §8.3, o escudo da marca, o
círculo da moeda nem a estrela da grandeza ponto da §9 — pela mesma razão que vale para o
símbolo que encabeça uma coluna da carta: ali ele afirmaria família, marca ou grandeza errada.
(documento 15 §§8.3, 9, 11.1, invariante 24)

#### Scenario: Nenhum glifo de caminho repete símbolo reservado

- **WHEN** um cartão de caminho é apresentado com glifo
- **THEN** o glifo não é silhueta de família de badge, escudo da marca, círculo da moeda nem
  estrela da grandeza ponto

#### Scenario: O glifo da carteira não traz a moeda

- **WHEN** o caminho da carteira é apresentado
- **THEN** o glifo dele não traz o círculo que a §9 reserva à moeda
