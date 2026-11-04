# Proposal

## Why

O acervo decidido em 2026-11-03 (documento 09 §1) precisa de três coisas que o núcleo não tem,
e sem elas nenhuma das quatro fatias seguintes se sustenta: o **áudio** não é tipo de produção
do aluno; a mídia da criação original é **write-only** — há `POST` e `PATCH` de
`/criacoes/{id}/arquivo` e **nenhum `GET`**, de modo que o arquivo entra e nunca pode ser lido,
nem pelo autor nem pela vitrine; e a `ProducaoDaMissao` nasceu **sem coluna de foto nem de
áudio**, por decisão hoje revertida.

É a fatia sem número do bloco PRD-01 do `openspec/cronograma-de-fatias.md`.

## What Changes

- **Áudio vira o sexto tipo de produção do aluno.** `TipoDeProducaoDaCriacaoOriginal` passa de
  cinco a seis valores. O `TipoDeConteudo` do Mestre **não muda** — os dois enums já são
  separados de propósito, e o documento 02 §4 só ampliou a entrega do Guerreiro(a).
- **A mídia da criação original passa a ser legível.** Nasce `GET /v1/criacoes/{id}/arquivo`,
  restrito a quem já pode ver a criação, no molde de `GET /conteudos/{id}/arquivo`.
- **A mídia da criação original passa a ser legível em público**, por rota própria, com o
  portão de `condicoes_de_criacao_publica` aplicado **ao byte** e não só à listagem: hoje o
  portão protege quem aparece na lista, não quem serve o arquivo.
- **A `ProducaoDaMissao` passa a guardar mídia** — ganha sessão de envio retomável e rota de
  leitura, como a criação original e o conteúdo já têm. **BREAKING** em relação à regra
  vigente: cai o "sem guardar a foto nem o áudio" do propósito de `producao-da-missao`, e a
  foto deixa de ser lida-e-descartada.
- Migração Alembic para as colunas de mídia da produção e para o valor novo do enum.

**Fora desta fatia**, e nomeado para não ser suposto: a comprovação do desafio prático, o
critério de aceite, o título curto, os dois vereditos e os 5 pontos. Esta fatia só entrega o
que as outras consomem.

## Capabilities

### New Capabilities

Nenhuma. A fatia amplia capacidades existentes.

### Modified Capabilities

- `criacao-original`: o tipo da produção passa a admitir **áudio** — os "cinco valores
  fechados" viram seis —, e a mídia ganha leitura por quem já pode ver a criação, que hoje não
  existe em rota alguma.
- `producao-da-missao`: a produção passa a **guardar** a foto e o áudio, com sessão de envio e
  leitura, revertendo o descarte declarado no propósito da capacidade.
- `leitura-publica-da-vitrine`: a mídia da criação original pública passa a ser servida, sob o
  mesmo portão de autorização que já rege a listagem.

## Impact

- **Núcleo**: `criacoes_originais/` (modelo, regra, rotas), `producoes/` (modelo, regra, rotas,
  porta de armazenamento), `vitrine/` (rota pública de mídia).
- **Contratos**: três rotas novas; `tipo` da criação original aceita um valor a mais — ampliação
  compatível para quem envia, e os clientes que **listam** tipos precisam saber do sexto.
- **Dados**: migração Alembic — colunas de mídia em `producao_da_missao` e novo valor de enum.
- **PRD-01**: identificadores novos, a partir de `RF-01-77` e `RN-01-60`, livres hoje. O PRD-01
  §14 não tem pendência que trave esta fatia.
- **Documentação**: a decisão já está gravada nos documentos 02 §4, 11 §§2.2, 5 e 8.2, 99 §6 e
  09 §1. Esta change revisa o **PRD-01** e fecha a linha do cronograma.
- **Não alcança** aplicação alguma: nenhuma das oito muda nesta fatia.
