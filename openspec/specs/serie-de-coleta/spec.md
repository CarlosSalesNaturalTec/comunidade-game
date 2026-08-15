## Purpose

A série de coleta é o compromisso individual do Guerreiro(a) com um desafio num ponto do
território: é ela que dá endereço à medição, herda a cadência do desafio e sustenta a
progressão do Poder do Território enquanto estiver viva.

## Requirements

### Requirement: O Guerreiro(a) abre a série sobre um desafio e um local da sua comunidade

O núcleo SHALL abrir a série de coleta a pedido de um **Guerreiro(a) em sessão**, sobre um
**desafio de coleta** vigente e um **local** cadastrado na Comunidade Virtual a que ele está
vinculado. A série SHALL nascer com a **cadência herdada do desafio** e no estado **`ativa`**.
Persona de outro papel SHALL receber **403**. Local de outra comunidade SHALL ser recusado com
**403**, e desafio fora da vigência SHALL ser recusado com **422**. (`RF-08-07`, `RN-08-02`,
PRD-08 §§4, 5.3, 9)

#### Scenario: Guerreiro(a) abre a série sobre desafio vigente e local da sua comunidade

- **WHEN** um Guerreiro(a) em sessão abre série sobre um desafio vigente, escolhendo um local
  cadastrado na comunidade a que está vinculado
- **THEN** o núcleo grava a série no estado `ativa`, com a cadência do desafio, o coletor da
  sessão e o local escolhido

#### Scenario: Local de outra comunidade é recusado

- **WHEN** um Guerreiro(a) vinculado à comunidade A tenta abrir série sobre um local da
  comunidade B
- **THEN** o núcleo responde 403 e nenhuma série é gravada

#### Scenario: Desafio fora da vigência é recusado

- **WHEN** um Guerreiro(a) tenta abrir série sobre um desafio cuja vigência já terminou
- **THEN** o núcleo responde 422 e nenhuma série é gravada

#### Scenario: Mestre não abre série

- **WHEN** um Mestre em sessão tenta abrir uma série
- **THEN** o núcleo responde 403 e nenhuma série é gravada

### Requirement: A abertura da série confere o teto de granularidade da comunidade

O núcleo SHALL conferir, **na abertura da série**, a **granularidade exigida pelo desafio**
contra a **granularidade máxima da Comunidade Virtual** do Guerreiro(a), e SHALL recusar com
**422** a abertura cuja granularidade exigida seja mais fina que o teto daquela comunidade. O
**nível do local escolhido** SHALL corresponder à granularidade exigida pelo desafio; nível
diferente SHALL ser recusado com **422**. É aqui — e não na criação do desafio — que o teto é
conferido. (`RN-08-25`, `RF-08-07`, 02 §1)

#### Scenario: Granularidade exigida mais fina que o teto da comunidade é recusada

- **WHEN** um Guerreiro(a) de comunidade cuja granularidade máxima é `rua` tenta abrir série
  sobre desafio que exige granularidade `quadra`
- **THEN** o núcleo responde 422 e nenhuma série é gravada

#### Scenario: Granularidade exigida dentro do teto é aceita

- **WHEN** um Guerreiro(a) de comunidade cuja granularidade máxima é `quadra` abre série sobre
  desafio que exige granularidade `rua`, escolhendo um local de nível `rua`
- **THEN** o núcleo grava a série

#### Scenario: Local de nível diferente da granularidade exigida é recusado

- **WHEN** o desafio exige granularidade `rua` e o Guerreiro(a) escolhe um local de nível
  `bairro`
- **THEN** o núcleo responde 422 e nenhuma série é gravada

### Requirement: A série é individual e pertence a quem está na sessão

O núcleo SHALL manter **um único coletor por série** e SHALL atribuí-la ao **Guerreiro(a) da
sessão**, nunca ao aparelho de onde veio a chamada — o ponto de apoio usa aparelho
compartilhado. O núcleo SHALL recusar com **409** a abertura de uma segunda série do mesmo
Guerreiro(a) sobre o mesmo par de desafio e local, e NEVER SHALL aceitar coletor informado no
corpo da requisição. (`RN-08-04`, PRD-08 §§8, 10)

#### Scenario: A série é do Guerreiro(a) da sessão

- **WHEN** um Guerreiro(a) abre série informando no corpo o identificador de outro Guerreiro(a)
  como coletor
- **THEN** o núcleo ignora o coletor informado e grava a série em nome do Guerreiro(a) da sessão

