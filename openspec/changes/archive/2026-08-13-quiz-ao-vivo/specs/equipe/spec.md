## MODIFIED Requirements

### Requirement: O Guerreiro(a) integra mais de uma equipe da mesma aula

O núcleo SHALL aceitar o mesmo Guerreiro(a) em **mais de uma** equipe da mesma aula. Na
**partida de quiz**, porém, ele SHALL disputar por **uma única** das equipes: a abertura de
partida que o traga em duas ou mais das equipes disputantes SHALL ser recusada com **422**.
(`RF-01-39`, documento 02 §5, documento 03 §4.1)

#### Scenario: Mesmo Guerreiro(a) em duas equipes da aula

- **WHEN** um Guerreiro(a) que já integra uma equipe da aula entra em outra equipe da mesma
  aula
- **THEN** o núcleo grava a entrada e ele passa a integrar as duas

#### Scenario: As duas equipes não disputam a mesma partida

- **WHEN** alguém tenta abrir uma partida de quiz entre duas equipes da aula que compartilham
  um integrante
- **THEN** o núcleo responde 422 e nenhuma partida é aberta

#### Scenario: Cada equipe do Guerreiro(a) disputa uma partida diferente

- **WHEN** um Guerreiro(a) integra duas equipes da aula e cada uma disputa uma partida
  diferente
- **THEN** o núcleo aceita as duas partidas, porque em nenhuma delas ele aparece duas vezes
