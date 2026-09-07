## ADDED Requirements

### Requirement: A camada comum entrega o bloco recolhível das telas da Operação

A camada comum SHALL entregar um bloco recolhível para as telas do temperamento Operação que
reúnem muitos blocos de declaração. O bloco SHALL nascer **fechado** e SHALL apresentar, na
linha fechada, o **resumo do estado** que quem o monta declara — quantos itens ele guarda, ou
que não guarda nenhum —, para a existência de cada parte ficar visível sem o peso do conteúdo
de todas. O controle de abrir e fechar SHALL ser botão com rótulo textual e SHALL declarar se
o bloco está aberto ou fechado a quem navega por leitor de tela. O bloco NEVER SHALL animar a
abertura, e NEVER SHALL comunicar seu estado apenas por cor ou apenas por ícone.
(PRD-02 §10, documento 15 §§5, 6.1, decisão do fundador de 2026-09-07)

#### Scenario: Tela que reúne muitos blocos abre com todos fechados

- **WHEN** o operador abre uma tela da Operação montada com blocos recolhíveis
- **THEN** todos os blocos aparecem fechados, e cada linha fechada apresenta o resumo do
  estado do seu bloco

#### Scenario: Bloco sem conteúdo declara que está vazio

- **WHEN** um bloco recolhível não guarda item nenhum
- **THEN** a linha fechada diz que não há nenhum, e o bloco continua visível e alcançável

#### Scenario: Operador abre e fecha um bloco

- **WHEN** o operador aciona o controle de um bloco fechado
- **THEN** o conteúdo do bloco passa a ser apresentado sem animação de altura, o controle
  informa que o bloco está aberto, e acioná-lo de novo o fecha

#### Scenario: Quem navega por leitor de tela alcança o bloco

- **WHEN** um leitor de tela percorre a tela
- **THEN** o controle de cada bloco é anunciado com rótulo textual e com o estado de aberto
  ou fechado, sem depender de cor nem de ícone

### Requirement: A escrita que grava sozinha declara que gravou

A camada comum SHALL entregar uma marca de gravação para as telas em que cada bloco tem
escrita própria e não há botão de salvar que feche a tela inteira. A marca SHALL ser texto
persistente no próprio bloco que gravou, SHALL informar o momento da gravação e SHALL
permanecer até a escrita seguinte daquele bloco. A marca NEVER SHALL desaparecer por decurso
de tempo, NEVER SHALL depender de cor para ser compreendida e NEVER SHALL animar. Bloco que
ainda não gravou nada NEVER SHALL apresentar marca.
(PRD-02 §10, PRD-09 §10, documento 15 §§5, 6.2, decisão do fundador de 2026-09-07)

#### Scenario: Bloco grava e declara a gravação

- **WHEN** o operador confirma a escrita de um bloco e ela é gravada
- **THEN** o bloco passa a apresentar a marca com o momento da gravação, em texto

#### Scenario: A marca não some sozinha

- **WHEN** o tempo passa depois de uma gravação, sem nova escrita naquele bloco
- **THEN** a marca continua apresentada, com o mesmo momento

#### Scenario: Nova escrita no mesmo bloco atualiza a marca

- **WHEN** o operador grava de novo no bloco que já tem marca
- **THEN** a marca passa a informar o momento da gravação mais recente

#### Scenario: Bloco que nunca gravou não tem marca

- **WHEN** o operador abre a tela e um bloco ainda não recebeu escrita nenhuma
- **THEN** aquele bloco não apresenta marca de gravação

#### Scenario: A escrita que falha não deixa marca

- **WHEN** a escrita de um bloco é recusada ou falha
- **THEN** o bloco não ganha marca de gravação, e a recusa aparece como o erro já aparece
