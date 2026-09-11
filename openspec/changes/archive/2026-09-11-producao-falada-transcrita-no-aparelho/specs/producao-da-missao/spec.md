## MODIFIED Requirements

### Requirement: A equipe entrega a produção por texto, fala ou foto do manuscrito

O núcleo SHALL aceitar, de uma equipe, a entrega da produção da missão em **uma** destas três
formas: **texto** digitado, **áudio** da fala ou **foto** do que a equipe fez à mão. A forma da
entrega SHALL ser **declarada na chamada** e gravada com a produção — é ela que distingue a
fala do texto digitado, que chegam ambos como texto.

Entrega em **texto** ou em **áudio** SHALL trazer o **texto** e NEVER SHALL trazer arquivo — a
fala é transcrita no aparelho e o que chega é a transcrição. Entrega em **foto** SHALL trazer o
**arquivo** e NEVER SHALL trazer texto. Entrega sem o conteúdo da forma declarada, ou com o
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
- **THEN** o núcleo grava a produção com a forma "áudio" e a transcrição recebida, sem receber
  áudio algum

#### Scenario: Entrega por foto do manuscrito

- **WHEN** uma equipe entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega sem conteúdo é recusada

- **WHEN** chega uma entrega sem texto e sem arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega com texto e foto juntos
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega por fala com arquivo é recusada

- **WHEN** chega uma entrega com a forma "áudio" acompanhada de arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Equipe sem atividade corrente não entrega

- **WHEN** uma equipe que ainda não declarou a atividade que está trabalhando tenta entregar
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: O Guerreiro(a) entrega sozinho a produção de uma missão do próprio percurso

O núcleo SHALL aceitar, de um **Guerreiro(a) em sessão**, a entrega da produção de uma missão
em **uma** destas três formas: **texto** digitado, **áudio** da fala ou **foto** do que ele fez
à mão. A forma SHALL ser declarada na chamada e gravada com a produção.

Entrega em **texto** ou em **áudio** SHALL trazer o **texto** e NEVER SHALL trazer arquivo;
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
- **THEN** o núcleo grava a produção com a forma "áudio" e a transcrição recebida, sem receber
  áudio algum

#### Scenario: Entrega individual por foto do manuscrito

- **WHEN** o Guerreiro(a) entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega individual sem conteúdo é recusada

- **WHEN** chega uma entrega individual sem texto e sem arquivo
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega individual com texto e foto juntos
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual por fala com arquivo é recusada

- **WHEN** chega uma entrega individual com a forma "áudio" acompanhada de arquivo
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

## ADDED Requirements

### Requirement: A foto é descartada na leitura, e o áudio nunca chega ao núcleo

O núcleo NEVER SHALL receber o **áudio** da produção: a fala é transcrita **no próprio
aparelho** e o que trafega é a **transcrição**, indistinguível, no contrato, da produção
digitada. Nenhuma das duas portas SHALL aceitar arquivo de áudio, e o núcleo NEVER SHALL
transcrever fala.

A **foto** SHALL ser **descartada na leitura**: gravadas ficam apenas a **transcrição** e a
**devolutiva**. A foto NEVER SHALL ser persistida — nem em banco, nem em armazenamento de
arquivo, nem em registro de erro — e NEVER SHALL aparecer em resposta alguma. Vale igual nas
**duas portas**: a da equipe e a individual do Guerreiro(a). (`RF-04-46`, `RF-05-76`,
`RN-05-32`, `RN-05-36`, documento 03 §§1.12, 12.2, PRD-04 §11)

#### Scenario: O áudio da fala não chega ao núcleo

- **WHEN** uma equipe ou um Guerreiro(a) entrega a produção falada
- **THEN** o núcleo recebe só a transcrição, e nenhum áudio é recebido, lido ou registrado

#### Scenario: Arquivo de áudio na entrega é recusado

- **WHEN** chega uma entrega que declara a forma "áudio" e manda arquivo
- **THEN** o núcleo responde 422, nada é gravado e nada do arquivo fica em lugar nenhum

#### Scenario: A foto some depois de lida

- **WHEN** uma equipe entrega a foto do manuscrito e o núcleo a lê
- **THEN** a fotografia não existe em lugar nenhum e resta a transcrição

#### Scenario: A foto da entrega individual também some

- **WHEN** o Guerreiro(a) entrega sozinho a foto do manuscrito
- **THEN** a fotografia não existe em lugar nenhum e resta a transcrição

#### Scenario: A resposta da entrega não devolve foto nem áudio

- **WHEN** o núcleo responde à entrega
- **THEN** a resposta traz a transcrição e a devolutiva, e nenhum campo com foto ou áudio

#### Scenario: A falha na leitura não guarda o que foi enviado

- **WHEN** a leitura da foto falha
- **THEN** o núcleo responde o erro sem gravar nem registrar em log a foto recebida

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

## REMOVED Requirements

### Requirement: Foto e áudio são descartados na leitura e nunca persistidos

**Reason**: O áudio deixa de ser descartado depois de transcrito porque deixa de chegar: a fala
é transcrita no próprio aparelho (`RF-05-76`, `RN-05-32`, documento 03 §1.12). A garantia nova
é mais forte e está em `A foto é descartada na leitura, e o áudio nunca chega ao núcleo`.

**Migration**: Nenhuma no dado gravado — a produção sempre guardou só transcrição e devolutiva.
Quem entrega a fala manda a transcrição como texto, com a forma "áudio" declarada.

### Requirement: A leitura indisponível não perde o que já está legível

**Reason**: A regra se dividia entre "texto" e "áudio ou foto"; com a fala transcrita no
aparelho, só a foto depende da leitura do modelo. Substituída por `A leitura da foto
indisponível não perde o que já está legível`.

**Migration**: A entrega falada que antes recebia 503 sem leitura passa a receber 201 com a
devolutiva em branco, como a entrega por texto. Nada muda na entrega por foto.
