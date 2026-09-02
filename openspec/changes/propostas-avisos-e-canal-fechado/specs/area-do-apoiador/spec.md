## ADDED Requirements

### Requirement: A App 08 tem a área de propostas de evolução da plataforma

A App 08 SHALL permitir ao Apoiador registrar **proposta de evolução da plataforma** em texto,
que entra na **fila única da gestão** — a mesma que recebe as sugestões do Guerreiro(a), do
responsável e do Mestre —, sem alvo de atividade nem de trilha.

A tela NEVER SHALL prometer ponto, badge ou recompensa pela proposta: o Apoiador não pontua, e
a proposta não altera moeda, selo nem nível de sustento. (`RF-14-56`, `RN-14-26`, `RN-14-29`)

#### Scenario: A proposta entra na fila única

- **WHEN** o Apoiador registra uma proposta em texto
- **THEN** ela entra na fila única da gestão e passa a aparecer entre as propostas dele

#### Scenario: A tela não promete ponto nem moeda

- **WHEN** o Apoiador abre a área de propostas
- **THEN** nenhuma tela promete ponto, badge, moeda, selo ou nível pela proposta registrada

### Requirement: O Apoiador acompanha o status da proposta dentro da plataforma

A App 08 SHALL apresentar o **status** de cada proposta do Apoiador até o retorno e, quando a
gestão a concluir como não adotada, SHALL apresentar o **motivo em linguagem simples**.

O retorno SHALL acontecer **dentro da plataforma**: a aplicação NEVER SHALL prometer aviso por
e-mail. A tela NEVER SHALL exibir o parecer interno da gestão. (`RF-14-57`, `RN-14-27`)

#### Scenario: O status aparece até o retorno

- **WHEN** o Apoiador abre a área de propostas
- **THEN** cada proposta dele aparece com o status em que está

#### Scenario: A proposta não adotada traz o motivo

- **WHEN** a gestão conclui a proposta do Apoiador como não adotada
- **THEN** ele vê o status e o motivo em linguagem simples, dentro da plataforma

#### Scenario: A tela não promete e-mail

- **WHEN** o Apoiador registra a proposta
- **THEN** a tela não promete aviso por e-mail e informa que o retorno chega na plataforma

### Requirement: A App 08 tem a área detalhada de direitos e dados

A App 08 SHALL oferecer uma **área detalhada**, de leitura, que declara o que a aplicação
coleta do Apoiador, com **finalidade, base legal, prazo de guarda e quem acessa** cada dado,
conforme a PRD-14 §11, e que declara que o pedido de acesso, correção ou exclusão é feito à
gestão.

A área NEVER SHALL escrever, exportar ou excluir dado, e NEVER SHALL exibir dado de
Guerreiro(a). (`RF-14-58`, PRD-14 §11)

#### Scenario: A área lista o destino e o uso de cada dado

- **WHEN** o Apoiador abre a área de direitos e dados
- **THEN** ele vê cada dado coletado com finalidade, base legal, prazo de guarda e quem acessa

#### Scenario: A área diz por onde correm os direitos

- **WHEN** o Apoiador abre a área de direitos e dados
- **THEN** a tela declara que acesso, correção e exclusão são pedidos à gestão

### Requirement: Toda tela da App 08 que grava dado avisa o que ali se coleta

A App 08 SHALL exibir um **aviso discreto** do que está sendo coletado em toda tela em que
grava dado — o pré-cadastro da porta pública; a troca da senha provisória; a identidade
pública; o envio de comprobatório; a declaração de aporte; a cobertura de missão; a proposta de
desafio extra; o favorito; e o registro da proposta de evolução. Cada aviso SHALL nomear o dado
**daquela** tela e SHALL oferecer o acesso à **área detalhada**.

O aviso NEVER SHALL bloquear a tela, NEVER SHALL exigir confirmação para continuar e NEVER
SHALL impedir o envio do formulário. (`RF-14-58`, PRD-14 §11)

#### Scenario: A tela de declaração de aporte traz o aviso

- **WHEN** o Apoiador abre a tela em que declara o aporte
- **THEN** um aviso discreto nomeia o dado coletado ali e oferece o acesso à área detalhada

#### Scenario: A porta pública traz o aviso antes de qualquer cadastro

- **WHEN** o visitante abre a porta pública de pré-cadastro, sem sessão
- **THEN** um aviso discreto nomeia o dado coletado ali e oferece o acesso à área detalhada

#### Scenario: O aviso não interrompe o uso

- **WHEN** o Apoiador preenche e envia o formulário de uma tela que grava dado
- **THEN** o aviso não bloqueia a tela, não pede confirmação e não impede o envio

### Requirement: Nenhuma tela da App 08 oferece canal com Guerreiro(a), família ou Mestre

A App 08 NEVER SHALL oferecer campo de mensagem, telefone, e-mail, resposta ou qualquer outro
canal de contato com Guerreiro(a), família ou Mestre, em nenhuma tela — inclusive nas que
tratam de desafio extra, de missão, de efetividade, de favoritos e de proposta de evolução.

Todo contato do Apoiador com a plataforma SHALL ser mediado pela gestão. (`RF-14-59`,
`RN-14-20`, `RN-14-24`)

#### Scenario: Nenhuma tela oferece campo de mensagem

- **WHEN** o Apoiador percorre as telas da aplicação
- **THEN** nenhuma delas oferece campo de mensagem, telefone ou e-mail de Guerreiro(a), família
  ou Mestre

#### Scenario: A proposta de evolução vai à gestão, não a uma pessoa

- **WHEN** o Apoiador registra a proposta de evolução
- **THEN** ela vai à fila da gestão, e a tela não oferece destinatário, resposta nem conversa
