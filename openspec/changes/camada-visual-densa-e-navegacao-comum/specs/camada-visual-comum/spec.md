## ADDED Requirements

### Requirement: O temperamento Operação ganha densidade a partir do marco de largura

A camada comum SHALL entregar o temperamento Operação com o **celular em pé como piso** — o
caso que dimensiona a interface — e SHALL aumentar a densidade **a partir do marco de largura
de `768` px** declarado no documento 15 §4: mais colunas visíveis na tabela, diálogo e blocos
lado a lado. A camada comum SHALL declarar em token os **marcos de largura** e a **grade de
colunas** do documento 15 §4. NEVER SHALL exigir largura maior que a do celular para que uma
área seja operável, e NEVER SHALL introduzir marco de largura que o documento 15 §4 não
declare. (PRD-02 §10, documento 15 §§4, 6, decisão do fundador de 2026-09-06)

#### Scenario: A área é inteira operável no celular em pé

- **WHEN** uma área do temperamento Operação é aberta em largura abaixo do primeiro marco
- **THEN** toda ação e todo dado essencial dela continuam alcançáveis, sem rolagem lateral da
  página

#### Scenario: A partir do marco, aparece o que estava recolhido

- **WHEN** a mesma área é aberta em largura igual ou maior que o marco de `768` px
- **THEN** as colunas e os blocos que o celular recolhia passam a ser apresentados

#### Scenario: Nenhum marco fora do documento

- **WHEN** a camada comum declara os marcos de largura
- **THEN** os valores declarados são os do documento 15 §4, e nenhum outro

### Requirement: A camada comum entrega a tabela do temperamento Operação

A camada comum SHALL entregar um componente de **tabela** com marcação semântica de tabela,
célula de cabeçalho com escopo declarado e legenda opcional, e SHALL confinar a rolagem
horizontal **ao próprio componente**. NEVER SHALL fazer a página rolar na horizontal por causa
de uma tabela larga. Cada aplicação SHALL usar esse componente em lugar de marcação de tabela
própria. (PRD-02 §10, documento 15 §6)

#### Scenario: Leitura por tecnologia assistiva

- **WHEN** a tabela é percorrida por leitor de tela
- **THEN** cada célula é anunciada com o cabeçalho da coluna a que pertence

#### Scenario: Tabela mais larga que a tela

- **WHEN** a tabela tem mais colunas do que cabem na largura disponível
- **THEN** a rolagem horizontal acontece dentro da tabela, e a página não rola de lado

### Requirement: A camada comum entrega o diálogo de leitura e de formulário

A camada comum SHALL entregar um componente de **diálogo** que prende o foco enquanto está
aberto, fecha pela tecla de escape, devolve o foco ao elemento que o abriu e apresenta rótulo
acessível. O fechamento SHALL ter rótulo textual visível ou acessível — ícone nunca sozinho.
(PRD-02 §10, documento 15 §5)

#### Scenario: O foco não escapa do diálogo aberto

- **WHEN** a pessoa percorre a tela pelo teclado com o diálogo aberto
- **THEN** o foco permanece dentro do diálogo

#### Scenario: Fechar devolve o foco

- **WHEN** o diálogo é fechado, pela tecla de escape ou pelo botão de fechar
- **THEN** o foco volta ao elemento que o abriu

### Requirement: A navegação de áreas apresenta a saída da sessão uma única vez

A camada comum SHALL entregar um componente de **navegação de áreas** que apresenta as áreas da
aplicação, marca a corrente de modo perceptível sem depender de cor e apresenta a **saída da
sessão uma única vez**, na própria navegação. Aplicação com navegação de áreas NEVER SHALL
apresentar a saída da sessão dentro das telas de área. (PRD-02 §10, documento 15 §§5, 6)

#### Scenario: A saída existe uma vez

- **WHEN** a pessoa percorre a aplicação e troca de área
- **THEN** encontra exatamente um caminho de saída da sessão, sempre no mesmo lugar da navegação

#### Scenario: A área corrente é reconhecível sem cor

- **WHEN** uma área está aberta
- **THEN** o item correspondente da navegação é anunciado como o atual e se distingue por outro
  sinal além da cor
