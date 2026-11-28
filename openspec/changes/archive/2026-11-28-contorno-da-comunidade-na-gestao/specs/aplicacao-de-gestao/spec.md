## ADDED Requirements

### Requirement: O Admin cadastra e substitui o contorno da comunidade pela App 03

A lista de Comunidades Virtuais da App 03 SHALL mostrar, em cada comunidade, se ela **tem
contorno** — com o elemento de origem no OSM, a data da cópia e o crédito e a licença que o
núcleo devolve — ou que **ainda não tem**, apresentado como informação e NEVER como erro.
(`RF-02-122`, `RN-08-31`)

Só ao **Admin** a App 03 SHALL oferecer, em cada comunidade, a ação de **cadastrar** o contorno,
ou de **substituí-lo** quando já houver um. A ação SHALL abrir um formulário com o **GeoJSON**
copiado do OSM e o **elemento de origem**, e gravar pela rota do núcleo que cadastra ou substitui
o contorno. Ao adulto que não é Admin a ação NEVER SHALL ser oferecida. (`RF-02-122`,
`RF-08-33`, PRD-02 §4)

Campo vazio e texto que não é JSON SHALL ser apontados no campo, sem chamar o núcleo. A validade
da geometria e do elemento de origem SHALL ser a do núcleo: a recusa dele SHALL aparecer no campo
que ele indicar, e a recusa por papel, num aviso do formulário. Gravado o contorno, a lista SHALL
mostrar o novo, com a origem e a data da nova cópia. (`RF-02-122`, `RF-08-33`)

#### Scenario: Comunidade sem contorno aparece sem ele, sem erro

- **WHEN** o adulto abre a lista e uma comunidade ainda não tem contorno
- **THEN** a comunidade informa que ainda não tem contorno, sem aviso de erro

#### Scenario: Comunidade com contorno mostra origem, data e crédito

- **WHEN** o adulto abre a lista e uma comunidade tem contorno copiado de `relation/12582832`
- **THEN** a comunidade mostra a origem `relation/12582832`, a data da cópia e o crédito
  "© colaboradores do OpenStreetMap" com a licença ODbL

#### Scenario: Admin cadastra o contorno copiado do OSM

- **WHEN** um Admin abre o cadastro do contorno de uma comunidade sem contorno, cola o polígono
  GeoJSON, informa `relation/12582832` e grava
- **THEN** a App 03 envia a geometria e a origem ao núcleo, e a lista passa a mostrar o contorno
  com aquela origem

#### Scenario: Admin substitui o contorno existente

- **WHEN** um Admin abre a ação de uma comunidade que já tem contorno
- **THEN** a ação se apresenta como substituição, e gravar troca o contorno mostrado pelo novo

#### Scenario: Texto que não é JSON é apontado sem chamar o núcleo

- **WHEN** o Admin grava o contorno com um texto que não é JSON, ou com um dos campos vazio
- **THEN** o campo é apontado com a mensagem, e o núcleo não é chamado

#### Scenario: Recusa do núcleo aparece no campo indicado

- **WHEN** o núcleo recusa o contorno com 422 no campo `geometria` ou `origem_osm`
- **THEN** a mensagem do núcleo aparece naquele campo, e a lista segue com o contorno anterior

#### Scenario: Quem não é Admin não vê a ação

- **WHEN** um Mestre abre a lista de Comunidades Virtuais
- **THEN** vê a situação do contorno de cada comunidade, sem a ação de cadastrar ou substituir
