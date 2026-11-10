## ADDED Requirements

### Requirement: A camada comum entrega a montagem do avatar por camada

A camada comum SHALL entregar a **montagem do avatar**: o avatar desenhado e, para cada uma das
nove camadas do documento 15 §7.1, na ordem delas, uma escolha rotulada pelo nome da camada
com os traços do catálogo fechado pelo **nome dizível**. A montagem SHALL partir do avatar que
recebe — o vigente de quem altera, ou o de partida de quem cadastra — e SHALL redesenhar o
avatar a cada traço escolhido. (`RF-04-07`, `RF-05-51`, documento 15 §7)

A montagem NEVER SHALL oferecer traço fora do catálogo nem campo de texto livre, e a composição
SHALL acontecer no próprio aparelho: escolher um traço NEVER SHALL gerar requisição. Gravar é
ato de quem consome a montagem, não dela. (documento 15 §7, `RF-05-51`)

As aplicações que montam avatar — a App 01 no cadastro e a App 05 na alteração — SHALL
consumir esta mesma montagem, e NEVER SHALL manter cópia própria dela. (`RF-04-07`, `RF-05-51`)

#### Scenario: A montagem oferece as nove camadas, na ordem

- **WHEN** a montagem é apresentada
- **THEN** ela mostra o avatar e uma escolha por camada, nas nove camadas e na ordem do
  documento 15 §7.1, cada traço pelo nome dizível

#### Scenario: A montagem parte do avatar recebido

- **WHEN** a montagem recebe um avatar já composto
- **THEN** cada escolha abre no traço daquele avatar, e o desenho é o dele

#### Scenario: Escolher um traço redesenha sem rede

- **WHEN** um traço de uma camada é escolhido
- **THEN** o avatar desenhado passa a ter aquele traço, e nenhuma requisição sai do aparelho
