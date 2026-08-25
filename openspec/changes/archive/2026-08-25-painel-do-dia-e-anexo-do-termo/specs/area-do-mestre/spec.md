## ADDED Requirements

### Requirement: Minhas turmas leva o Mestre ao painel do dia da sua aula

A App 09 SHALL oferecer, em **Minhas turmas**, o caminho para o **painel do dia** da aula do
Mestre. O painel é operado na **App 03** (`RN-02-20`), e a App 09 NEVER SHALL reconstruí-lo:
ela apenas leva o Mestre até lá, na aula que ele abriu.

O caminho SHALL aparecer apenas na aula **em andamento** — aquela cuja janela de data e horários
contém o instante da consulta. Aula futura, já realizada ou cancelada NEVER SHALL oferecê-lo,
porque não há encontro a acompanhar. (`RF-09-50`, `RF-09-42`, `RN-02-20`, PRD-09 §6.6)

#### Scenario: A aula em andamento oferece o caminho do painel

- **WHEN** o Mestre abre Minhas turmas durante a janela de uma aula dele
- **THEN** aquela aula apresenta o caminho para o painel do dia dela, na App 03

#### Scenario: Aula fora da janela não oferece o caminho

- **WHEN** a turma listada é de uma aula futura ou já realizada
- **THEN** o caminho para o painel do dia não é oferecido naquela aula

#### Scenario: A App 09 não reconstrói o painel

- **WHEN** o Mestre segue o caminho do painel do dia
- **THEN** ele chega ao painel operado na App 03, e a App 09 não apresenta cópia própria dele
