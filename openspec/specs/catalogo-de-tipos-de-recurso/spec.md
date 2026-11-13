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

### Requirement: Nenhum preço de referência fica abaixo de vinte e cinco pontos extras

O núcleo SHALL recusar com **422** todo preço de referência **menor que 25 pontos extras**,
inclusive zero e negativo, indicando o piso. O piso SHALL valer em qualquer vigência, também na
alteração de um preço já registrado. As vigências encerradas antes da elevação do piso
permanecem no histórico com o preço que tinham. (`RF-07-44`, `RN-07-30`, invariante 23)

#### Scenario: Preço no piso é aceito

- **WHEN** um Admin registra um preço de referência de exatamente 25 pontos extras
- **THEN** o núcleo grava a vigência

#### Scenario: Preço abaixo do piso é recusado

- **WHEN** chega um preço de referência de 24 pontos extras
- **THEN** o núcleo responde 422 indicando o piso de 25 e nada é gravado

#### Scenario: Alteração para abaixo do piso é recusada

- **WHEN** um Admin tenta abrir vigência nova com preço menor que 25 para um tipo que já tem
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

### Requirement: A gestão lê o catálogo de tipos de recurso

O núcleo SHALL devolver os tipos de recurso cadastrados com **nome**, **natureza**,
**unidade**, se **exige comprovante**, se está **ativo** e o **valor em moedas vigente** na data
da consulta, ordenados por nome. A leitura SHALL exigir persona **Admin ou Mestre** em sessão — o
Admin porque cadastra, o Mestre porque escolhe entre os tipos ao assumir uma necessidade como
absorção e precisa saber a natureza do tipo, que decide se há valor de origem em reais a
declarar, e se o tipo exige comprovante. Persona de qualquer outro papel SHALL receber **403**.
A **escrita** do catálogo segue privativa do Admin. (`RF-07-01`, `RF-07-52`, `RF-01-16`,
`RF-09-56`, `RF-09-57`)

Tipo de recurso sem valor de referência vigente na data da consulta NEVER SHALL quebrar a
leitura dos demais: ele SHALL sair da listagem, e os outros SHALL vir normalmente. O tipo
**desativado** SHALL sair na listagem, assinalado como não ativo, para que a aplicação o leia
pelo nome e não o ofereça em escolha nova.

#### Scenario: Admin lê o catálogo com o valor vigente

- **WHEN** um Admin em sessão consulta os tipos de recurso
- **THEN** vêm todos os cadastrados, com nome, natureza, unidade, a marca de ativo e o valor em
  moedas da vigência corrente

#### Scenario: Mestre lê o catálogo para escolher o tipo que absorve

- **WHEN** um Mestre em sessão consulta os tipos de recurso
- **THEN** vêm os mesmos campos que o Admin lê, com a natureza e a marca de exige comprovante

#### Scenario: O tipo desativado sai assinalado

- **WHEN** o catálogo tem um tipo de recurso desativado com valor vigente e a leitura é
  consultada
- **THEN** o tipo aparece assinalado como não ativo

#### Scenario: Quem não é Admin não lê o catálogo

- **WHEN** um Apoiador em sessão consulta os tipos de recurso
- **THEN** o núcleo responde 403

#### Scenario: O Mestre não cadastra tipo de recurso

- **WHEN** um Mestre em sessão tenta cadastrar um tipo de recurso
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O preço vigente abaixo do piso novo sobe para 25 na entrega

Na entrega do piso de 25, o núcleo SHALL abrir, para **todo tipo de recurso cuja vigência
aberta tem preço menor que 25**, uma vigência nova de **25 pontos extras** com início na data
da entrega, encerrando a anterior nessa mesma data. A vigência anterior NEVER SHALL ser
alterada no preço nem apagada: a troca feita antes da entrega continua lida pelo preço que
cobrou. Tipo com vigência aberta de 25 ou mais NEVER SHALL ganhar vigência nova. (`RF-07-50`,
`RF-07-43`, `RF-07-46`, 02 §8.2)

#### Scenario: Preço de 20 vigente sobe para 25

- **WHEN** a entrega é aplicada a um tipo cuja vigência aberta cobra 20 pontos extras
- **THEN** a vigência de 20 termina na data da entrega e uma vigência de 25 começa nela

#### Scenario: Preço de 40 vigente não muda

