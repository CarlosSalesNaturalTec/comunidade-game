# Spec Delta

## ADDED Requirements

### Requirement: A sondagem da Área do Guerreiro(a) é respondida por voz com o áudio ligado

Na App 05, com o áudio ligado, a sondagem SHALL abrir a janela de escuta da capacidade
`sondagem-por-voz` depois de cada pergunta falada; com ele desligado, SHALL seguir por toque como
antes. (`RF-05-97`, `RF-05-98`, `RN-05-54`, `RF-05-72`)

#### Scenario: A sondagem fala, escuta e avança

- **WHEN** o Guerreiro(a) com o áudio ligado chega à sondagem na App 05
- **THEN** cada pergunta é falada, a janela de 5 segundos abre, e a resposta segue sozinha

#### Scenario: Com o áudio desligado nada muda

- **WHEN** o Guerreiro(a) com o áudio desligado chega à sondagem na App 05
- **THEN** a sondagem é respondida por toque, como antes desta change
