## ADDED Requirements

### Requirement: O Admin encerra o ciclo por uma tela da gestão

A App 03 SHALL oferecer ao Admin a tela do **encerramento do ciclo**, e SHALL exigir
confirmação explícita antes de executá-lo, porque o expurgo do motivo das ocorrências de
conduta não se desfaz. A tela SHALL dizer, antes da confirmação, os dois efeitos do ato — o
expurgo dos motivos guardados e a saída das ocorrências do ranking público — e SHALL deixar
claro que o ciclo seguinte **não** é declarado ali. (`RF-02-99`, `RF-02-100`, `RN-02-30`)

#### Scenario: O ato pede confirmação antes de executar

- **WHEN** o Admin aciona o encerramento do ciclo na App 03
- **THEN** a tela apresenta os dois efeitos do ato e pede confirmação explícita, sem executar
  nada ainda

#### Scenario: Confirmado, o ato é executado e o resultado é exibido

- **WHEN** o Admin confirma o encerramento
- **THEN** a App 03 executa o ato no núcleo e exibe o resultado dele

#### Scenario: Desistir não executa nada

- **WHEN** o Admin desiste diante da confirmação
- **THEN** nenhum motivo é expurgado e nada muda

#### Scenario: A tela não oferece declarar o ciclo seguinte

- **WHEN** a tela do encerramento do ciclo é apresentada
- **THEN** ela não oferece campo, opção nem etapa para declarar o ciclo seguinte
