## Purpose

O histórico de pontuação registra, um a um, os créditos e débitos de ponto regular e de ponto
extra de cada Guerreiro(a), para que ele, o Mestre do vínculo e o Admin saibam como e quando se
chegou a cada saldo.

## ADDED Requirements

### Requirement: Todo movimento de ponto grava um lançamento de pontuação

O núcleo SHALL gravar um **lançamento de pontuação** a cada crédito e a cada débito de ponto
regular e de ponto extra, **na mesma transação** do movimento: se o movimento não se grava, o
lançamento também não. O lançamento SHALL trazer o Guerreiro(a), a **conta** — regular ou
extra —, a **trilha ou o poder** da conta regular, a **data e hora** do registro, a **origem** e
a referência ao fato que o causou.

A origem SHALL ser uma destas: resultado de atividade, mérito do resultado, criação original,
partida de quiz, registro de coleta, estorno de registro de coleta, desafio prático de
desbloqueio, ocorrência de conduta, presença, estorno de presença, cuidado com o bem recebido,
proposta adotada, troca por recompensa avulsa e saldo anterior.

O **valor** do lançamento SHALL ser o que de fato moveu a conta: o débito que para em zero
registra só o que debitou. No ponto extra, o lançamento SHALL trazer separado o que moveu o
**acumulado** e o que moveu o **saldo disponível** — a troca move só o saldo. (`RF-01-88`,
`RN-01-67`, invariante 23 do documento 99 §6, 11 §5)

#### Scenario: Resultado lançado grava o lançamento do crédito

- **WHEN** um Resultado "realizada" credita ponto regular numa trilha
- **THEN** nasce um lançamento da conta regular daquela trilha, com a origem "resultado de
  atividade", o valor creditado e a data do registro

#### Scenario: Mérito grava dois lançamentos, um em cada conta

- **WHEN** um Resultado "realizada com mérito" credita ponto regular e ponto extra
- **THEN** nasce um lançamento na conta regular e outro na conta extra, cada um com o seu valor

#### Scenario: Ocorrência de conduta grava o débito

- **WHEN** uma ocorrência de conduta é lançada
- **THEN** nasce um lançamento de débito na conta regular da trilha da atividade, com a origem
  "ocorrência de conduta" e a referência à ocorrência

#### Scenario: Débito que para em zero registra o que debitou

- **WHEN** uma ocorrência de conduta de 5 pontos alcança uma trilha com 3 pontos
- **THEN** o lançamento registra o débito de 3, e o total da trilha fica em zero

#### Scenario: Troca move só o saldo disponível

- **WHEN** uma troca por recompensa avulsa debita 25 pontos extras
- **THEN** o lançamento registra 25 a menos no saldo disponível e nada no acumulado

#### Scenario: Estorno da presença move as duas contas

- **WHEN** uma presença anulada estorna 5 pontos extras de quem tem 2 de saldo disponível
- **THEN** o lançamento registra 5 a menos no acumulado e 2 a menos no saldo disponível

#### Scenario: Movimento recusado não deixa lançamento

- **WHEN** uma troca é recusada por saldo disponível insuficiente
- **THEN** nenhum lançamento é gravado

### Requirement: O lançamento nunca é editado nem removido

O lançamento de pontuação SHALL ser somente inserção: NEVER SHALL ser editado nem removido,
por rota alguma nem fora do ORM. Correção de pontuação SHALL ser novo lançamento, pelo fato que
a desfaz. (`RN-01-67`, `RN-01-38`)

#### Scenario: Alteração do lançamento é recusada

- **WHEN** uma escrita tenta alterar ou apagar um lançamento de pontuação, pelo ORM ou direto no
  banco
- **THEN** o núcleo recusa a escrita

### Requirement: O histórico começa com a linha de saldo anterior

Na implantação, o núcleo SHALL abrir o histórico de **cada conta já existente** — cada total
regular por trilha ou poder e cada conta de ponto extra — com um lançamento de origem **saldo
anterior**, no valor do total daquela data; no ponto extra, com o acumulado e o saldo disponível
de então. Conta zerada SHALL também receber a linha, com valor zero. O passado NEVER SHALL ser
reconstruído a partir dos fatos já gravados. (`RF-01-90`)

#### Scenario: Conta existente ganha a linha de saldo anterior

- **WHEN** a implantação encontra um Guerreiro(a) com 40 pontos regulares numa trilha e 12 de
  acumulado e 7 de saldo disponível de ponto extra
