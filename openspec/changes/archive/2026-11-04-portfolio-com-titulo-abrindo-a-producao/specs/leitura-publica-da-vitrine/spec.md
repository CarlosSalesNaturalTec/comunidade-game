# Spec Delta

## MODIFIED Requirements

### Requirement: Poderes, trilhas e criações originais respondem em leitura pública

O núcleo SHALL expor em rota pública o **catálogo de poderes** com as trilhas vinculadas a cada
um, e o **portfólio de criações originais** validadas. A criação original SHALL trazer a
autoria creditada, projetada como avatar e nick de **cada creditado** — os integrantes da
equipe da trilha, na modalidade em equipe, e o Guerreiro(a) que a entregou, na individual —, e
SHALL aparecer **apenas** quando todos os creditados nela tiverem autorização de divulgação
vigente. A trilha NEVER SHALL ser filtrada por comunidade nesta capacidade: ela é bem comum da
plataforma. (`RF-01-62`, `RF-01-26`, `RF-09-33`, `RN-01-13`, `RN-01-42`, `RN-09-19`, PRD-03 §9)

A criação original pública SHALL trazer também a **data de validação** e o **nome da trilha**
de que ela nasceu, mais o **título** do item de acervo, que na criação original **é o nome da
trilha**: o modelo não tem campo de título, e a trilha é o que nomeia a produção da culminância
(`RF-03-08`, `RN-03-43`, decisão do fundador, 2026-11-04). Isto **substitui** a proibição
anterior de trazer título, decidida em 2026-09-28, quando título nenhum existia.

O **acervo público** SHALL responder em ordem **decrescente** pela data em que o Mestre aprovou
o item — a validação, na criação original —, do mais recente para o mais antigo, e a paginação
por cursor SHALL percorrer essa ordem **nas duas fontes do acervo**, sem pular nem
repetir item. (`RF-03-83`, `RF-03-84`, decisão do fundador, 2026-10-11)

Cada poder do catálogo público SHALL trazer os **Mestres responsáveis** dele — os autores das
trilhas publicadas daquele poder —, cada um com o **identificador** que alcança a leitura
individual do Mestre, mais avatar e nick, ou o nome quando a persona não tiver nick. Poder sem
trilha publicada SHALL sair com a lista de Mestres **vazia**, nunca omitida. (`RF-03-02`,
documento 11 §8.2, decisão do fundador, 2026-09-29)

#### Scenario: Catálogo público traz poderes e trilhas

- **WHEN** uma consulta pública pede os poderes
- **THEN** a resposta traz cada poder com as trilhas vinculadas a ele

#### Scenario: O poder traz os Mestres responsáveis

- **WHEN** um poder tem duas trilhas publicadas, de Mestres autores diferentes
- **THEN** a resposta traz os dois Mestres, sem repetição, cada um com o identificador que
  alcança a leitura individual dele

#### Scenario: Poder sem trilha publicada sai com a lista vazia

- **WHEN** um poder ativo não tem trilha publicada alguma
- **THEN** a resposta traz aquele poder com a lista de Mestres responsáveis vazia

#### Scenario: Criação original pública credita a autoria

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick de cada integrante creditado

#### Scenario: Criação individual pública credita quem a entregou

- **WHEN** uma criação original individual validada aparece no portfólio público
- **THEN** ela traz o avatar e o nick do Guerreiro(a) que a entregou

#### Scenario: Criação com integrante sem autorização não aparece

- **WHEN** uma criação original tem entre os creditados um Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

#### Scenario: Criação individual sem autorização não aparece

- **WHEN** uma criação original individual validada é de Guerreiro(a) sem autorização vigente
- **THEN** a criação não aparece no portfólio público

#### Scenario: A criação pública traz data e trilha

- **WHEN** uma criação original validada aparece no portfólio público
- **THEN** ela traz a data em que foi validada e o nome da trilha de que nasceu

#### Scenario: O título da criação original é o nome da trilha

- **WHEN** uma criação original validada aparece no acervo público
- **THEN** o título dela é o nome da trilha de que nasceu

#### Scenario: O portfólio responde da mais recente para a mais antiga

- **WHEN** uma consulta pública pede o portfólio de criações originais
- **THEN** a primeira criação da resposta é a validada mais recentemente

#### Scenario: A paginação do portfólio não pula nem repete

- **WHEN** uma consulta pública percorre o acervo inteiro por cursor, em páginas de dez, com
  criações originais e comprovações aprovadas intercaladas no tempo
- **THEN** cada item apareceu uma vez, em ordem decrescente de data de aprovação

## ADDED Requirements

