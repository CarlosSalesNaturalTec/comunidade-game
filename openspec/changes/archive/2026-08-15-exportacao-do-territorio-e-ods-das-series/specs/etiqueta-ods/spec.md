## MODIFIED Requirements

### Requirement: Cobertura de ODS agrega por trilha, poder e comunidade, nunca por Guerreiro(a)

O núcleo SHALL agregar a cobertura de ODS — o conjunto de objetivos distintos etiquetados — por
**trilha**, por **poder** (a união das etiquetas das trilhas vinculadas a ele), por
**comunidade** e por **ciclo**. A cobertura NEVER SHALL ser exposta nem calculada por
Guerreiro(a) individual. (`RF-01-42`, `RN-01-24`, 11 §2.1)

A cobertura **por comunidade** SHALL ter **duas fontes**, somadas em união:

1. as etiquetas das **trilhas** em que há Guerreiro(a) daquela comunidade com **Resultado
   registrado**;
2. as etiquetas dos **desafios de coleta** com **série aberta** por Guerreiro(a) daquela
   comunidade — a etiqueta que o desafio herdou da missão, ou da trilha.

A segunda fonte SHALL valer ainda que nenhuma trilha da comunidade tenha Resultado registrado:
a comunidade que só coletou cobre o objetivo do desafio que coletou. O estado da série NEVER
SHALL alterar a cobertura — série ativa, interrompida e encerrada contam igual, porque a
cobertura mede **alcance declarado**, não continuidade. (`RF-08-26`, `RF-08-25`, `RN-08-22`,
documento 04 §4)

O **ciclo** é o quarto eixo, exigido por `RF-01-42` e sem o qual `RF-01-43` não se cumpre. Ele
SHALL ser o **rótulo declarado na implantação**, não uma entidade com período: `Ciclo` não é
entidade em nenhum PRD, e o calendário do Ciclo 01 segue pendente no documento 09 §1. Toda
agregação SHALL carregar o rótulo do ciclo em que foi apurada. (`RF-01-42`, `RF-01-43`,
invariantes 13 e 20 do documento 99 §6)

#### Scenario: Cobertura por trilha soma os objetivos da trilha e das missões dela

- **WHEN** a trilha tem etiqueta de objetivo 4 e uma missão dela tem etiqueta de objetivo 13
- **THEN** a cobertura da trilha inclui os objetivos 4 e 13

#### Scenario: Cobertura por poder soma as trilhas vinculadas a ele

- **WHEN** duas trilhas do mesmo poder têm etiquetas de objetivos diferentes
- **THEN** a cobertura do poder inclui os dois objetivos

#### Scenario: Cobertura por comunidade soma as trilhas em curso na comunidade

- **WHEN** um Guerreiro(a) de uma comunidade tem Resultado registrado numa trilha etiquetada
- **THEN** a cobertura daquela comunidade inclui o objetivo da trilha

#### Scenario: Cobertura por comunidade soma os desafios de coleta com série aberta

- **WHEN** um Guerreiro(a) de uma comunidade abre série sobre um desafio de coleta cuja
  etiqueta herdada é o objetivo 11
- **THEN** a cobertura daquela comunidade inclui o objetivo 11

#### Scenario: Comunidade que só coletou cobre o objetivo do desafio

- **WHEN** uma comunidade não tem nenhum Resultado registrado e tem uma série aberta sobre
  desafio etiquetado
- **THEN** a cobertura daquela comunidade traz o objetivo do desafio, e não fica vazia

#### Scenario: O estado da série não altera a cobertura

- **WHEN** a única série de um desafio etiquetado na comunidade está interrompida ou encerrada
- **THEN** a cobertura daquela comunidade continua incluindo o objetivo do desafio

#### Scenario: Cobertura nunca é calculada por Guerreiro(a)

- **WHEN** se procura no núcleo uma função que agregue cobertura de ODS por Guerreiro(a)
- **THEN** nenhuma existe: as agregações são por trilha, poder, comunidade e ciclo

#### Scenario: Toda agregação carrega o rótulo do ciclo

- **WHEN** a cobertura é apurada por qualquer um dos eixos
- **THEN** o resultado carrega o rótulo do ciclo declarado na implantação
