# comunidade-virtual Specification

## Purpose

A Comunidade Virtual é a representação digital da comunidade real em que o Guerreiro(a)
vive, criada por Admin e nascida vazia, e os vínculos que prendem as pessoas a ela: o do
Guerreiro(a), que é de **exatamente uma** e vem da aula agendada em que ele se cadastra, e o
do Mestre, que é de **uma ou mais**, vem do agendamento das aulas que ele ministra e não
encerra no Ciclo 01. O Admin não tem vínculo de comunidade.

## Requirements

### Requirement: Admin cria a Comunidade Virtual, que nasce vazia

O núcleo SHALL permitir que **apenas um Admin** crie a Comunidade Virtual, com **nome**,
**localização** e **granularidade máxima**. A comunidade recém-criada SHALL nascer vazia —
sem locais, sem séries e sem Guerreiros e Guerreiras — e o núcleo SHALL registrar o Admin
criador e a data de criação. Persona de qualquer outro papel que tente criar comunidade
SHALL receber **403**. (`RF-08-01`, `RN-08-01`, 02 §1)

#### Scenario: Comunidade recém-criada não tem nada dentro

- **WHEN** um Admin cria a Comunidade Virtual com nome, localização e granularidade máxima
- **THEN** o núcleo a grava com o Admin criador e a data, e a consulta a ela devolve nenhum
  local, nenhuma série e nenhum Guerreiro(a)

#### Scenario: Comunidade sem os atributos declarados é recusada

- **WHEN** chega uma criação de comunidade sem nome, sem localização ou sem granularidade
  máxima
- **THEN** o núcleo recusa com **422**, apontando o campo em falta

#### Scenario: Persona que não é Admin não cria comunidade

- **WHEN** um Mestre, um Guerreiro(a), um responsável ou um Apoiador tenta criar comunidade
- **THEN** o núcleo recusa com **403**, e nenhuma comunidade é criada

### Requirement: O vínculo do Guerreiro(a) é atribuído pela comunidade da aula agendada

O núcleo SHALL atribuir a comunidade do Guerreiro(a) a partir da **comunidade da aula
agendada** em que ele se cadastra. O Guerreiro(a) NEVER SHALL informar a própria comunidade,
e o núcleo NEVER SHALL aceitar comunidade declarada na criação da persona de Guerreiro(a).
Cadastro de Guerreiro(a) sem aula agendada que o origine SHALL ser recusado. (`RF-08-02`,
`RN-08-02`, documento 99 §6 invariante 4)

#### Scenario: O Guerreiro(a) aparece vinculado sem ter informado a comunidade

- **WHEN** um Guerreiro(a) é cadastrado no onboarding de uma aula agendada
- **THEN** o núcleo o vincula à comunidade daquela aula, sem que ele a tenha informado

#### Scenario: Comunidade declarada na criação é recusada

- **WHEN** chega uma criação de persona de Guerreiro(a) com a comunidade declarada no corpo
- **THEN** o núcleo recusa, porque a comunidade vem da aula e não de quem cadastra

### Requirement: O vínculo de comunidade é entidade com histórico e um só vigente

O núcleo SHALL manter o vínculo do Guerreiro(a) com a comunidade como **entidade própria**,
com **data de início**, **data de fim** e o **Admin responsável** pela mudança, de modo que
o histórico fique registrado. Cada Guerreiro(a) SHALL ter **exatamente um vínculo vigente** —
aquele sem data de fim — em qualquer momento, e o núcleo SHALL recusar a abertura de um
segundo vínculo vigente para o mesmo Guerreiro(a). (`RF-08-02`, `RN-08-02`, `RN-01-05`,
PRD-08 §§3.1, 8)

No Ciclo 01 **não há troca de comunidade**: o histórico existe no modelo, e o núcleo NEVER
SHALL expor rota que transfira Guerreiro(a) entre comunidades. A transferência é `RF-08-03`,
marcado fora do Ciclo 01. (documento 99 §6 invariante 4)

#### Scenario: Segundo vínculo vigente é recusado

- **WHEN** um segundo vínculo de comunidade vigente é pedido para o mesmo Guerreiro(a)
- **THEN** o núcleo recusa, e o vínculo existente permanece vigente

#### Scenario: O vínculo guarda o começo e fica sem fim enquanto vale

- **WHEN** o vínculo do Guerreiro(a) é criado pela aula em que ele se cadastra
- **THEN** o núcleo grava a data de início e deixa a data de fim vazia, e é esse o vínculo
  vigente

#### Scenario: Não existe rota de transferência no Ciclo 01

- **WHEN** se procura no núcleo uma rota que mova o Guerreiro(a) de uma comunidade para outra
- **THEN** nenhuma existe, e a tentativa devolve **404**

### Requirement: A gestão lê o vínculo vigente do Guerreiro(a), e nada além disso

O núcleo SHALL devolver, na **listagem de Guerreiros e Guerreiras restrita ao Admin**, o
**vínculo vigente** de cada um: a **comunidade** e a **data de início** do vínculo. É o que a
gestão precisa para **conferir** o que a aula agendada atribuiu, sem tela de transferência.
(`RF-02-15`, `RF-08-02`, `RN-02-06`)

Guerreiro(a) **sem vínculo vigente** SHALL sair com a comunidade e a data **vazias**, e a
ausência NEVER SHALL virar erro da listagem. A leitura NEVER SHALL devolver o **histórico** dos
vínculos encerrados — só o vigente —, e NEVER SHALL abrir caminho de escrita: continua não
existindo rota que mova o Guerreiro(a) de comunidade no Ciclo 01 (`RF-08-03`). Persona que não é
Admin SHALL receber **403**, como já recebe da listagem.

#### Scenario: A listagem traz a comunidade e a data de início

- **WHEN** um Admin em sessão consulta a listagem de Guerreiros e Guerreiras
- **THEN** cada Guerreiro(a) sai com a comunidade do vínculo vigente e a data de início dele

#### Scenario: Guerreiro(a) sem vínculo vigente sai com os campos vazios

- **WHEN** a listagem alcança um Guerreiro(a) que não tem vínculo vigente
- **THEN** ele sai com comunidade e data de início vazias, e a listagem responde normalmente

#### Scenario: O histórico encerrado não sai na listagem

- **WHEN** um Guerreiro(a) tem vínculo encerrado além do vigente
- **THEN** a listagem devolve apenas o vigente

#### Scenario: A leitura não abre caminho de troca

- **WHEN** se procura, a partir desta leitura, rota que troque a comunidade do Guerreiro(a)
- **THEN** nenhuma existe, e a tentativa devolve **404**

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
