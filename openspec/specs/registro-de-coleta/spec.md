## Purpose

O registro é a medição em si — o dado do território que a plataforma guarda em definitivo, com
o coletor identificado e a hora em que a medição aconteceu. É o único fato que credita o Poder
do Território e a matéria-prima de todo painel, exportação e pesquisa que vierem depois.

## Requirements

### Requirement: O Guerreiro(a) grava medição na sua própria série

O núcleo SHALL aceitar o registro de medição enviado pelo **Guerreiro(a) dono da série**, em
sessão. Guerreiro(a) que não é o coletor daquela série SHALL receber **403**, e persona de outro
papel SHALL receber **403**. O registro SHALL ser recusado com **422** quando a data da medição
cair fora da vigência do desafio da série. Todo registro SHALL gravar autoria, data e hora, como
as demais escritas do núcleo. (`RF-08-08`, `RF-01-03`, PRD-08 §§4, 9)

#### Scenario: O coletor grava medição na sua série

- **WHEN** o Guerreiro(a) dono de uma série ativa envia uma medição com valor e data e hora da
  medição
- **THEN** o núcleo grava o registro na série, com o autor, a data e a hora com fuso

#### Scenario: Guerreiro(a) que não é o coletor é recusado

- **WHEN** um Guerreiro(a) tenta gravar medição numa série de outro Guerreiro(a)
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Medição fora da vigência do desafio é recusada

- **WHEN** chega uma medição cuja data cai depois do fim da vigência do desafio da série
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A hora da medição é distinta da hora do envio, e é a que vale

O núcleo SHALL guardar em campos distintos a **data e hora da medição**, informada por quem
registra, e a **data e hora do registro**, marcada pelo núcleo no momento em que recebe a
chamada. Toda regra que depende de tempo — período de cadência e vigência do desafio — SHALL
usar a **data da medição**. Medição com data no futuro SHALL ser recusada com **422**. O núcleo
NEVER SHALL exigir que as duas coincidam: o Guerreiro(a) registra agora uma medição que fez
antes. (`RF-08-15`, PRD-08 §§8, 12)

#### Scenario: Medição registrada uma hora depois guarda a hora da medição

- **WHEN** um Guerreiro(a) envia às 15h uma medição feita às 14h
- **THEN** o núcleo grava 14h como data e hora da medição e 15h como data e hora do registro

#### Scenario: O período de cadência é apurado pela hora da medição

- **WHEN** uma medição feita no último dia de um período é enviada já dentro do período seguinte
- **THEN** o núcleo a atribui ao período em que a medição aconteceu, não ao do envio

#### Scenario: Medição com data no futuro é recusada

- **WHEN** chega uma medição cuja data e hora estão à frente do instante da chamada
- **THEN** o núcleo responde 422 e nada é gravado

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

### Requirement: Foto ou vídeo é o próprio registro quando o tipo assim o define

O núcleo SHALL aceitar **foto ou vídeo como o próprio registro**, sem valor numérico, quando o
**tipo de coleta** do desafio declara a forma de registro `foto` ou `video`. Nesse caso o valor
numérico SHALL ser dispensado e a **mídia** SHALL ser obrigatória; sem mídia o registro SHALL ser
recusado com **422**. Quando o tipo declara a forma `numero`, o **valor** e a **unidade** SHALL
ser obrigatórios e a mídia SHALL ser opcional. O registro por mídia SHALL creditar pontos como
qualquer outro registro válido do mesmo desafio. (`RF-08-21`, PRD-08 §§8, 12)

#### Scenario: Tipo de forma foto aceita a mídia como o registro

- **WHEN** o Guerreiro(a) envia uma foto numa série cujo tipo de coleta declara a forma `foto`
- **THEN** o núcleo grava o registro sem valor numérico e o considera válido

#### Scenario: Tipo de forma foto sem mídia é recusado

- **WHEN** chega um registro sem mídia numa série cujo tipo declara a forma `foto`
- **THEN** o núcleo responde 422 apontando o campo em falta e nada é gravado

#### Scenario: Tipo de forma número sem valor é recusado

