## ADDED Requirements

### Requirement: O Mestre cadastra e troca o próprio PIN de confirmação na App 09

A App 09 SHALL oferecer ao **Mestre** em sessão, na área do perfil, uma tela para cadastrar ou
trocar o **próprio** PIN de confirmação, de 4 dígitos, digitado duas vezes e mascarado. A tela
SHALL dizer se o Mestre já tem PIN cadastrado — sem mostrá-lo — e para que ele serve: confirmar
a identidade de um Guerreiro(a) no App 01. PIN fora do formato ou com as duas digitações
diferentes SHALL ser recusado na própria tela, antes do envio. (`RF-09-121`, `RF-01-75`)

#### Scenario: O Mestre cadastra o PIN

- **WHEN** um Mestre digita duas vezes o mesmo PIN de 4 dígitos e confirma
- **THEN** a aplicação envia o PIN ao núcleo e diz que ele está cadastrado, sem mostrá-lo

#### Scenario: PIN fora do formato não sai da tela

- **WHEN** o Mestre digita três dígitos ou uma letra
- **THEN** a aplicação não envia nada e diz que o PIN tem 4 dígitos

#### Scenario: A tela diz se já há PIN

- **WHEN** um Mestre que já cadastrou o PIN abre a tela
- **THEN** a tela diz que há PIN cadastrado e oferece a troca, sem exibir o PIN
