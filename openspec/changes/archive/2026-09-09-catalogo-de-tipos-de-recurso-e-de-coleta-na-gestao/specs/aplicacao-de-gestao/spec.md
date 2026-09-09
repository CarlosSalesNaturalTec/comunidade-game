## ADDED Requirements

### Requirement: A App 03 abre a área Catálogos, fora do escopo de comunidade

A App 03 SHALL abrir ao **adulto em sessão** a área **Catálogos**, que reúne os catálogos da
plataforma cadastrados por Admin — **tipos de recurso** e **tipos de coleta**. A área SHALL ficar
ao lado de **Poderes**, que já é catálogo em área própria pela mesma razão: catálogo é bem comum
da plataforma, não dado de comunidade.

A área NEVER SHALL apresentar seletor de comunidade, e nenhuma das suas listas SHALL ser filtrada
por comunidade — o mesmo catálogo vale para todas.

Cada catálogo **sem tipo algum** SHALL ser apresentado como catálogo vazio — o estado de quem
ainda não cadastrou nenhum —, e a ausência NEVER SHALL ser apresentada como falha. As duas
apresentações SHALL ser **lista densa**, no temperamento Operação, como a dos poderes e a dos
locais do território. (`RF-02-107`, `RF-02-108`, documento 15 §6)

#### Scenario: A área reúne os dois catálogos

- **WHEN** o adulto em sessão abre a área Catálogos
- **THEN** a aplicação apresenta o catálogo de tipos de recurso e o de tipos de coleta, cada um
  em sua lista

#### Scenario: A área não pede comunidade

- **WHEN** o adulto em sessão abre a área Catálogos
- **THEN** nenhum seletor de comunidade lhe é apresentado, e as listas são as mesmas qualquer que
  seja a comunidade escolhida nas demais áreas

#### Scenario: Catálogo vazio não é apresentado como falha

- **WHEN** o adulto abre a área Catálogos e um dos dois catálogos não tem tipo algum cadastrado
- **THEN** a aplicação informa que aquele catálogo está vazio, como informação, e não como aviso
  de erro

### Requirement: A área Catálogos apresenta os tipos de recurso com o valor vigente

A App 03 SHALL apresentar cada **tipo de recurso** com **nome**, **natureza**, **unidade**, a
marca de **exige comprovante** e o **valor em moedas vigente** na data da consulta.

O núcleo devolve apenas o tipo com **valor de referência vigente na data**. A aplicação SHALL
informar, junto da lista, que é isso que ela mostra, para que o tipo cadastrado com vigência
futura não seja lido como cadastro perdido. (`RF-02-107`, `RF-07-01`, `RF-07-02`)

#### Scenario: A lista traz o valor da vigência corrente

- **WHEN** o adulto em sessão abre a área Catálogos e há tipos de recurso com valor vigente
- **THEN** a aplicação apresenta cada tipo com nome, natureza, unidade, a marca de exige
  comprovante e o valor em moedas da vigência corrente

#### Scenario: A lista diz que mostra apenas o que tem valor vigente

- **WHEN** a área apresenta o catálogo de tipos de recurso
- **THEN** a aplicação informa que a lista traz os tipos com valor de referência vigente na data

### Requirement: O Admin cadastra o tipo de recurso pela aplicação

A App 03 SHALL permitir ao **Admin** cadastrar tipo de recurso informando **nome**, **natureza**,
**unidade**, **valor de referência em moedas** e **início de vigência**, e opcionalmente a marca
de **exige comprovante**. O cadastro do tipo e a **primeira vigência do valor** SHALL acontecer
num **ato único**, como o núcleo já os grava — a aplicação NEVER SHALL oferecer dois passos.

A **natureza** SHALL ser escolhida entre as quatro previstas — consumível, durável, serviço e
financeiro — e NEVER SHALL ser digitada. A marca de **exige comprovante** SHALL nascer **falsa**
quando não declarada.

A recusa do núcleo — campo em falta, natureza fora das quatro, valor negativo ou com mais de duas
casas decimais — SHALL ser apresentada **em linguagem simples**, no campo que a originou, e nada
SHALL ser apresentado como cadastrado. O caminho de cadastro NEVER SHALL ser oferecido a quem não
é Admin (`RN-02-20`), e a escrita bem-sucedida SHALL aparecer na trilha de auditoria com autor,
papel, data e hora (`RN-02-21`). (`RF-02-107`, `RF-07-01`, `RF-07-02`, `RN-07-04`, `RN-07-22`)

#### Scenario: Admin cadastra o tipo com a primeira vigência no mesmo ato

- **WHEN** um Admin em sessão informa nome, natureza, unidade, valor em moedas e início de
  vigência, e confirma
- **THEN** o tipo passa a existir com aquele valor vigente, e a aplicação o apresenta na lista

#### Scenario: A natureza é escolhida, nunca digitada

- **WHEN** o Admin abre o formulário de tipo de recurso
- **THEN** a natureza lhe é oferecida como escolha entre consumível, durável, serviço e
  financeiro, sem campo de texto livre

