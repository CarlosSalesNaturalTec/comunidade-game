## ADDED Requirements

### Requirement: A App 09 monta o desafio de desbloqueio da missão

A aplicação SHALL permitir ao **Mestre autor** montar o **desafio de desbloqueio** de cada
missão da trilha que ele autora, escolhendo entre **quiz** e **desafio prático**. A tela SHALL
dizer que é esse desafio que **abre a missão seguinte** para o Guerreiro(a). Missão que ainda
**não tem** desafio declarado SHALL ser sinalizada na bancada, sem impedir a publicação da
trilha. Trilha de outro Mestre NEVER SHALL ser oferecida para edição. (`RF-09-26`)

#### Scenario: O Mestre autor monta o desafio da sua missão

- **WHEN** o Mestre autor abre uma missão da sua trilha e monta o desafio de desbloqueio
- **THEN** a aplicação grava o desafio e a missão passa a exibi-lo

#### Scenario: A bancada sinaliza a missão sem desafio

- **WHEN** o Mestre autor abre uma trilha com missão que ainda não declarou desafio
- **THEN** a missão vem sinalizada como sem desafio, e a trilha segue publicável

#### Scenario: Trilha de outro Mestre não é editável

- **WHEN** o Mestre abre uma trilha de que não é autor
- **THEN** nenhuma ação de montar ou alterar o desafio de desbloqueio é oferecida

### Requirement: A App 09 mostra ao Mestre autor os desafios práticos a julgar

A aplicação SHALL listar ao **Mestre autor** os **desafios práticos declarados como cumpridos**
pelos Guerreiros e Guerreiras das suas trilhas e ainda **não julgados**, cada um com o
Guerreiro(a), a missão e quando foi declarado. O Mestre SHALL poder **julgar se passou** por
Guerreiro(a). A tela SHALL dizer que o julgamento **abre a missão seguinte** para aquele
Guerreiro(a) e que **não passar não o elimina**. Declaração de trilha de outro Mestre NEVER
SHALL aparecer nesta lista. (`RF-09-26`, `RF-05-13`, `RF-05-14`)

#### Scenario: A lista traz o que espera julgamento

- **WHEN** o Mestre autor abre a bancada dos desafios práticos
- **THEN** vê as declarações ainda não julgadas das suas trilhas, com Guerreiro(a), missão e
  data

#### Scenario: Julgar abre a missão seguinte para aquele Guerreiro(a)

- **WHEN** o Mestre autor julga que um Guerreiro(a) passou no desafio prático
- **THEN** a declaração sai da lista e a missão seguinte abre para aquele Guerreiro(a)

#### Scenario: Declaração de trilha alheia não aparece

- **WHEN** o Mestre abre a bancada dos desafios práticos
- **THEN** nenhuma declaração de trilha de que ele não é autor é listada
