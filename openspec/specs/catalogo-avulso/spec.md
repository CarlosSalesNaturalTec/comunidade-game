## Purpose

O catálogo de recompensas avulsas de cada comunidade — o item que o Guerreiro(a) troca por
pontos extras, com o tipo de recurso que o lastreia, o estoque declarado, o ponto de apoio em
que ele está guardado e o preço lido da tabela de referência da gestão. Cobre o cadastro, a
homologação, o lastro, a manutenção e a leitura do catálogo; a troca em si é capacidade
própria.

## Requirements

### Requirement: O item do catálogo avulso é cadastrado por Mestre ou por Apoiador

O núcleo SHALL manter o **item do catálogo avulso** com **nome**, **tipo de recurso**,
**estoque** declarado, **comunidade**, **ponto de apoio** e a **origem do cadastro**. O ponto de
apoio declarado SHALL pertencer à comunidade do item; ponto de apoio de outra comunidade SHALL
ser recusado com **422**. O tipo de recurso declarado NÃO SHALL ser de natureza **durável**:
o saldo durável é patrimônio e nunca lastreia recompensa, de modo que o item jamais poderia
ativar; o cadastro que o declare SHALL ser recusado com **422**, indicando o tipo. Essa recusa
convive com a regra do lastro sem contradizê-la: o item **sem lastro** nasce inativo e nunca é
recusado, porque o lastro ainda pode chegar; o item de tipo durável é recusado porque a
impossibilidade é estrutural. Cadastrar item SHALL exigir persona **Mestre** ou **Apoiador** em
sessão; **Admin**, **Guerreiro(a)** e **responsável** SHALL receber **403**. O Mestre SHALL só
cadastrar item em comunidade a que está vinculado. Cadastro sem nome, sem tipo de recurso, sem
estoque, sem comunidade ou sem ponto de apoio SHALL ser recusado com **422**, indicando o campo
em falta, e estoque menor que 1 SHALL ser recusado com **422**. A escrita SHALL gravar autoria,
data e hora com fuso. (`RF-07-33`, `RF-07-34`, `RN-07-07`, `RN-07-26`, `RF-09-99`, `RF-14-77`,
`RN-07-33`, `RF-01-16`, `RF-01-03`, `RF-01-27`, PRD-07 §8)

#### Scenario: Mestre cadastra item na sua comunidade

- **WHEN** um Mestre em sessão cadastra um item com nome, tipo de recurso, estoque, comunidade a
  que está vinculado e ponto de apoio dela
- **THEN** o núcleo grava o item com a origem de cadastro Mestre, o autor, a data e a hora com
  fuso

#### Scenario: Apoiador oferta item ao catálogo

- **WHEN** um Apoiador em sessão cadastra um item com nome, tipo de recurso, estoque, comunidade
  e ponto de apoio
- **THEN** o núcleo grava o item com a origem de cadastro Apoiador

#### Scenario: Ponto de apoio de outra comunidade é recusado

- **WHEN** chega um cadastro de item cujo ponto de apoio pertence a comunidade diferente da
  declarada no item
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Item de tipo durável é recusado no cadastro

- **WHEN** um Mestre em sessão cadastra um item cujo tipo de recurso é de natureza durável
- **THEN** o núcleo responde 422 indicando o tipo e nada é gravado

#### Scenario: Item de tipo consumível sem lastro segue aceito e inativo

- **WHEN** chega um cadastro de item de tipo consumível cujo ponto de apoio não tem saldo algum
  daquele tipo
- **THEN** o núcleo grava o item e ele nasce inativo, sem ser recusado

#### Scenario: Mestre não cadastra item em comunidade a que não está vinculado

- **WHEN** um Mestre em sessão tenta cadastrar item em comunidade a que não está vinculado
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Guerreiro(a) não cadastra item

- **WHEN** um Guerreiro(a) em sessão tenta cadastrar item do catálogo avulso
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Estoque menor que um é recusado

- **WHEN** chega um cadastro de item com estoque zero ou negativo
- **THEN** o núcleo responde 422 e nada é gravado

### Requirement: A origem do cadastro decide se o item precisa de homologação

O item cadastrado por **Mestre** SHALL entrar no catálogo **sem homologação**. O item cadastrado
por **Apoiador** SHALL nascer **pendente de homologação** e NEVER SHALL ficar ativo antes de um
**Admin** o homologar. Homologar item SHALL exigir persona **Admin** em sessão; persona de
qualquer outro papel SHALL receber **403**. O Admin SHALL poder **recusar** o item pendente, com
motivo registrado, e o item recusado NEVER SHALL ficar ativo. A homologação e a recusa SHALL
gravar autoria, data e hora com fuso. (`RF-09-100`, `RF-14-77`, `RN-14-42`, `RN-07-26`,
`RF-01-16`, PRD-07 §8)

