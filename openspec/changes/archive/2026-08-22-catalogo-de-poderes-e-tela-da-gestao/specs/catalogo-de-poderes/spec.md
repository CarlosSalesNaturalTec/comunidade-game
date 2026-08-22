## ADDED Requirements

### Requirement: A gestão lê o catálogo de poderes, inclusive o desativado

O núcleo SHALL expor o catálogo de poderes à gestão em listagem paginada, pelo contrato único
de listagem, exigindo persona em sessão. A listagem SHALL trazer, de cada poder, o nome, a
descrição, a **natureza**, a **vigência**, o **papel** declarado quando houver e se ele está
**ativo**, para que a distinção entre o poder vigente e o de ciclo futuro seja legível por quem
consulta. A listagem da gestão SHALL incluir o poder desativado, ao contrário da leitura
pública da vitrine, que NEVER SHALL trazê-lo. O poder é bem comum da plataforma e NEVER SHALL
ser filtrado por comunidade. (`RF-02-10`, `RF-01-62`, `RF-01-28`, 02 §2)

#### Scenario: A gestão lê o catálogo com natureza, vigência e papel

- **WHEN** uma persona em sessão consulta o catálogo de poderes
- **THEN** o núcleo devolve a página de poderes com nome, descrição, natureza, vigência, papel
  quando houver e a situação de ativo

#### Scenario: O poder desativado aparece para a gestão

- **WHEN** um poder do catálogo está desativado e a gestão consulta o catálogo
- **THEN** o núcleo o devolve na listagem, marcado como inativo

#### Scenario: O poder desativado não aparece na vitrine

- **WHEN** um poder do catálogo está desativado e a leitura pública da vitrine é consultada
- **THEN** o núcleo não o devolve, e a leitura pública permanece como estava

#### Scenario: Consulta sem persona em sessão é recusada

- **WHEN** o catálogo da gestão é consultado sem credencial de persona
- **THEN** o núcleo recusa a consulta e nenhum poder é devolvido

### Requirement: A desativação retira o poder da escolha sem desfazer vínculo

O núcleo SHALL permitir que o Admin desative um poder do catálogo, e a desativação SHALL apenas
retirá-lo da escolha de novas trilhas e da leitura pública. A desativação NEVER SHALL desfazer o
vínculo das trilhas já criadas naquele poder, NEVER SHALL apagar o poder e NEVER SHALL alterar
o percurso, os pontos ou os badges já acumulados nele. Desativar poder SHALL exigir persona
**Admin**; persona de qualquer outro papel SHALL receber **403**. (`RF-02-10`, `RF-01-62`,
`RN-01-43`)

#### Scenario: Admin desativa um poder do catálogo

- **WHEN** um Admin em sessão desativa um poder do catálogo
- **THEN** o núcleo grava o poder como inativo e a leitura pública deixa de trazê-lo

#### Scenario: A trilha vinculada ao poder desativado permanece

- **WHEN** um poder com trilha já vinculada é desativado
- **THEN** a trilha permanece vinculada a ele e o percurso já realizado pelos Guerreiros e
  Guerreiras permanece como estava

#### Scenario: Mestre não desativa poder

- **WHEN** um Mestre em sessão tenta desativar um poder do catálogo
- **THEN** o núcleo responde 403 e o catálogo permanece como estava

### Requirement: A alteração do poder não alcança a natureza nem o papel

O núcleo SHALL permitir que o Admin altere o **nome**, a **descrição** e a **vigência** de um
poder do catálogo. A **natureza** NEVER SHALL ser alterada, porque mudá-la reescreveria o
vínculo já concedido às trilhas existentes, e o **papel** NEVER SHALL ser alterado por esta
operação. Alterar poder SHALL exigir persona **Admin**; persona de qualquer outro papel SHALL
receber **403**. Alteração com nome vazio SHALL ser recusada com **422**, indicando o campo.
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
