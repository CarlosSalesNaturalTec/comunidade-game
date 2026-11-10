## ADDED Requirements

### Requirement: O Mestre declara os materiais da missão no formulário dela

O formulário da missão da App 09 SHALL oferecer ao **Mestre autor**, na **criação** e na
**correção**, o campo **Materiais necessários para a aula**: uma lista de nomes em que ele
**acrescenta** um item por vez e **remove** qualquer um. O campo SHALL ser opcional e SHALL
trazer exemplos ("cola, jumpers, papel") como dica. Na correção, o formulário SHALL abrir com
os materiais gravados. Item em branco NEVER SHALL ser acrescentado.

A linha da missão na trilha SHALL mostrar os materiais declarados; missão sem materiais NEVER
SHALL exibir rótulo vazio. (`RF-09-140`, `RN-09-61`)

#### Scenario: O Mestre declara materiais ao criar a missão

- **WHEN** o Mestre autor acrescenta "cola" e "jumpers" e salva a missão nova
- **THEN** a aplicação manda `materiais` com os dois nomes, e a linha da missão os mostra

#### Scenario: A correção abre com os materiais gravados

- **WHEN** o Mestre autor abre a correção de uma missão que declara "papel"
- **THEN** o campo dos materiais traz "papel", e removê-lo e salvar manda a lista vazia

#### Scenario: Item em branco não entra na lista

- **WHEN** o Mestre autor aciona acrescentar com o campo em branco
- **THEN** nenhum item é acrescentado

#### Scenario: Missão sem materiais não mostra rótulo

- **WHEN** a trilha tem missão sem materiais
- **THEN** a linha dessa missão não exibe o rótulo dos materiais
