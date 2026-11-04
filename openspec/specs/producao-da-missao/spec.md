# producao-da-missao Specification

## Purpose

A produção da missão é o que se entrega depois de trabalhar uma atividade — por texto, fala ou
foto do manuscrito — e a devolutiva construtiva que a plataforma lê de volta, sem creditar
ponto algum. A **mídia é guardada** desde 2026-11-03, e a **transcrição continua**, porque é
sobre ela que a devolutiva se faz. Duas portas: a da **equipe**, sobre a atividade corrente do
encontro, e a **individual** do Guerreiro(a), sobre uma missão do próprio percurso.

## Requirements

### Requirement: A equipe entrega a produção por texto, fala ou foto, e a mídia fica guardada

O núcleo SHALL aceitar, de uma equipe, a entrega da produção da missão em **uma** destas três
formas: **texto** digitado, **áudio** da fala ou **foto** do que a equipe fez à mão. A forma da
entrega SHALL ser **declarada na chamada** e gravada com a produção — é ela que distingue a
fala do texto digitado, que chegam ambos como texto.

Entrega em **texto** SHALL trazer o **texto** e NEVER SHALL trazer arquivo. Entrega em
**áudio** SHALL trazer a **transcrição** feita no aparelho **e** o **arquivo** do áudio, que o
núcleo passa a guardar. Entrega em **foto** SHALL trazer o **arquivo** e NEVER SHALL trazer
texto. Entrega sem o conteúdo da forma declarada, ou com o
conteúdo de outra forma junto, SHALL ser recusada com **422**.

A produção SHALL ser ancorada na **atividade corrente** que a equipe declarou na programação
do encontro, e SHALL guardar a **missão** daquela atividade. Equipe sem atividade corrente
declarada SHALL ser recusada com **422** — não há missão a que a produção pertença.
(`RF-04-45`, `RF-05-76`, `RN-05-32`, documento 03 §§1.12, 4.2, documento 11 §2.2)

#### Scenario: Entrega por texto

- **WHEN** uma equipe com atividade corrente declarada entrega a produção em texto
- **THEN** o núcleo grava a produção com a forma "texto", a missão e a atividade daquela
  escolha

#### Scenario: Entrega por fala

- **WHEN** uma equipe entrega a produção falada, já transcrita no aparelho
- **THEN** o núcleo grava a produção com a forma "áudio", a transcrição recebida e o arquivo
  do áudio

#### Scenario: Entrega por foto do manuscrito

- **WHEN** uma equipe entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega sem conteúdo é recusada

- **WHEN** chega uma entrega sem texto e sem arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega com texto e foto juntos
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega por fala sem a transcrição é recusada

- **WHEN** chega uma entrega com a forma "áudio" trazendo o arquivo e nenhuma transcrição
- **THEN** o núcleo responde 422 e nada é gravado, porque a devolutiva se faz sobre o texto

#### Scenario: Equipe sem atividade corrente não entrega

- **WHEN** uma equipe que ainda não declarou a atividade que está trabalhando tenta entregar
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A produção é da equipe e vale para todos os integrantes

A entrega feita no aparelho da equipe SHALL gerar **um único** registro, vinculado à **equipe
da aula** e válido para **todos** os integrantes dela — o mesmo desenho da resposta de quiz
(`RN-04-22`). O núcleo NEVER SHALL duplicar a produção por integrante, e a produção coletiva
SHALL ficar **sem Guerreiro(a)** declarado: quem responde por ela é a equipe.

A produção SHALL aparecer no histórico de **cada** integrante daquela equipe, pela composição
gravada. Decisão do fundador, 2026-08-30. (`RF-04-45`, documento 02 §5, documento 03 §4.2)

#### Scenario: Uma entrega gera um registro para a equipe

- **WHEN** um integrante entrega a produção pelo aparelho de uma equipe de cinco
- **THEN** o núcleo grava uma única produção, da equipe, e nenhuma cópia por integrante

#### Scenario: A produção da equipe alcança todos os integrantes

- **WHEN** se consulta a produção de um integrante que não foi quem enviou
- **THEN** a produção da equipe está entre as dele

#### Scenario: A produção coletiva não nomeia um Guerreiro(a)

- **WHEN** o núcleo grava a produção entregue pela equipe
- **THEN** o registro sai com a equipe declarada e o Guerreiro(a) em branco

