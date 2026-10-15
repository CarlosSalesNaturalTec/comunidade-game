# Spec Delta

## ADDED Requirements

### Requirement: A camada comum entrega o botão de alternância só de ícone

A camada comum SHALL entregar um botão de **alternância** apresentado apenas pelo glifo, para o
controle que liga e desliga uma coisa só. SHALL exigir de quem o monta um **rótulo acessível** e
SHALL anunciar o estado de **pressionado**, cumprindo o alvo de toque da camada. NEVER SHALL
aceitar ser montado sem rótulo. (documento 15 §§5, 11.1)

#### Scenario: O rótulo é obrigatório e alcança o leitor de tela

- **WHEN** uma aplicação monta o botão de alternância só de ícone
- **THEN** o rótulo declarado por ela é o nome do botão para quem navega por leitor de tela, e
  nenhuma descrição do desenho é anunciada

#### Scenario: O estado é anunciado, não deduzido da cor

- **WHEN** o botão está ligado e depois desligado
- **THEN** o estado de pressionado muda junto, e quem não distingue cor reconhece cada estado

#### Scenario: O alvo de toque é o mesmo dos demais botões

- **WHEN** o botão de alternância só de ícone é apresentado
- **THEN** ele cumpre o alvo de toque que a camada garante a todo elemento acionável, e mostra o
  foco

### Requirement: O glifo distingue os dois estados de um alternador pela forma

Servindo o sistema de ícone a um **alternador**, a camada comum SHALL oferecer um glifo para
cada estado, distintos pela **forma**, e NEVER SHALL pedir que a mesma forma mude só de cor para
dizer o estado. (documento 15 §§5, 11.1)

#### Scenario: Ligado e desligado têm desenhos diferentes

- **WHEN** o alternador é apresentado ligado e depois desligado
- **THEN** o glifo de cada estado é um desenho diferente do outro, reconhecível sem cor
