## RENAMED Requirements

- FROM: `### Requirement: O registro guarda a origem, e o sensor não é alcançável nesta entrega`
- TO: `### Requirement: O registro guarda a origem, e a de sensor entra por credencial de dispositivo`

## MODIFIED Requirements

### Requirement: O registro guarda a origem, e a de sensor entra por credencial de dispositivo

O núcleo SHALL gravar em cada registro a sua **origem**. As origens SHALL ser **manual**, **voz**
e **sensor**. A rota autenticada por **sessão de Guerreiro(a)** SHALL aceitar apenas as origens
`manual` e `voz`, e SHALL recusar `sensor` com **422** — o sensor não tem sessão, porque a sessão
é de pessoa. A origem **`sensor`** SHALL ser gravada quando, e somente quando, a chamada se
autenticar por **credencial de dispositivo** presa àquela série, e o registro SHALL apontar para
a **credencial que o gravou** — o atributo `dispositivo` do PRD-08 §8.

A **autoria** do registro de origem sensor SHALL ser a do **Guerreiro(a) coletor** da série a que
a credencial está presa, com o papel dele. O aparelho NEVER SHALL ser autor: a credencial é do
aparelho, nunca da criança, e o vínculo permanente do registro é com o coletor. Todas as demais
regras do registro SHALL valer igualmente para a origem sensor — hora da medição distinta da hora
do envio, faixa esperada do tipo, imutabilidade, comunidade vigente na data da medição e crédito
ao Poder do Território. (`RF-08-08`, `RF-08-14`, `RN-08-23`, `RN-08-11`, PRD-08 §8)

#### Scenario: Registro manual grava a origem manual

- **WHEN** o Guerreiro(a) digita uma medição na sua série
- **THEN** o núcleo grava o registro com origem `manual`

#### Scenario: Origem sensor é recusada na rota de sessão

- **WHEN** um Guerreiro(a) em sessão envia medição declarando origem `sensor`
- **THEN** o núcleo responde 422 e nada é gravado, porque o sensor entra por credencial de
  dispositivo

#### Scenario: O sensor autenticado grava a origem sensor

- **WHEN** um sensor apresenta a credencial de dispositivo da série e envia uma medição
- **THEN** o núcleo grava o registro com origem `sensor`

#### Scenario: O registro de sensor aponta a credencial que o gravou

- **WHEN** um registro é gravado por credencial de dispositivo
- **THEN** o registro guarda a credencial que o gravou, e o registro de origem manual ou voz não
  guarda credencial alguma

#### Scenario: A autoria é do coletor, nunca do aparelho

- **WHEN** um sensor grava medição pela credencial de dispositivo da série
- **THEN** a autoria do registro é a do Guerreiro(a) coletor daquela série, com o papel dele

#### Scenario: O valor de sensor fora da faixa entra a conferir como qualquer outro

- **WHEN** um sensor grava valor fora da faixa esperada do tipo de coleta
- **THEN** o núcleo aceita e grava o registro marcado "a conferir", como faria com uma digitação