### Requirement: O Guerreiro(a) entrega sozinho a produção da missão, e a mídia fica guardada

O núcleo SHALL aceitar, de um **Guerreiro(a) em sessão**, a entrega da produção de uma missão
em **uma** destas três formas: **texto** digitado, **áudio** da fala ou **foto** do que ele fez
à mão. A forma SHALL ser declarada na chamada e gravada com a produção.

Entrega em **texto** SHALL trazer o **texto** e NEVER SHALL trazer arquivo; entrega em
**áudio** SHALL trazer a **transcrição** e o **arquivo** do áudio;
entrega em **foto** SHALL trazer o **arquivo** e NEVER SHALL trazer texto. Entrega sem o
conteúdo da forma declarada, ou com o conteúdo de outra forma junto, SHALL ser recusada com
**422** — as mesmas recusas da entrega da equipe.

A produção SHALL ser ancorada em uma **atividade daquela missão**, declarada na entrega.
Atividade que não pertence à missão SHALL ser recusada com **422**.

A missão SHALL ser do **percurso do próprio Guerreiro(a)**: em trilha em que ele está
**inscrito** e por ele **desbloqueada**. Missão de trilha em que não está inscrito SHALL ser
recusada com **422**, e missão que ele ainda não desbloqueou SHALL ser recusada com **422** —
o percurso é o mesmo que já governa a leitura da missão, e a entrega não o atravessa.
(`RF-05-74`, `RF-05-76`, `RN-05-32`, `RN-05-35`, PRD-05 §9)

#### Scenario: Entrega individual por texto

- **WHEN** o Guerreiro(a) em sessão entrega, em texto, a produção de uma atividade de missão
  que ele desbloqueou em trilha em que está inscrito
- **THEN** o núcleo grava a produção com a forma "texto", a missão e a atividade declaradas

#### Scenario: Entrega individual por fala

- **WHEN** o Guerreiro(a) entrega a produção falada, já transcrita no aparelho
- **THEN** o núcleo grava a produção com a forma "áudio", a transcrição recebida e o arquivo
  do áudio

#### Scenario: Entrega individual por foto do manuscrito

- **WHEN** o Guerreiro(a) entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega individual sem conteúdo é recusada

- **WHEN** chega uma entrega individual sem texto e sem arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega individual com texto e foto juntos
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual por fala sem a transcrição é recusada

- **WHEN** chega uma entrega individual com a forma "áudio" sem a transcrição
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Atividade de outra missão é recusada

- **WHEN** o Guerreiro(a) declara, na entrega, uma atividade que não pertence à missão indicada
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Missão de trilha não inscrita é recusada

- **WHEN** o Guerreiro(a) tenta entregar a produção de uma missão de trilha em que não está
  inscrito
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Missão ainda não desbloqueada é recusada

- **WHEN** o Guerreiro(a) tenta entregar a produção de uma missão que ele ainda não desbloqueou
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A produção individual é do Guerreiro(a), nunca da equipe

A entrega feita pelo Guerreiro(a) em sessão SHALL gerar **um único** registro, vinculado a
**ele** e com a **equipe em branco** — o espelho da produção coletiva, que nasce com a equipe
declarada e sem Guerreiro(a). O núcleo NEVER SHALL gravar uma produção com equipe e
Guerreiro(a) ao mesmo tempo, nem com nenhum dos dois.

A produção individual SHALL aparecer no histórico **apenas** do Guerreiro(a) que a entregou, e
NEVER SHALL alcançar colega algum, ainda que ele trabalhe a mesma missão. (`RF-05-74`,
`RN-05-21`, PRD-05 §8)

#### Scenario: A entrega individual nasce com o Guerreiro(a) declarado

- **WHEN** o Guerreiro(a) em sessão entrega a produção de uma missão dele
- **THEN** o núcleo grava uma única produção, com ele declarado e a equipe em branco

#### Scenario: A produção individual não alcança colegas

- **WHEN** se consulta a produção de um colega da mesma trilha
- **THEN** a produção individual de outro Guerreiro(a) não está entre as dele

### Requirement: A entrega individual é alcançável por HTTP pelo Guerreiro(a) em sessão

