# Spec Delta

## ADDED Requirements

### Requirement: O campo declarado como inicial recebe o foco quando a tela abre

A camada comum SHALL permitir que quem monta a tela declare **um** campo como inicial, e SHALL
dar o foco a ele quando a tela abre. A declaração SHALL ser **opcional**: o componente de campo
NEVER SHALL tomar o foco por conta própria, porque foco automático em tela que apresenta
conteúdo acima do campo faz quem navega por leitor de tela começar no meio, saltando o que veio
antes. (PRD-02 §10, documento 15 §5, decisão do fundador de 2026-09-25)

Receber o foco inicial NEVER SHALL dispensar o **contorno de foco visível** nem alterar o
rótulo, a mensagem de erro ou o estado de inválido do campo: o foco inicial é onde o percurso
começa, não uma forma diferente de campo. (documento 15 §5)

#### Scenario: O campo declarado abre focado

- **WHEN** uma tela é apresentada com um campo declarado como inicial
- **THEN** aquele campo está com o foco, e quem opera digita sem antes alcançá-lo

#### Scenario: Campo sem declaração não toma o foco

- **WHEN** uma tela é apresentada sem declarar campo inicial algum
- **THEN** nenhum campo toma o foco, e o percurso começa no início da tela

#### Scenario: O foco inicial continua visível

- **WHEN** o campo declarado como inicial recebe o foco
- **THEN** o contorno de foco é apresentado nele, como em qualquer campo alcançado pelo teclado

#### Scenario: O foco inicial não muda o anúncio do campo

- **WHEN** o campo declarado como inicial está com erro
- **THEN** o rótulo, a mensagem de erro e o estado de inválido são anunciados como em qualquer
  outro campo
