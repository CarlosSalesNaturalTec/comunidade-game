## ADDED Requirements

### Requirement: O registro aprovado da customização é a terceira fonte do acervo público

O acervo público SHALL trazer, ao lado da criação original e da comprovação do prático, o
**registro de customização do kit** julgado **aprovado** pelo Mestre da aula, com a mídia
confirmada. Cada um SHALL sair com a **descrição** do Guerreiro(a) como **título**, o **nome da
trilha** da recompensa de marco que é o kit, a **data do julgamento** e a autoria — avatar e
nick do Guerreiro(a). As três fontes SHALL sair na mesma lista, ordenadas entre si pela data de
aprovação. (`RF-03-88`, documento 02 §4, documento 99 §6, invariante 5)

#### Scenario: A customização aprovada aparece no acervo

- **WHEN** o registro de customização de um Guerreiro(a) com autorização de divulgação vigente
  é aprovado pelo Mestre da aula
- **THEN** ele aparece no acervo público com a descrição como título, o nome da trilha do kit,
  a data do julgamento e o avatar e o nick dele

#### Scenario: As três fontes saem na mesma lista

- **WHEN** uma consulta pública pede o acervo, e há criação validada, comprovação aprovada e
  customização aprovada
- **THEN** a resposta traz as três na mesma lista, ordenadas entre si pela data de aprovação

### Requirement: A mídia da customização pública é servida sob o mesmo portão da listagem

O núcleo SHALL servir, **sem sessão**, os bytes do registro de customização que satisfaça o
**mesmo portão** do acervo público: **aprovado**, com mídia confirmada, e Guerreiro(a) com
autorização de divulgação vigente. Registro que não o satisfaça SHALL responder **404**, nunca
403. (`RF-03-88`, `RN-03-41`)

#### Scenario: A mídia da customização aprovada é servida sem sessão

- **WHEN** um visitante sem sessão pede a mídia de um registro aprovado, de Guerreiro(a) com
  autorização vigente
- **THEN** o núcleo devolve os bytes dele, com o tipo do arquivo declarado

#### Scenario: Registro pendente responde 404

- **WHEN** um visitante pede a mídia de um registro de customização ainda pendente
- **THEN** o núcleo responde 404, e nada é servido

## MODIFIED Requirements

### Requirement: O portão do acervo público exige aprovação do Mestre e autorização vigente

Um item SHALL aparecer no acervo público **apenas** quando tiver **aprovação do Mestre** —
criação original **validada**, declaração do prático julgada **cumpriu** e **publicável**, ou
registro de customização do kit **aprovado** — **e** autorização de divulgação vigente de todos
os creditados. Declaração não julgada, julgada não cumprida, julgada cumprida e **não**
publicável, **entrega presencial** sem comprovação gravada, e registro de customização
pendente, reprovado, cancelado ou expirado NEVER SHALL aparecer. (`RN-03-41`, `RN-03-02`,
`RN-09-52`, `RF-03-88`)

#### Scenario: A declaração não julgada não aparece

- **WHEN** o Guerreiro(a) declarou que cumpriu o prático e o Mestre autor ainda não julgou
- **THEN** a comprovação não aparece no acervo público

#### Scenario: Cumprida e não publicável não aparece

- **WHEN** o Mestre autor julga que o Guerreiro(a) cumpriu o prático e marca a entrega como
  não publicável
- **THEN** a comprovação não aparece no acervo público

#### Scenario: A entrega presencial não aparece

- **WHEN** a declaração do prático foi por entrega presencial, sem comprovação gravada, e o
  Mestre julgou que cumpriu
- **THEN** nada daquela declaração aparece no acervo público

#### Scenario: Comprovação aprovada de quem não autorizou não aparece

- **WHEN** uma comprovação julgada cumprida e publicável é de Guerreiro(a) sem autorização de
  divulgação vigente
- **THEN** ela não aparece no acervo público

#### Scenario: A revogação retira a comprovação na leitura seguinte

- **WHEN** a autorização de divulgação do Guerreiro(a) é revogada depois de a comprovação dele
  ter aparecido no acervo
- **THEN** a leitura seguinte do acervo não a traz

#### Scenario: A customização reprovada não aparece

- **WHEN** o Mestre da aula reprova o registro de customização de um Guerreiro(a)
- **THEN** o registro não aparece no acervo público

#### Scenario: Customização aprovada de quem não autorizou não aparece

- **WHEN** um registro de customização aprovado é de Guerreiro(a) sem autorização de
  divulgação vigente
- **THEN** ele não aparece no acervo público

### Requirement: O item do acervo público declara identificador, fonte e tipo da produção

Cada item do acervo público SHALL trazer o **identificador** dele, a **fonte** — criação
original, comprovação do prático ou customização do kit — e o **tipo** da produção entre os
seis: texto, imagem, áudio, vídeo, link externo e arquivo. O corpo do texto e o endereço do link
externo SHALL vir no próprio item; imagem, áudio, vídeo e arquivo SHALL ser alcançados pela rota
de bytes da fonte dele. (`RF-03-85`, `RF-03-88`)

#### Scenario: O item traz identificador, fonte e tipo

- **WHEN** uma consulta pública pede o acervo
- **THEN** cada item traz o identificador dele, a fonte de que veio e o tipo da produção

#### Scenario: Texto e link externo vêm no próprio item

- **WHEN** um item do acervo é do tipo texto ou link externo
- **THEN** o corpo do texto, ou o endereço do link, vem no próprio item, sem segunda leitura

#### Scenario: A customização sai com tipo imagem ou vídeo

- **WHEN** um item do acervo vem da customização do kit
- **THEN** a fonte é customização do kit, o tipo é imagem ou vídeo, e os bytes saem pela rota
  pública da mídia da customização

### Requirement: A produção das atividades da missão nunca é item do acervo público

A produção que o Guerreiro(a) envia nas **atividades** da missão SHALL ficar guardada e NEVER
SHALL aparecer no acervo público: ela não tem ato de aprovação do Mestre, e o acervo tem
**três** fontes — a comprovação aprovada do prático, a criação da culminância e o registro
aprovado da customização do kit. (`RN-03-42`, documento 99 §6, invariante 5)

#### Scenario: A produção da atividade fica fora do acervo

- **WHEN** o Guerreiro(a) enviou mídia na produção de uma atividade da missão
- **THEN** ela não aparece no acervo público, nem por rota de bytes pública
