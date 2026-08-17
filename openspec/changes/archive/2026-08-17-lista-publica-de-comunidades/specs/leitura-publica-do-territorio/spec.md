## ADDED Requirements

### Requirement: A lista pública de comunidades devolve os quatro indicadores do documento 02 §1

O núcleo SHALL expor uma rota pública que lista as Comunidades Virtuais, cada uma com **nome**,
**localização** e os **quatro indicadores** do documento 02 §1: séries abertas, séries ativas ao
fim do ciclo, registros válidos e continuidade. A rota SHALL responder **sem token de sessão** e
SHALL exigir a **chave de aplicação válida**, como toda rota de dados sob o prefixo de versão.
Nenhum quinto indicador SHALL sair por ela. (`RF-08-30`, `RN-08-29`, `RF-01-02`, `RN-01-32`,
documento 02 §1, PRD-08 §9)

#### Scenario: A lista responde sem token de sessão

- **WHEN** chega uma consulta da lista de comunidades com chave de aplicação válida e sem token
  de sessão
- **THEN** o núcleo responde normalmente, e nenhum dado restrito acompanha a resposta

#### Scenario: A lista sem chave é recusada

- **WHEN** chega uma consulta da lista de comunidades sem chave de aplicação
- **THEN** o núcleo responde 401, sem diferenciar chave ausente, inválida e revogada

#### Scenario: A lista devolve exatamente os quatro indicadores

- **WHEN** uma comunidade acima do piso de coletores sai na lista
- **THEN** a resposta traz séries abertas, séries ativas ao fim do ciclo, registros válidos e
  continuidade, e nenhum outro indicador

#### Scenario: Comunidade recém-criada sai com os indicadores zerados

- **WHEN** uma comunidade sem nenhuma série sai na lista
- **THEN** séries abertas, séries ativas e registros válidos saem em zero, e a continuidade sai
  nula — não há série sobre a qual tirar média

### Requirement: Comunidade abaixo do piso de coletores permanece na lista, sem os indicadores

O núcleo SHALL manter na lista a comunidade cujo número de coletores distintos não alcança o
**piso declarado na implantação**, com **nome e localização**, e SHALL devolver os **quatro
indicadores nulos** para ela. A comunidade NEVER SHALL ser omitida da lista por estar abaixo do
piso: ela é o **topo da hierarquia** e não há nível acima a que somá-la, de modo que a regra de
subir o recorte não se aplica. O que se omite é o indicador, nunca a comunidade. (`RF-08-31`,
`RN-08-28`, `RN-08-24`, documento 02 §1)

#### Scenario: Comunidade com coletores abaixo do piso sai sem os números

- **WHEN** uma comunidade tem dois coletores distintos e o piso declarado é três
- **THEN** ela sai na lista com nome e localização, e os quatro indicadores saem nulos

#### Scenario: Comunidade com coletores no piso sai com os números

- **WHEN** uma comunidade tem três coletores distintos e o piso declarado é três
- **THEN** ela sai na lista com os quatro indicadores apurados

#### Scenario: A supressão alcança os quatro, nunca um subconjunto

- **WHEN** uma comunidade está abaixo do piso
- **THEN** nenhum dos quatro indicadores sai — não há indicador que escape à supressão por ser
  agregado demais

#### Scenario: O recorte da série abaixo do piso continua sendo suprimido

- **WHEN** um recorte da série pública não alcança o piso nem depois de somado ao nível acima
- **THEN** ele continua não saindo, como esta capacidade já define — o tratamento da lista de
  comunidades é outro, porque ali não há nível acima a que somar

### Requirement: Os quatro indicadores se apuram como o documento 02 §1 define

O núcleo SHALL apurar **séries abertas** como a contagem das séries abertas na comunidade,
qualquer que seja o estado delas; **séries ativas ao fim do ciclo** como a contagem das séries
em estado ativo **no instante da consulta**, acompanhada do rótulo do ciclo corrente declarado
na implantação; **registros válidos** como a contagem dos registros em situação válida das
séries da comunidade; e **continuidade** como a **média, entre as séries da comunidade, da
fração dos períodos de cadência esperados que tiveram ao menos um registro válido**. Registro
invalidado na auditoria NEVER SHALL entrar na contagem de registros válidos nem na apuração da
continuidade. (`RN-08-29`, `RN-08-09`, documento 02 §1)

#### Scenario: Séries ativas se apura no instante da consulta

- **WHEN** uma série passa de ativa a interrompida entre duas consultas à lista
- **THEN** a segunda consulta já não a conta como ativa, sem depender de apuração anterior nem
  de fim de ciclo declarado

#### Scenario: Continuidade de série que cumpriu todos os períodos

- **WHEN** uma série tem três períodos de cadência vencidos e registro válido em cada um
- **THEN** a continuidade dela é 1, e a da comunidade é a média que a inclui

#### Scenario: Continuidade de série que falhou em um período

- **WHEN** uma série tem quatro períodos de cadência vencidos e registro válido em três
- **THEN** a continuidade dela é 0,75

#### Scenario: Série sem período vencido não pesa na média

- **WHEN** uma série foi aberta e ainda não venceu o primeiro período de cadência
- **THEN** ela fica fora da média da continuidade, em vez de entrar como zero

#### Scenario: Registro invalidado sai das duas apurações

- **WHEN** o Mestre invalida um registro na auditoria por amostragem
- **THEN** a consulta seguinte não o conta em registros válidos, e o período dele volta a
  contar como período sem registro na continuidade

#### Scenario: A resposta declara o ciclo a que os números se referem

- **WHEN** a lista responde
- **THEN** ela traz o rótulo do ciclo corrente, para que "ao fim do ciclo" seja legível por quem
  não conhece a configuração da implantação

### Requirement: A lista de comunidades não identifica coletor algum

O núcleo NEVER SHALL devolver, na lista de comunidades, identificador, nick, avatar ou nome de
coletor, nem contagem que isole um. Os quatro indicadores SHALL ser contagens agregadas da
comunidade inteira. O vínculo de autoria continua gravado: a anonimização é da **saída**, nunca
do armazenamento. (`RN-08-12`, `RN-08-11`, invariante 7 do documento 99 §6)

#### Scenario: Nenhum campo da resposta identifica quem coletou

- **WHEN** se percorre a resposta inteira da lista de comunidades
- **THEN** nenhum campo traz coletor, e a contagem de coletores distintos que decide o piso não
  sai na resposta

### Requirement: A lista de comunidades é paginada no contrato de listagem do núcleo

O núcleo SHALL paginar a lista de comunidades pelo contrato de listagem do núcleo — `cursor` e
`tamanho` —, SHALL ordenar de forma **estável** e SHALL recusar com **422** parâmetro de
consulta não declarado. O piso de coletores SHALL ser aplicado **antes** de qualquer corte de
página, para que a supressão dos indicadores não dependa de onde a página termina.
(`RF-01-28`, `RF-01-18`, `RF-08-31`)

#### Scenario: Parâmetro não declarado é recusado

- **WHEN** chega uma consulta da lista com parâmetro que a rota não declara
- **THEN** o núcleo responde 422, no formato de erro único do núcleo

#### Scenario: A supressão não depende da página

- **WHEN** uma comunidade abaixo do piso cai na segunda página da lista
- **THEN** ela sai sem os indicadores ali também, exatamente como sairia na primeira
