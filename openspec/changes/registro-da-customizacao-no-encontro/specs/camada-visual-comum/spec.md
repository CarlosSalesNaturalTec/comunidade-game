## ADDED Requirements

### Requirement: A camada comum entrega a situação e a ação da customização do kit

A camada comum SHALL entregar, para cada kit com customização aberta, a **situação do último
registro** do Guerreiro(a) — o mais recente do kit, pela data do registro — e a **ação que
cabe**, nos cenários abaixo. A App 05 e a App 01 SHALL consumir este mesmo bloco, e NEVER SHALL
decidir a situação ou a ação por conta própria. (`RF-05-103`, `RF-04-80`)

#### Scenario: Sem registro vivo, oferece registrar

- **WHEN** o kit não tem registro, ou o último foi cancelado ou expirou
- **THEN** o bloco oferece Registrar a customização

#### Scenario: Pendente sem mídia retoma o envio

- **WHEN** o último registro está pendente sem a mídia recebida
- **THEN** o bloco diz que falta a foto ou o vídeo, oferece o envio do mesmo registro e Cancelar

#### Scenario: Pendente com mídia aguarda a aula

- **WHEN** o último registro está pendente com a mídia recebida
- **THEN** o bloco diz que aguarda a aula e que expira no fim do ciclo, e oferece Cancelar

#### Scenario: Reprovado mostra o motivo

- **WHEN** o último registro foi reprovado
- **THEN** o bloco mostra o motivo do Mestre e oferece Enviar de novo

#### Scenario: Aprovado permite uma nova

- **WHEN** o último registro foi aprovado
- **THEN** o bloco diz que foi aprovado e oferece Registrar a customização para uma nova

#### Scenario: O último registro decide a ação

- **WHEN** o kit tem um registro reprovado e, depois dele, um pendente com a mídia recebida
- **THEN** o bloco mostra que aguarda a aula e oferece Cancelar, não Enviar de novo

#### Scenario: O mesmo kit mostra o mesmo nas duas aplicações

- **WHEN** um kit tem o mesmo último registro na App 05 e na App 01
- **THEN** as duas mostram a mesma situação e oferecem a mesma ação, com as mesmas palavras

#### Scenario: O cancelamento recusado aparece como vem

- **WHEN** o Guerreiro(a) cancela e o núcleo recusa
- **THEN** a recusa aparece em linguagem simples e a situação do kit é lida de novo
