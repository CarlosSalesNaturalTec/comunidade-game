# Spec Delta

## ADDED Requirements

### Requirement: Os modelos de biometria se carregam antes da primeira captura, sem travar a aula

A App 01 SHALL começar a carregar os modelos de biometria **assim que a sessão de trabalho do
aparelho é aberta**, ao fundo, de modo que a primeira captura do encontro não pague o
carregamento inteiro. A carga NEVER SHALL bloquear tela, caminho ou botão algum: a tela inicial,
o registro de presença e a fila local SHALL ficar disponíveis enquanto ela acontece, e SHALL
continuar disponíveis se ela não acontecer. (`RF-04-75`, documento 03 §§3.2, 3.4)

A pré-carga SHALL carregar **apenas os modelos**, e NEVER SHALL abrir a câmera do aparelho.
(`RN-04-42`, `RN-04-07`)

#### Scenario: A pré-carga começa com a sessão de trabalho

- **WHEN** Mestre ou Admin abre a sessão de trabalho do aparelho e há rede
- **THEN** a aplicação começa a carregar os modelos de biometria ao fundo

#### Scenario: O menu não espera pela pré-carga

- **WHEN** a sessão de trabalho é aberta e a pré-carga ainda está em andamento
- **THEN** a tela inicial e os caminhos dela são apresentados e operam normalmente

#### Scenario: A presença não espera pela pré-carga

- **WHEN** a pré-carga está em andamento ou não aconteceu
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

### Requirement: A pré-carga falha em silêncio, e a captura segue dizendo o que houve

Falha da pré-carga NEVER SHALL ser anunciada na tela: ela é otimização, não ato da pessoa. O
**caminho de erro visível continua sendo o do preparo da captura**, que SHALL seguir distinguindo
preparo que não concluiu, vivacidade reprovada e recusa do núcleo. (`RF-04-75`, `RF-04-65`)

#### Scenario: Falha da pré-carga não aparece na tela

- **WHEN** a pré-carga não consegue carregar os modelos
- **THEN** nenhuma mensagem de erro é apresentada, e a aplicação segue operando

#### Scenario: A falha de preparo continua sendo dita na captura

- **WHEN** a pré-carga falhou e, depois, uma tela de câmera é aberta e o preparo também falha
- **THEN** a tela diz que a captura não pôde ser preparada, com a frase distinta que já existe

#### Scenario: A pré-carga concluída não muda o que a captura faz

- **WHEN** a pré-carga concluiu e uma tela de câmera é aberta
- **THEN** o preparo da captura conclui normalmente, sem recarregar os modelos

### Requirement: O andamento da pré-carga é dito de forma discreta e honesta

A App 01 SHALL apresentar o andamento da pré-carga de forma **discreta**, por **modelo
carregado** — a granularidade que a biblioteca oferece —, e NEVER SHALL apresentá-lo como
percentual contínuo, que seria precisão inventada. O indicador SHALL desaparecer ao concluir e
NEVER SHALL impedir ação alguma. (`RF-04-75`)

#### Scenario: O andamento aparece enquanto dura

- **WHEN** a pré-carga está em andamento
- **THEN** o aparelho apresenta o andamento por modelo carregado, sem impedir qualquer ação

#### Scenario: O indicador sai ao concluir

- **WHEN** a pré-carga conclui
- **THEN** o indicador deixa de ser apresentado

#### Scenario: O andamento não promete precisão que não tem

- **WHEN** o andamento é apresentado
- **THEN** ele é expresso por modelo carregado, e não como percentual contínuo
