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
