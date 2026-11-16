# Remoção do template da missão

Origem: **PRD-09**, fatia **35** do `openspec/cronograma-de-fatias.md` (nova, aberta nesta
change). Decisão do fundador de 2026-11-16, em `/opsx:propose`: retirar da App 09 o bloco
"Template da missão — Sugestão de estrutura por IA" **para simplificar a autoria** — o Mestre
escreve a missão direto, sem a etapa de pedir estrutura.

Identificadores que **saem** do PRD-09: `RF-09-85` a `RF-09-89`, `RF-09-91`, `RF-09-95`,
`RN-09-33` e `RN-09-34`. Identificador **reescrito**: `RF-09-116` (a cadência de 2, 7 e 21 dias
deixa de vir do template e passa a abrir preenchida no próprio campo). Identificadores que
**perdem a marca de técnico** no PRD-01: `RF-01-62` e `RN-01-54`. `RF-09-90` (não medir consumo
de modelo) **fica**: a leitura da produção também o aplica.

## Why

O template devolvia esqueleto e checklist de lacunas a partir de um tópico, por modelo de IA. O
fundador decidiu que essa etapa complica mais do que ajuda a autoria no Ciclo 01. Com ela saem
os dois insumos que só existiam para servi-la: a **marca de técnico** do catálogo de poderes e o
**DeepSeek**, que atendia unicamente essa porta.

## What Changes

- **App 09** — o bloco recolhível "Template da missão" sai de cada missão; a ordem dos blocos
  passa a começar por **conteúdo**. O bloco **Cadência de retomada** abre com **2, 7, 21**
  preenchido quando a missão não tem cadência gravada, sem gravar nada até o Mestre confirmar
  (`RF-09-116` reescrito).
- **Núcleo** — **BREAKING**: saem `POST /v1/missoes/{id}/estrutura` e
  `POST /v1/sugestoes-de-estrutura/{id}/desfecho`, a porta de IA do template, o adaptador do
  DeepSeek e a entidade `SugestaoDeEstrutura`. Migração Alembic **apaga a tabela**
  `sugestao_de_estrutura` — os registros gravados se perdem, por decisão.
- **Catálogo de poderes** — **BREAKING**: o campo `tecnico` sai da escrita e da leitura de
  `/v1/poderes` e da coluna `poder.tecnico` (mesma migração). A App 03 perde o campo no
  formulário e a marca na lista.
- **DeepSeek fora de tudo** — saem a dupla `CG_DEEPSEEK_*` da configuração, do deploy e do
  README; o documento 03 §1.12 passa a ter o Gemini como único modelo de linguagem do Ciclo
  01; a nota de transparência sobre IA (texto semeado e documentos 01 e 03) deixa de citá-lo.
- **Documentação** — documentos 02, 03, 08, 09, 11 e 99, PRD-01, PRD-09 (e a menção do
  PRD-11) passam a refletir a decisão; o cronograma ganha a linha da fatia 35.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `template-da-missao`: todos os requisitos removidos — a capacidade deixa de existir.
- `area-do-mestre`: saem os dois requisitos do template na App 09; a cadência de retomada abre
  preenchida com 2, 7 e 21 dias; a ordem dos blocos da missão perde o template.
- `catalogo-de-poderes`: saem a marca de técnico e a leitura dela pela gestão; a alteração do
  poder deixa de alcançá-la.

## Impact

- **Backend**: `backend/src/nucleo/template_de_missao/` inteiro, `principal.py`, `modelos.py`,
  `configuracao.py`, `poderes/` (modelo, regra, rotas), semeadura do conteúdo institucional,
  migração nova, testes do template, das portas de IA, do poder e da migração.
- **Apps**: `apps/app-09-mestre/src/trilhas/` (`TemplateDaMissao`, `ListaDeMissoes`,
  `CadenciaDeRetomada`, `api.ts` e testes); `apps/app-03-gestao/src/poderes/` e testes que
  montam poder com `tecnico`.
- **Deploy**: `.github/workflows/backend-deploy.yml` deixa de declarar `CG_DEEPSEEK_MODELO`.
  Tirar `CG_DEEPSEEK_CHAVE_DE_API` do segredo `GCP_SECRETOS_CG` do GitHub e, depois, apagar
  `cg-deepseek-api-key` no Secret Manager são passos manuais do fundador.
- **Produção**: o texto da nota sobre IA já publicado é do Admin; ele o republica pela App 03
  (a semeadura não alcança banco semeado).
- **Fora do escopo**: as outras duas portas de IA (leitura da produção e assistente de trilhas)
  não mudam; a pendência "Provedor da leitura da produção" do documento 09 segue aberta.
