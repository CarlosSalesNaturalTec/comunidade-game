# Spec Delta

## ADDED Requirements

### Requirement: Admin e Mestre leem os responsáveis cadastrados, com os vinculados de cada um

O núcleo SHALL responder, a um **Admin** ou a um **Mestre** em sessão, os responsáveis
cadastrados, cada um com o **nome** e com os Guerreiros e Guerreiras **vinculados a ele por
vínculo vigente**, identificados por **nick** e acompanhados do **grau de parentesco** daquele
vínculo. A leitura SHALL ser paginada, na mesma convenção das demais listagens do núcleo.

O alcance SHALL depender do papel em sessão:

- ao **Admin**, todos os responsáveis cadastrados;
- ao **Mestre**, os responsáveis com vínculo vigente a Guerreiro(a) das **comunidades em que
  ele atua**, **e** os responsáveis que **ele próprio cadastrou**, ainda que estes não tenham
  vínculo algum. Responsável fora desses dois conjuntos NEVER SHALL aparecer na lista dele.

Responsável **sem vínculo vigente** SHALL aparecer na lista de quem o alcança, com a lista de
vinculados vazia: é o cadastro interrompido, e é para retomá-lo que a leitura existe. Vínculo
**encerrado** NEVER SHALL aparecer entre os vinculados.

A resposta SHALL trazer apenas o que identifica o responsável e os vinculados dele — nome,
nick e grau de parentesco — e NEVER SHALL trazer credencial, senha, usuário de acesso nem
contato do responsável, nem imagem real, nome civil, nascimento ou contato do Guerreiro(a). A
leitura SHALL usar a **mesma operação de vínculo** que a matriz de permissões já concede aos
dois papéis, sem `Operacao` nova, e persona de qualquer outro papel SHALL receber **403**.
(`RF-02-111`, `RF-09-122`, `RF-01-13`, `RN-01-20`, `RN-09-18`, invariante 12 do documento 99
§6, decisão do fundador, 2026-09-26)

#### Scenario: O Admin vê todos os responsáveis cadastrados

- **WHEN** um Admin em sessão pede os responsáveis
- **THEN** o núcleo devolve todos os cadastrados, cada um com o nome e com os vinculados
  vigentes por nick e grau de parentesco

#### Scenario: O Mestre vê os responsáveis das comunidades em que atua

- **WHEN** um Mestre em sessão pede os responsáveis
- **THEN** o núcleo devolve os que têm vínculo vigente com Guerreiro(a) de comunidade em que
  ele atua

#### Scenario: Responsável de outra comunidade não aparece ao Mestre

- **WHEN** existe responsável vinculado apenas a Guerreiro(a) de comunidade em que o Mestre em
  sessão não atua, e que não foi cadastrado por ele
- **THEN** ele não aparece na lista daquele Mestre

#### Scenario: O Mestre reencontra o responsável que ele mesmo cadastrou sem vincular

- **WHEN** um Mestre cadastrou um responsável e saiu antes de criar qualquer vínculo, e depois
  pede os responsáveis
- **THEN** aquele responsável aparece na lista dele, com a lista de vinculados vazia

#### Scenario: Responsável sem vínculo aparece ao Admin

- **WHEN** um Admin pede os responsáveis e existe um cadastrado sem vínculo algum
- **THEN** ele aparece na lista, com a lista de vinculados vazia

#### Scenario: Vínculo encerrado não entra entre os vinculados

- **WHEN** um responsável tem um vínculo já encerrado e outro vigente
- **THEN** a lista dele traz apenas o Guerreiro(a) do vínculo vigente

#### Scenario: A resposta não traz credencial nem contato

- **WHEN** um Admin ou um Mestre lê a lista
- **THEN** cada responsável traz nome e vinculados, e nenhum traz credencial, senha, usuário
  ou contato

#### Scenario: A lista não expõe dado pessoal da criança

- **WHEN** a lista traz os vinculados de um responsável
- **THEN** cada vinculado traz nick e grau de parentesco, e nenhum traz imagem real, nome
  civil, nascimento ou contato

#### Scenario: Outro papel não alcança a lista

- **WHEN** um responsável, um Apoiador ou um Guerreiro(a) chama a rota
- **THEN** o núcleo responde 403 e nada é devolvido
