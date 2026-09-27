# Proposal

Fatia 23 do **PRD-02 — Frontend de gestão (App 03)**, conforme
`openspec/cronograma-de-fatias.md`. Atende `RF-02-06`. Correção de defeito: nenhum
requisito, rota ou entidade nova.

## Why

Na App 03, a lista "Vínculos já criados" do formulário de Responsáveis imprime apenas o
**grau de parentesco** do vínculo. Um responsável vinculado a dois Guerreiros como "Pai"
produz duas linhas idênticas — "Pai" e "Pai" —, e o Admin não tem como saber a quem cada
uma se refere nem se acertou o vínculo que acabou de criar. Relatado pelo fundador em
2026-09-26, com evidência de tela.

O dado que falta já está na tela: o nick vem do mesmo estado que alimenta o seletor de
Guerreiro(a), e o `guerreiro_id` já vem na resposta do vínculo criado. A confirmação do
ato depende de cruzar os dois.

## What Changes

- Cada linha da lista de vínculos já criados passa a identificar o **Guerreiro(a) pelo
  nick**, ao lado do grau de parentesco.
- Nada mais: o cadastro, o vínculo, o teto de três e a credencial provisória seguem como
  estão.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-de-gestao`: o requisito "O Admin inclui outro Admin e cadastra o responsável
  com o vínculo" (`RF-02-06`) ganha a exigência de que o vínculo confirmado seja
  apresentado identificando o Guerreiro(a), não só o parentesco.

## Impact

- `apps/app-03-gestao/src/personas/FormularioDeResponsavel.tsx` — a lista de vínculos.
- `apps/app-03-gestao/src/personas/personas.test.tsx` — cobertura do caso de dois vínculos
  com o mesmo parentesco.
- Backend: nenhum. Rotas, contratos e migrações: nenhum.
- Documentação MkDocs: nenhuma — a change não toma decisão nova nem muda requisito de PRD.
  Fecha a fatia 23 no `openspec/cronograma-de-fatias.md`.

## Fora do escopo

- A App 09 tem o mesmo defeito, em `TelaDeResponsaveis.tsx`. É a **fatia 21 do PRD-09**,
  change própria — decisão do fundador de 2026-09-26, uma fatia por aplicação.
- Listar os responsáveis já cadastrados e retomar o vínculo de um deles: **fatia 24 do
  PRD-02**, que cria `RF-02-111` e a rota do núcleo.
- A App 01 não apresenta lista de vínculos; nada a corrigir lá.
