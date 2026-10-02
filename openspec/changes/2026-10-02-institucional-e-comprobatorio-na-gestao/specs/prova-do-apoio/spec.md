# Spec Delta

## ADDED Requirements

### Requirement: O Admin alcança o documento pendente pela listagem de Apoiadores

A listagem de Apoiadores que o Admin lê SHALL trazer, para cada documento comprobatório, o
**identificador** do documento e a marca de **publicado ou pendente**, ao lado do endereço e do
rótulo que já traz. (`RF-02-101`, decisão do fundador, 2026-10-02)

Sem o identificador a gestão NEVER SHALL conseguir chamar a anexação, que o exige na rota; sem a
marca NEVER SHALL conseguir separar o que espera do que já está público. Nenhuma rota nasce para
isto: a fila do que espera anexação SHALL ser derivada desta listagem.

A marca SHALL ser **derivada** do mesmo critério que a leitura do próprio Apoiador já usa, e
NEVER SHALL ser um campo que alguém grave à mão. (`RF-14-20`)

#### Scenario: A listagem distingue o pendente do publicado

- **WHEN** um Admin lê os Apoiadores e um deles tem um documento anexado e outro ainda não
- **THEN** a resposta traz os dois documentos, com identificador, um marcado como publicado e o
  outro como pendente

#### Scenario: O identificador serve à anexação

- **WHEN** um Admin toma o identificador de um documento pendente vindo da listagem e anexa o
  documento
- **THEN** a anexação é aceita e o documento passa a publicado

#### Scenario: A leitura do Apoiador não ganha o que não é dele

- **WHEN** um Apoiador lê os próprios documentos
- **THEN** a resposta segue trazendo apenas os da persona em sessão, como já fazia
