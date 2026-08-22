## Why

Origem: **PRD-02** (App 03 — Frontend de Gestão), com apoio no **PRD-01**. Atende `RF-02-01` a
`RF-02-07`, `RN-02-01`, `RN-02-02`, `RN-02-08`, `RN-02-21` e `RN-02-22`.

O núcleo sabe criar persona — `criar_persona` já existe e já governa nick, avatar e papel —,
mas **nenhuma rota a expõe**: hoje só a semeadura e o cadastro de responsável a alcançam. Sem
cadastro de persona não há Guerreiro(a) para o App 01 reconhecer, não há Mestre para conduzir
aula e não há Apoiador para aportar; é a fatia que destrava as aplicações do documento 99 §9
liberadas a partir do PRD-02.

Ela também recebe o desfecho da colisão de nick decidido junto da change `nick-de-adulto`: o
cadastro de adulto nasce sem nick quando o pretendido já pertence a alguém, e é aqui que o
Admin grava o nick novo depois de tratar com a pessoa fora da plataforma.

## What Changes

- **Rotas de cadastro de persona no núcleo**, de Admin: Guerreiro(a) com nome, nascimento, nick
  e avatar (`RF-02-01`); Mestre e Apoiador com os links comprobatórios declarados (`RF-02-02`,
  `RF-02-03`); Admin novo por inclusão manual (`RF-02-05`).
- **Recusa de cadastro de Mestre ou Apoiador sem ao menos um artefato comprobatório**
  (`RF-02-04`), que hoje não existe em lugar nenhum do núcleo.
- **Edição do nick de adulto pelo Admin**, o desfecho da colisão: o Admin grava o nick que a
  pessoa lhe passou por canal externo, sujeito à mesma unicidade global (`RN-01-30`).
- **Telas de cadastro na App 03** para as personas acima e para o responsável e o vínculo, cujas
  rotas de núcleo já existem (`RF-02-06`, `RF-02-07`).
- **Edição do Guerreiro(a)** já cadastrado, que `RF-02-01` pede junto do cadastro.

## Capabilities

### New Capabilities

- `cadastro-de-persona`: as rotas de Admin que criam e editam persona de cada papel, o artefato
  comprobatório obrigatório do adulto e a gravação do nick pelo Admin na colisão.

### Modified Capabilities

- `aplicacao-de-gestao`: a App 03 ganha as telas de cadastro de persona e de vínculo do
  responsável, com o caminho da colisão de nick.

## Impact

- **Núcleo (`backend/`)**: `personas/rotas.py` ganha as rotas de cadastro e a de edição de nick;
  `personas/regra.py` ganha o artefato comprobatório. Migração para os links comprobatórios e
  para os dados próprios de cada papel, se ainda não houver satélite que os guarde.
- **App 03 (`apps/app-03-gestao/`)**: módulo novo de personas, ao lado de `comunidades`,
  `agenda` e `pontos-de-apoio`.
- **Depende de** `nick-de-adulto`, que entrega o nick opcional em adulto e a unicidade que
  alcança o Mestre.
- **Documentação, no mesmo PR**: `docs/prds/index.md` e o que a fatia mudar no PRD-02.
- **Fora do escopo**: a fila do pré-cadastro e a homologação do aporte (`RF-02-83` a
  `RF-02-86`), com a publicação do card do Apoiador, que são fatia própria; o catálogo de
  poderes (`RF-02-10`); as equipes (`RF-02-08`, `RF-02-09`), que a App 03 não cria por
  `RN-02-09`.
