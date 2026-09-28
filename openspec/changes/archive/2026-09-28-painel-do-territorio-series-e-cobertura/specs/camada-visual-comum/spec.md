# Spec Delta

## ADDED Requirements

### Requirement: A carta tem a variante Comunidade Virtual, com a representação visual

A camada comum SHALL entregar a variante **Comunidade Virtual** da carta, com o que o documento
11 §8.2 atribui a ela: **nome**, **território**, **representação visual**, **séries ativas** e
**número de Guerreiros e Guerreiras vinculados**. A variante NEVER SHALL exibir granularidade
que permita inferir endereço de criança — nenhum local abaixo do bairro, nenhum coletor.

A variante SHALL seguir a regra já vigente da carta pela metade: leitura que não devolve o que a
tabela do documento 11 §8.2 exige daquela variante SHALL ser apresentada em outra forma, não em
carta incompleta. (documento 11 §8.2, `RF-03-02`, `RF-03-16`, `RN-03-09`, `RN-03-10`,
invariantes 7 e 12 do documento 99 §6)

#### Scenario: A carta da comunidade traz os cinco campos da variante

- **WHEN** a carta de uma Comunidade Virtual é apresentada
- **THEN** ela traz nome, território, representação visual, séries ativas e o número de
  Guerreiros e Guerreiras vinculados

#### Scenario: A carta da comunidade não desce abaixo do bairro nem identifica coletor

- **WHEN** a carta de uma Comunidade Virtual é apresentada
- **THEN** nela não aparece local de nível rua ou abaixo, nick, avatar ou código de coletor

#### Scenario: Comunidade sem os indicadores não vira carta incompleta

- **WHEN** a leitura da comunidade devolve nome e território, e as séries ativas saem nulas
- **THEN** a tela apresenta a comunidade em outra forma, e nenhuma carta incompleta é
  apresentada

### Requirement: A representação visual da comunidade é derivada de dado real e cresce com ele

A camada comum SHALL desenhar a representação visual da Comunidade Virtual a partir do **dado
real**, na progressão do documento 11 §8.3: comunidade sem registro algum SHALL sair como
**território vazio**, com nome e contorno; cada **tipo de coleta ativo** SHALL ganhar presença
na representação; e o desenho SHALL **crescer e ganhar detalhe** conforme os registros válidos
acumulam e mais bairros aparecem no recorte publicado.

A representação NEVER SHALL ser decoração: nenhum elemento visual SHALL aparecer sem um fato
que o sustente, e o **recorte inativo** SHALL permanecer desenhado, sinalizado como inativo, em
vez de desaparecer. A forma visual SHALL ser a mesma para todo tipo de coleta — o catálogo de
tipos não declara forma própria, e a camada comum NEVER SHALL inventar uma. (documento 11 §8.3,
documento 15 §5, `RF-03-19`, `RF-03-20`, `RF-03-21`, decisão do fundador de 2026-09-28)

#### Scenario: Comunidade recém-criada aparece como território vazio

- **WHEN** uma comunidade criada por Admin ainda não tem registro algum
- **THEN** a representação traz o nome e o contorno, sem preenchimento

#### Scenario: O desenho cresce com os registros acumulados

- **WHEN** a mesma comunidade passa a ter mais registros válidos e mais bairros no recorte
  publicado
- **THEN** a representação cresce e ganha detalhe na medida desse acúmulo

#### Scenario: O recorte inativo continua desenhado

- **WHEN** um recorte da comunidade está sinalizado como inativo
- **THEN** o elemento visual dele permanece, marcado como inativo, em vez de sumir

#### Scenario: Nenhum elemento visual aparece sem fato que o sustente

- **WHEN** um tipo de coleta não tem série aberta na comunidade
- **THEN** nenhuma presença dele aparece na representação
