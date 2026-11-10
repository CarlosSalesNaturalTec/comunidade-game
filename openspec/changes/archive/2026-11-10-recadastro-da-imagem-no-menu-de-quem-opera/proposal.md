# Proposal

Origem: **PRD-04 — Aula presencial (App 01)**, **fatia 32** do
`openspec/cronograma-de-fatias.md`.

Alcança `RF-04-22`, `RF-04-01`, `RF-04-21`, `RF-04-28` e `RN-04-37`, **sem identificador
novo**: `RF-04-22` diz que o Mestre ou o Admin recadastra "a partir da própria aplicação" e não
fixa a tela. Mesmo molde da fatia 26, que desceu a medição do limiar ao grupo de quem opera.

Decisão do fundador de **2026-11-10**.

## Why

O recadastro da imagem de referência mora hoje **dentro do caminho das equipes**, como botão
secundário abaixo de "Criar equipe", e só aparece quando a sessão do Guerreiro(a) foi aberta por
confirmação presencial. É ato do Mestre ou do Admin (`RF-04-22`) escondido num caminho que a
criança escolhe, e para chegar a ele o adulto precisa entrar em Equipes e passar pela guarda de
presença, que nada tem a ver com o recadastro.

## What Changes

- O grupo "Para quem opera o aparelho" ganha o item **"Recadastrar imagem de Guerreiro(a)"**,
  logo depois da medição do limiar, visível em toda sessão de trabalho.
- Escolhido o item, a entrada do Guerreiro(a) abre **direto na confirmação presencial**: o nick
  dito pela criança e o PIN de quem abriu o aparelho (`RF-04-21`, `RN-04-37`). A entrada por
  reconhecimento não é oferecida: o recadastro só serve a quem a imagem atual não reconhece, a
  mesma regra que hoje exige a sessão aberta por confirmação.
- Confirmada a identidade, a aplicação segue **direto à captura, sem a guarda de presença**
  (decisão do fundador de 2026-11-10): é ato de quem opera, como a medição e as entregas.
- Gravado o descritor, uma tela diz que a nova imagem foi gravada, e voltar encerra a sessão do
  Guerreiro(a) e volta à tela inicial (`RF-04-28`).
- O botão **sai da tela das equipes**, e com ele o estado que lembrava por qual via a sessão
  abriu (`viaDeEntrada`) e o aviso `aoAbrirSessao` da entrada, que só existiam para ele.
- A camada comum ganha o glifo **`recadastro`** — rosto dentro das quinas de captura —, porque
  todo cartão do menu leva glifo ao lado do rótulo (documento 15 §§5, 11.1) e nenhum dos
  existentes diz "imagem do rosto".

Sem rede, o item diz que o caminho precisa de rede, como os demais que não registram presença:
o descritor é comparado e gravado no núcleo (`RF-04-24`). Não há **BREAKING**: nenhuma rota,
contrato ou regra do núcleo muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `aplicacao-da-aula-presencial`: o requirement do recadastro passa a dizer onde ele é alcançado
  e como a sessão abre; o requirement da tela inicial acrescenta o recadastro ao grupo de quem
  opera, na ordem medição → recadastro → momento de troca → entregas → encerramento.

## Impact

| Alcance                                                         | O que muda                                                     |
| --------------------------------------------------------------- | -------------------------------------------------------------- |
| `apps/app-01-aula-presencial/src/inicio/TelaInicial.tsx`        | caminho `recadastro`, cartão no grupo, desfecho da captura     |
| `apps/app-01-aula-presencial/src/entrada/TelaDeEntradaDoGuerreiro.tsx` | caminho `recadastro`, que abre na confirmação; sai `aoAbrirSessao` |
| `apps/app-01-aula-presencial/src/equipes/TelaDeEquipes.tsx`     | sai o botão do recadastro                                      |
| `comum/react/Icone.tsx`                                         | glifo `recadastro`                                             |
| testes de `inicio`, `entrada` e `Icone`                         | cenários do delta                                              |
| `openspec/cronograma-de-fatias.md`                              | a linha da fatia 32                                            |

**Fora do alcance:** backend e rotas — a gravação segue pela rota do descritor com o token de
trabalho —, as demais aplicações e a regravação pelo próprio Guerreiro(a), que segue pendente no
documento 09.

**Documentação:** nada em `docs/` muda. O PRD-04 já diz "a partir da própria aplicação", a
situação do PRD em `docs/prds/index.md` não muda e não há decisão de regra nova para o
documento 09: é onde o ato mora, no molde das fatias 25 e 26.

**Verificação:** só a esteira de `apps/*` — `biome format --check .`, `biome check .` e
`vitest run` da App 01 e de `comum/`.
