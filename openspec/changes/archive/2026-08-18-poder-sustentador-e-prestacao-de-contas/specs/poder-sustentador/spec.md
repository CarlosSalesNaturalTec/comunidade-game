## Purpose

O reconhecimento de quem sustenta o projeto: quanto cada provedor aportou, em moedas, e quantas
vezes ele bancou do próprio bolso a atividade que não tinha recurso. São dois números com
origens diferentes — um deriva do livro-razão e se move com ele, o outro conta atos e não se
desfaz — e é esta capacidade que os mantém separados.

## ADDED Requirements

### Requirement: O Poder Sustentador é derivado dos lançamentos, nunca da soma dos aportes

O núcleo SHALL calcular o **Poder Sustentador** de um provedor como a soma, em moedas, dos
**lançamentos de crédito** originados dos aportes daquele provedor, mais os **lançamentos de
ajuste** que referenciem esses créditos. O número SHALL ser sempre derivado e recontável: refazer
a soma a partir dos lançamentos SHALL devolver o mesmo valor, sem depender de total guardado à
parte. Lançamento de **débito** NÃO SHALL compor o Poder Sustentador de provedor algum — o débito
é consumo da atividade, não contribuição de pessoa. (`RF-07-10`, `RN-07-15`, PRD-07 §§8, 12)

#### Scenario: O aporte sobe o Poder Sustentador exatamente no que valeu

- **WHEN** um provedor tem um aporte material de quantidade 3 de um tipo cujo valor de
  referência vigente é 0,50 moeda
- **THEN** o Poder Sustentador dele é 1,50

#### Scenario: O ajuste sobre o crédito move o Poder Sustentador

- **WHEN** um Admin lança um ajuste de -0,50 sobre o crédito de um aporte de 1,50 moeda
- **THEN** o Poder Sustentador do provedor daquele aporte passa a 1,00

#### Scenario: A recontagem devolve o mesmo número

- **WHEN** o Poder Sustentador de um provedor é recalculado a partir dos lançamentos
- **THEN** o valor devolvido é igual ao anterior

#### Scenario: O consumo da aula não desconta de ninguém

- **WHEN** uma aula dá baixa em 4 de um tipo de recurso, gerando um débito
- **THEN** o Poder Sustentador de todo provedor permanece o que era

#### Scenario: Provedor sem aporte tem Poder Sustentador zero

- **WHEN** um adulto cadastrado nunca aportou nada
- **THEN** o Poder Sustentador dele é zero, e a leitura responde normalmente

### Requirement: A contagem de absorções deriva dos aportes e não se move com o ledger

O núcleo SHALL contar, para cada provedor, **quantas vezes** ele sustentou atividade sem recurso
— o número de aportes dele de forma **absorção**. Essa contagem SHALL ser derivada dos
**aportes**, nunca dos lançamentos, e por isso NÃO SHALL ser alterada por ajuste, estorno ou
qualquer movimento posterior do livro-razão sobre aqueles créditos. A saída SHALL trazer o
número de absorções e NUNCA valor em reais. (`RF-07-26`, `RN-07-19`, PRD-07 §12, invariante 16
do documento 99 §6)

#### Scenario: Cada absorção conta uma vez

- **WHEN** um Mestre registrou três aportes por absorção e dois aportes de outra forma
- **THEN** a contagem de absorções dele é 3

#### Scenario: O ajuste no ledger não apaga a absorção

- **WHEN** um Admin lança um ajuste sobre o crédito de um aporte por absorção
- **THEN** o Poder Sustentador do provedor muda e a contagem de absorções dele continua a mesma

#### Scenario: Quem nunca absorveu conta zero

- **WHEN** um Apoiador tem aportes financeiros e nenhum por absorção
- **THEN** a contagem de absorções dele é zero

#### Scenario: A contagem nunca sai em reais

- **WHEN** a contagem de absorções de um provedor é lida
- **THEN** a resposta traz o número de atos e nenhum valor em reais

### Requirement: A leitura por provedor é pública e nunca alcança Guerreiro(a)

O núcleo SHALL responder `GET /provedores/{id}/poder-sustentador` **sem token de sessão**, e
SHALL exigir a **chave de aplicação válida**, como em toda rota de dados sob `/v1`; a recusa por
chave ausente, inválida ou revogada SHALL ser o **401** indistinto que a capacidade
`chave-de-aplicacao` já define. A resposta SHALL trazer o Poder Sustentador em **moedas** e a
contagem de absorções, e NÃO SHALL trazer valor em reais, comprovante, dado bancário nem dado de
contato.

O provedor é sempre adulto (`RN-07-06`). A rota SHALL responder **404** para persona de
Guerreiro(a) ou de responsável e para identificador inexistente, com **a mesma recusa** nos dois
casos, de modo que a resposta não confirme a existência de ninguém. (`RF-07-10`, `RF-07-26`,
`RN-07-05`, `RN-07-06`, `RF-01-02`, `RN-01-32`, `RN-01-33`, PRD-07 §9)

#### Scenario: Visitante sem persona lê o Poder Sustentador

- **WHEN** uma consulta chega com chave de aplicação válida e sem token de sessão
- **THEN** o núcleo responde com o Poder Sustentador em moedas e a contagem de absorções

#### Scenario: Sem chave a rota não responde

- **WHEN** uma consulta chega sem chave de aplicação válida
- **THEN** o núcleo responde 401, sem distinguir chave ausente de chave revogada

#### Scenario: A rota não serve Guerreiro(a)

- **WHEN** a consulta usa o identificador de uma persona de Guerreiro(a)
- **THEN** o núcleo responde 404, com a mesma recusa que daria a um identificador inexistente

#### Scenario: Nenhuma saída traz reais

- **WHEN** o provedor consultado tem aportes com valor de origem em reais registrado
- **THEN** a resposta traz apenas moedas, sem campo auxiliar algum com o valor em reais

### Requirement: O Apoiador lê os próprios aportes e o próprio Poder Sustentador, sem escrita

O núcleo SHALL responder `GET /meus-aportes` à persona **Apoiador** em sessão, devolvendo os
aportes dela e o Poder Sustentador dela. A rota SHALL alcançar **somente** os aportes da persona
em sessão. A leitura SHALL ser somente de consulta: esta capacidade NÃO SHALL expor rota de
escrita sobre aporte algum. O valor de origem em **reais** SHALL ficar fora da resposta — o
acesso a ele é da gestão (PRD-07 §11). (`RF-07-17`, `RN-07-05`, `RF-01-16`, PRD-07 §§9, 11)

#### Scenario: O Apoiador vê os aportes dele

- **WHEN** um Apoiador em sessão consulta os próprios aportes
- **THEN** o núcleo devolve os aportes dele, em moedas, e o Poder Sustentador dele

#### Scenario: O aporte alheio fica de fora

- **WHEN** um Apoiador em sessão consulta os próprios aportes e outro Apoiador também tem
  aportes registrados
- **THEN** a resposta traz apenas os aportes da persona em sessão

#### Scenario: Sem sessão de persona a rota não responde

- **WHEN** a consulta chega com chave de aplicação válida e sem token de sessão
- **THEN** o núcleo recusa, porque a rota exige a credencial da persona

#### Scenario: A leitura não abre edição

- **WHEN** um Apoiador tenta alterar um aporte próprio por esta capacidade
- **THEN** não há rota que o faça: a capacidade é somente de leitura
