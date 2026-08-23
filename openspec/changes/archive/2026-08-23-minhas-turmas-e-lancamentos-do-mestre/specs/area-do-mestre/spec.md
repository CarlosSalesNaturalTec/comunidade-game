## ADDED Requirements

### Requirement: A aplicação apresenta ao Mestre as suas turmas, separadas por formato

A App 09 SHALL apresentar ao Mestre em sessão a área **Minhas turmas**, com as aulas das
comunidades dele e as atividades de que é autor, **separadas pelo formato** — as presenciais do
encontro e as on-line entre encontros. A área NEVER SHALL exibir turma de outra comunidade nem
atividade de outro Mestre.

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

### Requirement: O Mestre lança a atividade que propôs pela aplicação

A App 09 SHALL permitir ao Mestre lançar uma atividade sua, escolhendo a aula, os participantes
e o **desfecho** de cada um entre os três valores — realizada, com mérito ou mérito extra por
auxílio aos colegas. A tela SHALL permitir lançar **vários participantes de uma vez**, o que
serve a equipe inteira sem repetir o lançamento por integrante.

Recusa do núcleo SHALL ser apresentada em **linguagem simples, sem jargão de TI**
(`RN-09-16`). (`RF-09-43`, `RF-09-44`, `RF-09-74`, `RF-09-49`)

#### Scenario: O Mestre lança a equipe inteira num envio

- **WHEN** o Mestre seleciona os integrantes de uma equipe e atribui o desfecho de cada um
- **THEN** a aplicação envia o lançamento num só ato e confirma o registro dos participantes

#### Scenario: A recusa chega em linguagem simples

- **WHEN** o núcleo recusa o lançamento
- **THEN** a aplicação mostra o que impediu em linguagem simples, sem código nem jargão

### Requirement: O Mestre confirma a presença e lança a ocorrência de conduta

A App 09 SHALL permitir ao Mestre **confirmar a presença** de um Guerreiro(a) no encontro dele,
suprindo o que não foi capturado, e **lançar a ocorrência de conduta** escolhendo a atividade e
escrevendo o motivo em texto livre.

A tela da ocorrência NEVER SHALL pedir o **valor** do débito — ele é fixo na tabela do
documento 11 §5 — nem item de catálogo do Código de Conduta. Ela SHALL deixar claro que o
lançamento vale **no ato**, sem revisão de outro Admin (`RN-09-09`), e SHALL apresentar em
linguagem simples a recusa por teto da aula alcançado. (`RF-09-45`, `RF-09-46`, `RN-09-09`)

#### Scenario: O Mestre confirma a presença que faltou

- **WHEN** o Mestre confirma a presença de um Guerreiro(a) da turma dele
- **THEN** a aplicação registra a presença por confirmação e a mostra na lista do encontro

#### Scenario: O Mestre lança a ocorrência sem arbitrar valor

- **WHEN** o Mestre lança uma ocorrência de conduta escolhendo a atividade e escrevendo o motivo
- **THEN** a aplicação a registra sem pedir valor algum e confirma que o lançamento já está
  efetivado

#### Scenario: A ocorrência exige o motivo

- **WHEN** o Mestre tenta lançar a ocorrência sem escrever o motivo
- **THEN** a aplicação impede o envio e diz que o motivo é obrigatório

#### Scenario: O teto da aula é explicado em linguagem simples

- **WHEN** o núcleo recusa a ocorrência porque o Guerreiro(a) já alcançou o teto da aula
- **THEN** a aplicação diz que o limite daquele encontro foi alcançado, sem código nem jargão
