## Purpose

O registro do que entra na plataforma — dinheiro, material, serviço ou trabalho absorvido —, em
nome de quem proveu, valorado em moedas pela tabela de referência vigente na data. É a única
porta de crédito do livro-razão e a origem do reconhecimento público de quem sustenta o projeto.

## Requirements

### Requirement: O aporte é registrado por Admin, com o ponto de apoio em que entra

O núcleo SHALL registrar o **aporte** com **provedor**, **tipo de recurso**, **quantidade**,
**ponto de apoio de entrada**, **comprovante**, **data do aporte** e **forma** — financeira,
material, serviço ou absorção. Registrar aporte SHALL exigir persona **Admin** em sessão;
persona de qualquer outro papel SHALL receber **403**. Aporte sem provedor, sem tipo, sem
quantidade, sem ponto de apoio ou sem data SHALL ser recusado com **422**, indicando o campo em
falta, e quantidade menor ou igual a zero SHALL ser recusada com **422**. O ponto de apoio SHALL
ser declarado qualquer que seja a natureza do tipo de recurso, inclusive serviço e financeiro.
Homologado o aporte, o núcleo SHALL gerar o **lançamento de crédito** no ponto de apoio
declarado. A escrita SHALL gravar autoria, data e hora com fuso. (`RF-07-04`, `RN-07-36`,
`RN-07-02`, `RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §§8, 9)

#### Scenario: Admin registra um aporte material

- **WHEN** um Admin em sessão registra um aporte com provedor, tipo, quantidade, ponto de apoio,
  comprovante e data
- **THEN** o núcleo grava o aporte e gera o lançamento de crédito daquele tipo naquele ponto de
  apoio, com autor, data e hora com fuso

#### Scenario: Aporte sem ponto de apoio é recusado

- **WHEN** chega um registro de aporte sem ponto de apoio
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Aporte de serviço também declara o ponto de apoio

- **WHEN** um Admin registra um aporte de tipo de natureza serviço, declarando o ponto de apoio
- **THEN** o núcleo grava o aporte e credita o saldo daquele tipo naquele ponto de apoio

#### Scenario: Mestre não registra aporte pela rota da gestão

- **WHEN** um Mestre em sessão tenta registrar um aporte pela rota da gestão
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Quantidade zero é recusada

- **WHEN** chega um registro de aporte com quantidade zero
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O aporte é valorado pela tabela vigente na data do aporte

O núcleo SHALL converter todo aporte em **moedas** pelo valor de referência do seu tipo de
recurso **vigente na data do aporte**, e não na data do registro. O valor em moedas SHALL ser o
produto da quantidade pelo valor de referência, guardado em decimal exato de **duas casas**.
Abrir vigência nova para um tipo NÃO SHALL alterar o valor em moedas de aporte já registrado.
Aporte cuja data não esteja coberta por nenhuma vigência do tipo SHALL ser recusado com **422**.
(`RF-07-05`, `RN-07-03`, `RN-07-04`, PRD-07 §12)

#### Scenario: Conversão pela tabela vigente

- **WHEN** um aporte de quantidade 3 é registrado para um tipo cujo valor de referência vigente
  na data do aporte é 0,50 moeda
- **THEN** o aporte é gravado com 1,50 moeda

#### Scenario: Valor novo não reescreve o passado

- **WHEN** o valor de referência de um tipo muda depois de um aporte daquele tipo já registrado
- **THEN** o valor em moedas do aporte já registrado permanece o que era

#### Scenario: Data do aporte anterior à vigência mais antiga

- **WHEN** chega um aporte cuja data não é coberta por nenhuma vigência do seu tipo
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: Quem homologa o aporte não pode ser o provedor

Na rota de registro pela gestão, o núcleo SHALL recusar com **403** o aporte cujo **provedor
seja a própria persona que o registra**. A recusa NÃO SHALL alcançar o aporte por absorção, que
não passa por homologação. (`RN-07-16`, `RN-07-35`, PRD-07 §9)

#### Scenario: Admin registra aporte em nome de si mesmo

- **WHEN** um Admin em sessão registra, pela rota da gestão, um aporte cujo provedor é ele
  próprio
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Admin registra aporte de outro provedor

- **WHEN** um Admin em sessão registra um aporte cujo provedor é outra persona
- **THEN** o núcleo grava o aporte e credita o saldo

### Requirement: O aporte por absorção credita no ato e nasce ressarcível

O núcleo SHALL registrar **aporte por absorção** em nome do **Mestre ou Admin** que proveu o
recurso sem receber. A absorção SHALL **creditar no ato**, sem homologação, e o campo do Admin
homologador SHALL ficar vazio. O aporte por absorção SHALL nascer marcado como **ressarcível**,
com situação de ressarcimento **em aberto**. Persona de papel diferente de Mestre ou Admin SHALL
receber **403**. Aporte registrado pela gestão SHALL nascer **não ressarcível**. (`RF-07-06`,
`RF-07-21`, `RN-07-06`, `RN-07-35`, PRD-07 §§9, 12)

#### Scenario: Mestre absorve um recurso

- **WHEN** um Mestre em sessão registra um aporte por absorção com tipo, quantidade e ponto de
  apoio
- **THEN** o núcleo grava o aporte em nome dele, credita o saldo no ato, deixa o homologador
  vazio e marca o aporte como ressarcível com situação em aberto

#### Scenario: Admin absorve um recurso em nome próprio

- **WHEN** um Admin em sessão registra um aporte por absorção em nome de si mesmo
- **THEN** o núcleo grava e credita, sem aplicar a recusa da homologação em causa própria

#### Scenario: Apoiador não absorve

- **WHEN** um Apoiador em sessão tenta registrar um aporte por absorção
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Aporte da gestão não nasce ressarcível

- **WHEN** um Admin registra um aporte pela rota da gestão
- **THEN** o aporte é gravado com situação de ressarcimento "não se aplica"

### Requirement: O aporte que fecha a diferença confirma a aula pendente de lastro

O núcleo SHALL, ao creditar um aporte, verificar as aulas em situação **pendente de lastro** no
**ponto de apoio** daquele aporte. Toda aula cuja lista inteira de recursos declarados passe a
ter **quantidade disponível** bastante SHALL ser **confirmada no mesmo ato**, com as reservas
efetivadas — sem ato humano de confirmação à parte. Aula cuja falta continue em qualquer parcela
SHALL permanecer **pendente de lastro**, sem reserva alguma. Havendo mais de uma aula
confirmável pelo mesmo aporte e disponível para menos que todas, o núcleo SHALL atendê-las pelo
**horário inicial da aula, da mais próxima para a mais distante**. A confirmação SHALL registrar autor e momento, como toda escrita.
(`RN-07-37`, `RF-07-08`, `RN-07-01`, `RF-01-03`, invariante 9 do documento 99 §6, documento
04 §1)

#### Scenario: Aporte que fecha a falta confirma a aula

- **WHEN** um aporte homologado entra no ponto de apoio de uma aula pendente de lastro e cobre
  toda a falta dela
- **THEN** a aula passa a confirmada e as reservas dela são efetivadas no mesmo ato

#### Scenario: Aporte insuficiente não confirma nada

- **WHEN** um aporte homologado cobre parte da falta de uma aula pendente de lastro
- **THEN** a aula segue pendente de lastro e nenhuma reserva é gravada

#### Scenario: Aporte em outro ponto de apoio não confirma a aula

- **WHEN** um aporte do tipo que falta entra num ponto de apoio diferente do da aula
- **THEN** a aula segue pendente de lastro

#### Scenario: Aula de data mais próxima é atendida primeiro

- **WHEN** um aporte fecha a falta de duas aulas pendentes de lastro, mas só tem disponível
  para uma
- **THEN** o núcleo confirma a aula cujo horário inicial é o mais próximo e mantém a outra
  pendente de lastro

#### Scenario: Absorção também confirma

- **WHEN** um aporte por absorção, que credita no ato, cobre a falta de uma aula pendente de
  lastro
- **THEN** a aula passa a confirmada e as reservas são efetivadas

### Requirement: O comprovante é anexado e nunca servido em rota pública

O núcleo SHALL aceitar o **comprovante** do aporte em **PDF, JPG ou PNG** e SHALL recusar com
**422** qualquer outro formato. O comprovante SHALL ser exigido quando o tipo de recurso o
exigir, e a falta dele nesse caso SHALL ser recusada com **422**. O núcleo NÃO SHALL confirmar
transferência automaticamente: a conferência é ato de Admin. Nenhuma rota SHALL devolver o
comprovante sem credencial de gestão, e nenhum campo do aporte SHALL aceitar chave PIX, banco ou
conta. (`RN-07-22`, `RN-07-20`, PRD-07 §§9, 11)

#### Scenario: Comprovante em PDF é aceito

- **WHEN** um aporte é registrado com comprovante em PDF
- **THEN** o núcleo grava o aporte e guarda o comprovante pela porta de armazenamento

#### Scenario: Comprovante em formato não previsto é recusado

- **WHEN** chega um aporte com comprovante que não é PDF, JPG nem PNG
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Tipo que exige comprovante recusa aporte sem ele

- **WHEN** chega um aporte de tipo que exige comprovante, sem comprovante anexado
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

### Requirement: O aporte aceita período apurado anterior à entrada do livro-razão no ar

O núcleo SHALL aceitar aporte cuja **data e período apurado** sejam anteriores à entrada do
livro-razão em operação, desde que o comprovante esteja anexado, para que o custo já incorrido
seja lançado retroativamente. A conversão em moedas SHALL seguir a vigência da **data do
aporte**, como em qualquer outro. (`RF-07-32`, `RF-07-05`, PRD-07 §8)

#### Scenario: Aporte retroativo com comprovante

- **WHEN** um Admin registra um aporte com data e período apurado anteriores à entrada do
  livro-razão no ar, com comprovante anexado
- **THEN** o núcleo grava o aporte, valorado pela vigência da data do aporte, e credita o saldo

### Requirement: Aporte de tipo inexistente aponta o cadastro do tipo

O núcleo SHALL recusar com **422** o aporte que referencie tipo de recurso inexistente, e a
resposta SHALL apontar a **rota de cadastro do tipo**, para que o Admin cadastre o tipo e o
valor de referência e retome o registro sem que o fluxo se perca. (`RF-07-03`, PRD-07 §9)

#### Scenario: Aporte de tipo que não está no catálogo

- **WHEN** chega um aporte que referencia um tipo de recurso inexistente
- **THEN** o núcleo responde 422 apontando a rota de cadastro do tipo, e nada é gravado

#### Scenario: Tipo cadastrado no ato e aporte retomado

- **WHEN** o Admin cadastra o tipo com o seu valor de referência e registra o aporte de novo
- **THEN** o núcleo grava o aporte e credita o saldo, sem exigir nenhum outro passo

### Requirement: O aporte declarado no pré-cadastro só credita ao ser registrado

O núcleo SHALL guardar em cada aporte a **origem do registro** — gestão ou pré-cadastro — e,
quando a origem for o pré-cadastro, a **solicitação de participação de origem** que o declarou.
O aporte declarado numa solicitação de participação NÃO SHALL creditar moeda alguma enquanto
existir apenas como declaração; o crédito SHALL nascer somente do registro do aporte por um
Admin, que é o ato de **homologação** e que converte o valor em moedas pela vigência da data.
Registrar mais de um aporte apontando a **mesma** solicitação de origem SHALL ser recusado com
**422**, para que a mesma declaração não credite duas vezes. (`RF-07-30`, `RN-07-21`,
`RF-07-05`, PRD-07 §8)

#### Scenario: Declaração no pré-cadastro não credita

- **WHEN** uma solicitação de participação é registrada com aporte declarado e comprovante
- **THEN** nenhum lançamento é gerado e o saldo de todo tipo de recurso permanece como estava

#### Scenario: Registro pelo Admin homologa e credita

- **WHEN** um Admin registra o aporte apontando a solicitação de participação de origem
- **THEN** o núcleo grava o aporte com origem "pré-cadastro", converte em moedas pela vigência
  da data do aporte e gera o lançamento de crédito

#### Scenario: Mesma solicitação não credita duas vezes

- **WHEN** um segundo aporte é registrado apontando uma solicitação de origem já homologada
- **THEN** o núcleo responde 422 e nada é gravado
