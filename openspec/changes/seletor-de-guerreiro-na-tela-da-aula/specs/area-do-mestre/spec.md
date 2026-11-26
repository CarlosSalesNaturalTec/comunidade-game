# Spec Delta

## MODIFIED Requirements

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

Nos dois formulários, o Guerreiro(a) SHALL ser **escolhido pelo nick** numa lista dos
Guerreiros e Guerreiras ativos das comunidades do Mestre; NEVER SHALL ser pedido ao Mestre que
digite identificador técnico. No formulário de presença, quem já consta da lista de presentes
desta aula NEVER SHALL ser oferecido. Enviar sem escolher o Guerreiro(a) SHALL ser impedido
com mensagem em linguagem simples (`RF-09-45`, `RF-09-46`, `RN-09-18`).

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

- **WHEN** o Mestre escolhe pelo nick um Guerreiro(a) da turma dele e confirma a presença
- **THEN** a aplicação registra a presença por confirmação e a mostra na lista do encontro

#### Scenario: O Guerreiro(a) é escolhido pelo nick, nunca digitado

- **WHEN** o Mestre abre os formulários de presença e de ocorrência
- **THEN** cada um oferece a lista dos Guerreiros e Guerreiras pelo nick, sem campo de
  identificador para digitar

#### Scenario: Quem já está presente não é oferecido de novo

- **WHEN** o Mestre abre o formulário de presença de uma aula com presentes registrados
- **THEN** o seletor da presença não oferece quem já consta da lista de presentes

#### Scenario: Enviar sem escolher o Guerreiro(a) é impedido

- **WHEN** o Mestre tenta confirmar a presença ou lançar a ocorrência sem escolher o
  Guerreiro(a)
- **THEN** a aplicação impede o envio e diz que é preciso escolher o Guerreiro(a)

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
