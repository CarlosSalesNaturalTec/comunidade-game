# Spec Delta

## ADDED Requirements

### Requirement: A App 01 apresenta a fila do cuidado do encontro a Mestre

A App 01 SHALL oferecer, no grupo de quem opera, o caminho **customizações a julgar**, **só**
quando quem abriu a sessão de trabalho é **Mestre**. A fila SHALL trazer cada Guerreiro(a) com
**presença registrada naquela aula**, por **nick e avatar**, com os bens recebidos dele; a
leitura e as escritas vão sob a **sessão de trabalho**. Encontro sem ninguém na fila diz que não
há, sem erro. (`RF-04-81`, `RF-04-84`, PRD-04 §5.13, invariante 12)

#### Scenario: O caminho aparece só a Mestre

- **WHEN** a sessão de trabalho foi aberta por Admin
- **THEN** o grupo de quem opera não oferece "customizações a julgar"

#### Scenario: A fila traz quem chegou, com os bens recebidos

- **WHEN** o Mestre abre o caminho e há Guerreiros(as) com presença registrada na aula
- **THEN** cada um aparece por nick e avatar, com os bens recebidos, a trilha e o tipo de recurso

#### Scenario: Encontro sem ninguém na fila

- **WHEN** a fila do encontro vem vazia
- **THEN** a aplicação diz que não há nada a julgar neste encontro, e não apresenta erro

### Requirement: O registro novo aparece ao lado do último aprovado do kit

Em cada kit com registro pendente, a App 01 SHALL apresentar a **mídia** e a **descrição** do
registro novo **lado a lado** com o **último registro aprovado** do kit, cuja mídia vem pela
rota do bem. Último aprovado sem mídia SHALL ser dito como tal, sem erro, e a mídia NEVER SHALL
ser exibida a quem não opera a sessão. (`RF-04-81`, PRD-04 §5.13.3)

#### Scenario: Kit com pendente mostra o antes e o agora

- **WHEN** o Mestre abre um kit com registro pendente
- **THEN** a tela mostra a mídia e a descrição do registro novo e a mídia do último aprovado

#### Scenario: O antes é a comprovação do prático

- **WHEN** o kit ainda não tem customização aprovada
- **THEN** o último aprovado mostrado é a comprovação do prático que abriu a customização

### Requirement: O Mestre da aula aprova ou reprova a customização com motivo

A App 01 SHALL permitir ao Mestre **aprovar** o registro pendente, ou **reprová-lo** com
**motivo** em linguagem simples, obrigatório antes do envio. Aprovado, a tela SHALL confirmar o
**ponto extra** e a **entrada no acervo**; a recusa do núcleo — bem que já pontuou no encontro,
registro já julgado, presença ausente — SHALL aparecer **como vem**. A fila SHALL ser **relida**
do núcleo depois de cada ato. (`RF-04-82`, `RF-04-83`, `RN-01-66`)

#### Scenario: Aprovado confirma o ponto extra e o acervo

- **WHEN** o Mestre aprova o registro pendente
- **THEN** a tela confirma 1 ponto extra e a entrada no acervo, e a fila é relida

#### Scenario: Reprovar exige motivo

- **WHEN** o Mestre escolhe reprovar e não escreveu motivo
- **THEN** a reprovação não é enviada, e o campo do motivo é apontado

#### Scenario: A recusa do núcleo aparece como vem

- **WHEN** o núcleo recusa a aprovação porque o kit já pontuou pela conservação no encontro
- **THEN** a tela apresenta a mensagem do núcleo, sem reescrevê-la

### Requirement: Sem registro, o Mestre captura a customização na hora

Em kit com customização **aberta** e **sem registro pendente**, a App 01 SHALL permitir ao
Mestre registrar, em nome do Guerreiro(a), a **foto ou o vídeo do kit** e a **descrição** dita
ou escrita pela criança, pela sessão de envio retomável; a descrição falada é transcrita no
aparelho. Só com o envio confirmado o registro passa a julgar. Kit sem customização aberta
NEVER SHALL oferecer captura. (`RF-04-82`, PRD-04 §5.13.3)

#### Scenario: Captura na hora vira registro a julgar

- **WHEN** o Mestre captura a foto do kit e a descrição da criança e o envio é confirmado
- **THEN** o kit passa a mostrar o registro pendente ao lado do último aprovado, pronto para o
  julgamento

#### Scenario: Kit fechado não oferece captura

- **WHEN** o bem recebido não tem customização aberta
- **THEN** a tela não oferece captura nem julgamento de customização para ele

### Requirement: Na mesma fila, o Mestre valida a conservação de cada bem

A App 01 SHALL oferecer, em cada bem recebido, a **validação da conservação**, a pedido da
criança, com **1 ponto extra** confirmado na tela. No kit com customização a julgar, a tela SHALL
pedir a escolha entre **conservação** e **customização**; o bem que **já pontuou** no encontro
SHALL dizer por qual caminho e NEVER SHALL oferecer nenhum dos dois. (`RF-04-84`, `RF-09-113`,
`RN-01-66`)

#### Scenario: Conservação validada confirma o ponto extra

- **WHEN** o Mestre valida a conservação do livro de um Guerreiro(a) da fila
- **THEN** a tela confirma 1 ponto extra, e o livro passa a dizer que já pontuou pela conservação

#### Scenario: O bem que já pontuou não oferece nada

- **WHEN** o kit já pontuou pela customização neste encontro
- **THEN** a tela diz que ele já pontuou pela customização e não oferece conservação nem
  julgamento

#### Scenario: No kit, conservação ou customização

- **WHEN** o kit tem registro pendente e ainda não pontuou no encontro
- **THEN** a tela oferece as duas, e escolher uma faz o kit dizer que já pontuou por ela
