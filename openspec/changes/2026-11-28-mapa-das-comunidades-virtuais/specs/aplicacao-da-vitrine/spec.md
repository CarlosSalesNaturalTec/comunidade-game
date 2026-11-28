## ADDED Requirements

### Requirement: A listagem de Comunidades Virtuais exibe o mapa com o contorno de cada uma

A seção Comunidades Virtuais da App 06 SHALL exibir um **mapa** com o **contorno** e o **nome** de
cada comunidade que tenha contorno cadastrado, e o contorno SHALL abrir a página daquela
comunidade. Comunidade sem contorno SHALL seguir na lista e NEVER SHALL ser apresentada no mapa
como falha; sem nenhum contorno cadastrado, o mapa NEVER SHALL ser desenhado vazio. O mapa
SHALL **complementar** a lista e a representação visual genérica, NEVER as substituir.
(`RF-03-89`, `RF-03-90`, `RN-03-46`)

#### Scenario: Comunidade com contorno aparece no mapa com o nome

- **WHEN** o visitante abre a seção e uma comunidade tem contorno
- **THEN** o mapa desenha aquele contorno com o nome da comunidade

#### Scenario: O contorno abre a página da comunidade

- **WHEN** o visitante toca o contorno de uma comunidade no mapa
- **THEN** a vitrine abre a página daquela comunidade, no endereço próprio dela

#### Scenario: Sem contorno cadastrado, não há mapa vazio

- **WHEN** nenhuma comunidade tem contorno
- **THEN** a seção mostra a lista como antes, sem mapa e sem aviso de erro

### Requirement: A página da comunidade exibe o mapa com o contorno dela em destaque

A página da comunidade SHALL exibir o mapa enquadrado no **contorno dela**, em destaque, junto da
representação visual genérica, que SHALL permanecer. Comunidade sem contorno SHALL ter a página
como antes, sem mapa. (`RF-03-91`, `RF-03-20`, `RN-03-46`)

#### Scenario: Página de comunidade com contorno mostra o mapa

- **WHEN** o visitante abre a página de uma comunidade com contorno
- **THEN** o mapa aparece enquadrado no contorno dela, e a representação visual genérica segue na
  página

#### Scenario: Comunidade recém-criada aparece com nome e contorno

- **WHEN** a comunidade tem contorno e nenhum registro
- **THEN** a página mostra o território vazio e o mapa com o contorno, sem erro

### Requirement: O fundo do mapa é servido pela plataforma, com crédito e licença do OSM

O fundo de ruas e quadras SHALL ser um recorte do OSM que cobre o **município de Salvador**,
servido pela **própria App 06**; o mapa NEVER SHALL fazer requisição a servidor de mapas de
terceiros — fundo, estilo, fonte ou ícone. O mapa SHALL exibir o crédito "© colaboradores do
OpenStreetMap" e a licença **ODbL**. O mapa SHALL desenhar só o contorno da comunidade e NEVER
SHALL mostrar ponto de coleta, local abaixo da comunidade ou coletor. (`RF-03-92`, `RN-03-44`,
`RN-03-45`)

#### Scenario: Crédito e licença acompanham o mapa

- **WHEN** qualquer mapa da vitrine é exibido
- **THEN** o crédito "© colaboradores do OpenStreetMap" e a licença ODbL aparecem junto dele

#### Scenario: Nenhum recurso do mapa vem de terceiro

- **WHEN** o mapa monta o fundo
- **THEN** o recorte, o estilo e os demais recursos do mapa são lidos da origem da própria App 06

#### Scenario: O mapa não desenha nada além do contorno

- **WHEN** o mapa é montado para uma comunidade com locais e registros
- **THEN** o que se sobrepõe ao fundo é só o contorno e o nome dela, sem local, ponto ou coletor
