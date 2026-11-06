## MODIFIED Requirements

### Requirement: O Guerreiro(a) entrega a comprovação e acompanha o envio

A tela SHALL receber a comprovação na forma aceita — corpo escrito, endereço ou arquivo — e
SHALL **impedir o envio antes de ela estar preenchida**, em vez de explicá-lo depois do toque.
No envio de arquivo, a tela SHALL apresentar o **progresso** e, caindo a rede, SHALL dizê-lo e
oferecer **retomar**, sem recomeçar do zero nem perder a declaração.

A declaração em **mídia**, ainda **não julgada**, sem entrega no encontro e **sem arquivo
recebido** pelo núcleo SHALL oferecer o envio do arquivo na tela da missão, como retomada da
mesma declaração: o envio NEVER SHALL exigir declarar de novo nem criar outra declaração.

A tela SHALL apresentar a comprovação **já entregue** em lugar de um formulário vazio, enquanto
o Mestre não julga, e NEVER SHALL apresentar o título "O que você entregou" sem nada abaixo
dele. Julgado que o Guerreiro(a) **não cumpriu**, a tela SHALL **reabrir a entrega** — a
comprovação anterior segue à vista, e ele SHALL poder entregar outra em cima dela, sem limite.
Julgado que **cumpriu**, a entrega SHALL estar encerrada: a tela SHALL apresentar o que ele
entregou e NEVER SHALL oferecer entregar de novo. (`RF-05-91`, `RF-05-93`, `RF-05-94`,
`RN-09-54`)

#### Scenario: O controle de entrega fica indisponível sem a comprovação

- **WHEN** o Guerreiro(a) abre o prático e ainda não preencheu a comprovação
- **THEN** o controle de declarar que cumpriu fica indisponível

#### Scenario: O envio do arquivo mostra o progresso

- **WHEN** o Guerreiro(a) envia a comprovação em vídeo
- **THEN** a tela apresenta o progresso do envio até concluir

#### Scenario: A rede cai no meio do envio

- **WHEN** a conexão cai durante o envio da comprovação
- **THEN** a tela diz o que houve e oferece retomar, sem perder a declaração nem o que já subiu

#### Scenario: A declaração em mídia sem arquivo recebe o arquivo

- **WHEN** o Guerreiro(a) volta a uma missão cujo prático aceita imagem, declarada sem arquivo,
  sem entrega no encontro e ainda não julgada
- **THEN** a tela diz que o arquivo não chegou, oferece enviá-lo e, concluído o envio, apresenta
  que o arquivo está guardado, sem nova declaração

#### Scenario: O Guerreiro(a) reencontra a comprovação entregue

- **WHEN** o Guerreiro(a) volta à missão depois de entregar e antes do julgamento
- **THEN** a tela apresenta a comprovação que ele entregou, e não um formulário vazio

#### Scenario: Recusado, a entrega reabre com o que ele já entregou à vista

- **WHEN** o Guerreiro(a) volta à missão depois de o Mestre ter julgado que ele não cumpriu
- **THEN** a tela apresenta a comprovação anterior e o controle de entregar de novo

#### Scenario: Cumprido, a tela não oferece entregar de novo

- **WHEN** o Guerreiro(a) volta à missão depois de o Mestre ter julgado que ele cumpriu
- **THEN** a tela apresenta o que ele entregou e nenhum controle de entrega é oferecido
