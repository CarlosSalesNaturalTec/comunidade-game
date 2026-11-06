## REMOVED Requirements

### Requirement: A consulta ao assistente do Desenvolvedor é pública e não se identifica

**Reason**: o assistente da Área do Apoiador Desenvolvedor saiu do produto — decisão do
fundador de 2026-11-06; `RF-03-71` e `RN-03-31` retirados do PRD-03.
**Migration**: `POST /v1/assistente-do-desenvolvedor` deixa de existir e passa a 404. O único
consumidor, a App 06, sai na mesma change. Quem quer conhecer a API lê a interface Swagger do
núcleo, aberta e sem chave.

### Requirement: Nada da conversa é guardado

**Reason**: sem assistente não há conversa — decisão do fundador de 2026-11-06.
**Migration**: nenhuma.

### Requirement: O corpus é fechado na documentação, no README e no contrato OpenAPI

**Reason**: sem assistente não há corpus — decisão do fundador de 2026-11-06; `RF-03-70`,
`RN-03-30` e `RN-03-38` retirados do PRD-03. A esteira deixa de montar o artefato do corpus.
**Migration**: nenhuma.

### Requirement: Fora do corpus, o assistente diz que não sabe e aponta a documentação

**Reason**: o assistente saiu — decisão do fundador de 2026-11-06; `RF-03-70` retirado.
**Migration**: nenhuma.

### Requirement: Toda mensagem termina com uma pergunta de múltipla escolha

**Reason**: o assistente saiu — decisão do fundador de 2026-11-06; `RF-03-69` retirado.
**Migration**: nenhuma.

### Requirement: A indisponibilidade do assistente é desfecho declarado, não falha da área

**Reason**: o assistente saiu — decisão do fundador de 2026-11-06; `RF-03-72` retirado.
**Migration**: nenhuma.
