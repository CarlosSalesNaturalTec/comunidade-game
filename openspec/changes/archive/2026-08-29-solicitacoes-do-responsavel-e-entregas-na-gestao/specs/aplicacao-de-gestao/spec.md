## ADDED Requirements

### Requirement: A área Filas apresenta a fila das solicitações do responsável

A aplicação SHALL apresentar, na área **Filas**, a fila das solicitações vindas da App 07, com
**protocolo**, **tipo**, **situação** e o **prazo de 7 dias** de cada uma, da mais antiga para a
mais recente, e SHALL identificar o Guerreiro(a) a que a solicitação se refere e o responsável
que a abriu. A lista é da gestão: NEVER SHALL ser alcançada por Mestre. (`RF-02-23`, PRD-02 §5.8)

#### Scenario: A fila mostra o que o Admin precisa para triar

- **WHEN** o Admin abre a fila das solicitações do responsável
- **THEN** cada item traz protocolo, tipo, situação e o prazo de 7 dias

#### Scenario: O Mestre não alcança a fila

- **WHEN** um Mestre abre a área Filas
- **THEN** a fila das solicitações do responsável não lhe é oferecida

### Requirement: O Admin registra o desfecho da solicitação do responsável

A aplicação SHALL oferecer, sobre a solicitação escolhida, a tela de tratamento com o texto do
pedido e o registro do **desfecho** — aceita ou recusada —, com o texto do que foi tratado. Feito
o registro, a tela SHALL mostrar **quem tratou** e **quando**, e a solicitação tratada NEVER
SHALL oferecer novo tratamento. (`RF-02-24`)

#### Scenario: Desfecho registrado mostra o autor e a data

- **WHEN** o Admin registra o desfecho de uma solicitação
- **THEN** a solicitação passa a exibir o desfecho, quem tratou e a data e hora

#### Scenario: Solicitação tratada não reabre o tratamento

- **WHEN** o Admin abre uma solicitação que já tem desfecho
- **THEN** a tela a apresenta em leitura, sem caminho para novo desfecho

### Requirement: A solicitação sem desfecho em 7 dias aparece em atraso na fila

A aplicação SHALL destacar na fila, como **em atraso**, a solicitação sem desfecho cujo prazo já
venceu, e o item em atraso SHALL continuar tratável como qualquer outro — o atraso NEVER SHALL
retirá-lo da fila nem bloquear o tratamento. (`RF-02-66`)

#### Scenario: Vencido o prazo, a fila destaca o atraso

- **WHEN** a fila traz uma solicitação sem desfecho com o prazo vencido
- **THEN** ela aparece destacada como em atraso

#### Scenario: O atraso não impede o tratamento

- **WHEN** o Admin abre uma solicitação em atraso
- **THEN** trata e registra o desfecho normalmente

### Requirement: A área Acervo mostra as entregas confirmadas pelo Mestre

A aplicação SHALL apresentar, na área **Acervo**, a leitura das entregas de recompensa de marco
já confirmadas pelo Mestre — entre elas o **exemplar da linha Alpha** e a **camisa** —, com o
Guerreiro(a), o **tipo de recurso** entregue, o **Mestre que entregou**, o ponto de apoio de onde
o recurso saiu e a data. A lista SHALL mostrar que a entrega deu **baixa definitiva** no
livro-razão, e NEVER SHALL exibir valor em moedas nem em reais. (`RF-02-50`, `RF-02-51`,
`RN-02-17`)

#### Scenario: A entrega do exemplar Alpha aparece com a baixa

- **WHEN** o Admin abre a lista de entregas na área Acervo
- **THEN** vê a entrega do exemplar Alpha com o Guerreiro(a), o Mestre que entregou, o ponto de
  apoio, a data e a baixa definitiva registrada

#### Scenario: A entrega da camisa aparece com o Guerreiro(a) inscrito

- **WHEN** o Admin abre a lista de entregas na área Acervo
- **THEN** vê a entrega da camisa ao Guerreiro(a) inscrito, com a mesma baixa definitiva

#### Scenario: A lista não mostra custo

- **WHEN** o Admin lê a lista de entregas
- **THEN** nenhum campo traz valor em moedas nem em reais

### Requirement: A gestão não confirma a entrega, apenas a mostra

A área Acervo SHALL apresentar as entregas em **leitura**, e NEVER SHALL oferecer à gestão o
caminho de confirmar, corrigir ou desfazer uma entrega: quem confirma é o Mestre que estava no
encontro. (`RF-02-50`, `RF-02-51`)

#### Scenario: Nenhuma tela da gestão confirma entrega

- **WHEN** o Admin percorre a área Acervo
- **THEN** encontra a lista de entregas em leitura e nenhum caminho para registrar entrega
