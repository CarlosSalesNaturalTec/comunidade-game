## ADDED Requirements

### Requirement: O Meu perfil apresenta e troca o nick e o avatar do próprio Mestre

A App 09 SHALL apresentar ao Mestre, na área do próprio perfil, o **nick** e o **avatar**
vigentes dele, e SHALL oferecer definir ou trocar cada um. A tela NEVER SHALL sugerir nick
algum, e NEVER SHALL condicionar o avatar a moeda acumulada — o piso é regra de marca do
Apoiador. Nick recusado por já estar em uso SHALL ser informado sem identificar de quem ele é.
(`RF-09-114`, `RN-01-30`, `RN-14-10`)

#### Scenario: O Mestre vê o que já tem antes de trocar

- **WHEN** o Mestre abre a área do próprio perfil
- **THEN** vê o nick e o avatar vigentes, ou a indicação de que ainda não os definiu

#### Scenario: O Mestre define o nick no primeiro acesso

- **WHEN** o Mestre ainda sem nick o escolhe e grava
- **THEN** o nick passa a ser o dele, e a tela não sugeriu nenhum

#### Scenario: Nick em uso é recusado sem denunciar ninguém

- **WHEN** o nick escolhido já pertence a outra persona
- **THEN** a tela diz que aquele nick está em uso e pede outro, sem dizer de quem é

### Requirement: O Meu perfil edita os artefatos do próprio Mestre

A App 09 SHALL oferecer ao Mestre alterar o **rótulo** e o **endereço** de cada artefato do
próprio perfil, o **declarado no cadastro** incluído — que continua **sem caminho de remoção** e
SHALL seguir marcado como declarado no cadastro. A tela SHALL continuar declarando que o
cadastro de Mestre é ato exclusivo de Admin e NEVER SHALL oferecer alteração de nome, e-mail ou
papel. (`RF-09-66`, `RF-09-67`, `RN-09-14`)

#### Scenario: O Mestre corrige um endereço errado

- **WHEN** o Mestre altera o endereço de um artefato do próprio perfil
- **THEN** o artefato passa a apontar para o novo endereço

#### Scenario: O do cadastro edita, mas não remove

- **WHEN** o Mestre abre um artefato declarado no cadastro
- **THEN** lhe é oferecido editá-lo e não lhe é oferecido removê-lo, e ele segue marcado como
  declarado no cadastro

#### Scenario: O perfil segue sem editar o cadastro

- **WHEN** o Mestre percorre a área do próprio perfil
- **THEN** não lhe é oferecido campo algum para alterar nome, e-mail ou papel
