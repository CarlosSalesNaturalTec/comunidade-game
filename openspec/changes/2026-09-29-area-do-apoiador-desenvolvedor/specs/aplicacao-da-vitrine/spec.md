# Spec Delta

## ADDED Requirements

### Requirement: A Área do Apoiador Desenvolvedor é seção da vitrine e reúne quatro coisas

A App 06 SHALL oferecer a **Área do Apoiador Desenvolvedor** em endereço próprio, pública e sem
login, como **seção da vitrine** — nunca uma nona aplicação (`RN-03-29`).

A área SHALL reunir, na mesma tela, as quatro coisas do `RF-03-67`: o **assistente de chat**, o
**link da documentação** publicada com MkDocs, o **formulário de solicitação de chave** e o
**link do repositório no GitHub**.

A área NEVER SHALL pedir login, cadastro ou qualquer dado do visitante fora dos campos do
formulário de chave.

#### Scenario: A área abre com as quatro coisas

- **WHEN** um visitante abre a Área do Apoiador Desenvolvedor
- **THEN** a tela traz o assistente de chat, o link da documentação, o formulário de chave e o
  link do repositório, sem pedir login

### Requirement: O assistente abre explicando a arquitetura, sem esperar a primeira pergunta

A primeira mensagem do assistente SHALL chegar **sem que se pergunte nada**, explicando como a
plataforma está montada — a API, as oito aplicações e o contrato de somente leitura — e
terminando com a pergunta de múltipla escolha sobre o próximo passo (`RF-03-68`, `RF-03-69`).

Essa abertura SHALL ser **texto da própria aplicação**, e não resposta do modelo: nenhuma
chamada ao assistente acontece ao abrir a área (decisão do fundador de 2026-09-29). Ela SHALL
continuar de pé com o assistente fora do ar.

#### Scenario: A primeira mensagem chega sozinha

- **WHEN** o visitante abre a área e não digita nada
- **THEN** o assistente já apresenta a arquitetura da plataforma e oferece as escolhas do
  próximo passo

#### Scenario: A abertura não consulta o modelo

- **WHEN** a área abre
- **THEN** nenhuma consulta ao assistente é enviada ao núcleo antes da primeira pergunta do
  visitante

### Requirement: Toda mensagem do assistente termina com a escolha do próximo passo

A tela SHALL apresentar, ao fim de **toda** mensagem do assistente, a pergunta de múltipla
escolha sobre o que conhecer em seguida — inclusive na recusa de assunto fora do corpus e na
última mensagem de uma conversa longa (`RF-03-69`).

Escolher uma das opções SHALL valer como a próxima pergunta, e o visitante SHALL poder
perguntar livremente em vez de escolher.

#### Scenario: A escolha conduz a conversa

- **WHEN** o visitante escolhe uma das opções oferecidas
- **THEN** o assistente aprofunda aquele tópico e oferece a escolha seguinte

#### Scenario: A pergunta livre também é aceita

- **WHEN** o visitante digita a própria pergunta em vez de escolher
- **THEN** o assistente responde a ela e ainda assim termina com a pergunta de múltipla escolha

### Requirement: A conversa não sobrevive à página, e nada dela é guardado no aparelho

A App 06 NEVER SHALL guardar a conversa com o assistente — nem no servidor, nem no
armazenamento local, nem em cookie (`RN-03-15`, `RN-03-22`, PRD-03 §8). Recarregar a página
SHALL perder a conversa inteira.

#### Scenario: Recarregar perde a conversa

- **WHEN** o visitante conversa com o assistente e recarrega a página
- **THEN** a área volta à mensagem de abertura, e nada da conversa anterior está no aparelho

### Requirement: A área segue utilizável com o assistente fora do ar

Quando o núcleo devolver a indisponibilidade do assistente, a tela SHALL exibir o **aviso de
que o assistente voltará**, dito como falha do assistente e não como recusa do domínio, e SHALL
manter acessíveis a **documentação**, o **repositório** e o **formulário de chave**
(`RF-03-72`, documento 99 §6 invariante 25).

