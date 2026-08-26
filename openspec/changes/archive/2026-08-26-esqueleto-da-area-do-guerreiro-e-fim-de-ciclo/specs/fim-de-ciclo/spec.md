## Purpose

O ato de Admin que encerra o ciclo corrente da plataforma: o seu isolamento — encerra e nada
mais, porque o ciclo seguinte é declaração à parte na implantação —, os dois efeitos que ele
dispara e a proibição de congelar indicador.

## ADDED Requirements

### Requirement: O Admin encerra o ciclo corrente num ato isolado

O núcleo SHALL oferecer ao **Admin** o ato de encerrar o ciclo corrente. O ato NEVER SHALL
declarar o ciclo seguinte: o rótulo do próximo ciclo é **declarado na implantação**, e o ciclo
NEVER SHALL ser entidade do modelo. Nenhuma outra persona SHALL executá-lo. (`RF-02-99`,
documentos 02 §1 e 09)

#### Scenario: O Admin encerra o ciclo

- **WHEN** um Admin executa o ato de encerramento do ciclo corrente
- **THEN** o núcleo dispara os dois efeitos do encerramento e responde com o resultado deles

#### Scenario: O ato não declara o ciclo seguinte

- **WHEN** o encerramento do ciclo é executado
- **THEN** nenhum ciclo novo é criado, e o rótulo do ciclo corrente segue sendo o declarado na
  implantação

#### Scenario: Quem não é Admin não encerra

- **WHEN** um Mestre, um Apoiador, um responsável ou um Guerreiro(a) tenta encerrar o ciclo
- **THEN** o núcleo recusa o ato

#### Scenario: Encerrar de novo não tem o que fazer

- **WHEN** o encerramento é executado uma segunda vez, sem nenhuma ocorrência de conduta nova
  desde o primeiro
- **THEN** o ato é aceito e nada é alterado, porque não há motivo guardado a expurgar

### Requirement: O encerramento do ciclo não congela indicador

O encerramento NEVER SHALL congelar, copiar ou fotografar indicador. Os quatro indicadores da
lista pública de comunidades SHALL seguir apurados **no instante da consulta**, antes e depois
do ato, e nada do que já está publicado SHALL mudar por causa dele. (`RN-02-30`, documento 02
§1)

#### Scenario: Os indicadores públicos seguem apurados na consulta

- **WHEN** a lista pública de comunidades é consultada depois do encerramento do ciclo
- **THEN** os quatro indicadores são apurados no instante da consulta, como eram antes dele

#### Scenario: O encerramento não grava indicador

- **WHEN** o encerramento do ciclo é executado
- **THEN** nenhum valor de indicador é gravado, e nenhuma leitura pública passa a servir valor
  congelado