### Requirement: A comprovação aprovada do desafio prático é a segunda fonte do acervo público

O acervo público SHALL trazer, ao lado da criação original, a **comprovação do desafio
prático** julgada **cumprida e publicável** pelo Mestre autor, com comprovação gravada. Cada
uma SHALL sair com o **título curto** declarado pelo Mestre no desafio, o **nome da trilha** da
missão, a **data do julgamento** e a autoria — avatar e nick do Guerreiro(a) que a entregou.
(`RF-03-84`, `RN-03-43`, documento 99 §6, invariante 5)

#### Scenario: A comprovação aprovada aparece no acervo

- **WHEN** uma declaração de desafio prático com comprovação gravada é julgada cumprida e
  publicável, e o Guerreiro(a) tem autorização de divulgação vigente
- **THEN** ela aparece no acervo público com o título curto do desafio, o nome da trilha,
  a data do julgamento e o avatar e o nick dele

#### Scenario: As duas fontes saem na mesma lista

- **WHEN** uma consulta pública pede o acervo, e há criação original validada e comprovação
  aprovada
- **THEN** a resposta traz as duas na mesma lista, ordenadas entre si pela data de aprovação

### Requirement: O portão do acervo público exige aprovação do Mestre e autorização vigente

Um item SHALL aparecer no acervo público **apenas** quando tiver **aprovação do Mestre** —
criação original **validada**, ou declaração do prático julgada **cumpriu** e **publicável** —
**e** autorização de divulgação vigente de todos os creditados. Declaração não julgada, julgada
não cumprida, julgada cumprida e **não** publicável, e **entrega presencial** sem comprovação
gravada NEVER SHALL aparecer. (`RN-03-41`, `RN-03-02`, `RN-09-52`)

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

### Requirement: O item do acervo público declara identificador, fonte e tipo da produção

Cada item do acervo público SHALL trazer o **identificador** dele, a **fonte** — criação
original ou comprovação do prático — e o **tipo** da produção entre os seis: texto, imagem,
áudio, vídeo, link externo e arquivo. O corpo do texto e o endereço do link externo SHALL vir
no próprio item; imagem, áudio, vídeo e arquivo SHALL ser alcançados pela rota de bytes da
fonte dele. (`RF-03-85`)

#### Scenario: O item traz identificador, fonte e tipo

- **WHEN** uma consulta pública pede o acervo
- **THEN** cada item traz o identificador dele, a fonte de que veio e o tipo da produção

#### Scenario: Texto e link externo vêm no próprio item

- **WHEN** um item do acervo é do tipo texto ou link externo
- **THEN** o corpo do texto, ou o endereço do link, vem no próprio item, sem segunda leitura

### Requirement: A mídia da comprovação pública é servida sob o mesmo portão da listagem

O núcleo SHALL servir, **sem sessão**, os bytes da comprovação de um desafio prático que
satisfaça o **mesmo portão** do acervo público: julgada **cumpriu** e **publicável**, com
comprovação gravada, e Guerreiro(a) com autorização de divulgação vigente. Comprovação que
não o satisfaça SHALL responder **404**, nunca 403, para a rota não virar oráculo sobre
quais crianças têm divulgação autorizada. (`RF-03-85`, `RN-03-41`)

#### Scenario: A mídia da comprovação pública é servida sem sessão

- **WHEN** um visitante sem sessão pede a mídia de uma comprovação julgada cumprida e
  publicável, de Guerreiro(a) com autorização vigente
- **THEN** o núcleo devolve os bytes dela, com o tipo do arquivo declarado

#### Scenario: Comprovação não publicável responde 404

- **WHEN** um visitante pede a mídia de uma comprovação julgada cumprida e não publicável
- **THEN** o núcleo responde 404, e nada da comprovação é servido

#### Scenario: Comprovação de quem não autorizou responde 404

- **WHEN** um visitante pede a mídia de uma comprovação aprovada de Guerreiro(a) sem
  autorização de divulgação vigente
- **THEN** o núcleo responde 404, e nada da comprovação é servido

### Requirement: A produção das atividades da missão nunca é item do acervo público

A produção que o Guerreiro(a) envia nas **atividades** da missão SHALL ficar guardada e NEVER
SHALL aparecer no acervo público: ela não tem ato de aprovação do Mestre, e o acervo tem
**duas** fontes, a comprovação aprovada do prático e a criação da culminância. (`RN-03-42`,
documento 99 §6, invariante 5)

#### Scenario: A produção da atividade fica fora do acervo

- **WHEN** o Guerreiro(a) enviou mídia na produção de uma atividade da missão
- **THEN** ela não aparece no acervo público, nem por rota de bytes pública