O núcleo SHALL expor a entrega individual por `POST /v1/eu/missoes/{id}/producao`, sob a
**sessão do Guerreiro(a)**, e sob a chave de aplicação, pelas convenções de erro do PRD-01.
Persona que não é Guerreiro(a) — Mestre ou Admin — SHALL receber **403**: a produção é da
criança, como já vale na porta da equipe. Chamada sem persona em sessão SHALL ser recusada.

A resposta SHALL trazer a produção gravada, com a **transcrição** e a **devolutiva**.
(`RF-05-74`, `RF-05-75`, `RF-01-16`, PRD-05 §9)

#### Scenario: O Guerreiro(a) entrega pela porta

- **WHEN** o Guerreiro(a) em sessão envia a produção de uma missão do percurso dele
- **THEN** o núcleo responde 201 com a produção gravada, a transcrição e a devolutiva

#### Scenario: A gestão não entrega pelo Guerreiro(a)

- **WHEN** um Mestre ou um Admin em sessão tenta entregar a produção individual
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Sem sessão de persona a porta não abre

- **WHEN** chega uma entrega individual sem credencial de persona
- **THEN** o núcleo recusa e nada é gravado

### Requirement: Nenhuma forma de entrega é obrigatória, e não entregar não tira a missão

O núcleo NEVER SHALL exigir **foto** ou **áudio** para que a produção seja aceita: o **texto**
SHALL ser sempre suficiente, e é ele a alternativa equivalente de quem não quer ser fotografado
nem gravado.

A **ausência** de produção NEVER SHALL bloquear, travar ou retirar a missão do percurso do
Guerreiro(a): missão sem produção entregue SHALL seguir desbloqueada e disponível, e quem
prefere entregar ao Mestre no encontro NEVER SHALL ser recusado, penalizado nem ter o percurso
alterado por isso. (`RF-05-78`, `RN-05-37`, documento 03 §3.3)

#### Scenario: Só texto basta para entregar

- **WHEN** o Guerreiro(a) entrega em texto, sem foto e sem áudio
- **THEN** a entrega é aceita normalmente, sem nenhuma exigência de mídia

#### Scenario: Missão sem produção não sai do percurso

- **WHEN** o Guerreiro(a) desbloqueia uma missão e não entrega produção alguma
- **THEN** a missão segue desbloqueada e disponível no percurso dele, e nada é bloqueado

#### Scenario: Quem entrega ao Mestre no encontro não perde nada

- **WHEN** o Guerreiro(a) opta por entregar ao Mestre no encontro em vez de fotografar ou gravar
- **THEN** nenhuma operação do núcleo é recusada por isso e o percurso dele segue igual

### Requirement: A devolutiva é construtiva e não credita ponto algum

O núcleo SHALL devolver, à produção entregue, um **retorno construtivo** — que aponta o
próximo passo em vez do erro. A devolutiva SHALL ser gravada com a produção. Vale igual nas
duas portas: a da equipe e a individual do Guerreiro(a).

A devolutiva NEVER SHALL creditar pontos, gravar `Resultado`, emitir lançamento, alterar nível,
badge ou percurso de missão: ela é **hipótese, não resultado**, e quem lança o resultado é o
**Mestre**. (`RF-04-47`, `RF-05-75`, `RF-05-77`, `RN-05-05`, `RN-05-35`, documento 11 §§2.2, 5,
documento 99 §6 invariante 19)

#### Scenario: A produção recebe o retorno construtivo

- **WHEN** uma equipe entrega a produção
- **THEN** o núcleo devolve e grava um retorno que aponta o próximo passo

#### Scenario: A entrega individual também recebe o retorno construtivo

- **WHEN** o Guerreiro(a) entrega sozinho a produção de uma missão dele
- **THEN** o núcleo devolve e grava um retorno que aponta o próximo passo

#### Scenario: A devolutiva não credita ponto

- **WHEN** a devolutiva é gravada
- **THEN** nenhum ponto é creditado, nenhum Resultado é gravado e nenhum lançamento é emitido

#### Scenario: A devolutiva da entrega individual não credita ponto

- **WHEN** o Guerreiro(a) entrega sozinho e recebe a devolutiva
- **THEN** nenhum ponto é creditado, nenhum Resultado é gravado e o percurso dele segue igual

#### Scenario: Nível e badge não mudam pela devolutiva

- **WHEN** uma equipe entrega várias produções no mesmo encontro
- **THEN** nível, badge e percurso de cada integrante seguem exatamente como estavam

#### Scenario: O resultado continua sendo do Mestre

