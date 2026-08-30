## Purpose

O template da missão: o Mestre autor cadastra em texto corrente o tópico que quer ensinar e
recebe de volta o **esqueleto** da missão e o **checklist do que falta** — nunca o conteúdo,
que é escrito por ele, autor creditado na licença. Nada do que o template propõe entra na
trilha sem o Mestre confirmar.

## ADDED Requirements

### Requirement: O Mestre autor cadastra o tópico e recebe a estrutura sugerida

O núcleo SHALL receber, para uma missão, o **tópico que o Mestre quer ensinar** em **texto
corrente**, e devolver a **estrutura sugerida** da missão no modelo do documento 11 §2.2: as
atividades que cabem ali, com modalidade e formato, a produção que cada uma pede do
Guerreiro(a), o desafio de desbloqueio e a retomada.

Só o **Mestre autor da trilha** a que a missão pertence SHALL pedir a estrutura; persona que
não é o autor SHALL ser recusada com **403**, como já vale para todo o restante da autoria da
trilha. Pedido **sem tópico**, ou com tópico vazio, SHALL ser recusado com **422** indicando o
campo.

O núcleo SHALL gravar cada pedido como uma **sugestão de estrutura** da missão, com o tópico
cadastrado, a estrutura proposta, as lacunas apontadas e a situação. Pedir de novo SHALL gravar
uma **sugestão nova**, sem apagar a anterior: a sugestão é registro do que foi proposto, não
estado da missão. (`RF-09-85`, `RF-09-91`, PRD-09 §8)

#### Scenario: O tópico em texto corrente devolve a estrutura

- **WHEN** o Mestre autor cadastra, em texto corrente, o tópico que quer ensinar numa missão
  dele
- **THEN** o núcleo devolve a estrutura sugerida da missão e grava a sugestão com o tópico
  cadastrado

#### Scenario: Quem não é o autor não pede a estrutura

- **WHEN** um Mestre que não é o autor da trilha pede a estrutura de uma missão dela
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Pedido sem tópico é recusado

- **WHEN** chega um pedido de estrutura sem tópico, ou com o tópico vazio
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: Pedir de novo não apaga a sugestão anterior

- **WHEN** o Mestre autor pede a estrutura da mesma missão uma segunda vez
- **THEN** o núcleo grava uma sugestão nova, e a anterior permanece registrada

### Requirement: O template aponta as lacunas da missão

Junto da estrutura, o núcleo SHALL apontar as **lacunas** da missão como ela está no momento
do pedido, em **linguagem simples e sem código de erro**, cobrindo ao menos:

1. missão **sem nenhuma atividade**;
2. atividade **sem produção declarada** do Guerreiro(a) — escrever, falar ou construir. A
   `RN-09-31` já é **trava na criação** da atividade, e o checklist a repete para que a missão
   montada por outro caminho, como a que nasce de uma duplicação, não escape dela;
3. **retomada não declarada** na missão;
4. em trilha de **poder técnico**, missão **sem nenhuma atividade desplugada**.

As lacunas SHALL ser conferidas pelo **núcleo**, contra o que está gravado na missão, e NEVER
SHALL depender do que o modelo respondeu: lacuna é fato da missão, não opinião. Missão sem
lacuna alguma SHALL devolver a lista **vazia**, nunca um erro. A lista de lacunas NEVER SHALL
recusar, travar ou alterar a missão: o template informa, e a trava de publicação segue sendo a
da capacidade `trilha-e-missao`. (`RF-09-86`, `RN-09-31`, `RN-09-33`, PRD-09 §12)

#### Scenario: Missão sem atividade é apontada

- **WHEN** o Mestre autor pede a estrutura de uma missão que ainda não tem atividade alguma
- **THEN** as lacunas trazem, em linguagem simples, que falta ao menos uma atividade

#### Scenario: Atividade sem produção é apontada

- **WHEN** a missão tem atividade cuja produção do Guerreiro(a) está em branco
- **THEN** as lacunas dizem qual atividade está sem produção

#### Scenario: Atividade com produção declarada não vira lacuna

- **WHEN** toda atividade da missão declara o que o Guerreiro(a) produz
- **THEN** nenhuma lacuna de produção é apontada

#### Scenario: Retomada não declarada é apontada

- **WHEN** a missão não tem cadência de retomada declarada
- **THEN** as lacunas dizem que a retomada não foi declarada

#### Scenario: Missão completa devolve lista vazia

- **WHEN** a missão já tem atividade com produção, retomada declarada e, sendo de poder
  técnico, atividade desplugada
