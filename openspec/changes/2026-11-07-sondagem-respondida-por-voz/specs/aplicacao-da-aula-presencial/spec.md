# Spec Delta

## ADDED Requirements

### Requirement: A sondagem no aparelho do encontro é respondida por voz com o áudio ligado

Na App 01, com o áudio ligado, a sondagem SHALL abrir a janela de escuta da capacidade
`sondagem-por-voz` depois de cada pergunta falada; com ele desligado, SHALL seguir por toque como
antes. (`RF-04-77`, `RF-04-73`, `RN-05-54`)

#### Scenario: A sondagem no encontro fala, escuta e avança

- **WHEN** o Guerreiro(a) com o áudio ligado responde à sondagem no aparelho do encontro
- **THEN** cada pergunta é falada, a janela de 5 segundos abre, e a resposta segue sozinha

## MODIFIED Requirements

### Requirement: O microfone abre por ação do Guerreiro(a) e fecha ao fim da fala

A App 01 SHALL abrir o microfone **somente** quando o Guerreiro(a) aciona o botão de falar, e
SHALL fechá-lo **ao fim da fala** — com uma exceção: a **janela de 5 segundos da sondagem**, com o
áudio ligado (`RF-04-77`), que abre depois da pergunta falada e fecha ao terminar. A aplicação
NEVER SHALL manter o microfone aberto entre uma pergunta e outra, NEVER SHALL captar o áudio
ambiente da aula e NEVER SHALL transcrever a conversa da turma.

A fala SHALL ser **transcrita no próprio aparelho**, e ao núcleo SHALL seguir **a transcrição**,
nunca o áudio. A aplicação NEVER SHALL gravar o áudio em arquivo, em armazenamento do navegador
ou em qualquer lugar do aparelho compartilhado. A transcrição SHALL aparecer no campo da
pergunta **antes do envio** e SHALL ser editável ali, como qualquer pergunta digitada.
(`RF-04-39`, `RF-04-40`, `RN-04-20`, `RN-04-21`, documento 03 §1.12, PRD-04 §11)

#### Scenario: Sem toque não há captação

- **WHEN** a tela do assistente está aberta e ninguém aciona o botão de falar
- **THEN** o microfone permanece fechado e nada é captado

#### Scenario: Terminada a fala, o microfone fecha

- **WHEN** o Guerreiro(a) encerra a pergunta falada
- **THEN** a aplicação fecha o microfone antes de enviar a pergunta

#### Scenario: O que segue ao núcleo é a transcrição

- **WHEN** a pergunta falada é enviada
- **THEN** a aplicação manda o texto transcrito no aparelho, e nenhum áudio sai dele

#### Scenario: O áudio não fica no aparelho

- **WHEN** a pergunta falada é enviada
- **THEN** nenhum áudio permanece no aparelho — nem em arquivo, nem em armazenamento do
  navegador

#### Scenario: A equipe corrige a transcrição antes de enviar

- **WHEN** a transcrição da fala aparece no campo da produção e a equipe a edita
- **THEN** o que segue ao núcleo é o texto corrigido, com a forma "áudio" declarada

#### Scenario: O áudio não fica no aparelho

- **WHEN** a produção falada é enviada
- **THEN** nenhum áudio permanece no aparelho — nem em arquivo, nem em armazenamento do
  navegador

#### Scenario: A equipe entrega a foto do manuscrito

- **WHEN** a equipe fotografa o que fez à mão e envia
- **THEN** a aplicação envia a foto e não a mantém no aparelho depois do envio

#### Scenario: A tela diz que a devolutiva não vale ponto

- **WHEN** a devolutiva é apresentada
- **THEN** a tela diz, em linguagem simples, que ela não credita ponto e que quem lança o
  resultado é o Mestre

#### Scenario: A produção esperada aparece antes da entrega

- **WHEN** a tela da entrega é apresentada
- **THEN** ela mostra a produção esperada declarada na atividade

#### Scenario: Devolutiva que não veio não perde a entrega por texto

- **WHEN** o núcleo registra a produção em texto sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Devolutiva que não veio não perde a entrega falada

- **WHEN** o núcleo registra a produção falada sem devolutiva
- **THEN** a aplicação confirma a entrega e avisa que o retorno não veio desta vez

#### Scenario: Leitura indisponível pede reenvio

- **WHEN** o núcleo recusa a entrega por foto porque a leitura não veio
- **THEN** a aplicação pede o reenvio em linguagem simples, sem dizer que a produção se perdeu

#### Scenario: O navegador não transcreve

- **WHEN** a tela da entrega abre num navegador sem a transcrição de fala
- **THEN** a tela avisa que ali a entrega é por texto ou por foto, e não oferece a fala

#### Scenario: A transcrição não entendeu a fala

- **WHEN** um integrante fala e o aparelho não devolve transcrição alguma
- **THEN** a tela o diz em linguagem simples, sem perder o que estava escrito, e a equipe pode
  falar de novo ou digitar

#### Scenario: Fora da janela da sondagem, sem toque não há captação

- **WHEN** o áudio está ligado e nenhuma pergunta da sondagem está em escuta
- **THEN** o microfone permanece fechado
