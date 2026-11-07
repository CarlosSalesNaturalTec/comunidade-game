# Spec Delta

## ADDED Requirements

### Requirement: A camada avisa quando a fala termina

A tela que pede uma fala SHALL poder saber quando ela **termina** de ser dita, para que a sondagem
abra a escuta só depois da pergunta falada. Fala cancelada, ou que não chegou a ser dita por
falta de voz, NEVER SHALL ser dada como terminada para quem a pediu. (`RF-05-97`,
`RF-04-77`)

#### Scenario: Fim da fala é avisado

- **WHEN** a narração termina de falar o texto que uma tela pediu
- **THEN** a tela que pediu é avisada do fim

#### Scenario: Fala cancelada não abre a escuta

- **WHEN** a fala é cancelada por troca de tela ou de pergunta
- **THEN** a tela não recebe aviso de fim daquela fala

### Requirement: Ligar o áudio pede a permissão do microfone

Onde a transcrição de fala existe, o toque que **liga** o áudio SHALL pedir a permissão do
microfone ao navegador, e o pedido NEVER SHALL manter o microfone aberto. Negada a permissão, a
narração SHALL seguir ligada e funcionando, sem alarme. (`RN-05-54`, `RF-05-97`)

#### Scenario: Ligar o áudio pede o microfone

- **WHEN** a pessoa liga o áudio num navegador com transcrição de fala
- **THEN** o navegador pede a permissão do microfone, e nada é captado nesse momento

#### Scenario: Microfone negado não desliga a narração

- **WHEN** a permissão do microfone é negada
- **THEN** a narração segue ligada, e nenhuma mensagem de erro aparece

#### Scenario: Sem voz, não há aviso de fim

- **WHEN** a narração está ligada mas o aparelho não tem voz que sirva
- **THEN** nada é falado e a tela não recebe aviso de fim, e a sondagem segue por toque
