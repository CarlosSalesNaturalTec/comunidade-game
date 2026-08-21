## ADDED Requirements

### Requirement: A gestão lê a agenda, filtrada por comunidade e por período

O núcleo SHALL devolver as aulas com **comunidade**, **ponto de apoio**, **data**, **horário
inicial**, **horário final**, **situação** e, quando cancelada, o **motivo do cancelamento**. A
leitura SHALL ser paginada e SHALL aceitar filtro por **comunidade** e por **período**.

A leitura SHALL exigir persona de gestão em sessão: o **Admin** SHALL ler todas as comunidades e
o **Mestre**, apenas as comunidades a que está vinculado. **Apoiador**, **Guerreiro(a)** e
**responsável** SHALL receber **403**.

A aula **pendente de lastro** SHALL sair com a situação que a distingue da confirmada, sem que a
leitura altere situação alguma. (`RF-02-12`, `RF-01-28`, `RF-01-18`, `RF-01-16`, `RN-02-09`,
PRD-02 §9)

#### Scenario: Admin lê a agenda das comunidades

- **WHEN** um Admin em sessão consulta a agenda
- **THEN** vêm as aulas com comunidade, ponto de apoio, data, horários e situação

#### Scenario: Mestre lê apenas a agenda das suas comunidades

- **WHEN** um Mestre vinculado a uma comunidade consulta a agenda
- **THEN** vêm apenas as aulas daquela comunidade

#### Scenario: Apoiador não lê a agenda da gestão

- **WHEN** um Apoiador em sessão consulta a agenda
- **THEN** o núcleo responde 403

#### Scenario: A agenda distingue a aula pendente de lastro

- **WHEN** a agenda traz uma aula pendente de lastro e outra confirmada
- **THEN** cada uma sai com a sua situação, e nenhuma delas muda por ter sido lida

#### Scenario: Filtro de período recorta a agenda

- **WHEN** a consulta declara um período
- **THEN** vêm apenas as aulas cujo horário inicial cai dentro dele

### Requirement: As aulas vigentes são lidas pela aplicação que abre, sem persona em sessão

O núcleo SHALL expor as **aulas vigentes** — as já derivadas pela capacidade, sem parâmetro de
liberação separado — em rota que exige **chave de aplicação** e NEVER SHALL exigir credencial de
persona: a consulta acontece antes de qualquer pessoa se identificar. A saída SHALL trazer, de
cada aula vigente, ao menos a **comunidade**, para que a aplicação que abre saiba em qual está
operando.

Não havendo aula vigente, o núcleo SHALL responder **200 com conjunto vazio** — é o que faz o
App 01 não abrir, e NEVER SHALL ser tratado como erro. (`RF-02-14`, `RF-02-13`, `RF-01-32`,
`RF-01-02`, `RN-02-05`, PRD-02 §§9, 12)

#### Scenario: Aplicação sem persona lê as vigentes

- **WHEN** uma aplicação com chave válida e sem nenhuma persona em sessão consulta as aulas
  vigentes
- **THEN** o núcleo responde com as aulas vigentes daquele momento

#### Scenario: Fora de qualquer janela a lista volta vazia

- **WHEN** o momento corrente não está dentro da janela de nenhuma aula agendada
- **THEN** o núcleo responde 200 com conjunto vazio, e não um erro

#### Scenario: Duas comunidades no mesmo horário chegam ambas a quem abre

- **WHEN** duas aulas de comunidades diferentes estão vigentes no mesmo momento
- **THEN** as duas saem na consulta, cada uma com a sua comunidade, sem que o núcleo escolha

#### Scenario: Consulta sem chave é recusada

- **WHEN** a consulta das aulas vigentes chega sem chave de aplicação válida
- **THEN** o núcleo recusa a chamada, como em qualquer rota de dados