#### Scenario: Item de Mestre dispensa homologação

- **WHEN** um Mestre cadastra um item do catálogo avulso
- **THEN** o núcleo grava o item com homologação não aplicável, e ele segue direto para a
  verificação de lastro

#### Scenario: Item de Apoiador nasce pendente

- **WHEN** um Apoiador cadastra um item do catálogo avulso
- **THEN** o núcleo grava o item pendente de homologação e inativo, ainda que haja lastro

#### Scenario: Admin homologa item pendente

- **WHEN** um Admin em sessão homologa um item pendente que tem lastro
- **THEN** o núcleo grava a homologação com autor, data e hora com fuso, e o item passa a ativo

#### Scenario: Admin recusa item pendente

- **WHEN** um Admin em sessão recusa um item pendente, com motivo
- **THEN** o núcleo grava a recusa com o motivo e o item permanece inativo

#### Scenario: Mestre não homologa item de Apoiador

- **WHEN** um Mestre em sessão tenta homologar um item pendente
- **THEN** o núcleo responde 403 e o item permanece pendente

### Requirement: O item só fica ativo com lastro igual ou maior que o estoque declarado

O núcleo SHALL considerar o item **lastreado** quando a **quantidade disponível** do seu tipo de
recurso no **seu ponto de apoio** for **igual ou maior que o estoque declarado**. Item sem
lastro SHALL ser gravado **inativo**, nunca recusado, e a resposta SHALL dizer a quantidade que
falta. Ativar item SHALL exigir persona **Admin** ou **Mestre vinculado à comunidade** do item,
SHALL reverificar o lastro no ato e SHALL ser recusado com **422** faltando qualquer parcela.
Item pendente de homologação ou recusado NEVER SHALL ser ativado. (`RF-07-34`, `RF-09-101`,
`RN-07-26`, `RN-09-37`, `RN-14-42`, invariante 9)

#### Scenario: Item com lastro nasce ativo

- **WHEN** um Mestre cadastra um item com estoque 10 e o saldo disponível daquele tipo no ponto
  de apoio do item é 10
- **THEN** o núcleo grava o item ativo

#### Scenario: Item sem lastro suficiente nasce inativo

- **WHEN** um Mestre cadastra um item com estoque 10 e o saldo disponível daquele tipo no ponto
  de apoio do item é 4
- **THEN** o núcleo grava o item inativo e a resposta diz que faltam 6

#### Scenario: Saldo de outro ponto de apoio não lastreia o item

- **WHEN** um Mestre cadastra um item cujo tipo de recurso tem saldo suficiente em outro ponto de
  apoio da mesma comunidade, e nenhum no ponto de apoio declarado
- **THEN** o núcleo grava o item inativo

#### Scenario: Ativação reverifica o lastro

- **WHEN** um Mestre vinculado à comunidade ativa um item inativo cujo saldo passou a cobrir o
  estoque declarado
- **THEN** o núcleo grava o item ativo, com autoria, data e hora com fuso

#### Scenario: Ativação sem lastro é recusada

- **WHEN** um Mestre tenta ativar um item cujo saldo disponível segue menor que o estoque
  declarado
- **THEN** o núcleo responde 422 dizendo a quantidade que falta, e o item permanece inativo

#### Scenario: Item pendente de homologação não é ativado

- **WHEN** um Mestre tenta ativar um item de Apoiador ainda pendente de homologação, mesmo com
  lastro
- **THEN** o núcleo responde 422 e o item permanece inativo

### Requirement: O item não tem preço próprio e lê o da tabela de referência

O cadastro do item NEVER SHALL aceitar campo de preço: o preço do item SHALL ser sempre o
**preço de referência vigente do seu tipo de recurso**, lido na data da consulta. Cadastro que
declare preço SHALL ser recusado com **422**. Item cujo tipo de recurso não tem preço de
referência vigente SHALL ser gravado **inativo**, e a resposta SHALL dizer que falta o preço.
(`RF-07-45`, `RF-07-38`, `RF-09-103`, `RN-07-25`, `RN-07-29`, invariante 23)

#### Scenario: Cadastro com preço declarado é recusado

- **WHEN** chega um cadastro de item do catálogo avulso declarando preço em pontos extras
- **THEN** o núcleo responde 422 e nada é gravado

#### Scenario: Item exibe o preço da vigência corrente

- **WHEN** o catálogo é consultado e o preço de referência do tipo de recurso de um item mudou
  desde o cadastro
- **THEN** o item aparece com o preço da vigência corrente, sem que o cadastro tenha sido tocado

#### Scenario: Item de tipo sem preço de referência nasce inativo

- **WHEN** um Mestre cadastra item de um tipo de recurso que não tem preço de referência vigente
- **THEN** o núcleo grava o item inativo e a resposta diz que falta o preço de referência

