# Spec Delta

## ADDED Requirements

### Requirement: O Mestre tem vínculo próprio com a Comunidade Virtual

O núcleo SHALL manter o vínculo do **Mestre** com a Comunidade Virtual como **entidade
própria**, separada do vínculo do Guerreiro(a). Um Mestre SHALL poder estar vinculado a
**uma ou mais** comunidades. O núcleo NEVER SHALL usar o vínculo do Guerreiro(a) para
recortar o alcance de um Mestre, e NEVER SHALL aceitar Mestre no vínculo do Guerreiro(a).
(`RN-08-02`, `RN-01-05`, documento 09 §1 — decisão do fundador de 2026-10-30)

#### Scenario: O Mestre é vinculado a mais de uma comunidade

- **WHEN** um Mestre é escalado em aulas de duas comunidades distintas
- **THEN** ele fica vinculado às duas, e as leituras de gestão dele alcançam ambas

#### Scenario: O vínculo do Guerreiro(a) recusa Mestre

- **WHEN** se tenta abrir vínculo de Guerreiro(a) para uma persona de papel Mestre
- **THEN** o núcleo recusa com **422**, e o vínculo do Mestre é o da entidade própria

#### Scenario: Mestre sem vínculo algum lê vazio, nunca erro

- **WHEN** um Mestre ainda não escalado em aula alguma consulta uma leitura de gestão
- **THEN** o núcleo responde **200** com lista vazia, e NEVER com erro

### Requirement: O vínculo do Mestre não encerra no Ciclo 01

O vínculo do Mestre com a comunidade NEVER SHALL ter data de fim no Ciclo 01: aberto, ele
permanece. O núcleo NEVER SHALL expor rota que encerre o vínculo de um Mestre, e o
**cancelamento** de uma aula NEVER SHALL encerrá-lo — nem quando for a única aula daquele
Mestre naquela comunidade. (documento 09 §1 — decisão do fundador de 2026-10-30)

#### Scenario: Aula cancelada não desfaz o vínculo

- **WHEN** a única aula que vinculou um Mestre a uma comunidade é cancelada
- **THEN** o vínculo dele com aquela comunidade permanece, e as leituras dele seguem
  alcançando-a

#### Scenario: Não há rota que encerre o vínculo do Mestre

- **WHEN** se procura caminho de desvincular um Mestre de uma comunidade
- **THEN** não existe rota alguma que o faça, em nenhum papel

### Requirement: O vínculo do Mestre é aberto pelo agendamento da aula

O núcleo SHALL abrir o vínculo do Mestre com a comunidade **no agendamento da aula**, para
cada Mestre nela escalado que ainda não esteja vinculado àquela comunidade. O Mestre NEVER
SHALL declarar a própria comunidade, e NEVER SHALL existir outro caminho que abra o vínculo.
É o mesmo ato de Admin que atribui a comunidade ao Guerreiro(a) (`RF-02-30`, `RF-01-20`,
invariante 4 do documento 99 §6)

#### Scenario: O agendamento abre o vínculo de cada Mestre escalado

- **WHEN** um Admin agenda aula numa comunidade escalando dois Mestres não vinculados a ela
- **THEN** o núcleo abre o vínculo dos dois com aquela comunidade

#### Scenario: Mestre já vinculado não ganha vínculo repetido

- **WHEN** um Admin agenda nova aula na mesma comunidade com um Mestre já vinculado a ela
- **THEN** o vínculo existente permanece, e nenhum segundo vínculo é aberto