- **THEN** a lista de lacunas vem vazia e nenhum erro é devolvido

#### Scenario: A lacuna não trava a missão

- **WHEN** o template aponta lacunas numa missão
- **THEN** a missão permanece exatamente como estava, e nada nela é recusado por causa das
  lacunas

### Requirement: Em trilha de poder técnico a estrutura começa por atividade desplugada

Sendo a trilha vinculada a um poder **marcado como técnico** no catálogo, a estrutura sugerida
SHALL incluir ao menos **uma atividade desplugada**, e ela SHALL vir **em primeiro lugar** na
sequência proposta. Em trilha de poder **não** marcado como técnico, a atividade desplugada
NEVER SHALL ser exigida na sugestão — ela pode aparecer, mas não é regra.

O núcleo NEVER SHALL deduzir do **nome** do poder que ele é técnico: a marca é declarada no
catálogo, como já vale para o papel do poder. (`RF-09-88`, `RN-09-34`, `RN-01-54`, documento
11 §2.2, decisão do fundador de 2026-08-29)

#### Scenario: Trilha de poder técnico começa desplugada

- **WHEN** o Mestre autor pede a estrutura de uma missão de trilha vinculada a poder marcado
  como técnico
- **THEN** a estrutura sugerida traz ao menos uma atividade desplugada, e ela é a primeira da
  sequência

#### Scenario: Trilha de área não técnica não exige a desplugada

- **WHEN** o Mestre autor pede a estrutura de uma missão de trilha vinculada a poder sem a
  marca de técnico
- **THEN** a estrutura sugerida é devolvida sem exigir atividade desplugada

#### Scenario: O nome do poder não o torna técnico

- **WHEN** existe no catálogo um poder de nome técnico sem a marca declarada
- **THEN** a estrutura sugerida das trilhas dele não exige atividade desplugada

### Requirement: A sugestão traz a etiqueta ODS e a cadência de retomada

A estrutura sugerida SHALL trazer a **etiqueta ODS** derivada do tópico cadastrado — o
objetivo e, quando couber, a meta — e a **cadência de retomada** de **2, 7 e 21 dias** contados
do desbloqueio.

As duas SHALL ser **sugestão**: o Mestre confirma, altera ou recusa, e a gravação continua
acontecendo pelas capacidades que já a fazem — `etiqueta-ods` para a etiqueta e
`trilha-e-missao` para a cadência. O template NEVER SHALL declarar etiqueta nem cadência por
conta própria. Não sendo possível derivar etiqueta alguma do tópico, a sugestão SHALL vir **sem
etiqueta**, nunca com um objetivo arbitrado. (`RF-09-95`, `RF-09-116`, `RN-09-35`, documento
11 §2.2)

#### Scenario: A sugestão traz o ODS derivado do tópico

- **WHEN** o Mestre autor cadastra um tópico que toca um objetivo de desenvolvimento
  sustentável
- **THEN** a estrutura sugerida traz aquele objetivo como etiqueta proposta, e nada é gravado
  como etiqueta da missão

#### Scenario: A retomada é sugerida em 2, 7 e 21 dias

- **WHEN** o Mestre autor recebe a estrutura sugerida de uma missão
- **THEN** a cadência de retomada proposta é de 2, 7 e 21 dias contados do desbloqueio

#### Scenario: Tópico sem ODS derivável não recebe objetivo arbitrado

- **WHEN** não é possível derivar objetivo algum do tópico cadastrado
- **THEN** a sugestão vem sem etiqueta ODS, e nenhum objetivo é proposto

### Requirement: O template não escreve o conteúdo da missão

O template SHALL propor **estrutura e lacunas** e NEVER SHALL escrever o **conteúdo** da
missão: nenhum campo de `Conteudo` — corpo de texto, imagem, link, vídeo ou arquivo — SHALL ser
criado, preenchido ou alterado por ele. A autoria do que for publicado SHALL permanecer do
**Mestre**, creditado na licença CC BY-SA, exatamente como a capacidade `trilha-e-missao` já
credita. (`RF-09-87`, `RN-09-33`, `RN-09-05`, documento 03 §11, PRD-09 §12)

#### Scenario: Nenhum conteúdo é criado pelo template

- **WHEN** o Mestre autor pede a estrutura de uma missão
- **THEN** nenhum conteúdo da missão é criado nem alterado, e os que já existiam permanecem
  como estavam

#### Scenario: A autoria continua do Mestre

