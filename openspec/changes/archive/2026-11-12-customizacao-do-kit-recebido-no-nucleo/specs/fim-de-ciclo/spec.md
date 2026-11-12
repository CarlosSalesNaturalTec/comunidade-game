## MODIFIED Requirements

### Requirement: O Admin encerra o ciclo corrente num ato isolado

O núcleo SHALL oferecer ao **Admin** o ato de encerrar o ciclo corrente. O ato NEVER SHALL
declarar o ciclo seguinte: o rótulo do próximo ciclo é **declarado na implantação**, e o ciclo
NEVER SHALL ser entidade do modelo. Nenhuma outra persona SHALL executá-lo. (`RF-02-99`,
documentos 02 §1 e 09)

#### Scenario: O Admin encerra o ciclo

- **WHEN** um Admin executa o ato de encerramento do ciclo corrente
- **THEN** o núcleo dispara os efeitos do encerramento e responde com o resultado de cada um

#### Scenario: O ato não declara o ciclo seguinte

- **WHEN** o encerramento do ciclo é executado
- **THEN** nenhum ciclo novo é criado, e o rótulo do ciclo corrente segue sendo o declarado na
  implantação

#### Scenario: Quem não é Admin não encerra

- **WHEN** um Mestre, um Apoiador, um responsável ou um Guerreiro(a) tenta encerrar o ciclo
- **THEN** o núcleo recusa o ato

#### Scenario: Encerrar de novo não tem o que fazer

- **WHEN** o encerramento é executado uma segunda vez, sem nenhuma ocorrência de conduta nova
  desde o primeiro
- **THEN** o ato é aceito e nada é alterado, porque não há motivo guardado a expurgar

## ADDED Requirements

### Requirement: O encerramento expira os registros de customização pendentes

O encerramento do ciclo SHALL passar a **expirado** todo registro de customização do kit ainda
**pendente**, e responder **quantos** expirou. Registro aprovado, reprovado ou cancelado NEVER
SHALL ser tocado, e nenhum ponto é creditado nem debitado. Encerrar de novo sem pendente novo
não altera nada. (`RF-01-86`, `RF-05-103`, documento 11 §5)

#### Scenario: O pendente expira no fim do ciclo

- **WHEN** o Admin encerra o ciclo e há registro de customização pendente
- **THEN** o registro passa a expirado, e a resposta diz quantos expiraram

#### Scenario: O julgado não expira

- **WHEN** o Admin encerra o ciclo e há registro de customização aprovado
- **THEN** o registro segue aprovado, e o acervo não muda
