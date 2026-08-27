## ADDED Requirements

### Requirement: O Admin lê os lançamentos de um ponto de apoio

O núcleo SHALL devolver ao **Admin** a lista paginada dos **lançamentos** de um **ponto de
apoio**, com natureza, tipo de recurso, quantidade, moedas, data e, quando o lançamento é um
ajuste, o **lançamento original** e o **motivo**. O filtro de **ponto de apoio** SHALL ser
obrigatório: sem ele o núcleo SHALL recusar com **422**, em vez de misturar o livro-razão de
pontos de apoio diferentes. A listagem SHALL aceitar também os filtros de **período** e de
**tipo de recurso**, e SHALL seguir as convenções de paginação por cursor do PRD-01.

Quem não é Admin SHALL receber **403**. A leitura é o que dá ao ajuste do `RF-07-19` como
alcançar o lançamento a corrigir; ela NEVER SHALL oferecer caminho de edição ou de remoção.
(`RF-02-40`, `RF-07-19`, `RF-01-18`, `RF-01-28`, `RN-02-12`)

#### Scenario: A listagem devolve os lançamentos do ponto de apoio

- **WHEN** um Admin lista os lançamentos informando o ponto de apoio
- **THEN** o núcleo devolve os lançamentos daquele ponto de apoio, com natureza, tipo de
  recurso, quantidade, moedas e data, paginados por cursor

#### Scenario: O ajuste vem com o original e o motivo

- **WHEN** a listagem inclui um lançamento de ajuste
- **THEN** ele traz o lançamento original que referencia e o motivo registrado

#### Scenario: Sem ponto de apoio a listagem é recusada

- **WHEN** chega a listagem de lançamentos sem o filtro de ponto de apoio
- **THEN** o núcleo responde 422 e nenhum lançamento é devolvido

#### Scenario: A listagem filtra por período e por tipo de recurso

- **WHEN** um Admin lista os lançamentos de um ponto de apoio com período e tipo de recurso
- **THEN** o núcleo devolve apenas os lançamentos daquele tipo dentro daquele período

#### Scenario: Quem não é Admin é recusado

- **WHEN** um Mestre em sessão tenta listar os lançamentos de um ponto de apoio
- **THEN** o núcleo responde 403 e nenhum lançamento é devolvido
