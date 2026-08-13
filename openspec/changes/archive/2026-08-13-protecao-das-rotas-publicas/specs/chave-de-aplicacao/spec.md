## MODIFIED Requirements

### Requirement: A recusa não diferencia os motivos

O núcleo SHALL responder chave ausente, chave inválida e chave revogada com a **mesma** resposta
401, sem indicar no código, na mensagem ou no tempo de resposta qual dos três ocorreu. (PRD-01
§9 e §12)

A cota de leitura por faixa NEVER SHALL enfraquecer essa regra: a conferência da chave SHALL
preceder a contagem da cota, de modo que chave ausente, inválida ou revogada receba **401** e
NEVER SHALL receber **429**. O 429 SHALL alcançar apenas chave reconhecida e vigente, e por
isso não revela nada que o 200 daquela mesma chave já não revelasse. (`RF-01-55`, `RF-01-48`)

#### Scenario: Os três motivos produzem a mesma resposta

- **WHEN** três chamadas chegam à mesma rota, uma sem chave, uma com chave inexistente e uma
  com chave revogada
- **THEN** as três recebem 401 com corpo idêntico, e nenhuma revela qual foi o motivo

#### Scenario: Recusa não confirma a existência de uma chave

- **WHEN** alguém tenta descobrir uma chave válida por tentativa e erro
- **THEN** nenhuma resposta do núcleo distingue "essa chave não existe" de "essa chave existe e
  foi revogada"

#### Scenario: Chave desconhecida nunca recebe 429

- **WHEN** chamadas com chave inexistente chegam em número muito acima de qualquer cota
- **THEN** todas recebem 401, e nenhuma recebe 429

#### Scenario: Chave revogada nunca recebe 429

- **WHEN** uma chave que estava em 429 por exceder a cota é revogada e volta a chamar
- **THEN** a resposta passa a ser 401, igual à de chave ausente ou inexistente
