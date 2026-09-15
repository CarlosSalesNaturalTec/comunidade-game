## MODIFIED Requirements

### Requirement: O Mestre lê as próprias trilhas, rascunhos inclusive

O núcleo SHALL expor ao Mestre em sessão as trilhas de que ele é **autor**, com a situação de
cada uma, incluindo as em rascunho. A leitura NEVER SHALL trazer rascunho de outro Mestre e
NEVER SHALL exigir filtro por comunidade, porque a trilha é bem comum da plataforma.
(`RF-09-04`, `RN-01-42`, PRD-09 §9)

Cada missão devolvida por essa leitura SHALL trazer o **desafio de desbloqueio** que ela tem
declarado: o **tipo**, o **enunciado** quando for prático e, quando for quiz, as **perguntas
vigentes** na ordem declarada, cada uma com o seu identificador, o enunciado, as quatro
alternativas, **qual delas é a correta** e a **referência da imagem** que ela tem. Missão sem
desafio declarado SHALL vir sem desafio, de modo distinto do quiz sem pergunta. Esta é a
leitura do desafio pelo Mestre autor de que trata `desbloqueio-da-missao`, e é o que permite
ao autor **reabrir e corrigir** o que declarou sem reenviar arquivo nem reescrever o quiz.
(`RF-09-26`, `RF-09-118`, `RF-09-119`)

A alternativa correta e a referência da imagem NEVER SHALL sair por leitura que alcance o
Guerreiro(a) ou qualquer persona que não seja o Mestre autor da trilha: esta leitura é
exclusiva do autor e é por isso que as carrega. (`RF-09-118`, `RF-05-89`)

Cada missão devolvida por essa leitura SHALL trazer também o **conteúdo** que ela tem
declarado — texto, imagem, link externo, vídeo e arquivo de apoio —, na ordem disposta pelo
Mestre, com o tipo, a referência e o tamanho de cada um que tem arquivo, e a autoria e a fonte
declaradas. Conteúdo sem envio confirmado SHALL vir sem referência de arquivo, do mesmo modo
que a leitura pública já trata. Missão sem conteúdo declarado SHALL vir com lista vazia, nunca
com erro. (`RF-09-14`, `RF-09-15`, `RF-09-24`)

Cada missão devolvida por essa leitura SHALL trazer também a **bibliografia** que ela tem
declarada — título, capítulo e o exemplar tombado apontado, quando houver. Missão sem
bibliografia declarada SHALL vir com lista vazia, nunca com erro. Esta leitura é a do Mestre
autor sobre a própria trilha, rascunho ou despublicada inclusive — diferente da leitura
pública, que só serve trilha publicada. (`RF-09-21`)

#### Scenario: O Mestre lê os próprios rascunhos

- **WHEN** um Mestre em sessão consulta as trilhas dele
- **THEN** o núcleo devolve as trilhas de que ele é autor, rascunhos inclusive, com a situação
  de cada uma

#### Scenario: Rascunho de outro Mestre não sai na leitura

- **WHEN** um Mestre em sessão consulta as trilhas dele e outro Mestre tem trilha em rascunho
- **THEN** a trilha do outro Mestre não é devolvida

#### Scenario: A leitura não exige comunidade

- **WHEN** a consulta chega sem parâmetro de comunidade
- **THEN** o núcleo responde normalmente, sem exigir o filtro

#### Scenario: A leitura devolve o quiz declarado, com a alternativa correta

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão tem quiz de três perguntas
- **THEN** a missão vem com as três perguntas na ordem declarada, cada uma com o seu
  identificador, as quatro alternativas e a indicação de qual é a correta

#### Scenario: A leitura devolve a referência da imagem de cada pergunta

- **WHEN** o Mestre autor consulta as trilhas dele e uma pergunta do quiz tem imagem anexada
- **THEN** aquela pergunta vem com a referência da imagem, e a pergunta sem imagem vem sem
  referência

#### Scenario: A pergunta substituída não volta na leitura

- **WHEN** o Mestre autor substituiu o quiz de uma missão e consulta as trilhas dele
- **THEN** a missão traz apenas as perguntas vigentes, e nenhuma das substituídas

#### Scenario: A leitura devolve o enunciado do desafio prático

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão tem desafio prático declarado
- **THEN** a missão vem com o tipo prático e o enunciado declarado, sem perguntas

#### Scenario: Missão sem desafio vem sem desafio

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão nunca teve desafio declarado
- **THEN** a missão vem sem desafio de desbloqueio, distinguível de um quiz sem pergunta

#### Scenario: A leitura devolve o conteúdo já gravado da missão

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão tem texto, imagem e vídeo
  declarados
- **THEN** a missão vem com os três conteúdos, na ordem declarada, cada um com o tipo, a
  referência de arquivo quando houver, a autoria e a fonte

#### Scenario: A leitura devolve o conteúdo de trilha em rascunho

- **WHEN** o Mestre autor consulta as trilhas dele e uma trilha em rascunho tem missão com
  conteúdo já gravado
- **THEN** a missão vem com o conteúdo, ainda que a trilha nunca tenha sido publicada

#### Scenario: Conteúdo sem envio confirmado vem sem referência de arquivo

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão tem conteúdo de vídeo cujo
  envio ainda não foi confirmado
- **THEN** aquele conteúdo vem sem referência de arquivo, e nenhuma referência quebrada é
  devolvida

#### Scenario: Missão sem conteúdo vem com lista vazia

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão nunca teve conteúdo declarado
- **THEN** a missão vem com a lista de conteúdo vazia, e nenhum erro é respondido

#### Scenario: A leitura devolve a bibliografia já declarada

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão tem duas entradas de
  bibliografia declaradas, uma vinculada a exemplar e outra não
- **THEN** a missão vem com as duas entradas, cada uma com título e capítulo, e a vinculada
  com o exemplar apontado

#### Scenario: Missão sem bibliografia vem com lista vazia

- **WHEN** o Mestre autor consulta as trilhas dele e uma missão nunca teve bibliografia
  declarada
- **THEN** a missão vem com a lista de bibliografia vazia, e nenhum erro é respondido
