# camada-visual-comum Specification

## Purpose

O que as oito aplicações e o jogo compartilham para cumprir o piso do documento 15 sem que cada
uma o reimplemente: as duas famílias tipográficas servidas pelo próprio domínio, as camadas de
token e o contrato de acessibilidade dos componentes comuns — alvo de toque, foco visível, erro
anunciado no próprio campo, estado nunca comunicado só por cor e largura de leitura. Inclui
também a densidade progressiva do temperamento Operação a partir do marco de largura do
documento 15 §4, e os componentes de tabela, diálogo e navegação de áreas com saída única.

## Requirements

### Requirement: As duas famílias tipográficas são servidas pelo próprio domínio

A camada comum SHALL servir Atkinson Hyperlegible Next no texto e Archivo no destaque, em
formato variável e nos subconjuntos latino e latino estendido, a partir do mesmo domínio que
serve a aplicação. NEVER SHALL buscar fonte em domínio de terceiro em tempo de execução.
(PRD-02 §10, documento 15 §4)

#### Scenario: Nenhuma fonte vem de fora

- **WHEN** uma aplicação é aberta e carrega os arquivos de que precisa
- **THEN** todo pedido de fonte vai para o próprio domínio da aplicação, e nenhum vai para
  domínio de terceiro

#### Scenario: O nome declarado no token é o que a fonte atende

- **WHEN** a aplicação aplica a família de texto ou a de destaque declarada nos tokens
- **THEN** o texto é desenhado pela família correspondente do documento 15, e não pela família
  de reserva do sistema

#### Scenario: Texto legível enquanto a fonte não chegou

- **WHEN** a fonte ainda está sendo transferida numa rede lenta
- **THEN** o texto é apresentado desde já na família de reserva, e nenhum trecho fica invisível
  à espera do arquivo

### Requirement: Todo elemento acionável cumpre o alvo de toque e mostra o foco

A camada comum SHALL entregar todo elemento acionável com ao menos 48 px de alvo de toque e ao
menos 8 px de separação de um alvo vizinho, e SHALL apresentar contorno de foco visível em todo
elemento que receba foco. (PRD-02 §10, documento 15 §§4, 5)

#### Scenario: Dois botões lado a lado

- **WHEN** dois elementos acionáveis são apresentados um ao lado do outro
- **THEN** cada um tem ao menos 48 px de alvo e há ao menos 8 px entre eles

#### Scenario: Percurso pelo teclado

- **WHEN** a pessoa alcança um elemento acionável pelo teclado
- **THEN** o elemento apresenta contorno de foco visível

### Requirement: O erro de um campo é anunciado no próprio campo

A camada comum SHALL associar a mensagem de erro ao campo que a originou, de modo que quem
alcança o campo — a qualquer momento, e não só quando o erro surge — receba a mensagem junto
com ele, e SHALL marcar o campo como inválido enquanto o erro durar. NEVER SHALL apresentar
erro de campo apenas como texto solto na tela. (PRD-02 §10, documento 15 §5)

#### Scenario: Campo com erro alcançado depois que o erro surgiu

- **WHEN** um campo está com erro e a pessoa o alcança pelo teclado ou por leitor de tela
- **THEN** a mensagem de erro é anunciada junto com o rótulo do campo, e o campo é anunciado
  como inválido

#### Scenario: Erro corrigido

- **WHEN** a pessoa corrige o valor e o erro deixa de valer
- **THEN** o campo deixa de ser anunciado como inválido e a mensagem deixa de acompanhá-lo

### Requirement: Nenhum estado se comunica apenas por cor

A camada comum SHALL acompanhar todo aviso e todo estado de um rótulo textual ou glifo que o
identifique sem depender da cor, e SHALL distinguir o aviso que interrompe o que a pessoa faz
do aviso que apenas informa o andamento. (PRD-02 §10, documento 15 §5)

#### Scenario: Aviso lido sem enxergar a cor

- **WHEN** um aviso de erro, de atenção ou de sucesso é apresentado
- **THEN** o que ele comunica é reconhecível pelo texto ou pelo glifo, sem depender da cor

#### Scenario: A urgência do aviso chega a quem não vê a tela

- **WHEN** um aviso interrompe o que a pessoa faz e outro apenas informa o andamento
- **THEN** cada um é anunciado conforme a urgência dele, e não da mesma forma

### Requirement: O texto respeita a largura de leitura e o corpo mínimo

A camada comum SHALL limitar a linha de texto corrido a no máximo 64 caracteres e NEVER SHALL
apresentar texto de leitura abaixo de 1 rem. (PRD-02 §10, documento 15 §4)

#### Scenario: Texto corrido em tela larga

- **WHEN** uma tela de texto corrido é apresentada numa tela larga
- **THEN** a linha não passa de 64 caracteres, ainda que sobre espaço na tela

### Requirement: A camada não impõe movimento

A camada comum NEVER SHALL apresentar movimento decorativo, e SHALL suprimir toda transição
quando o aparelho declara preferir menos movimento. Nenhum conteúdo SHALL depender de
movimento para ser lido. (PRD-02 §10, documento 15 §§5, 6)

#### Scenario: Aparelho que pede menos movimento

- **WHEN** o aparelho declara preferir menos movimento
- **THEN** nenhuma transição acontece, e todo conteúdo continua alcançável

### Requirement: O jogo consome a camada sem depender do framework das aplicações

A camada comum SHALL oferecer os tokens e as fontes de forma consumível por aplicação que não
use o framework das oito Webs, para que o jogo use a mesma tipografia e a mesma paleta.
(documento 03 §1.2, documento 15 §12)

#### Scenario: Consumidor que não é uma das oito aplicações Web

- **WHEN** o jogo consome os tokens e as fontes da camada comum
- **THEN** ele os obtém sem precisar do framework das aplicações Web, e apresenta a mesma
  tipografia e a mesma paleta que elas

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
