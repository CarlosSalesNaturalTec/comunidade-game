# local-do-territorio Specification

## Purpose

Os locais da Comunidade Virtual, organizados na hierarquia de seis níveis que o território
declara, e cadastrados por Admin. É a lista entre a qual o Guerreiro(a) escolhe onde mede,
quando a série de coleta chegar.

## Requirements

### Requirement: Os locais formam a hierarquia de seis níveis da comunidade

O núcleo SHALL manter o local com **comunidade**, **nível**, **rótulo** e **local pai**. O
nível SHALL ser um entre **comunidade**, **bairro**, **rua**, **condomínio**, **bloco** e
**quadra**, nessa ordem de contenção. O local pai SHALL ser do **nível imediatamente acima** e
SHALL pertencer à **mesma comunidade** do local que se cadastra; o local de nível
`comunidade` SHALL ser o único sem pai. Local cujo pai é de outro nível, de outra comunidade
ou inexistente SHALL ser recusado com **422**. (`RF-08-04`, PRD-08 §8)

#### Scenario: Local se prende ao pai do nível imediatamente acima

- **WHEN** um Admin cadastra um local de nível `rua` apontando um local de nível `bairro` da
  mesma comunidade como pai
- **THEN** o núcleo grava o local na hierarquia daquela comunidade

#### Scenario: Pai de nível que não é o imediatamente acima é recusado

- **WHEN** um Admin cadastra um local de nível `quadra` apontando um local de nível `rua`
  como pai
- **THEN** o núcleo recusa com **422**, porque o nível imediatamente acima de `quadra` é
  `bloco`

#### Scenario: Pai de outra comunidade é recusado

- **WHEN** um Admin cadastra um local apontando como pai um local de outra comunidade
- **THEN** o núcleo recusa com **422**, e nenhum local é criado

#### Scenario: Só o nível `comunidade` existe sem pai

- **WHEN** um Admin cadastra um local de nível `bairro` sem local pai
- **THEN** o núcleo recusa com **422**, porque apenas o nível `comunidade` dispensa pai

### Requirement: Admin cadastra o local, e o local não nasce de outra origem nesta entrega

O núcleo SHALL permitir que **apenas um Admin** cadastre local na hierarquia da comunidade.
Persona de qualquer outro papel que tente cadastrar local SHALL receber **403**. Nesta
entrega o cadastro por Admin SHALL ser a **única origem de local**: a solicitação do
Guerreiro(a) e a avaliação pelo Mestre da trilha ou por Admin são `RF-08-22` a `RF-08-24`, de
fatia posterior, porque dependem do desafio de origem que as vincula à trilha. (`RF-08-04`,
`RN-08-18`, PRD-08 §§5.3, 8)

#### Scenario: Persona que não é Admin não cadastra local

- **WHEN** um Mestre, um Guerreiro(a), um responsável ou um Apoiador tenta cadastrar local
- **THEN** o núcleo recusa com **403**, e nenhum local é criado

#### Scenario: A comunidade nasce sem local e ganha os que o Admin cadastra

- **WHEN** um Admin cria a comunidade e depois cadastra os locais do território
- **THEN** a consulta à comunidade devolve, antes do cadastro, nenhum local, e depois dele,
  os locais cadastrados na hierarquia

### Requirement: A consulta de local aplica o filtro por comunidade

O núcleo SHALL aceitar e aplicar o **filtro por comunidade** na consulta de locais, como toda
consulta de dado de comunidade, e SHALL paginar a listagem. A consulta NEVER SHALL devolver
local de comunidade diferente da filtrada. (`RF-01-18`, `RF-01-28`, 03 §1)

#### Scenario: A listagem devolve só os locais da comunidade filtrada

- **WHEN** uma consulta de locais chega com o filtro de uma comunidade
- **THEN** o núcleo devolve apenas os locais daquela comunidade, paginados
