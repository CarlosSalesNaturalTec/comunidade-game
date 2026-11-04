# Spec Delta

## MODIFIED Requirements

### Requirement: O Guerreiro(a) entrega a comprovação e acompanha o envio

A tela SHALL receber a comprovação na forma aceita — corpo escrito, endereço ou arquivo — e
SHALL **impedir o envio antes de ela estar preenchida**, em vez de explicá-lo depois do toque.
No envio de arquivo, a tela SHALL apresentar o **progresso** e, caindo a rede, SHALL dizê-lo e
oferecer **retomar**, sem recomeçar do zero nem perder a declaração.

A tela SHALL apresentar a comprovação **já entregue** em lugar de um formulário vazio, enquanto
o Mestre não julga. Julgado que o Guerreiro(a) **não cumpriu**, a tela SHALL **reabrir a
entrega** — a comprovação anterior segue à vista, e ele SHALL poder entregar outra em cima
dela, sem limite. Julgado que **cumpriu**, a entrega SHALL estar encerrada: a tela SHALL
apresentar o que ele entregou e NEVER SHALL oferecer entregar de novo. (`RF-05-91`, `RF-05-93`,
`RF-05-94`, `RN-09-54`)

#### Scenario: O controle de entrega fica indisponível sem a comprovação

- **WHEN** o Guerreiro(a) abre o prático e ainda não preencheu a comprovação
- **THEN** o controle de declarar que cumpriu fica indisponível

#### Scenario: O envio do arquivo mostra o progresso

- **WHEN** o Guerreiro(a) envia a comprovação em vídeo
- **THEN** a tela apresenta o progresso do envio até concluir

#### Scenario: A rede cai no meio do envio

- **WHEN** a conexão cai durante o envio da comprovação
- **THEN** a tela diz o que houve e oferece retomar, sem perder a declaração nem o que já subiu

#### Scenario: O Guerreiro(a) reencontra a comprovação entregue

- **WHEN** o Guerreiro(a) volta à missão depois de entregar e antes do julgamento
- **THEN** a tela apresenta a comprovação que ele entregou, e não um formulário vazio

#### Scenario: Recusado, a entrega reabre com o que ele já entregou à vista

- **WHEN** o Guerreiro(a) volta à missão depois de o Mestre ter julgado que ele não cumpriu
- **THEN** a tela apresenta a comprovação anterior e o controle de entregar de novo

#### Scenario: Cumprido, a tela não oferece entregar de novo

- **WHEN** o Guerreiro(a) volta à missão depois de o Mestre ter julgado que ele cumpriu
- **THEN** a tela apresenta o que ele entregou e nenhum controle de entrega é oferecido

## ADDED Requirements

### Requirement: A tela do prático apresenta o veredito do Mestre e o motivo

Julgado o prático, a tela SHALL apresentar ao Guerreiro(a) **o que o Mestre autor decidiu**: se
ele **cumpriu**, se a entrega é **publicável** — isto é, se vai à vitrine — e o **motivo**
escrito pelo Mestre, quando houver. O motivo SHALL ser apresentado **na íntegra**, como o Mestre
o escreveu, e NEVER SHALL ser resumido, substituído por frase da aplicação nem escondido atrás
de um controle.

Não tendo cumprido, a tela SHALL apresentar o motivo e oferecer **entregar de novo**, em
**linguagem acolhedora**, sem contagem de fracassos, sem punição e sem qualquer mensagem que
elimine, classifique ou culpe a criança — a mesma régua do quiz que não passa (`RN-05-20`). A
tela NEVER SHALL apresentar o veredito como nota, pontuação ou posição entre colegas.

Enquanto o Mestre **não julga**, a tela SHALL seguir dizendo que a missão **aguarda o Mestre**,
sem veredito e sem motivo, e NEVER SHALL apresentar a espera como recusa. (`RF-05-94`,
`RF-05-14`, `RN-05-20`, decisão do fundador de 2026-11-04)

#### Scenario: Cumprido e publicável, a tela diz as duas coisas

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu e que a entrega é publicável
- **THEN** a tela diz que ele cumpriu e que a produção pode ir à vitrine

#### Scenario: Cumprido e não publicável, a tela diz o motivo

- **WHEN** o Mestre autor julga que cumpriu, mas que a entrega não vai à vitrine, com motivo
- **THEN** a tela diz que ele cumpriu, que a produção não vai à vitrine e apresenta o motivo
  como o Mestre o escreveu

#### Scenario: Não cumprido, a tela traz o motivo e o convite a entregar de novo

- **WHEN** o Mestre autor julga que o Guerreiro(a) não cumpriu, com motivo
- **THEN** a tela apresenta o motivo na íntegra e oferece entregar de novo, em linguagem
  acolhedora

#### Scenario: O veredito não vira nota nem comparação

- **WHEN** a tela apresenta qualquer um dos vereditos
- **THEN** nenhuma nota, pontuação, contagem de tentativas ou comparação com colegas é
  apresentada

#### Scenario: Antes do julgamento, a tela diz que aguarda o Mestre

- **WHEN** o Guerreiro(a) abre o prático que ele declarou e o Mestre ainda não julgou
- **THEN** a tela diz que a missão aguarda o Mestre, sem veredito e sem motivo, e sem tratar a
  espera como recusa
