## MODIFIED Requirements

### Requirement: A tela inicial oferece os dois caminhos e volta ao início a cada atendimento

A App 01 SHALL apresentar, na tela inicial, os dois caminhos — **onboarding** e **trilhas**. Ao
fim de cada atendimento, a aplicação SHALL voltar à tela inicial e NEVER SHALL exibir dado do
atendimento anterior. Quem escolhe **trilhas** sem sessão de Guerreiro(a) aberta SHALL ser
levado à entrada do Guerreiro(a), nunca ao cadastro.

Com o **momento de troca aberto**, a tela inicial SHALL apresentar também o caminho da **troca
por recompensa avulsa**, ao lado dos dois. Fechado o momento — que é o estado em que a aplicação
começa —, o caminho NEVER SHALL aparecer. (`RF-04-01`, `RF-04-28`, `RF-04-49`, PRD-04 §12)

#### Scenario: Os dois caminhos aparecem

- **WHEN** a sessão de trabalho está aberta
- **THEN** a tela inicial apresenta o caminho do onboarding e o caminho das trilhas

#### Scenario: Trilhas sem sessão leva à entrada, não ao cadastro

- **WHEN** alguém escolhe trilhas sem sessão de Guerreiro(a) aberta
- **THEN** a aplicação apresenta a entrada do Guerreiro(a), e nenhuma tela de cadastro aparece

#### Scenario: O atendimento seguinte começa limpo

- **WHEN** um atendimento termina e a aplicação volta à tela inicial
- **THEN** nenhum dado do atendimento anterior aparece em tela alguma

#### Scenario: O terceiro caminho só existe com o momento de troca aberto

- **WHEN** o Mestre abre o momento de troca
- **THEN** a tela inicial passa a apresentar também o caminho da troca, e volta a escondê-lo
  quando o momento é fechado

## ADDED Requirements

### Requirement: O momento de troca é aberto e fechado pelo Mestre, e só por ele

A App 01 SHALL oferecer a **abertura e o fechamento do momento de troca** apenas quando a sessão
de trabalho do aparelho for de um **Mestre**. Aparelho cuja sessão de trabalho for de **Admin**
NEVER SHALL oferecer a abertura, porque o registro da troca é ato do Mestre que entrega e o
núcleo recusa o de qualquer outro papel.

O momento SHALL começar **fechado** e SHALL ser um estado do próprio aparelho, sem registro no
núcleo. Perdido esse estado — recarga da página ou queda da sessão de trabalho —, o momento
SHALL voltar a **fechado**, e NEVER SHALL reabrir sozinho.

O momento NEVER SHALL abrir **sem rede**: a troca inteira é operação do núcleo, e não entra em
fila local. Fora do momento aberto, o catálogo avulso NEVER SHALL ser oferecido em tela alguma.
(`RF-04-49`, `RF-04-57`, `RN-04-27`, `RN-04-29`, PRD-04 §§5.10, 12)

#### Scenario: O Mestre abre o momento de troca

- **WHEN** o Mestre que abriu a sessão de trabalho do aparelho abre o momento de troca no
  encerramento do encontro
- **THEN** a aplicação passa a oferecer a troca aos Guerreiros e Guerreiras

#### Scenario: Aparelho aberto por Admin não oferece a troca

- **WHEN** a sessão de trabalho do aparelho é de um Admin
- **THEN** a aplicação não oferece a abertura do momento de troca, e nenhuma tela de catálogo
  aparece

#### Scenario: Fora do momento, o catálogo não aparece

- **WHEN** o momento de troca está fechado
- **THEN** o catálogo avulso não é oferecido em tela alguma, e não há caminho que chegue a ele

#### Scenario: Sem rede o momento não abre

- **WHEN** o Mestre tenta abrir o momento de troca com o aparelho sem rede
- **THEN** a aplicação recusa a abertura, explica que a troca exige rede e não enfileira nada

#### Scenario: O momento começa e volta a ficar fechado

- **WHEN** a aplicação é recarregada com o momento de troca aberto
- **THEN** o momento volta a ficar fechado, e o Mestre precisa abri-lo de novo

### Requirement: O Guerreiro(a) vê o catálogo da sua comunidade, o preço e o próprio saldo

Aberto o momento de troca, o Guerreiro(a) SHALL entrar pelo **nick e pela imagem**, pelo mesmo
caminho de entrada das trilhas, e a aplicação SHALL exibir o **catálogo avulso da comunidade
dele**, com o **preço em pontos extras** e o **estoque restante** de cada item, e o **saldo
disponível** de pontos extras dele.

