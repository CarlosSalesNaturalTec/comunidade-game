## MODIFIED Requirements

### Requirement: A cobertura de ODS sai em rota pública, agregada por comunidade e ciclo

O núcleo SHALL expor a cobertura de ODS em rota pública, **sempre agregada** por comunidade e
por ciclo. A cobertura NEVER SHALL ser exposta por Guerreiro(a) individual, nem permitir recorte
que chegue a um. O **ciclo** SHALL ser o rótulo declarado na implantação, e a resposta SHALL
carregá-lo explicitamente. (`RF-01-43`, `RF-01-42`, `RN-01-24`, invariante 20 do documento 99 §6)

A rota SHALL refletir as **duas fontes** da cobertura por comunidade — as trilhas com Resultado
registrado e os **desafios de coleta com série aberta** —, e SHALL alcançar a comunidade cuja
única atividade é a coleta. O contrato da rota NEVER SHALL mudar por causa da fonte nova:
segue agregada por comunidade e ciclo, e segue sem recorte por Guerreiro(a). (`RF-08-26`,
`RN-08-22`)

#### Scenario: Cobertura pública vem agregada por comunidade e ciclo

- **WHEN** uma consulta pública pede a cobertura de ODS
- **THEN** a resposta traz os objetivos distintos por comunidade, com o rótulo do ciclo

#### Scenario: A cobertura pública inclui o objetivo vindo da coleta

- **WHEN** uma comunidade tem série aberta sobre desafio de coleta etiquetado
- **THEN** a resposta pública daquela comunidade inclui o objetivo do desafio

#### Scenario: Comunidade só com coleta aparece na cobertura pública

- **WHEN** uma comunidade não tem Resultado registrado e tem série aberta sobre desafio
  etiquetado
- **THEN** ela aparece na resposta pública, com o objetivo do desafio

#### Scenario: Não há recorte de cobertura por Guerreiro(a)

- **WHEN** uma consulta pública tenta recortar a cobertura por um Guerreiro(a)
- **THEN** o núcleo não oferece esse recorte, e nenhuma resposta o produz
