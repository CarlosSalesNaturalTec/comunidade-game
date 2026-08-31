# consulta-ao-assistente Specification

## Purpose

A consulta ao assistente é a conversa que a equipe tem com a plataforma durante o encontro —
pergunta por texto ou por fala, resposta tirada só do conteúdo que os Mestres cadastraram, e
guarda apenas da transcrição. É a mesma entidade que o apoio escolar da App 05 usará depois.

## Requirements

### Requirement: A consulta pertence a uma equipe ou a um Guerreiro(a), e nomeia o assistente

O núcleo SHALL manter a **consulta ao assistente** com **exatamente um** entre **equipe** e
**Guerreiro(a)** — a App 01 sempre preenche a equipe, e a porta individual da App 05 preencherá
o Guerreiro(a) —, o **assistente** consultado (trilhas ou apoio escolar), a **transcrição da
pergunta**, a **transcrição da resposta** e o **momento**, com fuso. Consulta com os dois
vínculos, ou com nenhum, SHALL ser recusada.

A consulta NEVER SHALL guardar o áudio da pergunta nem qualquer arquivo: só as duas
transcrições sobrevivem (`RF-04-40`, `RN-04-21`, PRD-04 §§8, 11).

#### Scenario: A consulta da equipe grava as duas transcrições

- **WHEN** uma equipe consulta o assistente de trilhas e o núcleo responde
- **THEN** a consulta é gravada com a equipe, o assistente de trilhas, a transcrição da
  pergunta, a transcrição da resposta e o momento com fuso

#### Scenario: A consulta não tem dois sujeitos

- **WHEN** chega uma consulta com equipe e Guerreiro(a) ao mesmo tempo, ou sem nenhum dos dois
- **THEN** o núcleo a recusa e nada é gravado

#### Scenario: Nenhum áudio sobrevive à consulta

- **WHEN** se lê uma consulta feita por fala
- **THEN** ela traz só as transcrições, e nenhum áudio consta do registro

### Requirement: Só o integrante da equipe consulta o assistente por ela

O núcleo SHALL aceitar a consulta ao assistente de trilhas do **Guerreiro(a) em sessão** que
seja **integrante da equipe** informada. Quem não integra a equipe SHALL receber **403**, e
nenhuma consulta SHALL ser gravada. Adulto em sessão — Mestre ou Admin — NEVER SHALL consultar
pela equipe: o assistente é da criança no encontro (`RF-04-36`, PRD-04 §9).

#### Scenario: O integrante pergunta pela equipe

- **WHEN** um Guerreiro(a) integrante da equipe envia a pergunta
- **THEN** o núcleo responde e grava a consulta vinculada àquela equipe

#### Scenario: Quem não integra a equipe é recusado

- **WHEN** um Guerreiro(a) que não integra a equipe envia a pergunta por ela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: O adulto não consulta pela equipe

- **WHEN** um Mestre ou Admin em sessão envia a pergunta pela equipe
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O corpus é o conteúdo da missão corrente e das já percorridas

O assistente de trilhas SHALL responder **apenas a partir do corpus fechado** montado com o
**conteúdo das missões** da trilha da equipe: a missão da **atividade corrente** que a equipe
declarou e as missões de **posição anterior** na mesma trilha. Conteúdo de missão **à frente**
na trilha NEVER SHALL entrar no corpus — servi-lo contornaria o desbloqueio.

O assistente NEVER SHALL responder de conhecimento próprio, de fora do corpus (`RF-04-36`,
`RN-04-19`, documento 03 §4.2, decisão do fundador de 2026-08-30).

Equipe **sem atividade corrente declarada** SHALL ser recusada com **422**: sem missão não há
corpus.

#### Scenario: A pergunta sobre a missão do dia é respondida

- **WHEN** a equipe pergunta sobre um conceito do conteúdo da missão da atividade corrente
- **THEN** o assistente responde a partir daquele conteúdo

#### Scenario: A pergunta sobre missão anterior também é respondida

- **WHEN** a equipe pergunta sobre um conceito de uma missão de posição anterior na mesma trilha
- **THEN** o assistente responde a partir do conteúdo daquela missão

#### Scenario: Missão à frente não entra no corpus

- **WHEN** a equipe pergunta sobre assunto que só aparece em missão de posição posterior
- **THEN** o assistente não o responde, e devolve a recusa explicada

#### Scenario: Sem atividade corrente não há corpus

- **WHEN** a equipe consulta o assistente sem ter declarado a atividade que está trabalhando
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A pergunta fora do corpus recebe recusa explicada, e não é erro

