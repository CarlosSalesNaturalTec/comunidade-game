# Spec Delta

## ADDED Requirements

### Requirement: Cada recorte publicado declara a metodologia da medição

O núcleo SHALL devolver, na série pública, a **metodologia do recorte** a que cada ponto
pertence: **o que se mede** — o nome do tipo de coleta e a unidade, quando o tipo a tem —, as
**cadências** das séries que compõem o recorte, o **período coberto** pela primeira e pela
última medição publicada naquele recorte, as **origens** da medição — manual, voz ou sensor —
e o **número de registros válidos** do recorte.

A metodologia SHALL ser apurada **sobre o mesmo conjunto publicado**: o período consultado, os
registros de situação válida e o recorte já resolvido pelo piso de coletores. Registro
invalidado, registro fora do período e registro de recorte que subiu de nível NEVER SHALL
contar na metodologia do recorte de onde saíram.

A metodologia SHALL ser do **recorte**, nunca da série individual: a série é de um coletor, e
publicá-la identificaria quem coletou. (`RF-03-17`, `RF-03-18`, `RN-03-10`, `RN-08-12`,
PRD-03 §5.2, decisão do fundador de 2026-09-28)

#### Scenario: O recorte sai com o que mede, a cadência, o período e a origem

- **WHEN** uma consulta pública alcança um recorte de tipo de coleta e bairro com medições
  publicadas
- **THEN** a resposta traz, para aquele recorte, o nome do tipo de coleta com a unidade, as
  cadências das séries que o compõem, a primeira e a última medição publicada e as origens
  das medições

#### Scenario: Os registros válidos do recorte saem contados

- **WHEN** um recorte reúne doze registros válidos no período consultado
- **THEN** a resposta declara doze registros válidos naquele recorte

#### Scenario: O registro invalidado não conta na metodologia

- **WHEN** um dos registros do recorte está com situação invalidada
- **THEN** ele não entra na contagem de registros válidos nem move o período coberto do
  recorte

#### Scenario: A metodologia acompanha o período consultado

- **WHEN** a consulta pede um período mais estreito que a série inteira
- **THEN** o período coberto e a contagem de registros válidos do recorte se referem ao
  período pedido, não à série inteira

#### Scenario: A metodologia não devolve série individual

- **WHEN** se percorre a metodologia inteira de um recorte
- **THEN** nenhuma série individual, nenhum identificador de série e nenhum coletor aparecem —
  só o agregado do recorte

### Requirement: O recorte sem série ativa sai sinalizado como inativo, sem desaparecer

O núcleo SHALL marcar o recorte publicado como **inativo** quando **nenhuma** das séries que o
compõem estiver em estado ativo no instante da consulta, e SHALL mantê-lo na resposta com todos
os seus pontos e a sua metodologia — o dado do território é permanente, e o que muda é o sinal.
Bastando **uma** série ativa, o recorte SHALL sair como ativo. (`RF-03-19`, documento 02 §1,
documento 11 §8.3, invariante 7 do documento 99 §6)

#### Scenario: Recorte com todas as séries interrompidas sai inativo

- **WHEN** todas as séries que compõem um recorte estão interrompidas
- **THEN** o recorte sai na resposta marcado como inativo, com os pontos e a metodologia dele
  inalterados

#### Scenario: Uma série ativa mantém o recorte ativo

- **WHEN** um recorte reúne séries interrompidas e ao menos uma ativa
- **THEN** o recorte sai marcado como ativo

#### Scenario: O sinal de inativo não retira o recorte da resposta

- **WHEN** uma consulta percorre todas as páginas de uma comunidade cujos recortes estão
  todos inativos
- **THEN** os recortes continuam saindo, com os seus pontos, e nenhum some por estar inativo

## MODIFIED Requirements

### Requirement: A comunidade responde em leitura pública com os locais até o bairro

O núcleo SHALL expor em leitura pública a **comunidade**, com os seus **locais até o bairro**,
os **tipos de coleta ativos** nela — os tipos sobre os quais há desafio com série aberta
naquela comunidade — e o **número de Guerreiros e Guerreiras vinculados** a ela. Local de nível
**rua ou abaixo** NEVER SHALL aparecer nesta rota, pela mesma linha de corte da série.
Comunidade inexistente SHALL receber **404**. (`RF-08-16`, `RN-08-13`, `RF-03-02`, PRD-08 §9,
documento 11 §8.2)

#### Scenario: A comunidade pública traz os seus bairros

- **WHEN** uma consulta pública pede uma comunidade que tem bairros e ruas cadastrados
- **THEN** o núcleo devolve a comunidade com os locais de nível comunidade e bairro, e nenhum
  de nível rua ou abaixo

#### Scenario: A comunidade pública traz os tipos de coleta ativos nela