### Requirement: O estoque é alterado e o item é retirado do catálogo, com autoria

Alterar o estoque de um item e **retirar** o item do catálogo SHALL exigir persona **Admin** ou
**Mestre vinculado à comunidade** do item; persona de qualquer outro papel SHALL receber **403**.
A retirada SHALL deixar o item **inativo** e NEVER SHALL apagar o item nem o seu histórico.
Estoque alterado para quantidade maior que o lastro disponível SHALL deixar o item **inativo**,
e a resposta SHALL dizer a quantidade que falta. Toda alteração SHALL gravar autoria, data e
hora com fuso.

Além desse caminho de gestão, o estoque SHALL decrescer **uma unidade por troca entregue**, sem
persona alterando-o e sem passar pela verificação de papel acima — o decremento é parte da
operação única da troca. Item que chega a **estoque zero** por troca NÃO SHALL ser retirado nem
marcado inativo por isso: ele permanece cadastrado e ativo, e deixa de ser trocável pela recusa
por estoque, para que o Mestre reponha o estoque sem recadastrar o item. (`RF-07-33`,
`RF-09-102`, `RF-07-34`, `RF-07-36`, `RF-07-37`, `RF-01-16`, `RF-01-27`)

#### Scenario: Mestre altera o estoque do item

- **WHEN** um Mestre vinculado à comunidade altera o estoque de um item para quantidade coberta
  pelo lastro
- **THEN** o núcleo grava o estoque novo com autor, data e hora com fuso, e o item permanece
  ativo

#### Scenario: Estoque acima do lastro desativa o item

- **WHEN** um Mestre altera o estoque de um item ativo para quantidade maior que o saldo
  disponível do tipo no ponto de apoio do item
- **THEN** o núcleo grava o estoque novo, deixa o item inativo e diz a quantidade que falta

#### Scenario: Mestre retira o item do catálogo

- **WHEN** um Mestre vinculado à comunidade retira um item do catálogo
- **THEN** o núcleo deixa o item inativo, preservando o registro, com autor, data e hora com fuso

#### Scenario: Apoiador não altera item já cadastrado

- **WHEN** um Apoiador em sessão tenta alterar o estoque de um item do catálogo
- **THEN** o núcleo responde 403 e o item permanece como estava

#### Scenario: A troca decrementa o estoque em uma unidade

- **WHEN** uma troca de um item de estoque 5 é entregue
- **THEN** o estoque do item passa a 4, sem alteração de gestão e sem mudar a marca de ativo

#### Scenario: Estoque zerado por troca não retira o item

- **WHEN** a última unidade em estoque de um item ativo é trocada
- **THEN** o item permanece cadastrado e ativo com estoque zero, e a próxima troca é recusada
  por falta de estoque

### Requirement: O catálogo é lido por comunidade, com o preço vigente e o estoque

O núcleo SHALL devolver o catálogo avulso **filtrado por comunidade**, trazendo de cada item o
nome, o tipo de recurso, o **preço em pontos extras da vigência corrente**, o **estoque** e a
marca de ativo. A leitura SHALL exigir persona em sessão: **Guerreiro(a)** SHALL ler o catálogo
da **sua** comunidade, **Mestre** e **Apoiador** o das comunidades a que estão vinculados, e
**Admin** o de qualquer comunidade. A leitura SHALL trazer apenas itens **ativos**, salvo para
Admin e para Mestre vinculado, que SHALL poder pedir também os inativos. NEVER SHALL a resposta
trazer valor em moedas nem em reais. (`RF-07-33`, `RF-04-50`, `RF-05-83`, `RF-09-103`,
`RN-07-24`, `RF-01-24`, invariante 23)

#### Scenario: Guerreiro(a) lê o catálogo da sua comunidade

- **WHEN** um Guerreiro(a) em sessão consulta o catálogo avulso
- **THEN** o núcleo devolve apenas os itens ativos da comunidade dele, com nome, tipo de recurso,
  preço em pontos extras da vigência corrente e estoque

#### Scenario: Catálogo de outra comunidade não aparece

- **WHEN** um Guerreiro(a) em sessão consulta o catálogo avulso e há itens ativos em outra
  comunidade
- **THEN** os itens da outra comunidade NEVER aparecem na resposta

#### Scenario: Mestre pede também os itens inativos

- **WHEN** um Mestre vinculado à comunidade consulta o catálogo pedindo os inativos
- **THEN** o núcleo devolve os itens ativos e os inativos daquela comunidade, com a marca de cada
  um

#### Scenario: Nenhuma leitura do catálogo devolve moedas nem reais

- **WHEN** o catálogo avulso é consultado por qualquer persona
- **THEN** a resposta traz o preço em pontos extras, e NEVER traz valor em moedas nem em reais
