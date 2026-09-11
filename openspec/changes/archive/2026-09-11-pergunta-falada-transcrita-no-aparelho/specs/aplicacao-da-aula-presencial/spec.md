## MODIFIED Requirements

### Requirement: O microfone abre por ação do Guerreiro(a) e fecha ao fim da fala

A App 01 SHALL abrir o microfone **somente** quando o Guerreiro(a) aciona o botão de falar, e
SHALL fechá-lo **ao fim da fala**. A aplicação NEVER SHALL manter o microfone aberto entre uma
pergunta e outra, NEVER SHALL captar o áudio ambiente da aula e NEVER SHALL transcrever a
conversa da turma.

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

- **WHEN** a transcrição da fala aparece no campo da pergunta e a equipe a edita
- **THEN** o que segue ao núcleo é o texto corrigido

## ADDED Requirements

### Requirement: Sem transcrição no navegador, a tela avisa e mantém a pergunta por texto

Onde o navegador do aparelho não oferecer a transcrição da fala, a App 01 SHALL **dizê-lo em
linguagem simples** e SHALL manter disponível a pergunta **por texto digitado** — o caminho que
a tela já oferece sempre, ao lado do botão de falar, nunca escondido atrás de uma escolha de
forma. A aplicação NEVER SHALL deixar a equipe sem caminho para perguntar, e NEVER SHALL cair de
volta no envio de áudio ao núcleo (`RF-04-39`, `RF-04-40`, documento 03 §1.12).

O mesmo aviso SHALL valer quando a transcrição falhar ou não entender nada da fala: a pergunta
digitada continua à mão, e a fala pode ser refeita.

#### Scenario: O navegador não transcreve

- **WHEN** a tela do assistente abre num navegador sem a transcrição de fala
- **THEN** a tela avisa que ali a pergunta é por texto, e o campo de texto segue disponível

#### Scenario: A transcrição não entendeu a fala

- **WHEN** o Guerreiro(a) fala e o aparelho não devolve transcrição alguma
- **THEN** a tela o diz em linguagem simples, sem perder o que estava escrito, e a equipe pode
  falar de novo ou digitar