- **WHEN** o Mestre lança o resultado da atividade depois da entrega
- **THEN** é esse lançamento que credita, e ele não é substituído nem antecipado pela devolutiva

### Requirement: A devolutiva sempre opera no aparelho da equipe

O núcleo NEVER SHALL consultar a chave de personalização de integrante algum para produzir a
devolutiva no App 01: o aparelho é **da equipe**, a tela não é de ninguém em particular e a
reescrita **sempre opera**. Integrante com a chave desligada NEVER SHALL desligar a devolutiva
da equipe.

A adaptação SHALL acontecer **na sessão** e SHALL ser descartada com ela: o núcleo NEVER SHALL
inferir nem guardar traço algum sobre ritmo, dificuldade ou interesse de quem entregou.
(`RN-04-31`, documento 03 §7.1, documento 99 §6 invariante 11)

#### Scenario: Integrante com a chave desligada não desliga a devolutiva

- **WHEN** uma equipe em que um integrante tem a personalização desligada entrega a produção
- **THEN** a devolutiva é produzida normalmente para a equipe

#### Scenario: Nada é inferido sobre quem entregou

- **WHEN** a devolutiva é produzida
- **THEN** nenhum traço de ritmo, dificuldade ou interesse de integrante algum é gravado

### Requirement: A entrega é alcançável por HTTP pelo integrante da equipe em sessão

O núcleo SHALL expor a entrega por `POST /v1/equipes/{id}/producao`, sob a **sessão do
Guerreiro(a)** e sob a chave de aplicação, pelas convenções de erro do PRD-01. Quem entrega
SHALL ser **integrante daquela equipe**; Guerreiro(a) em sessão que não a integra SHALL receber
**403**, e Mestre ou Admin que tentarem entregar pela equipe SHALL receber **403** — a produção
é da criança.

Entrega em equipe cuja **aula já se encerrou** SHALL ser recusada com **422**. A resposta SHALL
trazer a produção gravada, com a transcrição e a devolutiva. (`RF-04-45` a `RF-04-47`,
`RF-01-16`, PRD-04 §9)

#### Scenario: O integrante entrega pela porta

- **WHEN** um integrante da equipe em sessão envia a produção
- **THEN** o núcleo responde 201 com a produção gravada, a transcrição e a devolutiva

#### Scenario: Quem não integra a equipe não entrega por ela

- **WHEN** um Guerreiro(a) em sessão que não integra aquela equipe envia a produção
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: A gestão não entrega pela equipe

- **WHEN** um Mestre ou um Admin em sessão tenta entregar a produção de uma equipe
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Equipe de aula encerrada não entrega

- **WHEN** um integrante tenta entregar numa equipe cuja aula já se encerrou
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Sem sessão de persona a porta não abre

- **WHEN** chega uma entrega sem credencial de persona
- **THEN** o núcleo recusa e nada é gravado

### Requirement: A leitura da foto indisponível não perde o que já está legível

O núcleo SHALL separar a **leitura** — o que transforma a foto em transcrição — da
**devolutiva**, nas duas portas:

- Entrega por **texto** ou por **áudio**: a transcrição é o próprio texto recebido — digitado
  ou transcrito no aparelho — e não depende de leitura alguma. Se a devolutiva não vier — erro,
  demora ou resposta fora do formato esperado —, o núcleo SHALL gravar a produção assim mesmo,
  com a **devolutiva em branco**, e responder **201**. O que foi escrito ou falado NEVER SHALL
  se perder por indisponibilidade do modelo.
- Entrega por **foto**: sem leitura não há transcrição, e gravar o registro vazio seria guardar
  uma entrega que não diz nada. O núcleo SHALL responder **503**, sem gravar, para quem
  entregou reenviar.

O núcleo NEVER SHALL medir, contar nem lançar no livro-razão o consumo do modelo usado pela
leitura e pela devolutiva — o custo entra como recurso de nuvem, na mesma régua do template de
missão (`RF-09-90`). A resposta da entrega NEVER SHALL trazer custo, cota ou contagem de uso.
(`RF-04-45`, `RF-04-46`, `RF-05-74`, `RF-05-76`)

#### Scenario: Devolutiva que não vem não derruba a entrega por texto

- **WHEN** uma equipe entrega a produção em texto e a devolutiva não vem
- **THEN** o núcleo responde 201 com a produção gravada e a devolutiva em branco

