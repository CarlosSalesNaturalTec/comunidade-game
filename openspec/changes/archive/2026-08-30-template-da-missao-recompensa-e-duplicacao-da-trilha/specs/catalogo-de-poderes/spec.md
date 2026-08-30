## ADDED Requirements

### Requirement: O catálogo declara se o poder é técnico

O núcleo SHALL registrar, em cada poder do catálogo, se ele é **técnico**, declarado por
**Admin** ao lado da natureza, da vigência e do papel. A marca SHALL ser **opcional**: poder sem
ela é aceito, e o padrão de quem não declara é **não técnico**.

O núcleo NEVER SHALL deduzir do **nome** nem da **descrição** do poder que ele é técnico — o
nome é rótulo de exibição, alterável por Admin, e não identifica regra, exatamente como já vale
para o papel do poder. A marca SHALL alcançar **quantos poderes o Admin quiser**: ela não é
papel, e nenhum limite de um só se aplica a ela.

A marca SHALL servir apenas de **insumo da sugestão** do template da missão, que propõe
atividade desplugada nas trilhas de poder técnico. Ela NEVER SHALL alterar pontuação, nível,
badge, crédito de coleta, trava de publicação nem qualquer outra regra do poder. (`RF-01-62`,
`RN-01-54`, `RF-09-88`, `RN-09-34`, 02 §2, decisão do fundador de 2026-08-29)

#### Scenario: Admin marca o poder como técnico

- **WHEN** um Admin em sessão cadastra um poder declarando que ele é técnico
- **THEN** o núcleo grava o poder com a marca, e o template passa a propor atividade desplugada
  nas trilhas dele

#### Scenario: Poder sem a marca é não técnico

- **WHEN** um Admin cadastra um poder sem declarar a marca
- **THEN** o núcleo grava o poder como não técnico, sem recusa alguma

#### Scenario: Mais de um poder pode ser técnico

- **WHEN** um Admin marca como técnico um segundo poder do catálogo
- **THEN** o núcleo grava a marca nos dois, e nenhuma recusa acontece

#### Scenario: O nome não torna o poder técnico

- **WHEN** existe no catálogo um poder de nome técnico sem a marca declarada
- **THEN** o núcleo o trata como não técnico

#### Scenario: A marca não muda regra alguma do poder

- **WHEN** um poder marcado como técnico credita pontos, níveis e badges
- **THEN** tudo acontece exatamente como acontecia antes da marca

### Requirement: A gestão lê a marca de técnico junto do catálogo

A leitura do catálogo pela gestão SHALL trazer, em cada poder, se ele é **técnico**, ao lado da
natureza, da vigência, do papel e da situação de ativo — sem o que o Admin não sabe quais
trilhas recebem a sugestão de atividade desplugada. (`RF-02-10`, `RF-01-62`, `RN-09-34`)

#### Scenario: O catálogo lido pela gestão traz a marca

- **WHEN** um Admin lê o catálogo de poderes
- **THEN** cada poder traz se é técnico, junto da natureza, da vigência e do papel

## MODIFIED Requirements

### Requirement: A alteração do poder não alcança a natureza nem o papel

O núcleo SHALL permitir que o Admin altere o **nome**, a **descrição**, a **vigência** e a
**marca de técnico** de um poder do catálogo. A **natureza** NEVER SHALL ser alterada, porque
mudá-la reescreveria o vínculo já concedido às trilhas existentes, e o **papel** NEVER SHALL ser
alterado por esta operação. A marca de técnico é alterável porque dela não deriva vínculo,
crédito nem pontuação: ela só muda a sugestão que o template faz daí em diante, e nenhuma
sugestão já registrada SHALL ser reescrita por ela. Alterar poder SHALL exigir persona **Admin**;
persona de qualquer outro papel SHALL receber **403**. Alteração com nome vazio SHALL ser
recusada com **422**, indicando o campo. (`RF-02-10`, `RF-01-62`, `RN-01-43`, `RN-01-54`,
`RN-09-34`)

#### Scenario: Admin altera nome, descrição e vigência

- **WHEN** um Admin em sessão altera o nome, a descrição e a vigência de um poder
- **THEN** o núcleo grava as três alterações e a natureza e o papel permanecem como estavam

#### Scenario: Admin altera a marca de técnico

- **WHEN** um Admin em sessão altera a marca de técnico de um poder do catálogo
- **THEN** o núcleo grava a alteração e a natureza e o papel permanecem como estavam

#### Scenario: Tirar a marca não reescreve sugestão já registrada

- **WHEN** um Admin retira a marca de técnico de um poder cujas trilhas já receberam sugestão de
  estrutura
- **THEN** as sugestões já registradas permanecem como estavam, e só as seguintes deixam de
  propor atividade desplugada

#### Scenario: Renomear o poder do Território não muda o papel

- **WHEN** um Admin altera o nome do poder que exerce o papel do Território
- **THEN** o papel permanece com ele e o crédito da coleta segue chegando ao mesmo poder

#### Scenario: Alteração com nome vazio é recusada

- **WHEN** um Admin tenta alterar um poder informando nome vazio
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado