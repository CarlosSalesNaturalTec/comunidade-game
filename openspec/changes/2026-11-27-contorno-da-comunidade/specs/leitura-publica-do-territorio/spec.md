## ADDED Requirements

### Requirement: A leitura pública da comunidade devolve o contorno com o crédito do OSM

A lista pública de comunidades e a leitura pública de uma comunidade SHALL devolver, em cada
comunidade, o **contorno** cadastrado, com o **elemento de origem** no OSM, a **data da
cópia**, o crédito **"© colaboradores do OpenStreetMap"** e a licença **ODbL**. A comunidade
**sem contorno** cadastrado SHALL sair **sem ele**, e segue na lista. O contorno SHALL sair
também abaixo do piso de coletores: ele delimita a comunidade e não é indicador. (`RF-08-34`,
`RN-08-31`, `RN-08-28`, PRD-08 §9, documento 03 §8)

#### Scenario: A comunidade com contorno sai com ele e com o crédito

- **WHEN** uma consulta pública pede a lista de comunidades e uma delas tem contorno
  cadastrado
- **THEN** o núcleo devolve, naquela comunidade, o contorno, o elemento de origem, a data da
  cópia, o crédito do OSM e a licença ODbL

#### Scenario: A comunidade sem contorno sai sem ele

- **WHEN** uma consulta pública pede uma comunidade que não tem contorno cadastrado
- **THEN** o núcleo a devolve com o contorno vazio, e nada mais muda na resposta

#### Scenario: O contorno não carrega dado de coleta

- **WHEN** uma consulta pública pede uma comunidade com contorno e com séries abertas
- **THEN** o contorno devolvido traz só a geometria, a origem, a data, o crédito e a licença,
  sem local, série, registro ou coletor

### Requirement: A exportação do território não leva o contorno

A exportação da série da comunidade e o dicionário de dados dela NEVER SHALL incluir o
contorno: o conjunto exportado segue sob **CC BY-SA**, e o contorno, derivado do OSM, segue sob
**ODbL**. (`RN-08-31`, documento 03 §12.3)

#### Scenario: A exportação de comunidade com contorno não o inclui

- **WHEN** uma consulta pública exporta a série de uma comunidade que tem contorno cadastrado
- **THEN** o CSV e o dicionário de dados não trazem geometria nem campo de contorno, e a
  licença declarada segue CC BY-SA
