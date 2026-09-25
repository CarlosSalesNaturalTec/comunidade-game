# camada-visual-comum Specification

## Purpose

O que as oito aplicações e o jogo compartilham para cumprir o piso do documento 15 sem que cada
uma o reimplemente: as duas famílias tipográficas servidas pelo próprio domínio, as camadas de
token e o contrato de acessibilidade dos componentes comuns — alvo de toque, foco visível, erro
anunciado no próprio campo, estado nunca comunicado só por cor e largura de leitura. Inclui
também a camada de tema dos dois temperamentos — com a densidade progressiva da Operação a
partir do marco de largura do documento 15 §4 —, o sistema de ícone do documento 15 §11.1 e os
componentes de tabela, diálogo e navegação de áreas com saída única. Inclui ainda o **avatar
paramétrico** do Guerreiro(a) do documento 15 §7 — catálogo fechado das nove camadas,
renderizador SVG, objeto versionado e avatar padrão do projeto.

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

### Requirement: O campo declarado como inicial recebe o foco quando a tela abre

A camada comum SHALL permitir que quem monta a tela declare **um** campo como inicial, e SHALL
dar o foco a ele quando a tela abre. A declaração SHALL ser **opcional**: o componente de campo
NEVER SHALL tomar o foco por conta própria, porque foco automático em tela que apresenta
conteúdo acima do campo faz quem navega por leitor de tela começar no meio, saltando o que veio
antes. (PRD-02 §10, documento 15 §5, decisão do fundador de 2026-09-25)

Receber o foco inicial NEVER SHALL dispensar o **contorno de foco visível** nem alterar o
rótulo, a mensagem de erro ou o estado de inválido do campo: o foco inicial é onde o percurso
começa, não uma forma diferente de campo. (documento 15 §5)

#### Scenario: O campo declarado abre focado

- **WHEN** uma tela é apresentada com um campo declarado como inicial
- **THEN** aquele campo está com o foco, e quem opera digita sem antes alcançá-lo

#### Scenario: Campo sem declaração não toma o foco

- **WHEN** uma tela é apresentada sem declarar campo inicial algum
- **THEN** nenhum campo toma o foco, e o percurso começa no início da tela

#### Scenario: O foco inicial continua visível

- **WHEN** o campo declarado como inicial recebe o foco
- **THEN** o contorno de foco é apresentado nele, como em qualquer campo alcançado pelo teclado

#### Scenario: O foco inicial não muda o anúncio do campo

- **WHEN** o campo declarado como inicial está com erro
- **THEN** o rótulo, a mensagem de erro e o estado de inválido são anunciados como em qualquer
  outro campo

### Requirement: A camada declara os dois temperamentos, e cada aplicação declara o seu

A camada comum SHALL declarar a camada de tema dos **dois** temperamentos do documento 15 §6 —
Operação e Arena —, e cada aplicação SHALL declarar na raiz do documento o temperamento que o
documento 15 §6 lhe atribui: **Operação** nas Apps 03, 07, 08 e 09; **Arena** nas Apps 01, 04, 05
e 06. NEVER SHALL uma aplicação declarar o temperamento da outra família, e NEVER SHALL o
temperamento valer por região de uma tela: ele é da aplicação inteira. (documento 15 §6,
invariante 24)

A camada de tema da Arena SHALL declarar o que o documento 15 §6 fixa em número para ela: **raio
de carta de `12` px** e **duração de transição de `300` ms**. A supressão de movimento por
preferência do aparelho SHALL continuar valendo sobre os dois temperamentos. (documento 15 §§5, 6)

A camada NEVER SHALL declarar, para a Arena, valor que o documento 15 não fixe. A densidade da
Arena é descrita como composição — poucos elementos, uma decisão por tela —, sem número, e o token
de densidade é lido apenas pelas telas densas da Operação. (documento 15 §6)

#### Scenario: Cada aplicação declara o temperamento do documento 15

- **WHEN** a App 01 ou a App 05 é aberta
- **THEN** o documento declara o temperamento Arena, e nenhuma das duas declara Operação

#### Scenario: A Arena tem camada de tema própria

- **WHEN** uma aplicação declara o temperamento Arena
- **THEN** o raio de carta vale `12` px e a duração de transição vale `300` ms, em vez dos valores
  da Operação

#### Scenario: As aplicações da Operação seguem como estão

- **WHEN** as Apps 03, 07, 08 e 09 são abertas
- **THEN** cada uma declara o temperamento Operação, e a densidade progressiva delas continua
  valendo a partir do marco de largura

#### Scenario: Menos movimento vence o temperamento

- **WHEN** o aparelho declara preferir menos movimento numa aplicação da Arena
- **THEN** nenhuma transição acontece, como já vale na Operação

