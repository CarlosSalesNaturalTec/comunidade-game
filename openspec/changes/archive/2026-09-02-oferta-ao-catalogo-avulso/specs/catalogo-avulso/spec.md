## ADDED Requirements

### Requirement: Quem ofertou lê os próprios itens em qualquer situação

O núcleo SHALL devolver ao **Apoiador** em sessão os itens do catálogo avulso que **ele
cadastrou**, em **qualquer situação** — pendente de homologação, homologado, recusado, ativo ou
inativo —, trazendo de cada um o nome, o tipo de recurso, o **estoque restante**, a **situação da
homologação** com o **motivo** da recusa quando houver, a marca de **ativo**, o **preço em pontos
extras da vigência corrente**, a marca de **preço de referência ausente** e a **quantidade que
falta de lastro**. Essa leitura NEVER SHALL trazer item cadastrado por outra persona, e NEVER
SHALL trazer valor em moedas nem em reais. Persona de qualquer outro papel SHALL receber **403**.
(`RF-14-80`, `RF-14-77`, `RN-14-42`, `RN-07-24`, invariante 23)

#### Scenario: O item pendente aparece para quem o ofertou

- **WHEN** um Apoiador em sessão consulta os itens que ofertou e um deles segue pendente de
  homologação, portanto inativo
- **THEN** o núcleo devolve o item com a situação pendente e a marca de inativo

#### Scenario: O item recusado aparece com o motivo

- **WHEN** um Admin recusa, com motivo, um item que o Apoiador ofertou
- **THEN** a consulta do Apoiador devolve o item como recusado, com o motivo registrado

#### Scenario: O item sem preço de referência diz o que falta

- **WHEN** o Apoiador consulta um item que ofertou cujo tipo de recurso não tem preço de
  referência vigente
- **THEN** o núcleo devolve o item inativo, com a marca de preço de referência ausente

#### Scenario: O item sem lastro diz a quantidade que falta

- **WHEN** o Apoiador consulta um item que ofertou cujo saldo do tipo no ponto de apoio é menor
  que o estoque declarado
- **THEN** o núcleo devolve o item inativo, com a quantidade que falta de lastro

#### Scenario: Item de outro proponente não aparece

- **WHEN** um Apoiador em sessão consulta os itens que ofertou e há itens cadastrados por um
  Mestre ou por outro Apoiador na mesma comunidade
- **THEN** esses itens NEVER aparecem na resposta

#### Scenario: Persona de outro papel não lê esta consulta

- **WHEN** um Mestre, um Admin, um Guerreiro(a) ou um responsável em sessão pede os itens
  ofertados por si
- **THEN** o núcleo responde 403

### Requirement: A leitura da própria oferta traz as trocas em contagem, nunca em identificação

A leitura dos próprios itens SHALL trazer, de cada item, a **quantidade de trocas** já
entregues — a contagem simples das trocas registradas daquele item. A resposta NEVER SHALL
trazer identificação alguma de quem trocou: nem persona, nem nick, nem avatar, nem aula, nem
data de troca individual. (`RF-14-80`, `RF-14-81`, `RN-14-44`, `RN-14-20`)

#### Scenario: A contagem de trocas acompanha as entregas

- **WHEN** três trocas de um item ofertado pelo Apoiador foram entregues
- **THEN** a consulta do Apoiador devolve aquele item com a quantidade de trocas igual a três

#### Scenario: Item sem troca alguma traz contagem zero

- **WHEN** o Apoiador consulta um item que ofertou e que ainda não foi trocado por ninguém
- **THEN** o núcleo devolve o item com a quantidade de trocas igual a zero

#### Scenario: A resposta não identifica quem trocou

- **WHEN** o Apoiador consulta os itens que ofertou e há trocas entregues
- **THEN** a resposta traz apenas a contagem, e NEVER traz persona, nick, avatar, aula ou data de
  troca individual
