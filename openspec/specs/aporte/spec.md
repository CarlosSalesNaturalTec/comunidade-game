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

### Requirement: O aporte declara a destinação do que entra

O núcleo SHALL registrar em todo aporte a **destinação** do que entra — **lastro** ou
**ressarcimento**. Aporte sem destinação declarada SHALL nascer com destinação **lastro**, que é
o caso comum. Destinação fora dos dois valores previstos SHALL ser recusada com **422**.

O aporte de destinação **ressarcimento** SHALL creditar o **Poder Sustentador** de quem doou,
como qualquer outro aporte, e NÃO SHALL virar lastro: NÃO SHALL compor o saldo de recurso algum
e NÃO SHALL confirmar aula pendente de lastro. É o que impede o mesmo dinheiro de destravar uma
aula e devolver a quem absorveu.

Aporte de forma **absorção** NÃO SHALL ter destinação ressarcimento: quem absorve provê recurso,
não doa dinheiro para devolver a terceiro — a tentativa SHALL ser recusada com **422**.
(`RF-07-23`, `RN-07-38`, PRD-07 §8)

#### Scenario: Doação destinada a ressarcir credita sem virar lastro

- **WHEN** um Admin registra um aporte financeiro com destinação ressarcimento
- **THEN** o Poder Sustentador do doador sobe pelas moedas do aporte, e o saldo daquele tipo de
  recurso no ponto de apoio permanece como estava

#### Scenario: A receita destinada não confirma aula pendente de lastro

- **WHEN** existe uma aula pendente de lastro cuja falta é exatamente do tipo de recurso da
  doação, e entra um aporte de destinação ressarcimento que cobriria a diferença
- **THEN** a aula permanece pendente de lastro e nenhuma reserva é criada

#### Scenario: Aporte sem destinação declarada é de lastro

- **WHEN** um Admin registra um aporte sem declarar destinação
- **THEN** o aporte é gravado com destinação lastro e credita o saldo normalmente

#### Scenario: Absorção não se destina a ressarcimento

- **WHEN** um Mestre tenta registrar uma absorção com destinação ressarcimento
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O aporte por absorção credita no ato e nasce ressarcível

O núcleo SHALL registrar **aporte por absorção** em nome do **Mestre ou Admin** que proveu o
recurso sem receber. A absorção SHALL **creditar no ato**, sem homologação, e o campo do Admin
homologador SHALL ficar vazio. O aporte por absorção de tipo de natureza **consumível, durável
ou financeira** SHALL nascer marcado como **ressarcível**, com situação de ressarcimento **em
aberto**. Persona de papel diferente de Mestre ou Admin SHALL receber **403**. Aporte registrado
pela gestão SHALL nascer **não ressarcível**.

A absorção de tipo de natureza **serviço** SHALL nascer **não ressarcível**, com situação de
ressarcimento **não se aplica**: quem absorve serviço dá tempo, não dinheiro, e não há
desembolso a devolver. Ela credita o **Poder Sustentador** e conta no **selo de absorções**
como qualquer outra.

A absorção SHALL poder declarar a **aula cuja necessidade atende** — é como quem cobre uma falta
publicada declara qual falta cobriu. A aula declarada SHALL ser uma aula existente e o tipo de
recurso do aporte SHALL ser um dos que aquela aula consome; fora disso, o registro SHALL ser
recusado com **422**. A necessidade segue **derivada**, sem tabela a referenciar: a declaração
liga o aporte à aula, não a um registro de necessidade. A aula SHALL ser gravada **apenas** na
forma absorção; aporte de outra forma que a declare SHALL ser recusado com **422**.

A absorção SHALL exigir o **valor de origem em reais** quando o tipo de recurso for de natureza
**consumível, durável ou financeira** — houve desembolso, e é esse valor que o ressarcimento
devolve; sem ele o registro SHALL ser recusado com **422**. Na natureza **serviço** o valor de
origem SHALL ficar **vazio** e NÃO SHALL ser exigido: o valor daquele aporte é o **em moedas**,
que a tabela de referência já fornece, e reais e moedas NÃO SHALL ser convertidos um no outro.
(`RF-07-06`, `RF-07-21`, `RF-07-28`, `RN-07-06`, `RN-07-24`, `RN-07-35`, `RN-07-39`,
PRD-07 §§8, 9, 12)

#### Scenario: Mestre absorve um recurso

- **WHEN** um Mestre em sessão registra um aporte por absorção com tipo, quantidade, ponto de
  apoio e o valor de origem em reais
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

#### Scenario: Mestre assume a necessidade publicada de uma aula