O assistente SHALL responder à pergunta **fora do corpus** com a **recusa explicada** no corpo
da resposta, em **200** — dizendo que o assunto ainda não está no material e orientando a
**procurar um Mestre no encontro**. A recusa NEVER SHALL ser devolvida como erro: a equipe
perguntou o que podia perguntar (`RF-04-37`, PRD-04 §9).

A recusa SHALL ser gravada como consulta, com a transcrição da pergunta e a da recusa: é o que
mostra ao Mestre o que falta no material.

#### Scenario: Fora do corpus, a recusa vem em 200

- **WHEN** a equipe pergunta algo que o corpus não cobre
- **THEN** o núcleo responde 200 com a recusa explicada e a orientação de procurar um Mestre

#### Scenario: A recusa também é consulta gravada

- **WHEN** o assistente recusa uma pergunta fora do corpus
- **THEN** a consulta é gravada com a transcrição da pergunta e a da recusa

### Requirement: A pergunta de tarefa escolar é encaminhada à App 05, sem resposta aqui

O assistente de trilhas SHALL reconhecer a pergunta de **tarefa escolar** e SHALL devolver o
**encaminhamento à App 05**, em 200, sem responder o conteúdo escolar — o apoio escolar tem
assistente próprio, e não é este. O encaminhamento SHALL ser gravado como consulta, do mesmo
modo que a recusa (`RF-04-38`, documento 03 §4.2).

#### Scenario: A tarefa escolar é encaminhada

- **WHEN** a equipe pergunta algo que é tarefa da escola
- **THEN** o núcleo responde 200 dizendo que esse apoio é da App 05, sem responder a tarefa

#### Scenario: O encaminhamento fica registrado

- **WHEN** o assistente encaminha uma pergunta escolar
- **THEN** a consulta é gravada com a transcrição da pergunta e a do encaminhamento

### Requirement: A pergunta por fala é transcrita e o áudio descartado no ato

O núcleo SHALL aceitar a pergunta em **texto** ou em **áudio**, e SHALL exigir **exatamente
uma** das duas formas — as duas juntas, ou nenhuma, SHALL ser recusadas com **422**. Recebido
o áudio, o núcleo SHALL transcrevê-lo e SHALL **descartá-lo assim que a transcrição existir**:
o áudio NEVER SHALL ser gravado em disco, em armazenamento de arquivo ou em registro de log
(`RF-04-39`, `RF-04-40`, `RN-04-21`, PRD-04 §11).

#### Scenario: A pergunta falada vira transcrição

- **WHEN** a equipe envia a pergunta em áudio
- **THEN** o núcleo grava a transcrição da pergunta e responde a partir do corpus

#### Scenario: Duas formas ao mesmo tempo são recusadas

- **WHEN** chega uma consulta com texto e áudio juntos, ou sem nenhum dos dois
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: O áudio não sobrevive à chamada

- **WHEN** a consulta em áudio termina
- **THEN** o áudio não está em armazenamento algum, nem em log

### Requirement: A resposta indisponível não grava consulta pela metade

Não vindo a resposta do assistente — erro, demora ou formato inesperado —, o núcleo SHALL
responder **503** e NEVER SHALL gravar a consulta: consulta com pergunta e sem resposta
guardaria uma conversa que não aconteceu. A equipe SHALL poder perguntar de novo, e a pergunta
falada SHALL ser refeita, porque o áudio já foi descartado (PRD-04 §9, mesmo desfecho da
leitura da produção).

#### Scenario: Sem resposta, nada é gravado

- **WHEN** o assistente não responde a tempo ou responde fora do formato esperado
- **THEN** o núcleo responde 503 e nenhuma consulta é gravada

#### Scenario: A equipe pergunta de novo

- **WHEN** a equipe reenvia a pergunta depois de um 503
- **THEN** o núcleo a trata como consulta nova, sem resíduo da tentativa anterior

### Requirement: A consulta não credita ponto e não altera progressão

A consulta ao assistente NEVER SHALL creditar ponto, conceder badge, desbloquear missão nem
lançar resultado: ela é conversa, não realização. Perguntar muito ou não perguntar NEVER SHALL
alterar a progressão do Guerreiro(a) nem a da equipe (`RF-04-36`, documento 11 §5).

#### Scenario: Perguntar não pontua

- **WHEN** uma equipe faz várias consultas ao assistente num encontro
- **THEN** nenhum ponto, badge, desbloqueio ou resultado nasce delas
