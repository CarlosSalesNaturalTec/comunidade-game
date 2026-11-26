# Proposal

PRD-02 — Frontend de gestão (App 03), **fatia 31** do `openspec/cronograma-de-fatias.md`.
Alcança `RF-02-15` e `RN-02-22`, sem identificador novo: é reorganização de tela sobre
requisito já entregue, decisão de exibição do fundador de 2026-11-26.

## Why

Na lista de Guerreiros e Guerreiras da área Personas o Admin só reconhece a criança pelo nick,
e o nick nem sempre diz quem ela é. Duas colunas ocupam espaço sem ajudar a conferência: a
"Avatar" traz sempre o mesmo texto ("Avatar definido") e a "Início do vínculo" repete uma data
que o Admin não usa para conferir o vínculo — o que `RF-02-15` pede é a comunidade.

## What Changes

- A lista passa a mostrar o **nome** do Guerreiro(a) ao lado do nick.
- Sai a coluna **"Avatar"**.
- Sai a coluna **"Início do vínculo"**; a comunidade do vínculo vigente segue em leitura, e a
  ausência de vínculo continua informada em linguagem simples (`RF-02-15`, `RN-02-06`).
- A lista segue sem imagem real (`RN-02-22`, invariante 12 do documento 99 §6). O nome é dado
  que o próprio Admin cadastra e já vê na edição; a App 03 é restrita a Admin e não é
  superfície pública, onde o Guerreiro(a) segue só por avatar e nick.

Fora do escopo: o contrato `GET /v1/guerreiros` (já devolve `nome`), a ficha, o formulário de
cadastro e edição e qualquer outra aplicação.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: o requisito "A lista de Guerreiros e Guerreiras mostra o vínculo, sem
  caminho de troca" deixa de exigir a data de início do vínculo e passa a exigir o nome ao lado
  do nick.

## Impact

- `apps/app-03-gestao/src/personas/ListaDeGuerreiros.tsx` e
  `apps/app-03-gestao/src/personas/personas.test.tsx`.
- Sem backend, sem migração, sem rota nova; nada em `docs/` muda — o enunciado de `RF-02-15`
  não fixa a data.