### Requirement: O ícone é SVG servido pelo próprio domínio e nunca aparece sozinho

A camada comum SHALL entregar o sistema de ícone do documento 15 §11.1: SVG servido pelo **próprio
domínio** da aplicação, desenhado em grade de `24` px, com traço de `2` px de ponta e junta
arredondadas, **sem preenchimento**, e cor herdada do texto que o ícone acompanha. NEVER SHALL
buscar ícone em domínio de terceiro, e NEVER SHALL guardar valor de cor no arquivo do glifo: trocar
o tema SHALL trocar o ícone junto. (documento 15 §§11.1, 12, princípio 6)

Todo ícone SHALL ser apresentado com **rótulo textual** visível ou acessível. NEVER SHALL um ícone
ser a única forma de identificar um elemento acionável, e NEVER SHALL substituir o rótulo que o
elemento já tem. (documento 15 §5)

#### Scenario: Nenhum ícone vem de fora

- **WHEN** uma aplicação apresenta um ícone
- **THEN** ele é servido pelo próprio domínio, e nenhum pedido vai para domínio de terceiro

#### Scenario: O ícone acompanha o tema

- **WHEN** o tema claro dá lugar ao escuro
- **THEN** o ícone muda de cor junto com o texto que acompanha, sem que arquivo algum declare cor

#### Scenario: O ícone não aparece sozinho

- **WHEN** um elemento acionável é apresentado com ícone
- **THEN** ele tem rótulo textual visível ou acessível, e quem navega por leitor de tela alcança o
  rótulo, não a descrição do desenho

### Requirement: A camada comum compõe o avatar paramétrico no próprio aparelho

A camada comum SHALL entregar o avatar do Guerreiro(a) como composição **paramétrica em camadas
SVG**, montada de **catálogo fechado**, nas nove camadas e na ordem do documento 15 §7.1 — fundo,
tom de pele, cabelo, cor do cabelo, rosto, olhos, boca, roupa e acessório. NEVER SHALL aceitar
traço fora do catálogo, e NEVER SHALL desenhar avatar a partir de texto livre. (documento 15 §7)

Cada traço do catálogo SHALL ter **nome dizível em português simples** — "cabelo black power", não
"modelo 7" —, porque no onboarding o avatar nasce de características ditas em voz alta por uma
criança de 6 anos. (documento 15 §7, `RF-04-06`)

A escala de **tons de pele** SHALL abrir pelo **mais retinto**, e as texturas de **cabelo crespo**
SHALL vir antes das lisas. É requisito de conteúdo do catálogo, não ordem de tabela: o documento 15
declara a representatividade como construção, e a ordem é onde ela se realiza. (documento 15 §7.1)

Nenhum item do catálogo SHALL carregar marca de gênero, e todo item SHALL ser oferecido a qualquer
pessoa. A **forma de tratamento** é campo próprio da persona e NEVER SHALL derivar do avatar nem
restringi-lo. (documento 15 §7)

A composição SHALL acontecer **no próprio aparelho, sem rede**, e o desenho NEVER SHALL depender de
requisição ao núcleo nem a domínio de terceiro. (documento 15 §7, princípio 6)

A camada comum SHALL ler e escrever o avatar como o **objeto pequeno e versionado** do documento 15
§7.2. **Traço desconhecido** SHALL cair no padrão da camada e NEVER SHALL quebrar a renderização —
é o que permite crescer o catálogo sem migrar avatar de ninguém, e o que faz o avatar gravado antes
deste contrato continuar renderizando. (documento 15 §7.2)

A camada comum SHALL entregar o **avatar padrão do projeto** — mesmo sistema, composição fixa e
neutra, em cores da marca — e SHALL usá-lo no lugar de **qualquer avatar que falte**, na mesma
moldura e sem nenhuma outra marca de diferença. (documento 15 §7.3)

#### Scenario: O avatar se compõe pelas nove camadas do catálogo

- **WHEN** um avatar é composto
- **THEN** ele se monta pelas nove camadas do documento 15 §7.1, na ordem delas, e cada escolha vem
  do catálogo fechado

#### Scenario: Cada traço tem nome dizível

- **WHEN** o catálogo é apresentado a quem escolhe
- **THEN** cada traço aparece com nome em português simples, e nenhum aparece como código ou número

#### Scenario: A escala de pele abre pelo mais retinto

- **WHEN** a camada de tom de pele é apresentada
- **THEN** a escala começa pelo tom mais retinto, e as texturas de cabelo crespo vêm antes das lisas

#### Scenario: Nenhum item é de um gênero

- **WHEN** qualquer camada do catálogo é apresentada
- **THEN** todos os itens dela são oferecidos, sem depender da forma de tratamento da persona