#### Scenario: Série duplicada do mesmo par de desafio e local é recusada

- **WHEN** um Guerreiro(a) que já tem série sobre um desafio e um local tenta abrir outra sobre
  o mesmo par
- **THEN** o núcleo responde 409 e nenhuma série nova é gravada

#### Scenario: Dois Guerreiros abrem série sobre o mesmo desafio e local

- **WHEN** dois Guerreiros e Guerreiras da mesma comunidade abrem série sobre o mesmo desafio e
  o mesmo local
- **THEN** o núcleo grava duas séries independentes, uma para cada coletor

### Requirement: A série nasce ativa e o estado é derivado da última medição válida

O núcleo SHALL abrir a série no estado **`ativa`** e SHALL **derivar** o estado dela da **data
da última medição válida**, da **cadência da série** e da **vigência do desafio**, apurados no
momento em que o estado é consultado. O estado NEVER SHALL ser informado na requisição nem
editado à mão. Os estados SHALL ser **`ativa`**, **`interrompida`** e **`encerrada`**, e o
núcleo SHALL devolver sempre o estado derivado, nunca um valor gravado que o contradiga.
(`RF-08-07`, `RF-08-10`, `RF-08-11`, PRD-08 §8)

#### Scenario: Série recém-aberta aparece como ativa

- **WHEN** uma série é aberta
- **THEN** o núcleo a devolve no estado `ativa`, com a data de abertura gravada

#### Scenario: O estado informado na requisição é ignorado

- **WHEN** um Guerreiro(a) abre série informando no corpo o estado `interrompida`
- **THEN** o núcleo ignora o valor informado e grava a série como `ativa`

#### Scenario: A data da última medição válida acompanha a série

- **WHEN** um registro válido é gravado numa série
- **THEN** o núcleo atualiza na série a data da última medição válida

### Requirement: A data da última medição válida nunca retrocede

O núcleo SHALL manter em `ultima_medicao_valida_em` a **data da medição mais recente** entre os
registros válidos da série, e NEVER SHALL substituí-la por uma data anterior à que já está
gravada. Registrar uma medição mais antiga depois de uma mais recente SHALL gravar o registro
normalmente e SHALL deixar o campo inalterado — é a **última** medição válida, não a última
gravada. (`RF-08-10`, PRD-08 §8)

#### Scenario: Medição mais antiga enviada depois não move o campo para trás

- **WHEN** o coletor grava uma medição de hoje e em seguida grava uma medição de três dias atrás
- **THEN** o núcleo grava os dois registros e mantém em `ultima_medicao_valida_em` a data de
  hoje

#### Scenario: Medição mais recente avança o campo

- **WHEN** o coletor grava uma medição posterior à última medição válida da série
- **THEN** o núcleo passa `ultima_medicao_valida_em` a valer aquela data

### Requirement: Dois períodos de cadência seguidos sem registro interrompem a série

O núcleo SHALL marcar a série como **`interrompida`** quando se passarem **dois períodos de
cadência seguidos** sem registro válido, contados a partir da **última medição válida** ou, na
falta dela, da **data de abertura** da série. **Um** período sem registro NEVER SHALL
interromper — uma falha isolada não interrompe. A série `interrompida` SHALL **cessar o
cômputo**: enquanto nesse estado ela não rende pontos novos. Os pontos **já creditados** SHALL
permanecer, e a interrupção NEVER SHALL estornar ponto algum. (`RF-08-10`, `RN-08-07`,
`RN-08-08`, documento 02 §1)

#### Scenario: Série sem registro por dois períodos aparece como interrompida

- **WHEN** uma série de cadência semanal passa duas semanas seguidas sem nenhum registro válido
- **THEN** o núcleo a apresenta no estado `interrompida`

#### Scenario: Um só período sem registro não interrompe

- **WHEN** uma série de cadência semanal passa uma semana sem registro e o coletor registra na
  semana seguinte
- **THEN** a série permanece `ativa`, porque uma falha isolada não interrompe

#### Scenario: A interrupção não estorna os pontos já creditados

- **WHEN** uma série que já creditou pontos é interrompida
- **THEN** o saldo do Poder do Território do coletor permanece o mesmo, e nenhum estorno é
  lançado

#### Scenario: Série sem nenhum registro conta da abertura

- **WHEN** uma série de cadência semanal é aberta e passa duas semanas sem que o coletor
  registre qualquer medição
