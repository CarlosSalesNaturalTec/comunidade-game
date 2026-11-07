# Spec Delta

## ADDED Requirements

### Requirement: A resposta da sondagem aceita transcrição sem alternativa

Na submissão de **missão de sondagem**, cada resposta SHALL trazer a alternativa escolhida **ou**
a transcrição da resposta falada, sem alternativa. A resposta sem alternativa SHALL ser gravada
no histórico com a transcrição e como **não acertada**, e a sondagem SHALL ser dada por
respondida como sempre. Fora da sondagem, a alternativa SHALL seguir obrigatória. (`RF-05-98`,
`RN-05-55`, `RN-05-46`, `RN-05-47`)

#### Scenario: Sondagem com resposta sem alternativa é aceita

- **WHEN** o Guerreiro(a) submete a sondagem com uma resposta que traz só a transcrição
- **THEN** a submissão é aceita, aquela resposta é gravada com a transcrição e como não acertada,
  e a trilha abre

#### Scenario: Silêncio grava transcrição vazia

- **WHEN** a resposta da sondagem chega sem alternativa e com transcrição vazia
- **THEN** ela é gravada sem alternativa, com transcrição vazia e como não acertada

#### Scenario: Desbloqueio sem alternativa é recusado

- **WHEN** a submissão de um desafio de desbloqueio que não é sondagem traz resposta sem
  alternativa
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Alternativa e transcrição juntas são recusadas

- **WHEN** uma resposta traz a alternativa escolhida e também a transcrição
- **THEN** o núcleo responde 422, porque cada resposta tem uma forma só

#### Scenario: A transcrição não passa do limite

- **WHEN** a transcrição de uma resposta passa de 500 caracteres
- **THEN** o núcleo responde 422 e nada é gravado
