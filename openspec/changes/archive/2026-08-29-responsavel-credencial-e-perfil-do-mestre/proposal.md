## Why

Origem: **PRD-09 — Área do Mestre**, fatias **10** e **11** do
`openspec/cronograma-de-fatias.md`. Recorte: `RF-09-62` a `RF-09-68`, `RN-09-14`, `RN-09-15`.

As duas fatias fecham a §6.9 do PRD-09 e vão juntas porque abrem a mesma superfície: a área do
Mestre sobre **pessoas** — a família da criança e a prova de habilidade dele. Uma sem a outra
deixaria a App 09 com metade de uma seção do PRD e dois PRs no mesmo arquivo.

O núcleo já sabe cadastrar responsável, vincular com grau de parentesco, recusar o quarto
vínculo e criar credencial de usuário e senha provisória — as rotas existem desde o PRD-01 e
estão consolidadas em `responsavel-e-vinculo` e `persona-e-credencial`. **Nenhuma delas tem
porta na App 09.** Hoje o responsável só entra pela App 03 (Admin) ou pelo onboarding da App 01,
que já sabe de qual criança se trata; o Mestre que recebe a família no encontro, fora do
cadastro de um Guerreiro(a) novo, não tem por onde registrar — e sem esse cadastro a fatia 1 do
PRD-13 nasce sem responsável com acesso.

A fatia 11 fecha o que a App 09 deve à LGPD e à governança de personas: o Mestre publica a
prova da própria habilidade (`RF-09-66`), a aplicação declara que **não cadastra Mestre**
(`RF-09-67`, `RN-09-14`, invariante 3 do documento 99 §6) e **toda tela que coleta dado avisa o
que coleta** (`RF-09-68`) — hoje a App 09 grava presença, resultado, ocorrência de conduta e
criação original sem um único aviso e sem área de direitos, enquanto a App 03 e a App 05 já as
têm.

## What Changes

- A App 09 ganha a área **Responsáveis**: o Mestre cadastra o responsável que se apresentou
  pessoalmente e o vincula a Guerreiros e Guerreiras **já ativos**, com o **grau de parentesco
  em texto livre** por vínculo (`RF-09-62`, `RF-09-63`, `RN-09-15`). A tela declara que o
  cadastro pressupõe a apresentação presencial.
- O **quarto vínculo é recusado** em linguagem simples, sem jargão nem código, e os três
  vigentes continuam válidos (`RF-09-64`). O teto é conferido pelo núcleo; a App não conta.
- Do mesmo fluxo, o Mestre cria a **credencial de usuário e senha provisória** para o
  responsável sem conta Google. A senha aparece **uma vez**, para entrega em mãos, e não é
  recuperável depois (`RF-09-65`).
- A App 09 ganha a área **Meu perfil**: o Mestre publica **currículo, portfólio, redes sociais
  e artefatos comprobatórios** da sua habilidade, cada um como **endereço e rótulo** — link
  declarado, nunca upload de arquivo (`RF-09-66`, documento 02 §1).
- A App 09 declara, no perfil, que **não cadastra Mestre nem cria acesso de Mestre**: não há
  caminho para criar persona de Mestre, nem para o Mestre editar nome, e-mail ou papel do
  próprio cadastro (`RF-09-67`, `RN-09-14`).
- **Toda tela da App 09 que grava dado pessoal passa a exibir o aviso discreto** do que ali se
  coleta, com acesso à área detalhada, e a aplicação ganha a área **Direitos e dados**, em
  leitura, com a tabela do PRD-09 §11 (`RF-09-68`).
- O núcleo ganha duas portas que o PRD-09 §9 já declara e que a App 09 não tem como cumprir sem
  elas: a **leitura dos Guerreiros e Guerreiras que o Mestre pode vincular**, recortada pelas
  comunidades em que ele atua, e a **publicação dos próprios artefatos comprobatórios** pelo
  Mestre em sessão.

Duas decisões do fundador, tomadas em 2026-08-29 para esta change, entram no documento 09 §1 e
no documento-fonte de cada uma antes de virar código (§ *Impact*).

Fora do escopo, como o PRD-09 §§3.2 e 6.9 já excluem: o **cadastro de Mestre e de Apoiador**,
que é ato exclusivo de Admin na App 03; o **acesso do responsável à App 07** e tudo o que ele lê
por lá, que é PRD-13; o **nick e o avatar do Mestre** (`RF-09-114`), entregues na fatia
`2026-08-21-nick-de-adulto`; e o **exercício dos direitos** — acesso, correção e exclusão —, que
chega pela App 07 e é tratado pela gestão: a área Direitos e dados da App 09 é de leitura.

## Capabilities

### New Capabilities

- `prova-de-habilidade`: o Mestre em sessão lê e publica os **próprios** artefatos
  comprobatórios — endereço e rótulo, link declarado e nunca arquivo —, nunca os de outra
  persona; o que o Admin declarou no cadastro permanece e não é removível por ele; a rota NEVER
  cria persona nem altera papel (`RF-09-66`, `RF-09-67`, `RN-09-14`, invariante 3).

### Modified Capabilities

- `area-do-mestre`: a App 09 ganha a área Responsáveis (cadastro, vínculo com grau de
  parentesco, recusa do quarto vínculo e credencial provisória exibida uma vez), a área Meu
  perfil (prova de habilidade e a declaração de que a aplicação não cadastra Mestre) e a
  camada de direitos (aviso de coleta em toda tela que grava dado pessoal e a área Direitos e
  dados, em leitura) — `RF-09-62` a `RF-09-68`, `RN-09-14`, `RN-09-15`.
- `responsavel-e-vinculo`: o núcleo passa a servir ao **Mestre** a lista dos Guerreiros e
  Guerreiras que ele pode vincular, recortada pelas comunidades em que atua e apresentada por
  **nick e avatar**, nunca por imagem real. Sem ela o `RF-09-62` não tem como apontar quem
  vincular: `GET /guerreiros` é privativa de Admin e o Mestre não guarda identificadores. O
  cadastro, o vínculo e o teto de três não mudam.

## Impact

- **Código**: `apps/app-09-mestre/src/` — áreas novas `responsaveis/`, `perfil/` e `direitos/`,
  mais o aviso de coleta acrescentado às telas já existentes de `turmas/`,
  `criacoesOriginais/`, `territorio/` e `propostas/`; `backend/src/nucleo/personas/` (rotas de
  artefato do próprio Mestre) e `backend/src/nucleo/responsaveis/` (leitura dos vinculáveis),
  com a linha correspondente na matriz de `backend/src/nucleo/permissoes.py`.
- **API**: duas rotas novas sob `/v1`, ambas de Mestre em sessão; nenhuma rota existente muda de
  contrato nem de permissão.
- **Dados**: nenhuma entidade nova. `Persona`, `Responsavel`, `Vinculo` e
  `ArtefatoComprobatorio` já existem; a última ganha **uma coluna e uma migração** — quem
  declarou o artefato —, sem a qual não há como distinguir o que o Admin registrou no cadastro
  do que o Mestre publicou.
- **Documentação, no mesmo PR**: documento 02 §1 e documento 03 §9 (as duas decisões novas),
  documento 09 §1 (as mesmas duas, em "Já decididos"), PRD-01 e PRD-09 (as rotas novas na §9 de
  cada um) e as linhas 10 e 11 do `openspec/cronograma-de-fatias.md`.
