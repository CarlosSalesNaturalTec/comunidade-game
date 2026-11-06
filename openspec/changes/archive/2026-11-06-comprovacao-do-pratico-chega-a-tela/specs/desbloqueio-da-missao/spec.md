## MODIFIED Requirements

### Requirement: A leitura do desafio prático traz os três campos declarados

Toda leitura que já serve o **desafio de desbloqueio** SHALL trazer, no prático, a **forma de
comprovação aceita**, o **critério de aceite** e o **título curto**, ao lado do enunciado que
ela já serve: a das trilhas do Mestre autor, a resposta da própria declaração e a do percurso
do Guerreiro(a) inscrito.
Nenhum dos três é segredo do Mestre — é deles que o Guerreiro(a) sabe o que entregar e sob que
critério será julgado. No quiz os três SHALL vir **nulos**. (`RF-09-129` a `RF-09-131`)

Na leitura do percurso e na resposta da declaração, os três SHALL vir dentro de
`desafio_de_desbloqueio` como `forma_de_comprovacao`, `criterio_de_aceite` e `titulo_curto`, e
toda tela do Guerreiro(a) SHALL lê-los por esses nomes. O contrato SHALL ser conferido por
teste dos dois lados contra o **mesmo exemplo** de resposta, de modo que nome divergente entre
núcleo e tela quebre a suíte. (`RF-05-91`, `RF-04-76`)

#### Scenario: O Mestre autor reencontra o que declarou

- **WHEN** o Mestre autor lê as trilhas dele depois de declarar o prático de uma missão
- **THEN** a missão traz o tipo, o enunciado, a forma aceita, o critério de aceite e o título
  curto, como ele os declarou

#### Scenario: O Guerreiro(a) inscrito lê a forma e o critério

- **WHEN** o Guerreiro(a) inscrito na trilha lê a missão cujo desbloqueio é prático
- **THEN** o desafio vem com a forma de comprovação aceita e o critério de aceite

#### Scenario: No quiz os três campos vêm nulos

- **WHEN** alguém lê uma missão cujo desbloqueio é quiz
- **THEN** a forma de comprovação, o critério de aceite e o título curto vêm nulos

#### Scenario: Nome divergente entre núcleo e tela quebra a suíte

- **WHEN** a resposta do percurso deixa de trazer um campo com o nome do exemplo de contrato
- **THEN** o teste do núcleo falha; e quando a tela lê um nome que o exemplo não traz, o teste
  da tela falha
