## Purpose

Governa como o Mestre publica a prova da própria habilidade: os artefatos comprobatórios que ele
mesmo declara — currículo, portfólio, redes sociais e documentos externos, sempre como link —,
o alcance restrito à própria persona e a permanência do que o Admin declarou no cadastro, que é
o que sustenta a governança de personas do invariante 3. Governa também a edição de rótulo e
endereço de qualquer artefato do próprio perfil, o do cadastro incluído, que segue irremovível
e passa a ter o valor original guardado.

## Requirements

### Requirement: O Mestre lê e publica os próprios artefatos comprobatórios

O núcleo SHALL expor rota em que a persona de **Mestre em sessão** lê e acrescenta os artefatos
comprobatórios da **própria** persona, cada um com **endereço** e **rótulo** do que aponta —
currículo, portfólio, rede social ou documento externo. A rota SHALL exigir credencial de
persona e SHALL alcançar **apenas a própria persona**: Mestre que apontar outra persona SHALL
receber **403**, e persona de outro papel SHALL receber **403**. O núcleo NEVER SHALL aceitar
anexo de arquivo como artefato: a prova é link declarado. Artefato sem endereço ou sem rótulo
SHALL ser recusado com **422**. (`RF-09-66`, `RN-02-01`, documento 02 §1, PRD-09 §9)

#### Scenario: Mestre publica o currículo e o portfólio

- **WHEN** um Mestre em sessão acrescenta dois artefatos ao próprio perfil, cada um com endereço
  e rótulo
- **THEN** o núcleo grava os dois na persona dele, e a leitura do perfil passa a trazê-los

#### Scenario: Artefato sem endereço é recusado

- **WHEN** um Mestre acrescenta artefato sem endereço, ou sem rótulo
- **THEN** o núcleo responde 422 indicando o campo em falta, e nenhum artefato é gravado

#### Scenario: Mestre não publica no perfil de outra persona

- **WHEN** um Mestre em sessão tenta acrescentar artefato ao perfil de outra persona
- **THEN** o núcleo responde 403 e nada é gravado

#### Scenario: Persona de outro papel não usa a rota

- **WHEN** uma persona que não é Mestre chama a rota de artefatos do próprio perfil
- **THEN** o núcleo responde 403 e nada é gravado

### Requirement: O artefato declarado por Admin permanece

O núcleo SHALL permitir que o Mestre remova **apenas** os artefatos que ele mesmo publicou. O
artefato declarado por **Admin** no cadastro da persona SHALL aparecer na leitura do perfil,
SHALL indicar que foi declarado no cadastro e NEVER SHALL ser removido pelo Mestre — é a prova
de habilidade que sustentou o cadastro dele. Tentativa de removê-lo SHALL ser recusada com
**403**, e o artefato SHALL permanecer. (`RF-09-66`, `RN-09-14`, invariante 3 do documento 99 §6,
documento 02 §1, decisão do fundador, 2026-08-29, documento 09 §1)

#### Scenario: O Mestre remove um artefato que ele publicou

- **WHEN** um Mestre remove um artefato que ele mesmo acrescentou
- **THEN** o núcleo o remove, e os demais artefatos do perfil permanecem

#### Scenario: O artefato do cadastro não é removível pelo Mestre

- **WHEN** um Mestre tenta remover um artefato declarado por Admin no cadastro dele
- **THEN** o núcleo responde 403 e o artefato continua no perfil

#### Scenario: A leitura distingue quem declarou cada artefato

- **WHEN** um Mestre lê o próprio perfil, que tem artefatos do cadastro e artefatos publicados
  por ele
- **THEN** cada artefato indica se foi declarado no cadastro ou publicado pelo próprio Mestre

### Requirement: A rota de artefatos nunca cria persona nem muda papel

A rota de artefatos do próprio perfil SHALL alcançar **apenas** os artefatos comprobatórios.
NEVER SHALL criar persona, NEVER SHALL alterar nome, e-mail, WhatsApp ou papel da persona, e
NEVER SHALL servir de caminho para o cadastro de um Mestre: o cadastro de Mestre continua sendo
ato exclusivo de Admin. (`RF-09-67`, `RN-09-14`, `RN-01-01`, invariante 3 do documento 99 §6)

#### Scenario: Campo de cadastro enviado junto é recusado

- **WHEN** a chamada de artefatos traz também nome, e-mail ou papel da persona
- **THEN** o núcleo recusa a chamada e nenhum dado de cadastro é alterado

#### Scenario: Nenhuma persona nasce pela rota de artefatos

- **WHEN** a rota de artefatos é chamada com o identificador de uma persona que não existe
- **THEN** o núcleo recusa a chamada e nenhuma persona passa a existir

### Requirement: O Mestre edita rótulo e endereço dos artefatos do próprio perfil

O núcleo SHALL permitir ao **Mestre em sessão** alterar o **rótulo** e o **endereço** de
qualquer artefato comprobatório do **próprio** perfil, **inclusive o declarado pelo Admin no
cadastro**. O artefato declarado no cadastro NEVER SHALL ser removível por ele. Tentativa
de editar artefato de outra persona SHALL receber 403, e artefato inexistente no perfil, 404.
(`RF-09-66`, `RN-09-14`, documento 02 §1, decisão do fundador de 2026-09-06)

#### Scenario: O Mestre corrige o que ele mesmo publicou

- **WHEN** o Mestre altera o rótulo e o endereço de um artefato que publicou
- **THEN** o artefato passa a valer com os novos valores

#### Scenario: O Mestre corrige o link errado do cadastro

- **WHEN** o Mestre altera o endereço de um artefato declarado pelo Admin no cadastro
- **THEN** a alteração é aceita, e o artefato continua constando do perfil

#### Scenario: A remoção do artefato do cadastro segue vedada

- **WHEN** o Mestre tenta remover um artefato declarado pelo Admin no cadastro
- **THEN** a remoção é recusada e o artefato permanece

#### Scenario: Perfil alheio não se edita

- **WHEN** o Mestre tenta editar artefato do perfil de outra persona
- **THEN** recebe 403 e nada é alterado

### Requirement: O artefato do cadastro editado guarda o valor original

O núcleo SHALL guardar o **rótulo e o endereço originais** de um artefato **declarado no
cadastro** na **primeira** vez que o adulto o editar, junto do momento da edição, e SHALL
servi-los à gestão ao lado dos valores vigentes. Edição posterior SHALL alterar apenas o valor
vigente, preservando o original já guardado. Artefato nunca editado NEVER SHALL apresentar valor
original. (`RN-09-14`, documento 02 §1, decisão do fundador de 2026-09-06)

#### Scenario: A primeira edição fixa o original

- **WHEN** o Mestre edita pela primeira vez um artefato declarado no cadastro
- **THEN** o rótulo e o endereço que o Admin declarou ficam guardados, com o momento da edição

#### Scenario: A segunda edição não apaga o original

- **WHEN** o Mestre edita de novo o mesmo artefato
- **THEN** o valor vigente muda e o original guardado permanece o que o Admin declarou

#### Scenario: Artefato intocado não tem original

- **WHEN** a gestão lê um artefato que ninguém editou
- **THEN** nenhum valor original é apresentado para ele