#### Scenario: Devolutiva que não vem não derruba a entrega falada

- **WHEN** uma equipe ou um Guerreiro(a) entrega a produção falada e a devolutiva não vem
- **THEN** o núcleo responde 201 com a produção gravada, a transcrição do aparelho e a
  devolutiva em branco

#### Scenario: Devolutiva que não vem não derruba a entrega individual por texto

- **WHEN** o Guerreiro(a) entrega sozinho em texto e a devolutiva não vem
- **THEN** o núcleo responde 201 com a produção gravada e a devolutiva em branco

#### Scenario: Leitura que não vem recusa a entrega por foto

- **WHEN** uma equipe entrega a foto do manuscrito e a leitura não vem
- **THEN** o núcleo responde 503, nada é gravado e a foto recebida não fica em lugar nenhum

#### Scenario: Leitura que não vem recusa a entrega individual por foto

- **WHEN** o Guerreiro(a) entrega sozinho a foto do manuscrito e a leitura não vem
- **THEN** o núcleo responde 503, nada é gravado e a foto recebida não fica em lugar nenhum

#### Scenario: A entrega não lança custo no livro-razão

- **WHEN** a leitura e a devolutiva são produzidas
- **THEN** nenhum lançamento é emitido no livro-razão e nenhum contador de consumo é gravado

#### Scenario: A resposta não traz custo nem cota

- **WHEN** o núcleo responde à entrega
- **THEN** nenhum campo da resposta traz custo, cota, contagem de uso ou valor

### Requirement: A mídia da produção da missão é guardada

O núcleo SHALL **guardar** o arquivo entregue na produção da missão — a **foto** do manuscrito
e o **áudio** da fala —, nas duas portas. O arquivo SHALL chegar na **mesma requisição** da
entrega, em `multipart/form-data`, como a foto já chega: é dela que o núcleo tira a
transcrição, e guardar é deixar de descartar o que ele já recebeu. A **transcrição** SHALL
continuar gravada. (`RF-01-79`, `RN-01-61`, `RF-04-45`, `RF-05-76`)

#### Scenario: A foto entregue fica guardada

- **WHEN** uma equipe entrega a foto do manuscrito
- **THEN** a produção fica com a mídia guardada, e a transcrição continua gravada com ela

#### Scenario: O áudio entregue fica guardado

- **WHEN** o Guerreiro(a) entrega a produção falada, com a transcrição e o arquivo do áudio
- **THEN** a produção fica com a mídia guardada, e a transcrição continua gravada com ela

#### Scenario: A entrega em texto não ganha mídia

- **WHEN** chega uma entrega na forma texto
- **THEN** a produção é gravada sem mídia, e a leitura dela responde 404

#### Scenario: A devolutiva continua a ser feita sobre o texto

- **WHEN** a produção tem transcrição e arquivo
- **THEN** a devolutiva é construída a partir da transcrição, e nunca a partir do arquivo

### Requirement: A mídia da produção da missão é servida a quem pode ver a produção

O núcleo SHALL servir os **bytes** da mídia de uma produção a quem já pode vê-la: quem a
entregou ou os **integrantes da equipe** dona dela, o **Mestre** da trilha e o **Admin**. Fora
desse conjunto SHALL responder **403**; produção sem mídia, **404**. NEVER SHALL haver rota
pública: a produção da missão não é item de acervo. (`RF-01-80`, `RN-01-62`)

#### Scenario: O integrante da equipe lê a mídia da produção dela

- **WHEN** um integrante da equipe dona da produção pede a mídia dela
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: O Mestre lê a mídia da produção da sua trilha

- **WHEN** o Mestre da trilha pede a mídia de uma produção dela
- **THEN** o núcleo devolve os bytes com o tipo MIME gravado no envio

#### Scenario: Quem não é da equipe nem Mestre é recusado

- **WHEN** um Guerreiro(a) de fora da equipe pede a mídia da produção dela
- **THEN** o núcleo responde 403 e nenhum byte é servido

#### Scenario: Produção sem mídia responde 404

- **WHEN** se pede a mídia de uma produção entregue em texto, ou gravada antes desta change
- **THEN** o núcleo responde 404

#### Scenario: Não há rota pública para a mídia da produção

- **WHEN** se procura a mídia de uma produção da missão sem sessão
- **THEN** não há rota pública que a sirva, porque a produção não é item de acervo
