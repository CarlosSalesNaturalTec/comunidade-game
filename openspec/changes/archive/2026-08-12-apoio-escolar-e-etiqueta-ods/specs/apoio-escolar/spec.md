## Purpose

O apoio escolar é o corpus fechado que o assistente de voz da App 05 e da App 01 vai consultar —
sem disciplina e conteúdo cadastrados, não há sobre o que responder.

## ADDED Requirements

### Requirement: Disciplina é catálogo aberto, único por nome normalizado

O núcleo SHALL manter a **disciplina** como catálogo aberto: **qualquer Mestre** cadastra, sem
restrição de posse — é taxonomia compartilhada, não conteúdo pessoal. O **nome** SHALL ser
normalizado antes de gravar, no mesmo padrão da natureza da atividade, e disciplina com o mesmo
nome normalizado de uma já existente SHALL ser recusada com **422**. Disciplina sem nome SHALL
ser recusada com **422**. (`RF-01-35`, `RF-01-03`, `RF-01-16`, 03 §7)

#### Scenario: Mestre cadastra disciplina nova

- **WHEN** um Mestre em sessão cadastra uma disciplina com nome
- **THEN** o núcleo grava a disciplina com autoria, data e hora com fuso

#### Scenario: Disciplina duplicada é recusada

- **WHEN** chega uma disciplina cujo nome normalizado já existe no catálogo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Disciplina sem nome é recusada

- **WHEN** chega uma disciplina sem nome
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Quem não é Mestre nem Admin é recusado

- **WHEN** uma persona sem a operação `suas_trilhas_e_conteudos` nem `tudo` tenta cadastrar
  disciplina
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: Conteúdo do corpus pertence a uma disciplina e tem Mestre autor

O núcleo SHALL manter o **conteúdo do corpus** pertencente a **exatamente uma** disciplina, com
o **material** e o **Mestre autor** que o escreveu. Conteúdo sem disciplina SHALL ser recusado
com **422**. Só o **Mestre autor** do conteúdo altera o próprio conteúdo; outro Mestre SHALL
receber **403**, ainda que o papel dele permita escrever conteúdo em geral — a mesma posse já
aplicada à trilha, à missão e à atividade. (`RF-01-35`, `RF-01-16`, `RF-01-03`, 03 §7)

#### Scenario: Mestre autor cadastra conteúdo em uma disciplina

- **WHEN** o Mestre em sessão cadastra um conteúdo informando a disciplina e o material
- **THEN** o núcleo grava o conteúdo com aquele Mestre como autor, com data e hora com fuso

#### Scenario: Conteúdo sem disciplina é recusado

- **WHEN** chega um conteúdo sem disciplina vinculada
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Mestre que não é o autor é recusado

- **WHEN** um Mestre que não é o autor do conteúdo tenta alterá-lo
- **THEN** o núcleo responde 403 e o conteúdo permanece como estava

### Requirement: Admin despublica conteúdo com motivo, sem precisar ser o autor

O núcleo SHALL permitir que **Admin** despublique qualquer conteúdo do corpus, registrando
**motivo**, **quem despublicou** e **quando** — a mesma auditoria por amostragem que o Admin já
exerce sobre a trilha, sem precisar da posse do Mestre autor. Despublicação sem motivo SHALL ser
recusada com **422**. Conteúdo despublicado SHALL permanecer gravado, com a autoria original
intacta. (`RF-01-35`, `RF-01-16`, 03 §7)

#### Scenario: Admin despublica conteúdo de qualquer Mestre

- **WHEN** um Admin despublica, com motivo, um conteúdo de que não é autor
- **THEN** o núcleo grava a despublicação, quem despublicou e quando, mantendo a autoria original

#### Scenario: Despublicação sem motivo é recusada

- **WHEN** chega uma despublicação sem motivo
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado
