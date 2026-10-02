# Spec Delta

## ADDED Requirements

### Requirement: Os modelos de biometria se carregam antes da primeira captura, sem travar a aula

A App 01 SHALL começar a carregar os modelos de biometria **assim que a sessão de trabalho do
aparelho é aberta**, ao fundo, de modo que a primeira captura do encontro não pague o
carregamento inteiro. A carga NEVER SHALL bloquear tela, caminho ou botão algum: a tela inicial,
o registro de presença e a fila local SHALL ficar disponíveis enquanto ela acontece, e SHALL
continuar disponíveis se ela não acontecer. (`RF-04-75`, documento 03 §§3.2, 3.4)

A pré-carga SHALL carregar **apenas os modelos**, e NEVER SHALL abrir a câmera do aparelho.
(`RN-04-42`, `RN-04-07`, documento 03 §3.3)

#### Scenario: A pré-carga começa com a sessão de trabalho

- **WHEN** Mestre ou Admin abre a sessão de trabalho do aparelho e há rede
- **THEN** a aplicação começa a carregar os modelos de biometria ao fundo

#### Scenario: O menu não espera pela pré-carga

- **WHEN** a sessão de trabalho é aberta e a pré-carga ainda está em andamento
- **THEN** a tela inicial e os caminhos dela são apresentados e operam normalmente

#### Scenario: A presença não espera pela pré-carga

- **WHEN** a pré-carga está em andamento, falhou ou não aconteceu
- **THEN** o registro de presença e a fila local operam como se ela não existisse

#### Scenario: A pré-carga não abre a câmera

- **WHEN** a pré-carga acontece
- **THEN** a câmera do aparelho não é aberta, e nenhuma imagem é capturada

#### Scenario: Sem rede, a pré-carga não acontece e nada quebra

- **WHEN** a sessão de trabalho é aberta sem rede
- **THEN** a pré-carga não acontece, a aplicação segue operando e a captura continua preparando
  os modelos quando a câmera for aberta

#### Scenario: A rede que volta retoma a pré-carga

- **WHEN** a sessão de trabalho foi aberta sem rede e a rede volta durante o encontro
- **THEN** a pré-carga acontece a partir dali, ainda ao fundo

### Requirement: O andamento da pré-carga é dito, e dito por modelo carregado

A App 01 SHALL apresentar o andamento da pré-carga enquanto ela dura, por **modelo carregado** —
a granularidade que a biblioteca oferece —, e NEVER SHALL apresentá-lo como percentual contínuo,
que seria precisão inventada. O andamento SHALL ser apresentado como **informação, nunca como
erro**, SHALL desaparecer ao concluir e NEVER SHALL impedir ação alguma. Com a narração das telas
ativada, o andamento SHALL ser falado como qualquer outro aviso. (`RF-04-75`, documento 15 §5.1)

#### Scenario: O andamento aparece enquanto dura

- **WHEN** a pré-carga está em andamento
- **THEN** o aparelho apresenta o andamento por modelo carregado, sem impedir qualquer ação

#### Scenario: O indicador sai ao concluir

- **WHEN** a pré-carga conclui
- **THEN** o indicador deixa de ser apresentado

#### Scenario: O andamento não promete precisão que não tem

- **WHEN** o andamento é apresentado
- **THEN** ele é expresso por modelo carregado, e não como percentual contínuo

#### Scenario: A narração fala o andamento quando está ativada

- **WHEN** a narração das telas está ativada e o andamento é apresentado
- **THEN** ele é falado, como os demais avisos da aplicação

### Requirement: A falha da pré-carga é dita, e não trava o indicador

Falha da pré-carga SHALL ser dita na tela **como erro**, nomeando o que não carregou, e NEVER
SHALL deixar o indicador parado no passo em que travou. A mensagem NEVER SHALL depender da cor
para ser entendida: ela SHALL trazer rótulo textual próprio, como todo estado da aplicação.
(`RF-04-75`, documento 15 §5)

A falha NEVER SHALL impedir ação alguma, e o **caminho de erro do preparo da captura** SHALL
seguir intacto e distinto — a captura continua distinguindo preparo que não concluiu, vivacidade
reprovada e recusa do núcleo. (`RF-04-65`)

#### Scenario: A falha é dita, e o andamento sai

- **WHEN** a pré-carga não consegue carregar os modelos
- **THEN** a tela diz que não foi possível carregar os modelos de reconhecimento facial, e o
  indicador de andamento deixa de ser apresentado

#### Scenario: A mensagem não depende da cor

- **WHEN** a falha da pré-carga é apresentada
- **THEN** ela traz rótulo textual que a identifica como erro, sem depender da cor

#### Scenario: A rede que volta limpa a mensagem

- **WHEN** a pré-carga falhou e a rede volta
- **THEN** a mensagem de falha deixa de ser apresentada e o andamento volta a ser apresentado

#### Scenario: A falha não impede a aula

- **WHEN** a pré-carga falhou
- **THEN** a tela inicial, o registro de presença e os demais caminhos seguem operando

#### Scenario: A falha de preparo da captura continua sendo dita onde sempre foi

- **WHEN** a pré-carga falhou e, depois, uma tela de câmera é aberta e o preparo também falha
- **THEN** a tela da captura diz que a captura não pôde ser preparada, com a frase distinta que
  já existe, e não a confunde com a mensagem da pré-carga

#### Scenario: A pré-carga concluída não muda o que a captura faz

- **WHEN** a pré-carga concluiu e uma tela de câmera é aberta
- **THEN** o preparo da captura conclui normalmente, sem recarregar os modelos
