# Edição e exclusão de Mestre e Apoiador

**PRD de origem:** PRD-02 — Frontend de gestão (App 03), fatia **29** do
`openspec/cronograma-de-fatias.md`.
**Requisitos atendidos:** `RF-02-117`, `RF-02-118`, `RF-02-119`, `RN-02-34`, `RN-02-35` —
**novos**, a criar na revisão do PRD-02 no mesmo PR; alteram `RF-02-02` e `RF-02-03`
("cadastra" passa a "cadastra e mantém") e preservam `RF-02-04`, `RN-02-01` e `RN-14-10`.

## Why

Mestre e Apoiador cadastrados pela gestão são, hoje, **imutáveis**: o núcleo serve criar e
listar, a ficha da App 03 é só de leitura, e um e-mail digitado errado deixa o adulto sem
login social para sempre. Também não há como retirar um cadastro feito por engano. A fatia 18
deixou "editar o cadastro de adulto" para o Ciclo 02 (documento 09 §1, linha "O que a fatia 18
do PRD-02 deixa fora").

## Decisão de planejamento

Decisão do fundador de **2026-11-17**, tomada ao pedir esta change; a fatia 29 foi acrescentada
ao cronograma antes desta proposta. Quatro partes:

1. **A edição de adulto entra no Ciclo 01**, para **Mestre e Apoiador**.
2. **O que se altera:** nome, e-mail, WhatsApp e artefatos comprobatórios (incluir, corrigir,
   remover), mantido o **mínimo de um** artefato (`RF-02-04`). O **nick fica fora** — trocar
   nick é ato do próprio adulto (documento 02 §1) — e os **termos de doação** não se editam.
3. **Excluir** apaga o adulto **só se nunca usado** — nenhuma linha de nenhuma tabela aponta
   para ele além do próprio cadastro (nick, credencial, sessão e artefatos). Adulto usado é
   recusado, e o caminho dele é a **desativação**: perde o acesso e sai da vitrine; o que ele
   produziu (aporte, trilha, lançamento, selo) segue inalterado, porque o ledger é imutável e o
   comprovante homologado é prova contábil (PRD-14 §11).
4. **Reativação** pelo Admin desfaz a desativação, no precedente de `RF-02-115`.

A decisão entra no documento-fonte do cadastro de personas — documento 02 §1 — e a linha do
documento 09 §1 da fatia 18 é revista no mesmo PR.

## What Changes

- **Núcleo — edição:** `PATCH /v1/mestres/{id}` e `PATCH /v1/apoiadores/{id}`, restritas a
  Admin, alteram nome, e-mail e WhatsApp; trocar o e-mail troca o identificador da credencial de
  login social. E-mail já usado por outra credencial ativa é recusado com 422 (`RF-02-117`).
- **Núcleo — artefatos pela gestão:** incluir, corrigir e remover artefato comprobatório do
  adulto, por Admin; a remoção que deixaria o adulto sem artefato é recusada com 422
  (`RF-02-117`, `RF-02-04`, `RN-02-01`).
- **Núcleo — exclusão e desativação:** `DELETE /v1/{mestres|apoiadores}/{id}` apaga o nunca
  usado e recusa o usado com 422 (`RF-02-118`, `RN-02-34`); `POST .../desativacao` e
  `POST .../reativacao` marcam e desmarcam a persona (`RF-02-119`, `RN-02-35`). Desativado não
  entra (credencial e sessões revogadas) e some das listagens e páginas da vitrine.
- **Saída:** `AdultoSaida` passa a levar `ativo`.
- **App 03:** a ficha do adulto ganha edição dos dados e dos artefatos, e as ações excluir,
  desativar e reativar, com confirmação; a tabela marca o desativado.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `cadastro-de-persona`: o Admin edita, exclui, desativa e reativa Mestre e Apoiador.
- `aplicacao-de-gestao`: a ficha do adulto deixa de ser só leitura; a tabela marca o
  desativado.
- `leitura-publica-da-vitrine`: adulto desativado não aparece nas listagens nem na página
  individual.
- `sessao-do-adulto`: adulto desativado não abre sessão.

## Impact

- **Backend:** `personas/` (rotas, regra, modelo), migração Alembic (`persona.desativada_em`),
  `vitrine/` (filtro do desativado), login social (recusa do desativado), `referencias.py`
  (reuso de `esta_em_uso`).
- **App 03:** `personas/FichaDoAdulto.tsx`, `FormularioDeArtefatos.tsx`, `ListaDeAdultos.tsx`,
  `api.ts` e testes.
- **Documentação:** PRD-02 (§§6.1, 7, 9, 13, 15), documento 02 §1, documento 09 §1,
  cronograma.
- **Fora:** Admin, responsável e Guerreiro(a) (este já tem edição por `RF-02-01`); troca de nick
  e de papel; edição dos termos de doação; apagar aporte, trilha ou lançamento do adulto.
