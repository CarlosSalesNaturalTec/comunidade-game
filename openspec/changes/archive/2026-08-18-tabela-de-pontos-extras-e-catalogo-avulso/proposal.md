## Why

Sétima fatia do **PRD-07 — Economia de recursos e ledger**. Atende `RF-07-42`, `RF-07-43`,
`RF-07-44`, `RF-07-45`, `RF-07-33` e `RF-07-34`, e as regras `RN-07-24`, `RN-07-25`,
`RN-07-26`, `RN-07-29` e `RN-07-30`.

O **saldo disponível de pontos extras** existe desde a change `pontos-niveis-e-badges` e
**nunca debitou nada**: a única saída prevista para ele no Ciclo 01 é a troca por recompensa
avulsa, e a troca não tem por onde acontecer enquanto não houver catálogo nem preço. O
invariante 23 do documento 99 §6 — reais, moedas e pontos extras não se convertem entre si —
está implementado com duas das três unidades apenas. Esta fatia entrega a **régua** (o preço
em pontos extras, versionado como o valor em moedas já é) e o **catálogo** (o item com
lastro, estoque e comunidade); a troca vem na fatia seguinte.

## What Changes

- **Preço de referência em pontos extras por tipo de recurso**, cadastrado por Admin e
  versionado por data de vigência, exatamente como o valor de referência em moedas já é
  (`RF-07-42`, `RF-07-43`). O preço **não deriva** do valor em moedas do mesmo tipo: são duas
  réguas independentes sobre a mesma entidade (`RN-07-25`, `RN-07-24`).
- **Piso de 20 pontos extras**: preço menor é recusado (`RF-07-44`, `RN-07-30`).
- **Item do catálogo avulso** com nome, tipo de recurso, estoque, comunidade e **ponto de
  apoio** (`RF-07-33`). O item **não aceita preço próprio** — lê o da tabela vigente
  (`RF-07-45`, `RN-07-29`).
- **Duas origens de cadastro**: Mestre cadastra direto, sem homologação (`RF-09-100`);
  Apoiador cadastra pendente de **homologação de Admin** (`RN-14-42`).
- **Lastro exigido para ativar**: item só fica ativo havendo, no saldo do seu tipo de recurso
  no seu ponto de apoio, **quantidade igual ou maior que o estoque declarado** (`RF-07-34`,
  `RN-07-26`, `RN-09-37`, invariante 9).
- **Manutenção do item** — alteração de estoque e retirada do catálogo, com autoria
  registrada (`RF-07-33`, `RF-09-102`).
- **Leitura do catálogo por comunidade**, para as aplicações que o exibem (`RF-04-50`,
  `RF-05-83`, `RF-09-103`).
- **Três decisões novas gravadas no mesmo PR**, antes de virarem comportamento — no
  documento-fonte de cada uma e no documento 09, em "Já decididos":
  1. A **janela de troca** do `RF-04-49` — o momento que o Mestre abre e fecha no encerramento
     do encontro — é garantia **da App 01**; o núcleo não a verifica (documento 02 §8.2).
  2. O **item do catálogo declara o ponto de apoio**, como a `Aula` já declara: o saldo é por
     tipo **e** ponto de apoio, e sem essa dimensão o item não acha o saldo que o lastreia nem
     a troca acha de onde dar baixa. O PRD-07 §8 dava ao item apenas a comunidade
     (documento 04 §1).
  3. **Lastro do item é saldo igual ou maior que o estoque declarado**: o item só promete o
     que existe. O `RF-07-34` e o `RN-07-26` exigiam lastro sem dizer quanto
     (documento 02 §8.2).

## Capabilities

### New Capabilities

- `catalogo-avulso`: o item de recompensa avulsa — nome, tipo de recurso, estoque,
  comunidade, origem do cadastro, homologação, lastro e retirada. Não cobre a troca.

### Modified Capabilities

- `catalogo-de-tipos-de-recurso`: passa a manter, além do valor de referência em moedas, o
  **preço de referência em pontos extras**, com a mesma mecânica de vigência e o piso de 20.

## Impact

- **Código**: `backend/src/nucleo/recursos/` ganha o preço de referência; nasce
  `backend/src/nucleo/catalogo_avulso/`. Migração Alembic para as duas tabelas.
- **API**: rotas novas sob `/v1` para o preço de referência e para o catálogo — cadastro,
  homologação, estoque, retirada e leitura por comunidade.
- **Leitura**: nenhuma rota pública nova. O catálogo é lido por persona em sessão.
- **Depende de**: `catalogo-de-tipos-de-recurso`, `livro-razao` (saldo por tipo e ponto de
  apoio), `comunidade-virtual` e `persona-e-credencial` — todos já consolidados.
- **Não toca** o `ponto-extra`: o débito do saldo disponível é da fatia seguinte.
- **Documentação**: documentos 02 §8.2 e 04 §1 (fontes das três decisões), documento 09
  ("Já decididos"), PRD-04 e PRD-07 — que ganha o ponto de apoio no `ItemDeCatalogoAvulso`
  da §8 — e `docs/prds/index.md` pela situação do PRD-07. Nenhum arquivo novo em `docs/`,
  logo a `nav` do `mkdocs.yml` não muda.

## Fora do escopo

Reproduz o que o PRD-07 §3.2 já exclui, mais o recorte desta fatia:

- **A troca em si** — `RF-07-35`, `RF-07-36`, `RF-07-37`, `RF-07-38` e `RF-07-46`: oitava
  fatia. Aqui não há débito de ponto extra, baixa no livro-razão nem decremento de estoque
  por troca.
- **Interface de gestão do catálogo**: App 09 (PRD-09) e App 08 (PRD-14).
- **Recompensa de marco**: conquistada, nunca trocada — e depende de `RecompensaDeMarco`, que
  nasce no PRD-09.
- **Preços concretos de cada item acima do piso**: cadastro da gestão, pendente do calendário
  do Ciclo 01 no documento 09. A entidade opera com qualquer valor a partir de 20.
