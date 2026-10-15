# Proposal

Origem: **PRD-04 — Aula presencial (App 01)**, **fatia 26** do
`openspec/cronograma-de-fatias.md`.

Alcança `RF-04-01`, `RF-04-63`, `RF-04-71` e `RF-04-49`, **sem identificador novo**: a
ordem dos caminhos da tela inicial é apresentação, e nenhum enunciado a fixa — `RF-04-01`
e o cenário "Os três caminhos aparecem" apenas **enumeram** os caminhos. Mesmo molde da
fatia 25 (`2026-10-14-toggle-de-som-e-operacao-no-fim-do-menu`), que desceu encerrar e
abrir a troca ao menu pela mesma razão.

Decisão do fundador de **2026-10-15**.

## Why

A tela inicial apresenta hoje a **Medição do limiar** entre os caminhos da criança, embora
ela seja ato de quem opera o aparelho: `RF-04-63` a atribui a Mestre ou Admin, a tela monta
com `alcance="operador"` (`RN-04-33`) e pede o **mesmo PIN do aparelho** que o encerramento
da sessão de trabalho (`RN-04-41`). O grupo "Para quem opera o aparelho", criado na fatia
25, é exatamente a fronteira que ela deveria estar respeitando — e não está. Descê-la é
correção de coerência, não preferência visual.

Na mesma passada, a ordem dos caminhos deixa de ser a ordem em que as fatias os
acrescentaram e passa a ser a que o fundador decidiu: **equipes acompanha trilhas e
missões**, por serem o par de "trabalhar a trilha".

## What Changes

- A ordem dos caminhos da tela inicial passa a ser **onboarding**, **presença**, **trilhas
  e missões**, **equipes**, **quiz ao vivo** e, com o momento de troca aberto, **troca por
  recompensa avulsa**. O quiz é o quinto, não o quarto.
- A **medição do limiar** sai do bloco dos caminhos e entra no grupo "Para quem opera o
  aparelho", como **primeiro item** dele — antes da chave do momento de troca, porque
  calibração é ato de preparo, raríssimo, enquanto a chave é do encontro em curso.
- O **encerramento da sessão de trabalho continua por último**, agora como último dos três
  itens do grupo em vez de dos dois (`RF-04-71`).
- A ordem do bloco da criança passa a ser **verificada**: hoje nenhum teste a protege — o
  teste dos glifos lista os sete rótulos e **itera** sem asserir ordem.

Nada de comportamento muda. Em particular, o **papel não muda**: a medição segue visível a
toda sessão de trabalho (todo papel que não seja `guerreiro`), guardada pelo PIN do
aparelho e não pelo papel, embora a chave da troca ao lado dela seja só do Mestre. É
assimetria **conhecida e mantida por decisão do fundador de 2026-10-15** — não pendência
nova, e não se resolve nesta fatia.

Não há **BREAKING**: nenhum contrato, rota ou rótulo muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o requirement "A tela inicial oferece os três caminhos e
  volta ao início a cada atendimento" enumera o grupo de quem opera como "as **duas**
  ações" e fixa o encerramento como "o último **dos dois**". Com a medição ali passam a ser
  três, e o encerramento é o último **do grupo**. O delta também fixa, em cenário, a ordem
  dos caminhos — que hoje nenhum requisito nem cenário determina.

## Impact

| Alcance | O que muda |
| --- | --- |
| `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx` | ordem dos cartões na lista e o cartão da medição movido para dentro do `fieldset` do grupo |
| `apps/app-01-aula-presencial/src/inicio/inicio.test.tsx` | cenários novos da ordem e da medição dentro do grupo |
| `openspec/specs/aplicacao-da-aula-presencial/` | delta de spec, consolidado no arquivamento |
| `openspec/cronograma-de-fatias.md` | a linha da fatia 26 |

**Fora do alcance:** backend, rotas, `comum/` (nenhum glifo novo — todos já existem), as
demais aplicações, e qualquer tela da App 01 que não seja a inicial. A CSS do separador
(`.cg-caminhos__operacao`, `.cg-caminhos__grupo`) já existe e não muda.

**Fora do escopo**, reproduzindo o que o PRD-04 §3.2 já exclui e o que a fatia 25 deixou
assentado: nenhuma mudança de rótulo, de guarda de PIN, de papel ou de comportamento de
caminho algum.

**Documentação:** nada em `docs/` muda. `docs/prds/index.md` não muda — o PRD-04 segue em
implementação —, e o documento 09 não recebe linha: não há decisão nova de regra, é
apresentação, no molde da fatia 25. Por isso a change **não roda** `npm run fix`,
`npm run lint` nem `mkdocs build --strict`; `openspec/` fica fora do lint de documentação e
do site.

**Verificação:** só a esteira de `apps/*` — `biome format --check .`, `biome check .` e
`vitest run` da App 01.
