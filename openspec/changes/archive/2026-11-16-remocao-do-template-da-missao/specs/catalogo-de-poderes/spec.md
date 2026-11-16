## ADDED Requirements

### Requirement: A alteração do poder alcança só nome, descrição e vigência

O núcleo SHALL permitir que o Admin altere o **nome**, a **descrição** e a **vigência** de um
poder. A **natureza** NEVER SHALL ser alterada, porque reescreveria o vínculo já concedido às
trilhas, e o **papel** NEVER SHALL ser alterado por esta operação. Persona que não é Admin
SHALL receber **403**; nome vazio SHALL ser recusado com **422**, indicando o campo.
(`RF-02-10`, `RF-01-62`, `RN-01-43`, `RN-01-54`)

#### Scenario: Admin altera nome, descrição e vigência

- **WHEN** um Admin em sessão altera o nome, a descrição e a vigência de um poder
- **THEN** o núcleo grava as três alterações e a natureza e o papel permanecem como estavam

#### Scenario: Renomear o poder do Território não muda o papel

- **WHEN** um Admin altera o nome do poder que exerce o papel do Território
- **THEN** o papel permanece com ele e o crédito da coleta segue chegando ao mesmo poder

#### Scenario: Alteração com nome vazio é recusada

- **WHEN** um Admin tenta alterar um poder informando nome vazio
- **THEN** o núcleo responde 422 indicando o campo e nada é gravado

#### Scenario: A marca de técnico não é mais aceita

- **WHEN** um Admin cadastra ou altera um poder enviando o campo `tecnico`
- **THEN** o núcleo responde 422 indicando o campo desconhecido, como para qualquer campo fora
  do contrato, nada é gravado, e a leitura do poder não traz a marca

## REMOVED Requirements

### Requirement: A alteração do poder não alcança a natureza nem o papel

**Reason**: Incluía a marca de técnico entre os campos alteráveis; a marca sai pela decisão do
fundador de 2026-11-16.
**Migration**: Substituído por "A alteração do poder alcança só nome, descrição e vigência".

### Requirement: O catálogo declara se o poder é técnico

**Reason**: Decisão do fundador de 2026-11-16 — a marca servia só de insumo da sugestão do
template da missão, que sai da App 09. `RF-01-62` e `RN-01-54` perdem a menção à marca no
PRD-01.
**Migration**: A coluna `poder.tecnico` é apagada; o campo `tecnico` deixa de ser aceito e
devolvido por `/v1/poderes`, e a App 03 deixa de oferecê-lo.

### Requirement: A gestão lê a marca de técnico junto do catálogo

**Reason**: Mesma decisão — sem a marca, não há o que ler.
**Migration**: A leitura do catálogo pela gestão segue com nome, descrição, natureza, vigência,
papel e situação de ativo.