- **WHEN** a entrega é aplicada a um tipo cuja vigência aberta cobra 40 pontos extras
- **THEN** nenhuma vigência nova é aberta para ele

#### Scenario: A consulta por data anterior lê o preço antigo

- **WHEN** o preço de referência de um tipo elevado é consultado numa data anterior à entrega
- **THEN** o núcleo devolve o preço que vigorava naquela data

### Requirement: O Admin altera o nome, a unidade e a marca de exige comprovante do tipo

O núcleo SHALL permitir ao **Admin** em sessão alterar, em tipo de recurso já cadastrado, o
**nome**, a **unidade** e a marca de **exige comprovante**, um, dois ou os três no mesmo ato.
A **natureza** NEVER SHALL ser alterada: ela decide se há valor de origem em reais a declarar, e
a alteração que a traga SHALL ser recusada com **422**. Nome ou unidade em branco SHALL ser
recusados com **422**, indicando o campo. Persona de qualquer outro papel SHALL receber **403**,
e tipo inexistente SHALL receber **404**. A escrita SHALL gravar autoria, data e hora com fuso.

A alteração NEVER SHALL mexer nas vigências do valor em moedas nem do preço em pontos extras, e
o que já foi gravado com o tipo — aporte, lançamento, reserva, recompensa, item avulso — SHALL
continuar apontando para ele, lido com o nome e a unidade atuais. A marca de exige comprovante
alterada SHALL valer para o aporte registrado **depois** da alteração, nunca para o já gravado.
(`RF-07-51`, `RF-07-01`, `RN-07-22`, `RF-01-03`, `RF-01-16`)

#### Scenario: Admin corrige o nome de um tipo

- **WHEN** um Admin em sessão altera o nome de um tipo de recurso
- **THEN** o núcleo grava o nome novo com o autor, a data e a hora com fuso, e a leitura do
  catálogo passa a trazê-lo

#### Scenario: A natureza não se altera

- **WHEN** um Admin tenta alterar a natureza de um tipo de recurso
- **THEN** o núcleo responde 422 e o tipo permanece como estava

#### Scenario: Unidade em branco é recusada

- **WHEN** um Admin tenta alterar a unidade de um tipo para texto em branco
- **THEN** o núcleo responde 422 indicando a unidade e nada é gravado

#### Scenario: Alterar não mexe nas vigências

- **WHEN** um Admin altera o nome de um tipo que tem valor em moedas e preço em pontos vigentes
- **THEN** as vigências permanecem exatamente como estavam

#### Scenario: Passar a exigir comprovante não alcança o aporte já gravado

- **WHEN** um Admin marca que um tipo passa a exigir comprovante e há aporte daquele tipo já
  gravado sem comprovante
- **THEN** o aporte gravado segue válido, e o aporte novo daquele tipo sem comprovante passa a ser
  recusado

#### Scenario: Mestre não altera tipo de recurso

- **WHEN** um Mestre em sessão tenta alterar um tipo de recurso
- **THEN** o núcleo responde 403 e o tipo permanece como estava

### Requirement: O Admin abre vigência nova do valor em moedas de tipo já cadastrado

O núcleo SHALL permitir ao **Admin** em sessão registrar **valor de referência em moedas novo**
para tipo de recurso já cadastrado, com **início de vigência**, pela mecânica de vigência já
definida neste catálogo: a vigente se encerra no dia de início da nova, e nenhuma vigência é
reescrita nem apagada. As recusas SHALL ser as do valor de referência — negativo ou com mais de
duas casas decimais, **422**; outro papel, **403** —, e tipo inexistente SHALL receber **404**.
(`RF-07-51`, `RF-07-02`, `RN-07-03`, `RN-07-04`)

#### Scenario: Admin abre vigência nova do valor

- **WHEN** um Admin em sessão registra valor novo para um tipo que já tinha valor vigente
- **THEN** a vigência anterior se encerra no dia de início da nova e permanece consultável com o
  valor que tinha

#### Scenario: Valor novo com três casas é recusado

- **WHEN** um Admin registra valor novo com três casas decimais
- **THEN** o núcleo responde 422 e a vigência anterior permanece aberta

### Requirement: O tipo de recurso tem marca de ativo, e o desativado só bloqueia escolha nova

O núcleo SHALL manter em cada tipo de recurso se ele está **ativo**; o tipo SHALL nascer ativo,
e todo tipo cadastrado antes desta marca SHALL ficar ativo. O **Admin** em sessão SHALL poder
**desativar** e **reativar** o tipo; persona de qualquer outro papel SHALL receber **403**, e
tipo inexistente SHALL receber **404**. Desativar tipo já desativado e reativar tipo já ativo
SHALL ser aceitos sem efeito.

Tipo desativado SHALL ser recusado com **422** em toda **escolha nova** de tipo de recurso:
agendar aula declarando o recurso, registrar aporte, homologar declaração de aporte, absorção sem
necessidade de origem, declarar recompensa de marco, cadastrar item do catálogo avulso e propor
desafio extra. A desativação NEVER SHALL alterar o que já existe
com o tipo — saldo, reserva, necessidade publicada, recompensa declarada, item avulso, desafio,
missão, lançamento —, e o ato que só **segue** um fato já existente — absorção de necessidade
publicada, missão do Apoiador sobre necessidade publicada, transferência de saldo, entrega de
recompensa declarada, troca de item já cadastrado — SHALL continuar aceito. O catálogo governa a escolha, não o que já foi declarado.
(`RF-07-52`, `RF-07-01`, `RF-01-16`)

#### Scenario: Admin desativa um tipo de recurso

- **WHEN** um Admin em sessão desativa um tipo de recurso
- **THEN** o núcleo grava o tipo como não ativo, com o autor, a data e a hora com fuso

#### Scenario: Agendar aula com tipo desativado é recusado

- **WHEN** um Admin agenda uma aula declarando recurso de um tipo desativado
- **THEN** o núcleo responde 422 e nenhuma aula é agendada

#### Scenario: Declarar recompensa com tipo desativado é recusado

- **WHEN** um Mestre autor declara recompensa de marco de um tipo desativado
- **THEN** o núcleo responde 422 e nenhuma recompensa é declarada

#### Scenario: Desativar não mexe no que já existe

- **WHEN** um Admin desativa um tipo que tem saldo em ponto de apoio e recompensa declarada
- **THEN** o saldo e a recompensa seguem inalterados, e a entrega daquela recompensa continua
  aceita

#### Scenario: A absorção da necessidade já publicada segue aceita

- **WHEN** um Mestre assume como absorção a necessidade publicada de um tipo que foi desativado
  depois da publicação
- **THEN** o núcleo aceita a absorção pelas regras de sempre

#### Scenario: Admin reativa o tipo

- **WHEN** um Admin em sessão reativa um tipo de recurso desativado
- **THEN** o tipo volta a ser aceito em escolha nova

#### Scenario: Mestre não desativa tipo de recurso

- **WHEN** um Mestre em sessão tenta desativar ou reativar um tipo de recurso
- **THEN** o núcleo responde 403 e o tipo permanece como estava

### Requirement: Só o tipo de recurso nunca usado é excluído

O núcleo SHALL permitir ao **Admin** em sessão **excluir** tipo de recurso **nunca usado** — sem
nenhum registro, de qualquer entidade, que aponte para ele além das suas próprias vigências de
valor e de preço, que saem com ele. Tipo **já usado** SHALL ser recusado com **422**, dizendo que
o tipo está em uso e que o caminho é desativá-lo, e nada SHALL ser apagado. Persona de qualquer
outro papel SHALL receber **403**, e tipo inexistente SHALL receber **404**. A exclusão NEVER
SHALL apagar nem reescrever lançamento do livro-razão. (`RN-07-40`, `RF-07-01`, `RF-01-16`)

#### Scenario: Admin exclui tipo cadastrado por engano

- **WHEN** um Admin em sessão exclui um tipo de recurso que nenhum registro usa
- **THEN** o tipo e as suas vigências deixam de existir, e o catálogo não o traz mais

#### Scenario: Tipo usado não é excluído

- **WHEN** um Admin tenta excluir um tipo de recurso que já tem aporte, reserva, recompensa ou
  item avulso
- **THEN** o núcleo responde 422 dizendo que o tipo está em uso e pode ser desativado, e nada é
  apagado

#### Scenario: Mestre não exclui tipo de recurso

- **WHEN** um Mestre em sessão tenta excluir um tipo de recurso
- **THEN** o núcleo responde 403 e o tipo permanece