#### Scenario: O tipo nasce sem exigir comprovante

- **WHEN** o Admin cadastra um tipo sem declarar a marca de exige comprovante
- **THEN** o tipo passa a existir com a marca falsa

#### Scenario: A recusa do núcleo é apresentada no campo

- **WHEN** o núcleo recusa o cadastro por valor com mais de duas casas decimais
- **THEN** a aplicação apresenta a recusa em linguagem simples, no campo do valor, e nenhum tipo
  passa a existir

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área Catálogos
- **THEN** o caminho de cadastro de tipo de recurso não lhe é oferecido

### Requirement: A área Catálogos apresenta os tipos de coleta com a marca de ativo

A App 03 SHALL apresentar cada **tipo de coleta** com **nome**, **forma de registro**, a
**unidade** e a **faixa esperada** quando houver, e a indicação de estar **ativo**. O tipo
**desativado** SHALL sair assinalado como tal, para que o Admin distinga o que o núcleo ainda
aceita em desafio novo do que ele já recusa.

A apresentação SHALL seguir a leitura **paginada** do núcleo até o fim, como a área Território já
faz com os locais. (`RF-02-108`, `RF-08-05`, `RF-08-06`, `RF-01-28`)

#### Scenario: A lista traz os tipos cadastrados

- **WHEN** o adulto em sessão abre a área Catálogos e há tipos de coleta cadastrados
- **THEN** a aplicação apresenta cada tipo com nome, forma de registro, unidade e faixa esperada
  quando houver, e a indicação de estar ativo

#### Scenario: O tipo por evidência aparece sem unidade e sem faixa

- **WHEN** a lista apresenta um tipo cuja forma de registro é foto ou vídeo
- **THEN** ele aparece sem unidade e sem faixa esperada, porque não produz valor a comparar

#### Scenario: O tipo desativado aparece assinalado

- **WHEN** o catálogo tem um tipo desativado
- **THEN** a aplicação o apresenta assinalado como não ativo

#### Scenario: A lista segue a paginação até o fim

- **WHEN** o catálogo de tipos de coleta tem mais tipos do que cabe numa página do núcleo
- **THEN** a aplicação apresenta todos, seguindo o cursor até o fim

### Requirement: O Admin cadastra o tipo de coleta pela aplicação

A App 03 SHALL permitir ao **Admin** cadastrar tipo de coleta informando **nome** e **forma de
registro**, e — apenas quando a forma for **número** — a **unidade** e a **faixa esperada**, com
mínimo e máximo. A forma de registro SHALL ser escolhida entre as três previstas — número, foto e
vídeo — e NEVER SHALL ser digitada.

Escolhida a forma **número**, a aplicação SHALL exigir unidade e faixa antes de deixar confirmar;
escolhida **foto** ou **vídeo**, NEVER SHALL pedir nenhuma das duas.

A recusa do núcleo — campo em falta, forma fora das três, tipo por número sem unidade ou sem
faixa, faixa com mínimo maior que o máximo — SHALL ser apresentada **em linguagem simples**, no
campo que a originou, e nada SHALL ser apresentado como cadastrado. O caminho de cadastro NEVER
SHALL ser oferecido a quem não é Admin (`RN-02-20`), e a escrita bem-sucedida SHALL aparecer na
trilha de auditoria com autor, papel, data e hora (`RN-02-21`). (`RF-02-108`, `RF-08-05`,
`RF-08-12`, `RF-08-21`)

#### Scenario: Admin cadastra o tipo que se mede por número

- **WHEN** um Admin em sessão informa nome, forma de registro número, unidade e faixa esperada, e
  confirma
- **THEN** o tipo passa a existir com a unidade e a faixa, e a aplicação o apresenta na lista

#### Scenario: A forma número exige unidade e faixa antes de confirmar

- **WHEN** o Admin escolhe a forma de registro número e deixa a unidade ou a faixa em branco
- **THEN** a aplicação exige as duas antes de deixar confirmar

#### Scenario: A forma por evidência dispensa unidade e faixa

- **WHEN** o Admin escolhe a forma de registro foto ou vídeo
- **THEN** a aplicação não pede unidade nem faixa esperada, e o cadastro se confirma sem elas

#### Scenario: A forma de registro é escolhida, nunca digitada

- **WHEN** o Admin abre o formulário de tipo de coleta
- **THEN** a forma de registro lhe é oferecida como escolha entre número, foto e vídeo, sem campo
  de texto livre

#### Scenario: A recusa da faixa é apresentada no campo

- **WHEN** o núcleo recusa o cadastro por faixa cujo mínimo é maior que o máximo
- **THEN** a aplicação apresenta a recusa em linguagem simples, no campo da faixa, e nenhum tipo
  passa a existir

#### Scenario: Quem não é Admin não alcança o cadastro

- **WHEN** um Mestre em sessão abre a área Catálogos
- **THEN** o caminho de cadastro de tipo de coleta não lhe é oferecido