- **WHEN** uma consulta pública pede uma comunidade em que há séries abertas de dois tipos de
  coleta
- **THEN** o núcleo devolve aqueles dois tipos, e não os tipos do catálogo sem série ali

#### Scenario: A comunidade pública traz o número de vinculados

- **WHEN** uma consulta pública pede uma comunidade a que há Guerreiros e Guerreiras
  vinculados
- **THEN** o núcleo devolve a contagem deles, e nenhum nick, avatar ou identificador de
  pessoa alguma

#### Scenario: Comunidade inexistente responde 404

- **WHEN** uma consulta pública pede uma comunidade que não existe
- **THEN** o núcleo responde 404

### Requirement: A lista pública de comunidades devolve os quatro indicadores do documento 02 §1

O núcleo SHALL expor uma rota pública que lista as Comunidades Virtuais, cada uma com **nome**,
**localização**, os **quatro indicadores** do documento 02 §1 — séries abertas, séries ativas ao
fim do ciclo, registros válidos e continuidade — e o **número de Guerreiros e Guerreiras
vinculados**. A rota SHALL responder **sem token de sessão** e SHALL exigir a **chave de
aplicação válida**, como toda rota de dados sob o prefixo de versão. Nenhum **quinto indicador**
do documento 02 §1 SHALL sair por ela.

O número de vinculados NEVER SHALL ser tratado como indicador: ele é o atributo de
**vitalidade** que o card da Comunidade Virtual exige, e por isso sai fora da regra dos quatro —
não entra na avaliação do Poder do Território nem na supressão por piso. (`RF-08-30`,
`RN-08-29`, `RF-01-02`, `RN-01-32`, `RF-03-02`, documento 02 §1, documento 11 §§8.2, 8.3,
PRD-08 §9, decisão do fundador de 2026-09-28)

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

#### Scenario: A vitalidade acompanha os indicadores sem ser um deles

- **WHEN** uma comunidade sai na lista
- **THEN** o número de Guerreiros e Guerreiras vinculados acompanha a resposta, distinto dos
  quatro indicadores

#### Scenario: Comunidade recém-criada sai com os indicadores zerados

- **WHEN** uma comunidade sem nenhuma série sai na lista
- **THEN** séries abertas, séries ativas e registros válidos saem em zero, e a continuidade sai
  nula — não há série sobre a qual tirar média

### Requirement: Comunidade abaixo do piso de coletores permanece na lista, sem os indicadores

O núcleo SHALL manter na lista a comunidade cujo número de coletores distintos não alcança o
**piso declarado na implantação**, com **nome e localização**, e SHALL devolver os **quatro
indicadores nulos** para ela. A comunidade NEVER SHALL ser omitida da lista por estar abaixo do
piso: ela é o **topo da hierarquia** e não há nível acima a que somá-la, de modo que a regra de
subir o recorte não se aplica. O que se omite é o indicador, nunca a comunidade.

O **número de vinculados** SHALL continuar saindo: ele conta quem está vinculado à comunidade,
não quem coletou, e o piso é de coletores distintos no recorte publicado. (`RF-08-31`,
`RN-08-28`, `RN-08-24`, documento 02 §1, decisão do fundador de 2026-09-28)

#### Scenario: Comunidade com coletores abaixo do piso sai sem os números

- **WHEN** uma comunidade tem dois coletores distintos e o piso declarado é três
- **THEN** ela sai na lista com nome e localização, e os quatro indicadores saem nulos

#### Scenario: A vitalidade sai mesmo abaixo do piso

- **WHEN** uma comunidade abaixo do piso de coletores sai na lista
- **THEN** o número de Guerreiros e Guerreiras vinculados a ela sai apurado, ao lado dos
  quatro indicadores nulos

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

### Requirement: A lista de comunidades não identifica coletor algum

O núcleo NEVER SHALL devolver, na lista de comunidades, identificador, nick, avatar ou nome de
coletor, nem contagem que isole um. Os quatro indicadores e o número de vinculados SHALL ser
contagens agregadas da comunidade inteira. O vínculo de autoria continua gravado: a anonimização
é da **saída**, nunca do armazenamento. (`RN-08-12`, `RN-08-11`, `RF-03-16`, `RN-03-10`,
invariante 7 do documento 99 §6)

#### Scenario: Nenhum campo da resposta identifica quem coletou

- **WHEN** se percorre a resposta inteira da lista de comunidades
- **THEN** nenhum campo traz coletor, e a contagem de coletores distintos que decide o piso não
  sai na resposta

#### Scenario: A vitalidade é contagem, nunca lista de pessoas

- **WHEN** a lista devolve o número de Guerreiros e Guerreiras vinculados de uma comunidade
- **THEN** sai o número, e nenhum nick, avatar ou identificador de quem está vinculado