- **WHEN** chega um registro sem valor numérico numa série cujo tipo declara a forma `numero`
- **THEN** o núcleo responde 422 apontando o campo em falta e nada é gravado

#### Scenario: Registro por mídia credita como o registro por número

- **WHEN** um registro por foto é gravado numa série
- **THEN** o núcleo credita os mesmos pontos que creditaria a um registro por número válido do
  mesmo desafio

### Requirement: Valor fora da faixa esperada é aceito e marcado "a conferir"

O núcleo SHALL **aceitar e gravar** o registro cujo valor cai fora da **faixa esperada** —
mínimo e máximo — do tipo de coleta, e SHALL marcá-lo **"a conferir"**. A marca SHALL valer
qualquer que seja a origem do registro. O registro marcado "a conferir" SHALL **creditar pontos
normalmente**: ele nasce válido como qualquer outro, e a marca só o destina à amostra de
auditoria do Mestre, de entrega posterior. Tipo sem faixa declarada NEVER SHALL produzir a
marca. (`RF-08-12`, PRD-08 §5.3)

#### Scenario: Valor acima do máximo entra a conferir

- **WHEN** chega uma medição de valor acima do máximo da faixa esperada do tipo
- **THEN** o núcleo grava o registro, marca-o "a conferir" e credita os pontos

#### Scenario: Valor abaixo do mínimo entra a conferir

- **WHEN** chega uma medição de valor abaixo do mínimo da faixa esperada do tipo
- **THEN** o núcleo grava o registro e marca-o "a conferir"

#### Scenario: Valor dentro da faixa não recebe a marca

- **WHEN** chega uma medição de valor dentro da faixa esperada do tipo
- **THEN** o núcleo grava o registro sem a marca "a conferir"

#### Scenario: Tipo sem faixa declarada não produz a marca

- **WHEN** chega uma medição numa série cujo tipo de coleta não declara faixa esperada
- **THEN** o núcleo grava o registro sem a marca "a conferir"

### Requirement: O registro é somente inserção e o vínculo com o coletor é permanente

O núcleo NEVER SHALL apagar nem editar registro gravado: **valor**, **data da medição** e
**coletor** SHALL ser imutáveis depois de gravados, e a **situação** SHALL ser o único campo que
evolui. Rota de alteração e rota de exclusão de registro NEVER SHALL existir; a correção se faz
por invalidação e novo registro, de entrega posterior. O vínculo entre registro e Guerreiro(a)
coletor(a) SHALL ser **permanente**, inclusive depois da saída dele do projeto. (`RN-08-10`,
`RN-08-11`, invariante 7 do documento 99 §6, PRD-08 §8)

#### Scenario: Não há rota de alteração de registro

- **WHEN** chega uma requisição para alterar o valor de um registro gravado
- **THEN** o núcleo responde 405 e o registro permanece como estava

#### Scenario: Não há rota de exclusão de registro

- **WHEN** chega uma requisição para apagar um registro gravado
- **THEN** o núcleo responde 405 e o registro permanece gravado

#### Scenario: O coletor permanece no registro depois da saída do projeto

- **WHEN** o vínculo de um Guerreiro(a) com a comunidade é encerrado
- **THEN** os registros que ele gravou seguem apontando para ele como coletor

### Requirement: O registro pertence à comunidade vigente do coletor na data da medição

O núcleo SHALL vincular cada registro à **Comunidade Virtual vigente do Guerreiro(a) na data da
medição**, e não à comunidade vigente no instante do envio nem à do local escolhido. O vínculo
SHALL ser gravado no registro, de modo que o filtro por comunidade sobre registros NEVER SHALL
depender do vínculo corrente do coletor. (`RN-08-03`, `RF-01-18`, 02 §1)

#### Scenario: A comunidade do registro é a da data da medição

- **WHEN** um Guerreiro(a) grava medição feita numa data em que estava vinculado à comunidade A
- **THEN** o núcleo grava o registro vinculado à comunidade A, ainda que o vínculo corrente seja
  outro

#### Scenario: O filtro por comunidade lê o vínculo gravado no registro

- **WHEN** uma consulta filtra registros por comunidade
- **THEN** o núcleo aplica o filtro sobre a comunidade gravada em cada registro
