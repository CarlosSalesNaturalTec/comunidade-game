## ADDED Requirements

### Requirement: O Guerreiro(a) entrega sozinho a produção de uma missão do próprio percurso

O núcleo SHALL aceitar, de um **Guerreiro(a) em sessão**, a entrega da produção de uma missão
em **uma** destas três formas: **texto** digitado, **áudio** da fala ou **foto** do que ele fez
à mão. A forma SHALL ser gravada com a produção, e entrega sem nenhuma das três, ou com mais de
uma ao mesmo tempo, SHALL ser recusada com **422** — as mesmas recusas da entrega da equipe.

A produção SHALL ser ancorada em uma **atividade daquela missão**, declarada na entrega.
Atividade que não pertence à missão SHALL ser recusada com **422**.

A missão SHALL ser do **percurso do próprio Guerreiro(a)**: em trilha em que ele está
**inscrito** e por ele **desbloqueada**. Missão de trilha em que não está inscrito SHALL ser
recusada com **422**, e missão que ele ainda não desbloqueou SHALL ser recusada com **422** —
o percurso é o mesmo que já governa a leitura da missão, e a entrega não o atravessa.
(`RF-05-74`, `RN-05-35`, PRD-05 §9)

#### Scenario: Entrega individual por texto

- **WHEN** o Guerreiro(a) em sessão entrega, em texto, a produção de uma atividade de missão
  que ele desbloqueou em trilha em que está inscrito
- **THEN** o núcleo grava a produção com a forma "texto", a missão e a atividade declaradas

#### Scenario: Entrega individual por fala

- **WHEN** o Guerreiro(a) entrega a produção em áudio
- **THEN** o núcleo grava a produção com a forma "áudio" e a transcrição da fala

#### Scenario: Entrega individual por foto do manuscrito

- **WHEN** o Guerreiro(a) entrega a foto do que fez à mão
- **THEN** o núcleo grava a produção com a forma "foto" e a leitura do manuscrito em texto

#### Scenario: Entrega individual sem conteúdo é recusada

- **WHEN** chega uma entrega individual sem texto, sem áudio e sem foto
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Entrega individual com duas formas ao mesmo tempo é recusada

- **WHEN** chega uma entrega individual com texto e foto juntos
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
**sessão do Guerreiro(a)** e sob a chave de aplicação, pelas convenções de erro do PRD-01.
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

## MODIFIED Requirements

### Requirement: Foto e áudio são descartados na leitura e nunca persistidos

O núcleo SHALL **descartar a foto e o áudio na leitura**: gravadas ficam apenas a
**transcrição** e a **devolutiva**. A foto e o áudio da produção NEVER SHALL ser persistidos —
nem em banco, nem em armazenamento de arquivo, nem em registro de erro — e NEVER SHALL
aparecer em resposta alguma. Vale igual nas **duas portas**: a da equipe e a individual do
Guerreiro(a). (`RF-04-46`, `RF-05-76`, `RN-05-36`, documento 03 §12.2, PRD-04 §11)

#### Scenario: O áudio some depois de transcrito

- **WHEN** uma equipe entrega a produção em áudio e o núcleo a transcreve
- **THEN** o áudio não existe em lugar nenhum e resta a transcrição

#### Scenario: A foto some depois de lida

- **WHEN** uma equipe entrega a foto do manuscrito e o núcleo a lê
- **THEN** a fotografia não existe em lugar nenhum e resta a transcrição

#### Scenario: A mídia da entrega individual também some

- **WHEN** o Guerreiro(a) entrega sozinho a produção em áudio ou em foto do manuscrito
- **THEN** o áudio e a foto não existem em lugar nenhum e resta a transcrição

#### Scenario: A resposta da entrega não devolve foto nem áudio

- **WHEN** o núcleo responde à entrega
- **THEN** a resposta traz a transcrição e a devolutiva, e nenhum campo com foto ou áudio

#### Scenario: A falha na leitura não guarda o que foi enviado

- **WHEN** a leitura da foto ou do áudio falha
- **THEN** o núcleo responde o erro sem gravar nem registrar em log a foto ou o áudio recebidos

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

### Requirement: A leitura indisponível não perde o que já está legível

O núcleo SHALL separar a **leitura** — o que transforma áudio e foto em transcrição — da
**devolutiva**, nas duas portas:

- Entrega por **texto**: a transcrição é o próprio texto e não depende de leitura alguma. Se a
  devolutiva não vier — erro, demora ou resposta fora do formato esperado —, o núcleo SHALL
  gravar a produção assim mesmo, com a **devolutiva em branco**, e responder **201**. O que foi
  escrito NEVER SHALL se perder por indisponibilidade do modelo.
- Entrega por **áudio** ou **foto**: sem leitura não há transcrição, e gravar o registro vazio
  seria guardar uma entrega que não diz nada. O núcleo SHALL responder **503**, sem gravar,
  para quem entregou reenviar.

O núcleo NEVER SHALL medir, contar nem lançar no livro-razão o consumo do modelo usado pela
leitura e pela devolutiva — o custo entra como recurso de nuvem, na mesma régua do template de
missão (`RF-09-90`). A resposta da entrega NEVER SHALL trazer custo, cota ou contagem de uso.
(`RF-04-45`, `RF-04-46`, `RF-05-74`, `RF-05-76`)

#### Scenario: Devolutiva que não vem não derruba a entrega por texto

- **WHEN** uma equipe entrega a produção em texto e a devolutiva não vem
- **THEN** o núcleo responde 201 com a produção gravada e a devolutiva em branco

#### Scenario: Devolutiva que não vem não derruba a entrega individual por texto

- **WHEN** o Guerreiro(a) entrega sozinho em texto e a devolutiva não vem
- **THEN** o núcleo responde 201 com a produção gravada e a devolutiva em branco

#### Scenario: Leitura que não vem recusa a entrega por foto

- **WHEN** uma equipe entrega a foto do manuscrito e a leitura não vem
- **THEN** o núcleo responde 503, nada é gravado e a foto recebida não fica em lugar nenhum

#### Scenario: Leitura que não vem recusa a entrega individual por áudio

- **WHEN** o Guerreiro(a) entrega sozinho em áudio e a leitura não vem
- **THEN** o núcleo responde 503, nada é gravado e o áudio recebido não fica em lugar nenhum

#### Scenario: A entrega não lança custo no livro-razão

- **WHEN** a leitura e a devolutiva são produzidas
- **THEN** nenhum lançamento é emitido no livro-razão e nenhum contador de consumo é gravado

#### Scenario: A resposta não traz custo nem cota

- **WHEN** o núcleo responde à entrega
- **THEN** nenhum campo da resposta traz custo, cota, contagem de uso ou valor