- **WHEN** um Mestre registra uma absorção declarando a aula cuja necessidade atende, de um tipo
  que aquela aula consome
- **THEN** o núcleo grava o aporte com a aula declarada e credita o saldo no ponto de apoio da
  aula

#### Scenario: Absorção de tipo que a aula não consome é recusada

- **WHEN** um Mestre declara uma aula cuja lista de recursos não inclui o tipo do aporte
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Absorção com desembolso exige o valor em reais

- **WHEN** um Mestre registra uma absorção de tipo de natureza consumível sem o valor de origem
- **THEN** o núcleo responde 422 indicando o campo em falta e nada é gravado

#### Scenario: Absorção de serviço não exige valor em reais e não é ressarcível

- **WHEN** um Mestre registra uma absorção de tipo de natureza serviço sem o valor de origem
- **THEN** o núcleo grava o aporte com o valor de origem vazio, situação de ressarcimento "não
  se aplica", e o Poder Sustentador dele sobe pelas moedas do aporte

#### Scenario: Absorção de serviço não entra na fila de ressarcimento

- **WHEN** um Mestre absorve um serviço e um Admin consulta os aportes ressarcíveis
- **THEN** aquele aporte não aparece na fila, e a contagem de absorções do Mestre segue
  contando-o

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
**422**, para que a mesma declaração não credite duas vezes. (`RF-07-29`, `RF-07-30`,
`RN-07-21`, `RF-07-05`, PRD-07 §8)

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

### Requirement: O Apoiador declara o aporte pela App 08, e a declaração nasce pendente

O núcleo SHALL aceitar do **Apoiador em sessão** a declaração de um aporte em dinheiro, com o
**valor transferido**, o **comprovante** e a **origem da escolha** — uma **missão aberta**, uma
necessidade de recurso publicada, um valor sugerido da escada do perfil declarado ou um valor
livre. Declarado por missão, o aporte SHALL apontar a missão escolhida e SHALL aceitar a
missão **inteira ou parte dela**; missão **concluída**, **vencida** ou inexistente SHALL ser
recusada com **409**, dizendo o que aconteceu com ela. A declaração SHALL nascer **pendente** e
NEVER SHALL, enquanto pendente, gerar lançamento, creditar saldo de tipo de recurso, compor o
Poder Sustentador, abater o que falta a necessidade ou missão alguma, ou concluir missão. O
comprovante SHALL ser obrigatório e SHALL seguir os formatos já aceitos no pré-cadastro; sem
ele, ou em formato não aceito, o núcleo SHALL responder **422** com os formatos válidos.
(`RF-14-25`, `RF-14-26`, `RF-14-63`, `RN-14-06`, `RN-14-07`, `RN-14-32`, PRD-14 §§5.3, 5.4, 9,
12)

#### Scenario: A declaração entra pendente e não credita

- **WHEN** o Apoiador declara um aporte com valor e comprovante
- **THEN** a declaração é gravada como pendente, nenhum lançamento é gerado e o Poder
  Sustentador dele permanece como estava

#### Scenario: A declaração por necessidade não abate o que falta

- **WHEN** o Apoiador declara o aporte escolhendo uma necessidade de recurso publicada
- **THEN** a declaração guarda a necessidade escolhida e a lista de necessidades continua
  mostrando a mesma quantidade faltante de antes

#### Scenario: A declaração por missão aceita a parte e não abate nada

- **WHEN** o Apoiador declara um aporte por parte do que uma missão aberta pede
- **THEN** a declaração guarda a missão escolhida e a missão continua mostrando o mesmo quanto
  falta de antes

#### Scenario: Missão fechada recusa a declaração

- **WHEN** o Apoiador declara aporte por uma missão já concluída ou vencida
- **THEN** o núcleo responde 409 dizendo o que aconteceu com a missão e nada é gravado

#### Scenario: Sem comprovante a declaração é recusada

- **WHEN** a declaração chega sem comprovante ou em formato não aceito
- **THEN** o núcleo responde 422 com os formatos válidos e nada é gravado

### Requirement: A declaração pela App 08 é sempre em dinheiro

O núcleo SHALL aceitar pela App 08 apenas o aporte em **dinheiro** e NEVER SHALL aceitar por
essa via aporte em material, serviço ou divulgação; recebendo a declaração de qualquer uma
dessas formas, SHALL responder **422** com a orientação de procurar a gestão, que os registra
com termo de doação ou registro do material. (`RF-14-28`, `RN-14-05`, PRD-14 §§3.2, 9, 12)

#### Scenario: Aporte em material devolve a orientação

- **WHEN** a declaração chega com forma de material, serviço ou divulgação
- **THEN** o núcleo responde 422 com a orientação de procurar a gestão e nada é gravado

