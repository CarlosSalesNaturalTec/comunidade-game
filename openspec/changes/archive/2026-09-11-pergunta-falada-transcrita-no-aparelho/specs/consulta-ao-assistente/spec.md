## ADDED Requirements

### Requirement: A pergunta chega sempre em texto, e o áudio nunca alcança o núcleo

A rota da consulta SHALL aceitar a pergunta **apenas em texto**, e SHALL exigir texto **não
vazio**: pergunta ausente, vazia ou só com espaços SHALL ser recusada com **422**, e nenhuma
consulta SHALL ser gravada. A rota NEVER SHALL receber arquivo de áudio, e o núcleo NEVER SHALL
transcrever fala.

A fala é transcrita **no próprio aparelho** e o que trafega é a transcrição — indistinguível,
no contrato, da pergunta digitada (`RF-04-40`, `RN-04-21`, documento 03 §1.12, PRD-04 §11).

#### Scenario: A pergunta em texto é respondida

- **WHEN** a equipe envia a pergunta em texto, venha ela do teclado ou da fala transcrita no
  aparelho
- **THEN** o núcleo responde a partir do corpus e grava a consulta com aquela transcrição

#### Scenario: Pergunta vazia é recusada

- **WHEN** chega uma consulta sem pergunta, ou com pergunta só de espaços
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Nenhum áudio entra na consulta

- **WHEN** se examina o que a rota da consulta aceita
- **THEN** não há campo de áudio nem de arquivo algum, e nada de áudio alcança o núcleo

## MODIFIED Requirements

### Requirement: A resposta indisponível não grava consulta pela metade

Não vindo a resposta do assistente — erro, demora ou formato inesperado —, o núcleo SHALL
responder **503** e NEVER SHALL gravar a consulta: consulta com pergunta e sem resposta
guardaria uma conversa que não aconteceu. A equipe SHALL poder perguntar de novo com **a mesma
pergunta**, sem refazer a fala: a transcrição é texto, e o aparelho a conserva na tela (PRD-04
§9).

#### Scenario: Sem resposta, nada é gravado

- **WHEN** o assistente não responde a tempo ou responde fora do formato esperado
- **THEN** o núcleo responde 503 e nenhuma consulta é gravada

#### Scenario: A equipe pergunta de novo

- **WHEN** a equipe reenvia a mesma pergunta depois de um 503
- **THEN** o núcleo a trata como consulta nova, sem resíduo da tentativa anterior

## REMOVED Requirements

### Requirement: A pergunta por fala é transcrita e o áudio descartado no ato

**Reason**: A transcrição passou a acontecer no aparelho (decisão do fundador, 2026-09-10,
documento 03 §1.12), e o enunciado novo de `RF-04-40` já não promete descartar o áudio depois
de transcrevê-lo: promete que ele **não chega**. Exigir "exatamente uma das duas formas" perdeu
objeto, porque só existe uma.

**Migration**: Substituída pelo requisito "A pergunta chega sempre em texto, e o áudio nunca
alcança o núcleo", que é a garantia mais forte. Quem chamava a rota com `arquivo` passa a
transcrever no aparelho e a mandar `texto`; nenhuma consulta gravada muda, porque a
`ConsultaAoAssistente` nunca guardou a forma da pergunta.
