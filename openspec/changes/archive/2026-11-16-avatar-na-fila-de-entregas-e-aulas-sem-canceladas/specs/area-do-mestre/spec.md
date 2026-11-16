## MODIFIED Requirements

### Requirement: A aplicação apresenta ao Mestre as suas turmas, separadas por formato

A App 09 SHALL apresentar ao Mestre em sessão a área **Minhas turmas**, com as aulas das
comunidades dele e as atividades de que é autor, **separadas pelo formato** — as presenciais do
encontro e as on-line entre encontros. A área NEVER SHALL exibir turma de outra comunidade nem
atividade de outro Mestre.
A aula de situação **cancelada** NEVER SHALL ser listada: não há encontro, presença nem
ocorrência a lançar nela (decisão do fundador de 2026-11-16).

Nenhuma tela desta área SHALL exibir imagem real de Guerreiro(a): o Guerreiro(a) aparece por
**nick e avatar** (`RN-09-18`). (`RF-09-42`, `RF-09-73`, `RN-09-08`)

#### Scenario: A área lista as turmas do Mestre em sessão

- **WHEN** o Mestre abre Minhas turmas
- **THEN** a aplicação lista as aulas das comunidades dele com as atividades de que é autor

#### Scenario: As atividades presenciais e on-line aparecem separadas

- **WHEN** a turma tem atividades dos dois formatos
- **THEN** a aplicação as apresenta separadas, presenciais de um lado e on-line do outro

#### Scenario: A área não exibe imagem real de criança

- **WHEN** a aplicação apresenta os Guerreiros e Guerreiras de uma turma
- **THEN** cada um aparece por nick e avatar, e nenhuma imagem real é exibida

#### Scenario: Aula cancelada não aparece na lista

- **WHEN** o Mestre abre Minhas turmas e uma das aulas das comunidades dele está cancelada
- **THEN** a lista de aulas traz as demais e não traz a cancelada

#### Scenario: Só aulas canceladas dão lista vazia

- **WHEN** todas as aulas das comunidades do Mestre estão canceladas
- **THEN** a área apresenta a mesma mensagem de nenhuma aula agendada
