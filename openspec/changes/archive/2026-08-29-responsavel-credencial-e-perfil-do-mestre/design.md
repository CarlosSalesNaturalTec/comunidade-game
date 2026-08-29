## Context

Ver `proposal.md` — *Why*. O que já está pronto e não se refaz:

- `responsavel-e-vinculo` e `persona-e-credencial` cobrem cadastro, vínculo com grau de
  parentesco, teto de três e credencial de usuário e senha provisória. Esta fatia abre a porta
  da App 09 para as rotas que já existem — `POST /v1/responsaveis`,
  `POST /v1/responsaveis/{id}/vinculos` e `POST /v1/credenciais`.
- A App 03 já resolveu o mesmo par de problemas duas vezes: `FormularioDeResponsavel.tsx`
  encadeia cadastro, vínculo e credencial, e `direitos/` traz o `AvisoDeColeta`, o
  `ContextoDeDireitos` e a `TelaDeDireitos`. A App 05 tem o seu próprio aviso. São **padrões
  consolidados por aplicação**, não código compartilhado em `comum/`.
- `ArtefatoComprobatorio` existe desde o cadastro de adulto pelo Admin, com `persona_id`,
  `endereco` e `rotulo`.

Duas restrições moldam o desenho: o Mestre **nunca vê imagem real nem nome civil de
Guerreiro(a)** (PRD-09 §11, invariante 12), e o **cadastro de Mestre é exclusivo de Admin**
(invariante 3) — a App 09 escreve sobre pessoas apenas nos dois pontos que o PRD-09 §6.9
autoriza.

## Goals / Non-Goals

**Goals:**

- Abrir na App 09 o fluxo de responsável em um caminho só: cadastro → vínculo(s) → credencial
  opcional, tolerante a falha no meio.
- Dar ao Mestre uma escolha de Guerreiro(a) **usável** sem ampliar o que ele enxerga.
- Distinguir, no perfil, o artefato do cadastro do artefato publicado pelo Mestre.
- Levar a camada de direitos da App 09 ao mesmo piso das Apps 03 e 05.

**Non-Goals:**

- Extrair `AvisoDeColeta`, `ContextoDeDireitos` ou a tela de direitos para `comum/`: a tabela de
  dados é **de cada PRD** (§11 do PRD-02, do PRD-05, do PRD-09) e o texto muda com ela.
- Edição do responsável já cadastrado, encerramento de vínculo e histórico de credenciais —
  nenhum requisito do recorte os pede.
- Página pública do Mestre com currículo e portfólio: é vitrine, PRD-03.

## Decisions

### 1. A escolha do Guerreiro(a) vem de rota nova, recortada pelas comunidades do Mestre

`GET /v1/guerreiros/vinculaveis`, de Mestre em sessão, devolve **nick e avatar** dos Guerreiros e
Guerreiras ativos das comunidades em que ele atua. Decisão do fundador, 2026-08-29 (documento 09
§1): sem ela o `RF-09-62` não tem como apontar quem vincular.

A rota **não cria entrada nova na matriz**: reaproveita a operação
`vinculo_com_guerreiros_e_guerreiras`, que o Mestre já tem em `escreve`, acrescentando-a ao
conjunto `le` do papel. Quem pode criar o vínculo pode ler quem vincular — o alcance da leitura é
exatamente o da escrita que ela serve, e nada além dela se abre.

- Descartado: abrir `GET /guerreiros` ao Mestre — daria a qualquer Mestre a lista de todas as
  crianças da plataforma, contra o recorte do PRD-09 §4.
- Descartado: identificador digitado, como na `TelaDeLancamento` — o Mestre não tem o
  identificador em mãos ao receber a família.
- Descartado: operação nova na matriz — inflaria o PRD-01 §4 com uma leitura que só existe para
  servir uma escrita já concedida.

### 2. O artefato guarda quem o declarou, e é isso que decide a remoção

`ArtefatoComprobatorio` ganha `declarado_por_id` — a persona que declarou —, com migração
Alembic. O Mestre remove apenas o artefato cujo `declarado_por_id` é a **própria** persona; o do
Admin, e a linha antiga que nasceu sem a coluna, são apresentados em leitura e recusados na
remoção com **403**. Decisão do fundador, 2026-08-29 (documento 09 §1): a prova que sustentou o
cadastro não sai pela mão de quem foi cadastrado (`RN-09-14`, invariante 3).

Sem backfill: linha antiga com `declarado_por_id` nulo é, por definição, do cadastro — que é
como todas nasceram até aqui.

- Descartado: permitir a remoção de qualquer artefato — apagaria a prova de habilidade do
  cadastro.
- Descartado: perfil só somativo — deixaria link quebrado e rede social antiga para sempre.

### 3. O `{id}` da rota de artefatos é conferido contra a sessão

O PRD-09 §9 declara `POST /v1/mestres/{id}/artefatos`; a rota mantém o `{id}` e **exige que ele
seja o da persona em sessão** — qualquer outro recebe 403. À rota declarada juntam-se a leitura
`GET /v1/mestres/{id}/artefatos` e a remoção `DELETE /v1/mestres/{id}/artefatos/{artefato_id}`,
sem as quais o `RF-09-66` não se cumpre: as três entram na §9 do PRD-09 e do PRD-01 no mesmo PR.
A escrita entra na matriz do Mestre como **documentos comprobatórios**, a mesma operação que o
Apoiador já tem no PRD-01 §4.

### 4. O fluxo do responsável é retomável, não transacional

O cadastro, cada vínculo e a credencial são chamadas separadas ao núcleo. A tela guarda o
identificador do responsável já criado e **não o recria** na retentativa — o mesmo precedente da
`TelaDoResponsavel` da App 01 (decisão 4 daquela change). Recusa do quarto vínculo (422) não
desfaz o que já passou: o responsável e os vínculos anteriores permanecem, e o Mestre segue de
onde estava.

### 5. A camada de direitos da App 09 espelha a da App 03, com a tabela do PRD-09 §11

`apps/app-09-mestre/src/direitos/` recebe `AvisoDeColeta`, `ContextoDeDireitos` e
`TelaDeDireitos`, com o mesmo desenho da App 03 — provedor no `App.tsx`, aviso em qualquer
profundidade sem _prop-drilling_ — e a tabela do **PRD-09 §11**, não a do PRD-02. Direitos entra
como área da navegação, ao lado das oito já existentes.

O aviso é acrescentado às telas que gravam dado pessoal, uma por linha da tabela do PRD-09 §11:
responsável e vínculo, perfil do Mestre, conteúdo autoral da missão, conferência de presença,
lançamento do desfecho, ocorrência de conduta e validação da criação original.

- Descartado: mover a camada para `comum/` — ver *Non-Goals*.

## Risks / Trade-offs

- **A tabela de direitos duplica texto do PRD-09 §11 em código** → é cópia declarada: o
  comentário do arquivo aponta a §11 como fonte única, e mudança lá exige mudar aqui. Mesmo
  precedente aceito na App 03.
- **`declarado_por_id` nulo vale como "do cadastro"** → é verdade para todo o legado, mas a
  leitura fica ambígua se algum dia uma linha nascer sem autor; a rota nova sempre grava a
  persona em sessão, e o cadastro por Admin passa a gravar o Admin.
- **Três avisos de coleta em três aplicações, sem código comum** → a divergência de redação é
  aceita em troca de cada §11 permanecer fonte única do seu texto.
- **A lista de vinculáveis cresce com a comunidade** → segue o contrato de listagem do PRD-01,
  com paginação por cursor, como as demais leituras.
