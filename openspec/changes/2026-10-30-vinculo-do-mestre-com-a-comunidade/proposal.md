# Proposal

**Origem:** PRD-02 (`RF-02-30`) e PRD-01 §8 — linha **sem número** do bloco do PRD-02 em
`openspec/cronograma-de-fatias.md` ("Vínculo do Mestre com a comunidade, aberto no
agendamento"). Correção de defeito preexistente, não fatia de requisito novo.

**Atende:** `RF-02-30`, `RF-01-20`, `RF-01-71`, `RF-01-72`, `RF-02-95`, `RF-07-13`,
`RF-07-11`, `RF-07-27`, `RF-07-47`, `RF-09-62`, `RF-09-75`, `RF-09-76`, `RF-09-122`,
`RF-02-41` a `RF-02-47`, `RN-08-02`, `RN-01-05`, `RN-02-17`.

**Decisão do fundador, 2026-10-30**, em `docs/09-topicos-em-aberto-e-sugestoes.md` §1, linha
"Vínculo do Mestre com a comunidade". Nenhuma regra nova nasce aqui.

## Why

`operador.vinculo_vigente` é **sempre** nulo para Mestre, em qualquer instalação: a relação
casa `VinculoJogador.guerreiro_id == Persona.id`, e `abrir_vinculo` recusa papel que não seja
Guerreiro(a) (`RN-08-02`). O Mestre nunca teve vínculo de comunidade — e dez pontos de leitura
do núcleo o consultam.

Em produção, saem **vazias** a fila de entregas pendentes (`RF-09-75`), a agenda do Mestre
(`RF-02-41` a `RF-02-47`), o acervo (`RF-07-11`), os pontos de apoio (`RF-07-47`), as
necessidades (`RF-07-27`), o painel do dia e as duas leituras de responsáveis (`RF-09-62`,
`RF-09-122`); e são **recusados** a confirmação da entrega da recompensa de marco
(`RF-07-13`) e o cancelamento de aula pelo Mestre (`RF-01-72`, `RF-02-95`).

A suíte está verde porque 24 arquivos de teste gravam o vínculo do Mestre à mão, por fora de
`abrir_vinculo` — provam um estado que o núcleo recusa criar.

As specs já descrevem o comportamento correto, **no plural** ("as comunidades a que está
vinculado", em `aula-e-presenca`, `patrimonio`, `necessidade-de-recurso`,
`responsavel-e-vinculo` e `area-do-mestre`). O desvio é só da implementação: faltava a
entidade que sustenta o plural.

## What Changes

- Nasce o **vínculo do Mestre com a Comunidade Virtual** como entidade própria, separada do
  `VinculoJogador`, que continua exclusivo do Guerreiro(a). **N comunidades por Mestre**, e
  **sem data de fim**: no Ciclo 01 o vínculo do Mestre **nunca encerra**.
- Nasce o registro de **quem ministra a aula**, N:N entre aula e Mestre.
- **BREAKING** — o agendamento passa a exigir **um ou mais Mestres** (`RF-02-30`, `RF-01-20`).
  Agendamento sem Mestre é recusado com 422. Abre, para cada Mestre escalado, o vínculo com a
  comunidade da aula, quando ainda não houver.
- A tela de agendamento da App 03 ganha a **seleção de Mestres**, obrigatória;
  `GET /v1/mestres` já a serve.
- Os **oito pontos de escopo de leitura** passam a alcançar o conjunto de comunidades do
  Mestre, em vez de uma só, cumprindo o que as specs já diziam.
- As **duas guardas de escrita** — cancelamento de aula e confirmação da entrega — conferem
  a comunidade contra o conjunto.
- As três cópias de `escopo_de_comunidade_da_leitura` (`aulas`, `pontos_de_apoio`,
  `patrimonio`) consolidam-se numa só.
- **Sem retroação**: as aulas da fase de testes foram canceladas (decisão do fundador,
  2026-10-30). A migração cria as tabelas vazias.

## Capabilities

### New Capabilities

Nenhuma. O vínculo do Mestre é comportamento da capacidade que já é dona de quem pertence a
uma Comunidade Virtual.

### Modified Capabilities

- `comunidade-virtual`: ganha o **vínculo do Mestre** — entidade própria, N comunidades, sem
  data de fim, aberto pelo agendamento. O vínculo do Guerreiro(a) permanece exatamente como
  está: um só vigente, atribuído pela aula em que se cadastra (`RN-08-02`, invariante 4 do
  documento 99 §6).
- `aula-e-presenca`: o agendamento passa a exigir **um ou mais Mestres** e a registrar quem
  ministra a aula; é o ato que abre o vínculo do Mestre com a comunidade (`RF-02-30`,
  `RF-01-20`).
- `recompensa-de-marco`: a fila de entregas pendentes deixa de alcançar "a Comunidade Virtual
  a que o Mestre está vinculado" e passa a alcançar **as comunidades** a que ele está
  vinculado (`RF-09-75`, `RF-07-13`).
- `painel-do-dia`: o painel do Mestre passa a considerar **as comunidades** dele, e com isso
  torna-se alcançável para o Mestre o caso de mais de uma aula vigente ao mesmo tempo, que o
  requisito já resolve para o Admin (`RF-02-41` a `RF-02-47`).
- `aplicacao-de-gestao`: a tela de agendamento da App 03 passa a exigir a seleção de um ou
  mais Mestres (`RF-02-30`).

As capacidades `patrimonio`, `necessidade-de-recurso`, `responsavel-e-vinculo` e
`area-do-mestre` **não entram no delta**: o enunciado delas já está no plural e não muda. O
que muda ali é implementação, e entra nas tasks.

## Impact

**Núcleo (`backend/`)** — duas tabelas novas e uma migração Alembic; `aulas/regra.py`
(agendamento e cancelamento), `comunidades/regra.py` (abertura do vínculo e o filtro por
comunidade), `patrimonio/regra.py`, `pontos_de_apoio/regra.py`, `necessidades/regra.py`,
`painel_do_dia/regra.py`, `responsaveis/regra.py` e `recompensas_de_marco/regra.py`.

**Rotas** — `POST /v1/aulas` ganha os Mestres no corpo. Nenhuma rota nova: `GET /v1/mestres`
já existe e serve o seletor.

**App 03 (`apps/app-03-gestao/`)** — `FormularioDeAgendamento` ganha a seleção de Mestres.

**Testes** — a fixture `criar_vinculo_jogador(mestre, …)` deixa de ser válida; 24 arquivos de
teste passam a abrir o vínculo do Mestre pela entidade própria.

**Documentação, no mesmo PR** — PRD-01 §8 e PRD-02 §8 (a `Aula/Agenda` ganha os Mestres),
`RF-02-30` (Mestres obrigatórios), `RF-02-59` (o singular "Mestre da aula" passa a plural),
PRD-07 §9 e o invariante 4 do documento 99 §6, que passa a ter a metade do Mestre. A linha do
cronograma fecha com o slug desta change.

**Fora do escopo** — a fatia 31 do PRD-04 (entregas pendentes do encontro na App 01) é change
própria e **depende** desta. A troca de comunidade do Guerreiro(a) segue fora do Ciclo 01
(`RF-08-03`), e nada aqui a abre.