#### Scenario: Compor e desenhar não pedem rede

- **WHEN** um avatar é composto e desenhado
- **THEN** nenhuma requisição sai do aparelho por causa do avatar

#### Scenario: Traço desconhecido cai no padrão da camada

- **WHEN** um avatar guardado traz traço que o catálogo não conhece, ou não traz o objeto do
  documento 15 §7.2
- **THEN** a camada desconhecida cai no padrão dela, o avatar é desenhado, e nada quebra

#### Scenario: Avatar que falta usa o padrão do projeto

- **WHEN** uma persona não tem avatar algum
- **THEN** o avatar padrão do projeto é desenhado, na mesma moldura dos demais e sem marca de
  diferença

### Requirement: A camada comum entrega a carta do personagem

A camada comum SHALL entregar a **carta do personagem**, o átomo de interface comum às oito
aplicações, com os valores do documento 15 §8.1: superfície de carta, borda de 1 px, **raio que vem
do temperamento** da aplicação, avatar **quadrado recortado em círculo ocupando metade da largura**
e nick na família de destaque. (documento 15 §8.1)

A carta SHALL exibir **apenas** o que o documento 11 §8.2 atribui à variante dela, e NEVER SHALL
exibir o que aquela tabela lista como nunca exibido — para a variante Guerreiro(a): nem imagem real,
nem nome civil, nem rede social, nem qualquer canal de contato. (documento 11 §8.2, invariantes 9 e
10)

A camada comum NEVER SHALL oferecer carta **pela metade**: variante cuja leitura não devolve o que a
tabela do documento 11 §8.2 exige SHALL ser apresentada em outra forma, não em carta incompleta.
(documento 11 §8.2, decisão do fundador registrada no documento 09 §1)

Havendo **rotação**, ela SHALL respeitar a preferência por menos movimento e NEVER SHALL ser a única
via ao conteúdo do verso. (documento 15 §§5, 8.1)

#### Scenario: A carta se monta com os valores do documento 15

- **WHEN** uma carta é apresentada
- **THEN** ela traz o avatar em círculo ocupando metade da largura, o nick na família de destaque, e
  o raio que o temperamento da aplicação declara

#### Scenario: A carta do Guerreiro(a) não expõe o que é vedado

- **WHEN** a carta de um Guerreiro(a) é apresentada
- **THEN** nela aparecem avatar, nick, badges, poderes com níveis e criações originais, e não
  aparecem imagem real, nome civil, rede social nem canal de contato

#### Scenario: Sem o dado que a variante exige, não se usa carta

- **WHEN** a leitura disponível não devolve o que a tabela do documento 11 §8.2 exige daquela
  variante
- **THEN** a tela apresenta a informação em outra forma, e nenhuma carta incompleta é apresentada

### Requirement: O emblema de nível é contável e nunca global

A camada comum SHALL apresentar o nível de uma trilha ou poder como **número de marcas na moldura,
igual ao nível** — uma marca no nível 1, cinco no nível 5 —, para que uma criança de 6 anos possa
**contá-lo**, e SHALL ser legível **sem depender de cor**. No nível 5 a moldura SHALL fechar, que é
a marca de **Mestre Aprendiz**. (documento 15 §8.2)

O emblema SHALL ser sempre **de uma trilha ou de um poder**, e a moldura SHALL carregar o nome do
poder. NEVER SHALL existir emblema de nível global. (documento 15 §8.2, `RN-05-03`)

#### Scenario: O nível se conta na moldura

- **WHEN** um emblema de nível 3 é apresentado
- **THEN** a moldura traz três marcas, contáveis, e o nível é reconhecível sem depender de cor

#### Scenario: O nível 5 fecha a moldura

- **WHEN** um emblema de nível 5 é apresentado
- **THEN** a moldura traz cinco marcas e aparece fechada, marcando Mestre Aprendiz

#### Scenario: Não há emblema global

- **WHEN** um emblema de nível é apresentado
- **THEN** ele é de uma trilha ou de um poder, e a moldura carrega o nome do poder

### Requirement: Cada família de badge tem silhueta própria, legível sem cor

A camada comum SHALL entregar **uma silhueta por família de badge** do documento 15 §8.3 — escudo
para nível, estrela para conquista, coração para valores e causas, gota para território, folha com
canto dobrado para autoria e hexágono para protagonismo —, cada uma legível a **`24` px** e
reconhecível **sem depender de cor**. (documento 15 §8.3)

A silhueta SHALL dizer a **família**, nunca o poder: dois badges de nível são ambos escudo. O que os
separa SHALL ser o **glifo do poder**. (documento 15 §§8.3, 8.4)

#### Scenario: A família se reconhece pela forma

