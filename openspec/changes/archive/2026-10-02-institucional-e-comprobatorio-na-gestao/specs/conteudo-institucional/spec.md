# Spec Delta

## ADDED Requirements

### Requirement: O Admin lê o conteúdo institucional com autor e data

O núcleo SHALL responder `GET /v1/conteudo-institucional` **somente a Admin**, devolvendo as
**três seções em ordem fixa** — publicadas ou não — cada uma com o texto, o link do vídeo quando
houver, **quem publicou** e **quando**. Persona que não seja Admin SHALL receber **403**. A rota
SHALL ser só de leitura. (`RF-02-80`, decisão do fundador, 2026-10-02)

Esta rota existe porque a leitura pública NEVER SHALL revelar o autor, e a tela de edição do
Admin precisa dele: autor e data chegavam apenas na resposta do `PUT`, e recarregar a tela os
perdia. A rota pública SHALL permanecer exatamente como está. (`RF-03-45`)

Seção que nunca foi publicada SHALL vir sem texto, sem autor e sem data, e o núcleo NEVER SHALL
inventá-los.

#### Scenario: O Admin lê as três seções com a autoria

- **WHEN** um Admin lê o conteúdo institucional
- **THEN** a resposta traz as três seções em ordem fixa, cada uma com texto, autor e data do que
  foi publicado

#### Scenario: Seção nunca publicada vem vazia

- **WHEN** um Admin lê o conteúdo institucional e uma das seções nunca foi publicada
- **THEN** essa seção vem sem texto, sem autor e sem data, e as outras vêm completas

#### Scenario: Quem não é Admin não lê a autoria

- **WHEN** um Mestre, um Apoiador ou um responsável pede a leitura de Admin
- **THEN** o núcleo responde 403

#### Scenario: A leitura pública continua sem autor

- **WHEN** um visitante lê a rota pública do conteúdo institucional
- **THEN** a resposta traz as três seções sem quem publicou e sem quando
