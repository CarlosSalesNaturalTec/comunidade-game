## Purpose

O vocabulário do que a plataforma consome e recebe — hora-aula, lanche, insumo, kit, livro,
camisa, cloud, serviços e produção executiva —, cada tipo com a sua unidade e o seu valor de
referência em moedas. É a tabela que valora o aporte não financeiro e, por ser versionada por
vigência, permite o valor mudar no tempo sem reescrever o passado.

## Requirements

### Requirement: O catálogo de tipos de recurso é cadastrado por Admin

O núcleo SHALL manter o catálogo de **tipos de recurso** com **nome**, **natureza** — consumível,
durável, serviço ou financeiro —, **unidade** e a marca de **exige comprovante**. Cadastrar tipo
de recurso SHALL exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL
receber **403**. Cadastro sem nome, sem natureza ou sem unidade SHALL ser recusado com **422**,
indicando o campo em falta, e natureza fora das quatro previstas SHALL ser recusada com **422**.
A marca de **exige comprovante** SHALL ser opcional no cadastro e SHALL nascer **falsa** quando
não declarada; quando verdadeira, o aporte daquele tipo sem comprovante SHALL ser recusado. O
cadastro SHALL ser operação **avulsa**, que não depende de nenhum outro fluxo em andamento. A
escrita SHALL gravar autoria, data e hora com fuso. (`RF-07-01`, `RF-07-03`, `RN-07-22`,
`RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Admin cadastra um tipo de recurso

- **WHEN** um Admin em sessão cadastra um tipo de recurso com nome, natureza e unidade
- **THEN** o núcleo grava o tipo no catálogo com o autor, a data e a hora com fuso

#### Scenario: Mestre não cadastra tipo de recurso

- **WHEN** um Mestre em sessão tenta cadastrar um tipo de recurso
- **THEN** o núcleo responde 403 e o catálogo permanece como estava

#### Scenario: Tipo sem unidade é recusado

- **WHEN** chega um cadastro de tipo de recurso sem unidade
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Natureza fora das quatro previstas é recusada

- **WHEN** chega um cadastro de tipo de recurso com natureza que não é consumível, durável,
  serviço nem financeiro
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Tipo nasce sem exigir comprovante

- **WHEN** um Admin cadastra um tipo de recurso sem declarar a marca de exige comprovante
- **THEN** o núcleo grava o tipo com a marca falsa

#### Scenario: Tipo cadastrado exigindo comprovante

- **WHEN** um Admin cadastra um tipo de recurso declarando que ele exige comprovante
- **THEN** o núcleo grava o tipo com a marca verdadeira, e o aporte daquele tipo sem comprovante
  passa a ser recusado

### Requirement: O valor de referência em moedas é versionado por vigência

O núcleo SHALL manter o **valor de referência em moedas** de cada tipo de recurso com **início de
vigência**. Alterar o valor de um tipo SHALL **abrir uma vigência nova** e NEVER SHALL reescrever
nem apagar a anterior, de modo que a consulta pela data devolva o valor que valia naquele
momento. Entre as vigências de um mesmo tipo NEVER SHALL haver sobreposição: abrir vigência nova
SHALL **encerrar a vigente no dia de início da nova**, que passa a ser o primeiro dia fora dela.
Havendo mais de uma vigência aberta no mesmo dia, SHALL valer a **registrada por último**. Registrar valor de referência SHALL exigir
persona **Admin**; persona de qualquer outro papel SHALL receber **403**. Valor negativo SHALL ser
recusado com **422**. (`RF-07-02`, `RN-07-03`, `RF-01-16`, `RF-01-03`, PRD-07 §8)

#### Scenario: Primeiro valor de referência de um tipo

- **WHEN** um Admin registra o valor de referência de um tipo de recurso com início de vigência
- **THEN** o núcleo grava a vigência aberta, sem encerramento

#### Scenario: Valor novo abre vigência e preserva a anterior

- **WHEN** um Admin registra um valor de referência novo para um tipo que já tinha um
- **THEN** o núcleo encerra a vigência anterior no dia de início da nova, e a anterior permanece
  consultável com o valor que tinha

#### Scenario: Duas vigências abertas no mesmo dia

- **WHEN** um Admin registra dois valores de referência para o mesmo tipo com o mesmo dia de
  início
- **THEN** a consulta por aquele dia devolve o valor registrado por último

#### Scenario: Consulta pela data devolve o valor da época

- **WHEN** o valor de referência de um tipo é consultado por uma data coberta por uma vigência
  encerrada
- **THEN** o núcleo devolve o valor daquela vigência, não o valor corrente

#### Scenario: Valor negativo é recusado

- **WHEN** chega um valor de referência negativo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre não registra valor de referência

- **WHEN** um Mestre em sessão tenta registrar um valor de referência
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: A moeda é guardada com duas casas decimais exatas

O núcleo SHALL guardar todo valor em **moedas da plataforma** com **exatamente duas casas
decimais**, sem perda de precisão em nenhuma etapa de gravação, leitura ou comparação. Valor com
mais de duas casas decimais SHALL ser recusado com **422**, e NEVER SHALL ser arredondado em
silêncio. (`RN-07-04`, `RF-01-27`, documento 04 §1)

#### Scenario: Valor com duas casas é aceito

- **WHEN** um Admin registra um valor de referência com duas casas decimais
- **THEN** o núcleo grava o valor exatamente como recebido

#### Scenario: Valor com mais de duas casas é recusado

- **WHEN** chega um valor de referência com três ou mais casas decimais
- **THEN** o núcleo responde 422 e nada é gravado, sem arredondar

### Requirement: O preço de referência em pontos extras é versionado por vigência

O núcleo SHALL manter, por tipo de recurso, o **preço de referência em pontos extras** com
**início de vigência**, pela mesma mecânica do valor de referência em moedas. Alterar o preço
SHALL **abrir uma vigência nova** e NEVER SHALL reescrever nem apagar a anterior, de modo que a
consulta pela data devolva o preço que valia naquele momento. Entre as vigências de um mesmo
tipo NEVER SHALL haver sobreposição: abrir vigência nova SHALL **encerrar a vigente no dia de
início da nova**, que passa a ser o primeiro dia fora dela. Havendo mais de uma vigência aberta
no mesmo dia, SHALL valer a **registrada por último**. Registrar preço de referência SHALL
exigir persona **Admin** em sessão; persona de qualquer outro papel SHALL receber **403**. O
preço SHALL ser número **inteiro** de pontos extras. A escrita SHALL gravar autoria, data e hora
com fuso. (`RF-07-42`, `RF-07-43`, `RN-07-29`, `RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Primeiro preço de referência de um tipo

- **WHEN** um Admin em sessão registra o preço de referência em pontos extras de um tipo de
  recurso com início de vigência
- **THEN** o núcleo grava a vigência aberta, sem encerramento, com o autor, a data e a hora com
  fuso

#### Scenario: Preço novo abre vigência e preserva a anterior

- **WHEN** um Admin registra um preço de referência novo para um tipo que já tinha um
- **THEN** o núcleo encerra a vigência anterior no dia de início da nova, e a anterior permanece
  consultável com o preço que tinha

#### Scenario: Duas vigências abertas no mesmo dia

- **WHEN** um Admin registra dois preços de referência para o mesmo tipo com o mesmo dia de
  início
- **THEN** a consulta por aquele dia devolve o preço registrado por último

#### Scenario: Consulta pela data devolve o preço da época

- **WHEN** o preço de referência de um tipo é consultado por uma data coberta por uma vigência
  encerrada
- **THEN** o núcleo devolve o preço daquela vigência, não o preço corrente

#### Scenario: Preço fracionário é recusado

- **WHEN** chega um preço de referência que não é número inteiro de pontos extras
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Mestre não registra preço de referência

- **WHEN** um Mestre em sessão tenta registrar um preço de referência em pontos extras
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: Nenhum preço de referência fica abaixo de vinte pontos extras

O núcleo SHALL recusar com **422** todo preço de referência **menor que 20 pontos extras**,
inclusive zero e negativo, indicando o piso. O piso SHALL valer em qualquer vigência, também na
alteração de um preço já registrado. (`RF-07-44`, `RN-07-30`, invariante 23)

#### Scenario: Preço no piso é aceito

- **WHEN** um Admin registra um preço de referência de exatamente 20 pontos extras
- **THEN** o núcleo grava a vigência

#### Scenario: Preço abaixo do piso é recusado

- **WHEN** chega um preço de referência de 19 pontos extras
- **THEN** o núcleo responde 422 indicando o piso de 20 e nada é gravado

#### Scenario: Alteração para abaixo do piso é recusada

- **WHEN** um Admin tenta abrir vigência nova com preço menor que 20 para um tipo que já tem
  preço registrado
- **THEN** o núcleo responde 422 e a vigência anterior permanece como estava

### Requirement: As duas réguas do tipo de recurso não se convertem entre si

O tipo de recurso SHALL ter **duas réguas independentes**: o **valor de referência em moedas**,
que valora o aporte, e o **preço de referência em pontos extras**, que precifica a recompensa
avulsa. Nenhuma das duas SHALL ser derivada, calculada ou inferida a partir da outra nem a
partir de valor em reais, e registrar uma NEVER SHALL alterar a outra. Um tipo de recurso SHALL
poder ter apenas uma das duas réguas registrada. (`RF-07-38`, `RN-07-24`, `RN-07-25`,
invariante 23)

#### Scenario: Registrar preço em pontos não mexe no valor em moedas

- **WHEN** um Admin registra o preço de referência em pontos extras de um tipo que já tem valor
  de referência em moedas
- **THEN** o valor em moedas permanece exatamente como estava, e as duas vigências convivem

#### Scenario: Tipo com preço em pontos e sem valor em moedas

- **WHEN** um Admin registra apenas o preço de referência em pontos extras de um tipo de recurso
- **THEN** o núcleo grava a vigência do preço, e a consulta do valor em moedas daquele tipo
  devolve vazio

#### Scenario: Nenhuma rota devolve conversão entre as réguas

- **WHEN** o preço de referência em pontos extras de um tipo é consultado
- **THEN** a resposta traz o preço em pontos extras, e NEVER traz equivalência em moedas nem em
  reais
