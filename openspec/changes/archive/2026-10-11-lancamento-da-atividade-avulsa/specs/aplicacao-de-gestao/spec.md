# Spec Delta

## MODIFIED Requirements

### Requirement: A App 03 cadastra a atividade avulsa, fora de trilha

A App 03 SHALL oferecer ao **Admin** o cadastro da **atividade avulsa**, com **título**,
**descrição**, **modalidade**, **natureza**, **produção esperada**, o **poder** que ela
desenvolve, escolhido no catálogo de poderes da gestão, e a **aula** do encontro em que ela
acontece. A modalidade SHALL ser oferecida como escolha fechada nos valores do documento 11 §4;
o **formato** SHALL ser presencial, sem escolha, e a tela SHALL dizer em uma linha que a avulsa
acontece no encontro.

A escolha da aula SHALL começar pela **comunidade**, que estreita a lista às aulas dela; a
comunidade NEVER SHALL ser enviada ao núcleo, que a deriva da aula. Aula **cancelada** NEVER
SHALL ser oferecida.

A aplicação NEVER SHALL oferecer campo de **pontuação** — o valor vem do motor do documento 11
§5 — nem campo de **recurso**, que é declaração da aula. A aplicação NEVER SHALL oferecer ao
Admin o cadastro de atividade **de trilha**, que é autoria do Mestre na App 09, e SHALL
apresentar no próprio campo as recusas do núcleo. (`RF-02-29`, PRD-02 §3.2, documento 11 §§4, 5)

#### Scenario: Admin cadastra a atividade avulsa

- **WHEN** um Admin informa título, modalidade, natureza, produção esperada, o poder e a aula,
  e confirma
- **THEN** a atividade avulsa passa a existir e a aplicação a apresenta na lista

#### Scenario: A tela não oferece pontuação nem recurso

- **WHEN** o Admin abre o cadastro da atividade avulsa
- **THEN** não há campo de pontuação nem campo de tipo de recurso no formulário

#### Scenario: Cadastro sem poder é apontado no campo

- **WHEN** o Admin confirma o cadastro sem escolher o poder
- **THEN** a aplicação aponta a falta no próprio campo e nenhuma atividade passa a existir

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão alcança a área
- **THEN** o caminho de cadastro da atividade avulsa não lhe é oferecido

#### Scenario: A comunidade escolhida estreita as aulas

- **WHEN** o Admin escolhe uma comunidade no cadastro
- **THEN** a lista de aulas passa a trazer só as daquela comunidade, e nenhuma cancelada

#### Scenario: Cadastro sem aula é apontado no campo

- **WHEN** o Admin confirma o cadastro sem escolher a aula
- **THEN** a aplicação aponta a falta no próprio campo e nenhuma atividade passa a existir

#### Scenario: O formato não é escolha

- **WHEN** o Admin abre o cadastro da atividade avulsa
- **THEN** não há escolha de formato, e a tela diz em uma linha que a avulsa é do encontro

## ADDED Requirements

### Requirement: A área Lançamentos lança as atividades avulsas da aula vigente

A App 03 SHALL apresentar, na área **Lançamentos**, as **atividades avulsas** da aula vigente,
ao lado dos três atos que a área já reúne. Cada uma SHALL ser lançada em ato próprio, e a tela
SHALL dizer que esse lançamento NÃO converte reserva em baixa nem passa a aula a realizada —
é o lançamento da atividade da aula que faz as duas coisas. (`RF-02-112`, `RF-02-29`, PRD-02
§§5.6, 6.3)

#### Scenario: As avulsas da aula aparecem na área

- **WHEN** um Admin abre a área Lançamentos numa aula que tem duas atividades avulsas
- **THEN** a tela apresenta as duas, cada uma com o seu caminho de lançamento

#### Scenario: A tela diz o que o lançamento da avulsa não faz

- **WHEN** o Admin abre o lançamento de uma atividade avulsa
- **THEN** a tela diz que ele não converte reserva em baixa nem passa a aula a realizada

#### Scenario: A tela não oferece campo de valor

- **WHEN** o Admin abre o lançamento de uma atividade avulsa
- **THEN** não há campo de valor de pontuação na tela

#### Scenario: Aula sem avulsa não é erro

- **WHEN** o Admin abre a área Lançamentos numa aula que não tem atividade avulsa alguma
- **THEN** a tela diz isso em uma frase, sem tela vazia nem erro cru

### Requirement: O lançamento da avulsa oferece só a forma que a modalidade admite

A App 03 SHALL oferecer, para cada atividade avulsa, a forma de lançamento que a **modalidade**
admite: **por aluno**, com desfecho e produção de cada participante, na individual; **por
equipe da aula**, com desfecho e produção da equipe, na em equipe e na em equipe com familiar.
A aplicação NEVER SHALL oferecer a forma que a modalidade não admite. (`RF-02-112`, `RN-02-33`)

#### Scenario: A atividade individual só oferece lançar por aluno

- **WHEN** o Admin abre o lançamento de uma atividade avulsa de modalidade individual
- **THEN** a tela oferece o lançamento por aluno e não oferece o por equipe

#### Scenario: A atividade em equipe só oferece lançar por equipe

- **WHEN** o Admin abre o lançamento de uma atividade avulsa de modalidade em equipe
- **THEN** a tela oferece o lançamento por equipe e não oferece o por aluno

### Requirement: O lançamento por equipe mostra as equipes pelo nome e quem ficou de fora

No lançamento por equipe, a tela SHALL apresentar as equipes daquela aula pelo **nome** e SHALL
dizer, antes de enviar, **quem ficou de fora por não ter presença**. Os três desfechos fechados
SHALL ser os mesmos do lançamento da atividade da aula, e participante ou equipe sem desfecho
SHALL impedir o envio, com a falta dita na tela. (`RF-02-112`, `RN-02-32`)

#### Scenario: A tela avisa quem ficou de fora

- **WHEN** o Admin escolhe uma equipe em que um integrante não tem presença naquela aula
- **THEN** a tela diz quem ficou de fora antes de o lançamento ser enviado

#### Scenario: Equipe sem desfecho impede o envio

- **WHEN** o Admin tenta enviar o lançamento por equipe sem escolher o desfecho
- **THEN** a aplicação não envia e diz o que está em falta

#### Scenario: A recusa do núcleo é dita em linguagem simples

- **WHEN** o núcleo recusa o lançamento porque um Guerreiro(a) já tem Resultado naquela
  atividade
- **THEN** a tela explica isso em linguagem simples, sem código de erro cru