- **THEN** o histórico dele começa com uma linha de saldo anterior de 40 naquela trilha e outra
  de 12 no acumulado e 7 no saldo disponível

#### Scenario: Soma dos lançamentos fecha com o total

- **WHEN** se somam os lançamentos de uma conta, da linha de saldo anterior em diante
- **THEN** a soma é igual ao total atual da conta

### Requirement: O histórico é servido com os saldos, do mais recente ao mais antigo

O núcleo SHALL servir o histórico de pontuação de um Guerreiro(a) **do lançamento mais recente
ao mais antigo**, paginado pelo contrato de listagem da API, e, junto, os **saldos**: o total
regular de cada trilha ou poder, com o nome dela, e as duas contas de ponto extra — acumulado e
saldo disponível. Cada lançamento SHALL vir com data, conta, origem, valor, o nome da trilha ou
do poder e, quando houver, o título do fato que o causou. O lançamento de ocorrência de conduta
SHALL vir com o **motivo** enquanto ele estiver guardado; apagado o motivo no fim da guarda, o
lançamento SHALL seguir no histórico sem ele. (`RF-01-89`, `RF-09-144`, `RF-05-104`, 11 §5)

#### Scenario: O mais recente vem primeiro

- **WHEN** o histórico de um Guerreiro(a) com lançamentos em três datas é lido
- **THEN** os lançamentos vêm do mais recente ao mais antigo, com a linha de saldo anterior no
  fim

#### Scenario: Os saldos acompanham o histórico

- **WHEN** o histórico é lido
- **THEN** a resposta traz o total regular de cada trilha ou poder e as duas contas de ponto
  extra, separadas

#### Scenario: A conduta vem com o motivo

- **WHEN** o histórico traz o lançamento de uma ocorrência de conduta cujo motivo está guardado
- **THEN** o lançamento vem com o motivo escrito pelo Mestre

#### Scenario: Motivo apagado não apaga o lançamento

- **WHEN** o motivo da ocorrência foi apagado no fim da guarda
- **THEN** o lançamento segue no histórico, com data, origem e valor, e sem motivo

#### Scenario: Guerreiro(a) sem pontuação tem histórico vazio

- **WHEN** o histórico de um Guerreiro(a) que nunca pontuou é lido
- **THEN** a resposta traz a lista vazia e os saldos em zero, sem erro

### Requirement: Leem o histórico só o próprio, o Mestre do vínculo e o Admin

O núcleo SHALL servir o histórico ao **próprio Guerreiro(a)** por uma rota sem identificador de
persona, que alcança só quem está em sessão. Pela rota com o identificador do Guerreiro(a), SHALL
servi-lo ao **Admin**, de qualquer Guerreiro(a), e ao **Mestre** com **vínculo vigente na
comunidade** do Guerreiro(a). As duas leituras SHALL trazer o saldo disponível. Mestre sem
vínculo na comunidade dele, Guerreiro(a), Apoiador e responsável SHALL receber **403** na rota
com identificador, e nada do histórico SHALL ser devolvido. Nenhuma rota de jogo SHALL alcançar
o histórico. (`RN-01-68`, `RN-01-41`, `RF-09-143`, `RF-02-116`)

#### Scenario: O Guerreiro(a) lê o próprio histórico

- **WHEN** um Guerreiro(a) em sessão lê o histórico pela rota sem identificador
- **THEN** o núcleo devolve o histórico e os saldos dele, e não há como apontar para outro

#### Scenario: O Mestre do vínculo lê o histórico

- **WHEN** um Mestre com vínculo vigente na comunidade de um Guerreiro(a) lê o histórico dele
- **THEN** o núcleo devolve o histórico com os saldos, inclusive o saldo disponível

#### Scenario: Mestre de outra comunidade é recusado

- **WHEN** um Mestre sem vínculo vigente na comunidade do Guerreiro(a) lê o histórico dele
- **THEN** o núcleo responde 403 e nada do histórico é devolvido

#### Scenario: O Admin lê o histórico de qualquer Guerreiro(a)

- **WHEN** um Admin lê o histórico de um Guerreiro(a)
- **THEN** o núcleo devolve o histórico com os saldos

#### Scenario: Guerreiro(a) não lê o histórico de outro

- **WHEN** um Guerreiro(a) em sessão usa a rota com o identificador de outro Guerreiro(a)
- **THEN** o núcleo responde 403

#### Scenario: Responsável e Apoiador são recusados

- **WHEN** um responsável ou um Apoiador lê o histórico pela rota com identificador
- **THEN** o núcleo responde 403
