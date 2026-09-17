## MODIFIED Requirements

### Requirement: A disponibilidade do App 01 é derivada da aula vigente no momento

O núcleo SHALL derivar as **aulas vigentes** como aquelas cuja data e cuja faixa entre o horário
inicial e o final **contêm o momento corrente** e cuja **situação não seja `cancelada`**, sem
nenhum outro parâmetro de liberação separado. Havendo aulas vigentes em comunidades diferentes
no mesmo momento, o núcleo SHALL devolver **todas** — a escolha é da aplicação que abre, nunca
do Guerreiro(a). Não havendo aula vigente, o núcleo SHALL devolver conjunto vazio. (`RF-01-32`,
`RF-01-18`, documento 09, "Comunidade do onboarding")

#### Scenario: Aula em curso é devolvida como vigente

- **WHEN** o momento corrente está entre o horário inicial e o final de uma aula daquela data
- **THEN** o núcleo devolve aquela aula entre as vigentes

#### Scenario: Aula fora do horário não é vigente

- **WHEN** o momento corrente é anterior ao horário inicial ou posterior ao final da aula
- **THEN** o núcleo não devolve aquela aula entre as vigentes

#### Scenario: Aula cancelada não é vigente

- **WHEN** o momento corrente está entre o horário inicial e o final de uma aula, mas ela foi
  cancelada
- **THEN** o núcleo não devolve aquela aula entre as vigentes

#### Scenario: Duas comunidades no mesmo horário devolvem duas aulas

- **WHEN** duas aulas de comunidades diferentes estão vigentes no mesmo momento
- **THEN** o núcleo devolve as duas, sem escolher uma delas

#### Scenario: Sem aula agendada não há operação

- **WHEN** nenhuma aula está vigente no momento corrente
- **THEN** o núcleo devolve conjunto vazio