- **WHEN** a trilha cuja missão usou o template é publicada
- **THEN** o crédito de autoria e a licença CC BY-SA continuam nomeando o Mestre autor

### Requirement: Nada entra na trilha sem o Mestre confirmar

O núcleo SHALL registrar, para cada sugestão, o desfecho que o Mestre autor lhe deu:
**aceita**, **recusada** ou **alterada**. Enquanto o Mestre não age, a missão SHALL permanecer
exatamente como estava: a sugestão NEVER SHALL criar atividade, declarar retomada, etiquetar a
missão nem alterar qualquer campo dela por si.

O que o Mestre aceita ou altera SHALL ser gravado pelas rotas de autoria que já existem — a
atividade pela capacidade `atividade-de-trilha`, a cadência e a missão por `trilha-e-missao`, a
etiqueta por `etiqueta-ods` —, com as mesmas recusas e as mesmas travas. A sugestão recusada
SHALL permanecer registrada com a situação de recusada, sem tocar a missão. (`RF-09-89`,
`RN-09-33`, PRD-09 §12)

#### Scenario: Sugestão não confirmada não muda a missão

- **WHEN** o núcleo devolve a estrutura sugerida e o Mestre ainda não agiu sobre ela
- **THEN** a missão permanece sem atividade nova, sem retomada nova e sem etiqueta nova

#### Scenario: O Mestre aceita e a gravação segue a rota de autoria

- **WHEN** o Mestre autor aceita uma atividade sugerida
- **THEN** ela é criada pela rota de atividade da missão, com as mesmas recusas de modalidade e
  formato, e a sugestão fica registrada como aceita

#### Scenario: O Mestre recusa a sugestão

- **WHEN** o Mestre autor recusa a estrutura sugerida
- **THEN** a sugestão fica registrada como recusada e nada da missão é alterado

#### Scenario: O Mestre altera antes de gravar

- **WHEN** o Mestre autor altera a atividade sugerida antes de criá-la
- **THEN** o que é gravado é o texto dele, e a sugestão fica registrada como alterada

### Requirement: Nenhum consumo do modelo é medido nem lançado

O núcleo NEVER SHALL medir, contar nem lançar no livro-razão o consumo do modelo usado pelo
template — nem por pedido, nem por token, nem por período. O custo SHALL entrar como recurso de
_cloud_ pela **fatura**, como já acontece com o armazenamento do conteúdo da missão. Nenhuma
resposta do template SHALL trazer custo, cota, contagem de uso ou valor em moedas ou reais.
(`RF-09-90`, `RN-09-07`, documento 04 §1)

#### Scenario: O pedido de estrutura não gera lançamento

- **WHEN** o Mestre autor pede a estrutura de uma missão
- **THEN** nenhum lançamento é emitido no livro-razão e nenhum contador de consumo é gravado

#### Scenario: A resposta não traz custo nem cota

- **WHEN** o núcleo devolve a estrutura sugerida
- **THEN** nenhum campo da resposta traz custo, cota, contagem de uso ou valor em moedas ou
  reais

### Requirement: A indisponibilidade do modelo não trava a autoria

Não sendo possível obter a estrutura do modelo — indisponibilidade, erro ou demora do provedor
—, o núcleo SHALL responder ao Mestre em **linguagem simples**, dizendo que a sugestão não veio
e que ele pode seguir escrevendo a missão à mão, e NEVER SHALL expor mensagem, código ou
detalhe técnico do provedor.

Mesmo sem a estrutura do modelo, o núcleo SHALL devolver as **lacunas**, que ele confere
sozinho. A missão SHALL permanecer editável e publicável por todas as rotas de autoria: o
template NEVER SHALL ser etapa obrigatória para escrever, completar ou publicar uma missão.
(`RF-09-91`, `RN-09-16`, PRD-09 §10)

#### Scenario: Modelo indisponível avisa sem jargão

- **WHEN** o provedor do modelo não responde ao pedido de estrutura
- **THEN** o Mestre recebe um aviso em linguagem simples de que a sugestão não veio, sem código
  nem mensagem técnica do provedor

#### Scenario: As lacunas vêm mesmo sem o modelo

- **WHEN** o provedor do modelo não responde e a missão está sem atividade
- **THEN** as lacunas são devolvidas assim mesmo, apontando que falta atividade

#### Scenario: A missão se completa sem o template

- **WHEN** o Mestre autor escreve, completa e publica uma trilha sem nunca pedir a estrutura
- **THEN** nada é recusado por falta de sugestão de estrutura
