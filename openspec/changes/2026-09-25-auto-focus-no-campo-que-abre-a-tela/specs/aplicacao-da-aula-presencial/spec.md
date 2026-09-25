# Spec Delta

## ADDED Requirements

### Requirement: A tela de propósito único abre com o campo que ela existe para preencher focado

A App 01 SHALL declarar como campo inicial, nas telas cujo propósito é preencher um campo, aquele
campo — para que o atendimento comece na digitação, e não em alcançar o campo. O encontro
recomeça a cada Guerreiro(a) que chega (`RF-04-28`), e o gesto se paga em toda chegada.

As telas e os campos SHALL ser:

| Tela                                          | Campo inicial       | Origem                 |
| --------------------------------------------- | ------------------- | ---------------------- |
| Cadastro do onboarding                        | nome                | `RF-04-07`             |
| Entrada do Guerreiro(a) por nick e imagem     | nick                | `RF-04-18`, `RF-04-29` |
| Entrada do Guerreiro(a) por confirmação       | nick                | `RF-04-21`             |
| Formação da equipe da aula                    | nome da equipe      | `RF-04-30`, `RF-04-69` |
| Troca do nome da equipe                       | nome novo           | `RF-04-70`             |
| Equipe da trilha                              | nick do integrante  | `RF-04-61`             |
| Cadastro do responsável mínimo                | nome do responsável | `RF-04-60`             |

A aplicação NEVER SHALL declarar como inicial **mais de um campo** da mesma tela, e NEVER SHALL
declarar os campos **seguintes** — nick e data de nascimento no cadastro, papel na equipe, PIN na
confirmação. Eles são alcançados pelo percurso a partir do primeiro, e disputar o foco tiraria a
pessoa de onde ela está. Em particular, o **PIN** NEVER SHALL tomar o foco da tela de
confirmação: o nick é o primeiro dado do ato (`RF-04-21`).

O foco inicial NEVER SHALL alterar validação, rótulo, recusa ou qualquer desfecho das telas
alcançadas.

#### Scenario: A entrada do Guerreiro(a) abre com o nick focado

- **WHEN** a entrada do Guerreiro(a) é aberta por qualquer um dos quatro caminhos — presença,
  equipes, quiz ou troca
- **THEN** o campo do nick está com o foco

#### Scenario: A confirmação por PIN também começa no nick

- **WHEN** a tela de confirmação de Mestre ou Admin é apresentada
- **THEN** o campo do nick está com o foco, e o campo do PIN não

#### Scenario: O cadastro do onboarding abre com o nome focado

- **WHEN** a tela de cadastro do onboarding é apresentada
- **THEN** o campo do nome está com o foco, e os campos seguintes não

#### Scenario: A formação da equipe abre com o nome da equipe focado

- **WHEN** a tela das equipes da aula é apresentada
- **THEN** o campo do nome da equipe está com o foco, e o campo do papel não

#### Scenario: O foco inicial não muda o que a tela faz

- **WHEN** uma dessas telas é usada até o desfecho
- **THEN** a validação, as recusas e o desfecho são os mesmos de antes do foco inicial
