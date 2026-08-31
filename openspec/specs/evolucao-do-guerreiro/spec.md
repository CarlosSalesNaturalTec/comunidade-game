## Purpose

O que o núcleo mostra ao responsável sobre a criança pela qual ele responde: presença,
atividades realizadas, pontos, poderes, badges, nível, progresso como percurso, criações
validadas e ocorrências de conduta — recortado pelo vínculo vigente e vedado ao que a criança
faz sozinha, que continua dela.

## Requirements

### Requirement: A evolução é servida ao responsável e recortada pelo vínculo

O núcleo SHALL servir a evolução de um Guerreiro(a) à persona de **responsável em sessão** que
tenha **vínculo vigente** com ele, e SHALL recusar com **403** o pedido de evolução de
Guerreiro(a) sem vínculo vigente com quem pede, sem devolver dado algum daquela criança. O
recorte SHALL valer por vínculo, e não por comunidade. (`RF-13-07`, `RN-13-04`, `RF-01-15`,
`RF-01-16`)

#### Scenario: Responsável lê a evolução do vinculado

- **WHEN** um responsável com vínculo vigente pede a evolução do Guerreiro(a) vinculado
- **THEN** o núcleo devolve a evolução daquela criança

#### Scenario: Criança sem vínculo é recusada

- **WHEN** um responsável pede a evolução de um Guerreiro(a) que não está vinculado a ele
- **THEN** o núcleo responde 403 e não devolve dado algum daquela criança

### Requirement: A evolução traz presença, atividades, pontos, poderes, badges e nível

A evolução SHALL trazer, do Guerreiro(a) pedido, a **presença** nas aulas, as **atividades
realizadas** com o desfecho de cada uma, os **pontos**, os **poderes**, os **badges**
conquistados e o **nível** alcançado. (`RF-13-07`)

#### Scenario: A evolução de quem já tem histórico

- **WHEN** o responsável lê a evolução de um Guerreiro(a) com presença registrada, atividade
  lançada, pontos creditados, poder atribuído, badge conquistado e nível certificado
- **THEN** a resposta traz presença, atividades realizadas, pontos, poderes, badges e nível

#### Scenario: A evolução de quem ainda não tem histórico

- **WHEN** o responsável lê a evolução de um Guerreiro(a) recém-cadastrado
- **THEN** a resposta traz cada item vazio ou zerado, e não falha

### Requirement: O progresso da trilha é percurso, nunca saldo de pontos

A evolução SHALL apresentar o progresso de cada trilha em que o Guerreiro(a) está inscrito como
**percurso** — quantas missões obrigatórias já foram desbloqueadas e quantas faltam —, na mesma
apuração que serve o próprio Guerreiro(a). NEVER SHALL apresentar o avanço do nível como saldo
de pontos. (`RF-13-08`, `RN-05-03`, `RN-05-04`)

#### Scenario: Trilha em andamento

- **WHEN** o responsável lê a evolução de um Guerreiro(a) inscrito numa trilha com missões
  obrigatórias desbloqueadas e outras por desbloquear
- **THEN** a resposta traz, daquela trilha, o nível atual, quantas obrigatórias foram
  desbloqueadas e quantas são as obrigatórias no total

#### Scenario: O nível não se comunica por saldo

- **WHEN** o responsável lê o progresso de uma trilha
- **THEN** o que exprime o avanço do nível é a contagem de missões, e não o saldo de pontos

### Requirement: As criações originais validadas aparecem com título, trilha e data

A evolução SHALL trazer as **criações originais validadas** do Guerreiro(a), cada uma com
**título**, **trilha** e **data**. Criação ainda não validada NEVER SHALL aparecer.
(`RF-13-10`)

#### Scenario: Criação validada aparece

- **WHEN** o Guerreiro(a) tem criação original validada e o responsável lê a evolução
- **THEN** a resposta traz aquela criação com título, trilha e data

#### Scenario: Criação ainda não validada não aparece

- **WHEN** o Guerreiro(a) tem criação original entregue e ainda não validada
- **THEN** ela não aparece na evolução lida pelo responsável

### Requirement: A ocorrência de conduta é visível ao responsável, com motivo e data

O núcleo SHALL servir ao responsável as **ocorrências de conduta** do Guerreiro(a) vinculado,
cada uma com o **motivo** e a **data** do fato, sob o mesmo recorte de vínculo da evolução.
Ocorrência cujo motivo já foi apagado pelo encerramento do ciclo SHALL continuar sendo servida
**sem o motivo**. (`RF-13-09`, `RN-13-21`, `RN-01-52`)

#### Scenario: Ocorrência do ciclo corrente

- **WHEN** o responsável lê as ocorrências de um Guerreiro(a) que teve ocorrência lançada no
  ciclo corrente
- **THEN** a resposta traz aquela ocorrência com o motivo e a data do fato

#### Scenario: Ocorrência com o motivo já expurgado

- **WHEN** o responsável lê uma ocorrência cujo motivo foi apagado pelo encerramento do ciclo
- **THEN** a resposta traz a ocorrência com a data e sem o motivo

#### Scenario: Ocorrência de criança não vinculada

- **WHEN** um responsável pede as ocorrências de um Guerreiro(a) não vinculado a ele
- **THEN** o núcleo responde 403 e nada é devolvido

### Requirement: O que a criança faz sozinha não vai ao responsável

A evolução NEVER SHALL trazer **consulta ao assistente** nem **transcrição de apoio escolar**,
em nenhuma forma — nem o texto, nem a contagem, nem a disciplina consultada. Transparência com a
família não alcança o que a criança faz sozinha. (`RF-13-11`, `RN-13-20`)

#### Scenario: Guerreiro(a) que usou o assistente

- **WHEN** o responsável lê a evolução de um Guerreiro(a) que fez consultas ao assistente e teve
  transcrição de apoio escolar guardada
- **THEN** nada disso aparece na resposta, em nenhuma forma

### Requirement: Nenhum dado de outra criança aparece na evolução

A evolução NEVER SHALL trazer dado identificável de **outro Guerreiro(a)** — nem em equipe, nem
em ranking, nem em criação coletiva. O que é de terceiro SHALL ser reduzido a **avatar e nick**
ou omitido. (`RF-13-12`, `RN-13-04`, invariantes 10 e 12 do documento 99 §6)

#### Scenario: Guerreiro(a) que participa de equipe

- **WHEN** o responsável lê a evolução de um Guerreiro(a) que integra equipe de trilha com
  outras crianças
- **THEN** nenhum dado identificável das outras crianças aparece na resposta

#### Scenario: Criação feita em conjunto

- **WHEN** a criação original validada do Guerreiro(a) tem outros integrantes
- **THEN** os demais integrantes aparecem, no máximo, por avatar e nick
