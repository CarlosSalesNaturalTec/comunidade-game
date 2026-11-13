# Proposal

**PRD de origem:** PRD-03 — Vitrine pública (App 06). **Fatia 14** do
`openspec/cronograma-de-fatias.md` ("Customização do kit no portfólio"). **Atende** `RF-03-88`;
**preserva** `RF-03-84` a `RF-03-87`, `RN-03-41` e `RN-03-43`. Decisão do fundador de
2026-11-12, registrada no documento 09 §1 ("Customização do kit recebido").

## Why

A change de núcleo `2026-11-12-customizacao-do-kit-recebido-no-nucleo` (implementada) já põe o
registro aprovado da customização na listagem pública do acervo, na carta do Guerreiro(a) e na
rota `GET /v1/vitrine/customizacoes/{id}/arquivo`. A App 06 conhece **duas** fontes: o tipo
`FonteDoAcervo` não tem `customizacao_do_kit`, e `lerArquivoDoAcervo` manda toda fonte que não é
criação original para a rota da **comprovação** — a imagem ou o vídeo da customização cai em
404 e a linha diz "A produção não está disponível agora." a quem tem item aprovado e autorizado.

## What Changes

- `api/leituras.ts`: `FonteDoAcervo` ganha `customizacao_do_kit`, e `lerArquivoDoAcervo`
  passa a escolher a rota pela fonte — `criacoes`, `comprovacoes` ou `customizacoes`
  (`RF-03-88`, `RF-03-85`).
- A **linha do acervo** (`linhaDoAcervo`), a mesma do portfólio da vitrine e da página do
  Guerreiro(a), desenha o item da customização com a **descrição como título** e a **trilha**
  ao lado da data — a trilha só se omite na criação da culminância (`RN-03-43`) —, e abre a
  imagem ou o vídeo na própria linha (`RF-03-88`, `RF-03-85`, `RF-03-87`).
- A coluna "Criações originais" da carta lista o item pela descrição e pela data, sem código
  próprio: já consome o que o núcleo envia (`RF-03-86`).
- Testes de Vitest das três superfícies com item da terceira fonte.
- Comentários que dizem "duas fontes" passam a dizer três.
- **Documentação:** a tabela de rotas do PRD-03 §9 ganha a linha de
  `GET /v1/vitrine/customizacoes/{id}/arquivo`, que o núcleo já serve e o PRD não lista; a
  linha da fatia 14 no cronograma fecha com o slug.
- **Sem núcleo, sem migração, sem rota nova.**

### Fora do escopo

O que o PRD-03 §3.2 exclui. Também ficam de fora, por serem de outras fatias já entregues: o
registro, o julgamento e a mídia da customização fora da vitrine (PRD-01, PRD-04, PRD-05,
PRD-09).

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-vitrine`: o portfólio, a linha do acervo, a coluna da carta e o portfólio da
  página do Guerreiro(a) passam a reconhecer a **terceira fonte** — a customização do kit —,
  com a descrição como título, a trilha e a mídia aberta pela rota da fonte dela.

## Impact

- **Código:** `apps/app-06-vitrine/src/api/leituras.ts`,
  `apps/app-06-vitrine/src/portfolio/` (comentários e, se preciso, a linha) e os testes em
  `apps/app-06-vitrine/src/testes/`.
- **API:** consumo de `GET /v1/vitrine/customizacoes/{id}/arquivo`, já existente; nenhum
  contrato muda.
- **Docs:** PRD-03 §9 (uma linha na tabela de rotas) e `openspec/cronograma-de-fatias.md`.
- **Esteiras:** a do frontend (Biome e Vitest) e, por tocar o PRD, a de documentação.