- **THEN** o núcleo a apresenta no estado `interrompida`, contados os dois períodos a partir da
  data de abertura

### Requirement: O registro seguinte retoma a série e credita normalmente

O núcleo SHALL **retomar** a série interrompida ao receber um **registro válido**, devolvendo-a
ao estado **`ativa`**, e NEVER SHALL recompor os períodos parados: os pontos que a série
deixou de render enquanto interrompida SHALL permanecer perdidos. O registro que retoma SHALL
ser creditado como qualquer outro registro válido — o crédito SHALL seguir condicionado apenas
a ser registro válido e à quantidade de registros que pontuam declarada no desafio, e NEVER
SHALL ser recusado por causa do estado em que a série se encontrava. (`RF-08-11`, `RN-08-05`,
`RN-08-08`, documento 02 §1)

#### Scenario: O registro seguinte devolve a série para ativa

- **WHEN** o coletor grava um registro válido numa série `interrompida`
- **THEN** o núcleo a apresenta de volta no estado `ativa`

#### Scenario: O registro que retoma credita os pontos dele

- **WHEN** o coletor grava numa série `interrompida` o primeiro registro válido do período, num
  desafio que declara que um registro do período pontua
- **THEN** o núcleo credita ao Poder do Território os pontos daquele registro, como faria em
  série que nunca interrompeu

#### Scenario: A retomada não recupera os períodos parados

- **WHEN** uma série de cadência semanal fica três semanas sem registro e depois recebe um
  registro válido
- **THEN** o núcleo credita apenas os pontos do registro recebido, e nenhum ponto pelas semanas
  em que nada foi registrado

### Requirement: O fim da vigência do desafio encerra a série, e o encerramento é terminal

O núcleo SHALL marcar a série como **`encerrada`** quando a **vigência do desafio** dela houver
terminado. O estado `encerrada` SHALL prevalecer sobre `ativa` e sobre `interrompida`, e SHALL
ser **terminal**: série encerrada NEVER SHALL retomar. Os pontos já creditados SHALL permanecer.
(PRD-08 §§3.1, 8)

#### Scenario: Vigência terminada encerra a série

- **WHEN** a vigência do desafio de uma série termina
- **THEN** o núcleo a apresenta no estado `encerrada`

#### Scenario: Série encerrada prevalece sobre a interrupção

- **WHEN** uma série passa dois períodos sem registro e a vigência do desafio também termina
- **THEN** o núcleo a apresenta como `encerrada`, não como `interrompida`

#### Scenario: Série encerrada não retoma

- **WHEN** o coletor tenta gravar medição numa série cujo desafio saiu de vigência
- **THEN** o núcleo recusa o registro com 422 e a série permanece `encerrada`

### Requirement: O Guerreiro(a) consulta as suas séries, com o estado e os pontos de cada uma

O núcleo SHALL devolver ao **Guerreiro(a) em sessão** a lista das **suas** séries, cada uma com
o **desafio**, o **local**, a **cadência**, o **estado** e os **pontos que a série está
rendendo** — a soma dos pontos creditados pelos registros válidos dela. A consulta NEVER SHALL
devolver série de outro Guerreiro(a), e persona de outro papel SHALL receber **403**. O estado
devolvido SHALL ser o derivado no momento da consulta. (`RF-08-17`, `RN-08-04`, PRD-08 §9)

#### Scenario: O Guerreiro(a) vê as suas séries com estado e pontos

- **WHEN** um Guerreiro(a) em sessão consulta as suas séries
- **THEN** o núcleo devolve cada série dele com o desafio, o local, a cadência, o estado e a
  soma dos pontos creditados pelos registros válidos daquela série

#### Scenario: A consulta não alcança série de outro Guerreiro(a)

- **WHEN** um Guerreiro(a) consulta as suas séries e há séries de outros coletores no mesmo
  desafio e local
- **THEN** o núcleo devolve apenas as séries do Guerreiro(a) da sessão

#### Scenario: A consulta reflete a interrupção sem depender de escrita anterior

- **WHEN** um Guerreiro(a) cuja série passou dois períodos sem registro consulta as suas séries
- **THEN** o núcleo devolve aquela série como `interrompida`, ainda que nenhuma escrita tenha
  acontecido desde a última medição

#### Scenario: Mestre não consulta pela rota do Guerreiro(a)

- **WHEN** um Mestre em sessão chama a consulta das séries do Guerreiro(a)
- **THEN** o núcleo responde 403