#### Scenario: O assistente fora do ar não derruba a área

- **WHEN** a consulta ao assistente devolve indisponibilidade
- **THEN** a tela avisa que o assistente voltará e a documentação, o repositório e o formulário
  de chave continuam acessíveis

### Requirement: O formulário de chave pede quem é, o contato e o que se pretende construir

O formulário de solicitação de chave SHALL pedir o **solicitante**, o **contato** e **o que se
pretende construir**, com a instituição opcional, e SHALL declarar na própria tela que o envio
**não emite chave nenhuma e não cria cadastro**: gera registro na fila de avaliação da App 03,
avaliada por Admin (`RF-03-73`, `RF-03-74`, `RN-03-32`).

O envio SHALL confirmar o registro com o **protocolo e o prazo**, e NEVER SHALL devolver chave,
segredo, arquivo ou acesso.

#### Scenario: O envio devolve protocolo e prazo, nunca chave

- **WHEN** o visitante envia o formulário de solicitação de chave completo
- **THEN** a tela confirma o registro com o protocolo e o prazo, e nenhuma chave nem segredo é
  devolvido

#### Scenario: A tela declara o que a solicitação não faz

- **WHEN** o visitante abre o formulário de chave
- **THEN** a tela declara que o envio não emite chave nem cria cadastro, e que quem avalia e
  emite é um Admin na gestão

### Requirement: O formulário de chave não encontra espera crescente

O envio repetido do formulário de solicitação de chave NEVER SHALL encontrar espera crescente
nem recusa por origem, porque nova solicitação é sempre possível (`RN-03-35`). A tela NEVER
SHALL anunciar espera para essa superfície.

#### Scenario: Enviar de novo não encontra espera

- **WHEN** a mesma pessoa envia o formulário de chave mais de uma vez seguida
- **THEN** cada envio é registrado normalmente, sem espera anunciada nem recusa por origem

### Requirement: A área informa os dois prazos e o que a chave é

A área SHALL informar o prazo de **7 dias** para a resposta à solicitação e os **30 dias** para
apresentar a URL do que foi construído, contados da emissão (`RF-03-75`).

A área SHALL declarar que **a API não responde sem chave** e que a **chave não amplia direito
de escrita**: o contrato de somente leitura vale igual para toda aplicação de terceiro
(`RF-03-76`).

#### Scenario: Os dois prazos estão na tela

- **WHEN** o visitante lê a área
- **THEN** ela informa os 7 dias da resposta e os 30 dias da apresentação da URL

#### Scenario: A tela declara o que a chave é e o que não é

- **WHEN** o visitante lê a área
- **THEN** ela declara que sem chave a API não responde e que a chave não amplia direito de
  escrita

### Requirement: A área oferece o caminho de apresentar a URL do que foi construído

A área SHALL oferecer a apresentação da **URL** do que foi construído, identificada pelo
**identificador da chave** que o solicitante recebeu na emissão, dentro do prazo (`RF-03-77`).

A tela NEVER SHALL pedir o segredo da chave, e SHALL mostrar a recusa que o núcleo declarar —
prazo vencido, chave inexistente ou identificador que não confere — com a causa dita como o que
é (documento 99 §6 invariante 25).

#### Scenario: A URL apresentada no prazo é aceita

- **WHEN** quem recebeu a chave informa o identificador dela e a URL, dentro do prazo
- **THEN** a tela confirma a apresentação

#### Scenario: A tela nunca pede o segredo

- **WHEN** o visitante abre a apresentação da URL
- **THEN** a tela pede o identificador da chave e a URL, e em momento nenhum o segredo

#### Scenario: A recusa do núcleo aparece como o que é

- **WHEN** a apresentação é recusada por prazo vencido ou por identificador que não confere
- **THEN** a tela mostra a causa que o núcleo declarou, sem disfarçá-la de outra coisa
