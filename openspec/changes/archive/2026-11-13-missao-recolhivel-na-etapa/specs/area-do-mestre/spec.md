## ADDED Requirements

### Requirement: A missão inteira se recolhe quando a etapa tem mais de uma

Quando a etapa aberta tem **mais de uma missão**, a App 09 SHALL apresentar cada missão
como **bloco recolhível** que **nasce fechado**, com posição, título e o resumo do estado da
missão na linha fechada; aberto, o bloco SHALL trazer a missão inteira, como hoje. Etapa com
**uma só missão** SHALL apresentá-la aberta, sem o bloco. (`RF-09-142`, `RF-09-03`)

#### Scenario: Etapa com várias missões nasce com todas recolhidas

- **WHEN** o Mestre autor abre uma etapa com duas missões
- **THEN** a aplicação apresenta as duas recolhidas, na ordem da posição, cada uma com posição,
  título e o resumo do estado, e nenhum ato nem bloco interno de nenhuma delas fica alcançável

#### Scenario: O Mestre mostra e oculta uma missão

- **WHEN** o Mestre autor aciona "Mostrar" na segunda missão da etapa
- **THEN** a aplicação apresenta a segunda missão inteira, a primeira segue recolhida, e o
  controle da segunda passa a dizer "Ocultar"

#### Scenario: Etapa com uma só missão fica aberta

- **WHEN** o Mestre autor abre uma etapa com uma só missão
- **THEN** a aplicação apresenta a missão inteira, sem controle de mostrar e ocultar

#### Scenario: Sondagem recolhida se identifica pela linha

- **WHEN** o Mestre autor abre a etapa de abertura com a sondagem e outra missão
- **THEN** a linha recolhida da sondagem a declara como sondagem
