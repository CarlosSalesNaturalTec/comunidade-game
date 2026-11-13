## ADDED Requirements

### Requirement: A App 09 declara, opcional, o kit que o prático apresenta

Escolhido o tipo **desafio prático**, a tela SHALL oferecer ao Mestre autor a escolha
**opcional** do **kit apresentado**, entre as **recompensas de marco já declaradas na trilha**,
cada uma pelo **nome do tipo de recurso** e pela **missão do marco**, com a opção de **nenhum
kit**. A tela SHALL dizer, em linguagem do Mestre, que a comprovação aprovada vira o primeiro
registro daquele kit e abre a customização dele, e que é ele quem diz o que é kit — camisa e
livro não são. No **quiz** e na **sondagem** a escolha NEVER SHALL aparecer nem o campo ser
mandado ao núcleo. (`RF-09-141`)

#### Scenario: O Mestre autor escolhe o kit entre as recompensas da trilha

- **WHEN** o Mestre autor escolhe desafio prático numa trilha com recompensas de marco
  declaradas
- **THEN** a tela oferece cada recompensa pelo tipo de recurso e pela missão do marco, mais a
  opção de nenhum kit, e grava o prático com o kit escolhido

#### Scenario: O kit é opcional

- **WHEN** o Mestre autor grava o prático sem escolher kit
- **THEN** a tela grava o prático normalmente, com o kit nulo

#### Scenario: Trilha sem recompensa declarada aponta o caminho

- **WHEN** o Mestre autor escolhe desafio prático numa trilha sem recompensa de marco
  declarada
- **THEN** a tela diz que não há recompensa para escolher como kit e que ela se declara no
  bloco da recompensa pelo desbloqueio, e grava o prático sem kit

#### Scenario: O quiz não mostra nem manda o kit

- **WHEN** o Mestre autor troca o tipo do desafio de prático para quiz e grava
- **THEN** a escolha do kit sai da tela e o quiz vai ao núcleo sem o campo

### Requirement: A App 09 reabre o kit declarado e o reenvia a cada declaração

A tela SHALL **reabrir** o kit declarado toda vez que o Mestre autor volta à missão, em sessão
nova inclusive, pela mesma leitura que reabre os demais campos do prático, e SHALL **reenviá-lo**
em toda nova declaração do prático: como declarar de novo substitui o kit, inclusive por
nenhum, corrigir outro campo NEVER SHALL apagar o kit. O kit declarado SHALL ser apresentado
pelo nome que a leitura traz, mesmo quando a lista das recompensas da trilha não carregou.
O resumo recolhido do desafio prático SHALL dizer o kit declarado, quando houver. A recusa do
campo pelo núcleo SHALL ser mostrada no bloco do desafio, com o motivo, sem apagar o que o
Mestre escreveu nos outros campos. (`RF-09-141`)

#### Scenario: O Mestre autor volta à missão e encontra o kit

- **WHEN** o Mestre autor sai da trilha e volta à missão cujo prático declarou um kit
- **THEN** a escolha do kit abre na recompensa que ele declarou

#### Scenario: Corrigir o critério não apaga o kit

- **WHEN** o Mestre autor corrige o critério de aceite de um prático com kit declarado e grava
- **THEN** a declaração vai ao núcleo com o mesmo kit, e o kit segue declarado

#### Scenario: A recusa do kit chega com o motivo

- **WHEN** o núcleo recusa o kit escolhido por não ser recompensa de marco da trilha
- **THEN** a tela mostra o motivo no bloco do desafio, e os demais campos seguem como o Mestre
  os escreveu