A aplicação SHALL exibir o **saldo disponível**, e NEVER SHALL exibir o **acumulado** nesta tela:
o que a criança precisa saber é o que dá para trocar hoje. Item com **estoque zero** NEVER SHALL
ser oferecido para troca, ainda que o núcleo o devolva ativo no catálogo. Nenhuma tela desta
aplicação SHALL oferecer **ponto regular** como moeda de troca, e preço e diferença SHALL
aparecer sempre em **pontos**, nunca em reais nem em moedas da plataforma. (`RF-04-50`,
`RF-04-51`, `RF-04-54`, `RF-04-56`, `RN-04-23`, `RN-04-28`, PRD-04 §§5.10, 12)

#### Scenario: O catálogo da comunidade aparece com preço e estoque

- **WHEN** o Guerreiro(a) entra no momento de troca
- **THEN** a aplicação exibe os itens do catálogo avulso da comunidade dele, cada um com o preço
  em pontos extras e o estoque restante

#### Scenario: O saldo aparece, o acumulado não

- **WHEN** a tela da troca exibe o que o Guerreiro(a) tem
- **THEN** ela mostra o saldo disponível de pontos extras e não mostra o acumulado

#### Scenario: Item sem estoque não é oferecido

- **WHEN** o catálogo traz um item ativo cujo estoque é zero
- **THEN** esse item não aparece entre os que dá para trocar

#### Scenario: Ponto regular nunca é moeda

- **WHEN** qualquer tela da troca é exibida
- **THEN** nenhum ponto regular aparece como moeda, e nenhum preço aparece em reais nem em
  moedas da plataforma

### Requirement: O Mestre confirma a entrega, e a troca acontece num ato só

Escolhido o item, a aplicação SHALL registrar a troca **na confirmação da entrega pelo Mestre**,
num único envio ao núcleo. O envio SHALL ir **sob a sessão de trabalho do aparelho** — é o Mestre
que entrega, e é ele o autor da troca —, e o Guerreiro(a) SHALL ser identificado pela **persona
da sessão aberta na entrada**, NEVER por nick digitado nem por busca de persona.

Confirmada a troca, a aplicação SHALL voltar à tela inicial, pronta para o próximo. NEVER SHALL
haver reserva, fila ou promessa de entrega em encontro seguinte. (`RF-04-52`, `RF-04-55`,
`RN-04-24`, `RN-04-27`, `RF-04-28`, PRD-04 §§5.10, 12)

#### Scenario: A confirmação da entrega é o envio

- **WHEN** o Mestre confirma a entrega do item escolhido
- **THEN** a aplicação registra a troca num único envio, e a entrega não fica pendente de
  nenhum passo posterior

#### Scenario: O Guerreiro(a) vem da sessão, não de um nick

- **WHEN** a troca é registrada
- **THEN** o Guerreiro(a) da troca é o da sessão aberta na entrada, e nenhum nick é digitado nem
  consultado para identificá-lo

#### Scenario: O saldo cai o preço e o acumulado não muda

- **WHEN** uma troca de um item de 40 pontos extras é confirmada para um Guerreiro(a) de saldo
  disponível 100 e acumulado 300
- **THEN** a tela seguinte mostra saldo disponível 60, e o acumulado segue 300

#### Scenario: Feita a troca, o atendimento termina

- **WHEN** a troca é confirmada
- **THEN** a aplicação volta à tela inicial e não exibe dado do atendimento anterior

### Requirement: A recusa por saldo diz a diferença em pontos

A aplicação SHALL recusar a troca cujo preço for maior que o saldo disponível do Guerreiro(a),
dizendo a **diferença em pontos** que falta — nunca em reais nem em moedas da plataforma —, e
NEVER SHALL enviar ao núcleo uma troca que já sabe recusada.

Mudando o saldo ou o estoque entre a leitura da tela e o envio, a recusa do núcleo SHALL ser
apresentada em linguagem simples, dizendo qual condição barrou, e o Guerreiro(a) SHALL poder
escolher outro item sem recomeçar a entrada. (`RF-04-53`, `RN-04-25`, `RN-04-28`, PRD-04 §12)

#### Scenario: Saldo insuficiente é recusado com a diferença

- **WHEN** um Guerreiro(a) de saldo disponível 25 escolhe um item de 40 pontos extras
- **THEN** a aplicação recusa a troca dizendo que faltam 15 pontos, e nada é enviado ao núcleo

#### Scenario: A recusa do núcleo é dita em linguagem simples

- **WHEN** o núcleo recusa a troca porque o saldo ou o estoque mudou depois da leitura da tela
- **THEN** a aplicação diz qual condição barrou, em linguagem simples, e oferece a escolha de
  outro item sem repetir a entrada