- **WHEN** badges de famílias diferentes são apresentados juntos
- **THEN** cada um traz a silhueta da família dele, distinguível a `24` px e sem depender de cor

#### Scenario: Dois badges da mesma família se distinguem pelo poder

- **WHEN** dois badges de nível de poderes diferentes são apresentados
- **THEN** ambos trazem escudo, e o glifo do poder dentro deles é o que os separa

### Requirement: O glifo de poder acompanha o nome do poder e tem genérico

A camada comum SHALL entregar o **glifo de poder** do documento 15 §8.4, desenhado no sistema de
ícone da §11.1, apresentado **dentro da silhueta do badge** e **na moldura de nível**, reconhecível
a `24` px em traço e sem depender de cor. O glifo SHALL acompanhar o **nome do poder** e NEVER SHALL
substituí-lo. (documento 15 §8.4)

A cobertura SHALL ser de **um glifo por poder do catálogo**, e poder sem glifo SHALL cair num
**genérico** que NEVER SHALL quebrar a tela — o catálogo de poderes é dado da gestão e cresce sem
passar por aqui. O poder NEVER SHALL ter cor própria: cor é da grandeza e do estado. (documento 15
§§8.4, 9)

#### Scenario: O glifo nunca aparece sem o nome do poder

- **WHEN** um glifo de poder é apresentado
- **THEN** o nome do poder aparece junto, e o glifo não o substitui

#### Scenario: Poder sem glifo cai no genérico

- **WHEN** o catálogo traz um poder para o qual não há glifo desenhado
- **THEN** o genérico é apresentado, com o nome do poder, e nenhuma tela quebra

#### Scenario: O poder não carrega cor

- **WHEN** glifos de poderes diferentes são apresentados
- **THEN** nenhum deles se distingue por cor própria

### Requirement: A Arena põe a ilustração em primeiro plano e devolve progresso e conquista

Nas aplicações do temperamento **Arena**, a camada comum SHALL apresentar a **ilustração em primeiro
plano**, com a **carta dominando a tela** e **uma decisão por tela** — a densidade baixa que o
documento 15 §6 atribui à Arena. NEVER SHALL reproduzir na Arena a densidade da Operação: tabela,
lote e painel são da outra família. (documento 15 §6, invariante 24)

A camada comum SHALL admitir **imagem de comunidade ao fundo** nas telas da Arena, atrás da cor
chapada. A imagem NEVER SHALL carregar significado sozinha, NEVER SHALL ser a única via a informação
alguma, e NEVER SHALL reduzir o contraste do texto e dos componentes que ficam sobre ela abaixo dos
pisos medidos — `4,5:1` em texto e `3:1` em componente, borda que informa e estado de foco.
(documento 15 §§3.3, 5, 6, princípio 3)

A camada comum SHALL apresentar, na Arena, **retorno de progresso e conquista**, com duração de
`300` ms e `ease-in-out`. O retorno SHALL acompanhar **fato real** — progresso alcançado, conquista
certificada — e NEVER SHALL existir sem fato que o justifique: movimento que não informa é o
movimento decorativo que esta camada já proíbe. (documento 15 §§5, 6, princípio 2)

O retorno SHALL ser **suprimido por completo** quando o aparelho declara preferir menos movimento, e
o fato que ele anuncia SHALL continuar legível sem ele — em texto, numeral ou forma. NEVER SHALL
haver conquista que só o movimento comunique. (documento 15 §5)

#### Scenario: A carta domina a tela da Arena

- **WHEN** uma tela da Arena apresenta personagem
- **THEN** a carta é o elemento maior da tela, e a tela pede uma decisão só

#### Scenario: A imagem de fundo não come o contraste

- **WHEN** uma tela da Arena apresenta imagem de comunidade ao fundo
- **THEN** o texto, os componentes, as bordas que informam e o estado de foco sobre ela continuam
  cumprindo os pisos de contraste medidos

#### Scenario: A imagem de fundo não carrega informação

- **WHEN** a imagem de fundo não é carregada, por rede ou por preferência do aparelho
- **THEN** nada do que a tela comunica se perde

#### Scenario: A conquista devolve retorno, e o fato fica legível sem ele

- **WHEN** uma conquista é certificada numa aplicação da Arena
- **THEN** o retorno acontece em `300` ms, e a conquista também aparece em texto, numeral ou forma

#### Scenario: Menos movimento suprime o retorno sem esconder o fato

- **WHEN** o aparelho declara preferir menos movimento e uma conquista é certificada
- **THEN** nenhum movimento acontece, e a conquista continua anunciada

#### Scenario: Não há retorno sem fato

- **WHEN** uma tela da Arena é apresentada sem progresso nem conquista nova
- **THEN** nenhum movimento acontece
