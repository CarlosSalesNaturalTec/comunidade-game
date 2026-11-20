## MODIFIED Requirements

### Requirement: A aplicação apresenta ao Mestre as suas turmas, separadas por formato

A App 09 SHALL apresentar ao Mestre em sessão a área **Minhas turmas**, com as aulas das
comunidades dele e as atividades **on-line** de que é autor. As atividades **presenciais** NEVER
SHALL ter seção própria na área: elas aparecem dentro da aula, no atalho de lançamento da tela
da aula (decisão do fundador de 2026-11-20). A área NEVER SHALL exibir turma de outra
comunidade nem atividade de outro Mestre.
A aula de situação **cancelada** NEVER SHALL ser listada: não há encontro, presença nem
ocorrência a lançar nela, e o núcleo já não a devolve (decisão do fundador de 2026-11-16 e de
2026-11-20).

Nenhuma tela desta área SHALL exibir imagem real de Guerreiro(a): o Guerreiro(a) aparece por
**nick e avatar** (`RN-09-18`). (`RF-09-42`, `RF-09-73`, `RN-09-08`)

#### Scenario: A área lista as turmas do Mestre em sessão

- **WHEN** o Mestre abre Minhas turmas
- **THEN** a aplicação lista as aulas das comunidades dele e as atividades on-line de que é autor

#### Scenario: As atividades presenciais e on-line aparecem separadas

- **WHEN** o Mestre abre Minhas turmas e é autor de atividades presenciais
- **THEN** a área não apresenta seção de atividades presenciais, e elas seguem oferecidas para
  lançamento na tela da aula

#### Scenario: A área não exibe imagem real de criança

- **WHEN** a aplicação apresenta os Guerreiros e Guerreiras de uma turma
- **THEN** cada um aparece por nick e avatar, e nenhuma imagem real é exibida

#### Scenario: Aula cancelada não aparece na lista

- **WHEN** o Mestre abre Minhas turmas e uma das aulas das comunidades dele está cancelada
- **THEN** a lista de aulas traz as demais e não traz a cancelada

#### Scenario: Só aulas canceladas dão lista vazia

- **WHEN** todas as aulas das comunidades do Mestre estão canceladas
- **THEN** a área apresenta a mesma mensagem de nenhuma aula agendada

### Requirement: O Mestre confirma a presença e lança a ocorrência de conduta

A App 09 SHALL apresentar, na tela da aula aberta pelo botão **Presença e ocorrência**, a lista
dos **presentes nesta aula** — os Guerreiros e Guerreiras com presença registrada e não
anulada, cada um por **nick e avatar desenhado**, com a **hora** e o **modo** da comprovação
(reconhecimento ou confirmação). Aula sem presença SHALL apresentar mensagem de lista vazia; a
falha da leitura SHALL ser dita em linguagem simples sem impedir os formulários da tela
(`RF-09-145`, `RN-09-18`).

A App 09 SHALL permitir ao Mestre **confirmar a presença** de um Guerreiro(a) no encontro dele,
suprindo o que não foi capturado — a presença confirmada SHALL passar a aparecer na lista dos
presentes —, e **lançar a ocorrência de conduta** escolhendo a atividade e escrevendo o motivo
em texto livre.

A tela da ocorrência NEVER SHALL pedir o **valor** do débito — ele é fixo na tabela do
documento 11 §5 — nem item de catálogo do Código de Conduta. Ela SHALL deixar claro que o
lançamento vale **no ato**, sem revisão de outro Admin (`RN-09-09`), e SHALL apresentar em
linguagem simples a recusa por teto da aula alcançado. (`RF-09-45`, `RF-09-46`, `RF-09-145`,
`RN-09-09`, `RN-09-18`)

#### Scenario: A tela da aula lista os presentes

- **WHEN** o Mestre abre Presença e ocorrência de uma aula com presenças registradas
- **THEN** a aplicação lista cada presente por nick e avatar desenhado, com a hora e o modo

#### Scenario: Aula sem presença diz que a lista está vazia

- **WHEN** o Mestre abre Presença e ocorrência de uma aula sem presença registrada
- **THEN** a aplicação diz que nenhuma presença foi registrada nesta aula

#### Scenario: A falha da leitura não trava a tela

- **WHEN** a leitura das presenças falha
- **THEN** a aplicação diz em linguagem simples que não conseguiu carregar os presentes, e os
  formulários de presença e ocorrência seguem disponíveis

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