### Requirement: O Apoiador acompanha a situação de cada declaração

O núcleo SHALL responder ao **Apoiador em sessão** a situação de cada declaração dele —
**pendente**, **homologada** ou **recusada** —, com o **valor declarado da transferência**, a
data, a origem da escolha e, na recusada, o **motivo** em linguagem simples. O valor sai como o
Apoiador o declarou, porque a valoração em moedas só nasce na homologação, pela vigência da
data do aporte (`RF-07-05`); apresentá-lo é da aplicação. A leitura SHALL alcançar apenas as
declarações do próprio Apoiador e NEVER SHALL exibir declaração de outra pessoa. (`RF-14-27`,
PRD-14 §§5.3, 9)

#### Scenario: As três situações aparecem ao Apoiador

- **WHEN** o Apoiador lê as próprias declarações
- **THEN** cada uma sai com a situação, o valor declarado, a data e a origem da escolha, e a
  recusada traz também o motivo

#### Scenario: A leitura não alcança declaração alheia

- **WHEN** o Apoiador lê as próprias declarações e existem declarações de outro Apoiador
- **THEN** a resposta traz apenas as dele

### Requirement: O Admin homologa a declaração registrando o aporte, e nunca a própria

O núcleo SHALL converter uma declaração pendente em aporte quando um **Admin** registrar o
aporte apontando a **declaração de origem**: o aporte SHALL nascer com **origem do registro
"App 08"**, SHALL ser valorado em moedas pela vigência da **data do aporte** e SHALL gerar o
lançamento de crédito, e a declaração SHALL passar a **homologada**. Registrar mais de um
aporte apontando a **mesma** declaração SHALL ser recusado com **422**. O Admin que homologa
NEVER SHALL ser o provedor da declaração; sendo, o núcleo SHALL responder **403**.

Sendo a declaração por **missão**, a mesma homologação SHALL abater o que falta àquela missão
e, quando o saldo fechar, SHALL concluí-la e creditar o selo dela a **cada participante**, no
mesmo ato. Fechando o saldo ou não, as moedas creditadas SHALL ser as do aporte de cada um.
(`RF-14-26`, `RF-14-64`, `RF-14-65`, `RF-14-66`, `RN-14-07`, `RN-14-08`, `RN-14-32`,
`RN-14-34`, PRD-14 §§5.3, 5.4, 8, 12)

#### Scenario: A homologação credita e fecha a declaração

- **WHEN** um Admin registra o aporte apontando a declaração de origem
- **THEN** o aporte é gravado com origem "App 08", convertido pela vigência da data do aporte,
  o lançamento de crédito é gerado e a declaração passa a homologada

#### Scenario: A homologação parcial abate e não conclui

- **WHEN** o Admin homologa uma declaração por missão que cobre parte do que ela pede
- **THEN** o quanto falta da missão cai pelo valor homologado, a missão segue aberta e nenhum
  selo é creditado

#### Scenario: A homologação que fecha o saldo conclui e credita os selos

- **WHEN** o Admin homologa a declaração que faz o que falta da missão chegar a zero
- **THEN** a missão passa a concluída e cada participante recebe o selo dela, cada um com as
  moedas do próprio aporte

#### Scenario: A mesma declaração não credita duas vezes

- **WHEN** um segundo aporte é registrado apontando uma declaração já homologada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: O provedor não homologa a própria declaração

- **WHEN** quem registra o aporte é o mesmo Apoiador que declarou
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O Admin recusa a declaração com motivo, e a recusa não credita

O núcleo SHALL permitir que um **Admin** recuse uma declaração **pendente**, com **motivo
obrigatório**, e a declaração SHALL passar a **recusada**, com o motivo visível ao Apoiador que
a fez. A recusa NEVER SHALL gerar lançamento nem creditar moeda. Recusar declaração que não
esteja pendente SHALL ser respondido com **409**, e recusar sem motivo, com **422**.
(`RF-14-27`, `RN-14-07`, decisão do fundador de 2026-09-01)

#### Scenario: A recusa grava o motivo e não credita

- **WHEN** um Admin recusa uma declaração pendente com motivo
- **THEN** a declaração passa a recusada com o motivo, nenhum lançamento é gerado e o Poder
  Sustentador permanece como estava

#### Scenario: Declaração já resolvida não se recusa

- **WHEN** um Admin recusa uma declaração já homologada ou já recusada
- **THEN** o núcleo responde 409 e nada muda

#### Scenario: Recusa sem motivo não é aceita

- **WHEN** a recusa chega sem motivo
- **THEN** o núcleo responde 422 e a declaração continua pendente
