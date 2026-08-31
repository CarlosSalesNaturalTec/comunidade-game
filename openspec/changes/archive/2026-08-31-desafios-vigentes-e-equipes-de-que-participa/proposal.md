# Desafios vigentes e equipes de que participa

Fatia 6 do **PRD-05 — Área do Guerreiro(a)**.

Atende `RF-05-19`, `RF-05-22`, `RF-05-23` e `RF-05-24`, sob `RN-05-12`, `RN-05-15` e
`RN-05-22`.

## Why

A jornada §5.2 do PRD-05 abre a Área do Guerreiro(a) na próxima missão e, logo abaixo, no que
está **em aberto hoje**. As fatias 1 a 5 entregaram o percurso da trilha, a coleta, a carteira
e a criação original; falta o meio da linha "em aberto": **nenhuma rota diz ao Guerreiro(a)
quais atividades ele ainda tem para fazer**, e **nenhuma diz de que equipes ele participa**.
Hoje a equipe só é alcançável uma trilha por vez, pela rota que a entrega da criação original
precisou (`GET /v1/eu/trilhas/{id}/equipe`), e a equipe da aula não é alcançável por ele de
forma alguma.

As duas rotas da §9 do PRD que cobrem isso — `GET /v1/eu/desafios` e `GET /v1/eu/equipes` —
seguem sem implementação, e a App 05 não tem o bloco que as consome.

### Decisão de recorte levada ao fundador

O `RF-05-19` fala em desafios semanais **vigentes**, e a `Atividade` não tem janela de
vigência — ao contrário do `DesafioExtra`, que tem. O fundador decidiu que "vigente", aqui, é
**em aberto para aquele Guerreiro(a)**: a atividade das missões que ele já desbloqueou, nas
trilhas em que está inscrito, e que ainda não tem `Resultado` lançado para ele. "Semanal"
segue sendo o nome da fonte de pontos do documento 11 §5, não uma janela de datas — nenhum
campo novo nasce nesta fatia.

O fundador decidiu também trocar, na linha desta fatia do cronograma, o `RN-05-23` (regra do
App 04, o jogo, que lê o progresso e nada escreve) pelo `RN-05-12`, que é a regra que sustenta
o `RF-05-24`.

## What Changes

**Núcleo**

- `GET /v1/eu/desafios` (PRD-05 §9): as atividades em aberto para o Guerreiro(a) em sessão,
  cada uma com **modalidade** e **formato** (`RF-05-19`). Em aberto é o que o fundador
  decidiu acima: missão desbloqueada, trilha inscrita, sem `Resultado` lançado para ele.
- `GET /v1/eu/equipes` (PRD-05 §9): as equipes de que o Guerreiro(a) em sessão participa — as
  da aula e as da trilha —, o **papel** dele em cada uma e as **atividades** de cada uma
  (`RF-05-22`). Os integrantes saem apenas por **avatar e nick** (`RF-05-23`, `RN-05-15`),
  como a leitura das equipes da aula já faz para a App 01.
- Nenhuma rota de escrita de equipe é acrescentada: formar, entrar, sair e homologar seguem
  onde estão, no App 01 e na App 09 (`RF-05-24`, `RN-05-12`).

**App 05 — Área do Guerreiro(a)**

- Bloco **Desafios**: os desafios em aberto, cada um com modalidade e formato em linguagem da
  criança, e a produção que se espera dele (`RF-05-19`). Sem desafio em aberto, a tela diz
  isso — nunca lista vazia muda.
- Bloco **Minhas equipes**: as equipes de que participa, o papel em cada uma e as atividades
  delas (`RF-05-22`); os colegas aparecem por avatar e nick, sem qualquer dado pessoal
  (`RF-05-23`).
- A tela **não oferece** formar, editar, entrar nem sair de equipe, e diz onde a equipe se
  forma (`RF-05-24`, `RN-05-12`). Não há canal de conversa em nenhuma das duas telas
  (`RN-05-22`).

### Fora do escopo

Reproduz o que o PRD já exclui, sem exclusão nova:

- **Desafio extra na Área do Guerreiro(a)** (`RF-05-20`, `RF-05-21`) — é a fatia 8 do PRD-05.
- Formação, edição e homologação de equipe — acontecem no App 01 e na App 09 (`RN-05-12`,
  PRD-05 §3.2).
- Lançamento de resultado, presença ou mérito — é do Mestre ou do Admin (`RN-05-06`,
  PRD-05 §3.2).
- Entrega da produção da missão e devolutiva (`RF-05-74` a `RF-05-80`) — é a fatia 7.
- Acervo do Guerreiro(a), canal de sugestões e apoio escolar — Ciclo 02 (PRD-05 §3.2).

## Capabilities

### New Capabilities

Nenhuma. O recorte estende capacidades que já existem.

### Modified Capabilities

- `area-do-guerreiro`: a leitura dos desafios em aberto do Guerreiro(a) em sessão, com
  modalidade e formato, e as telas dos dois blocos — desafios e equipes de que participa.
- `equipe`: as equipes de que o Guerreiro(a) em sessão participa passam a ser alcançáveis por
  HTTP em uma só leitura, com o papel dele e as atividades de cada equipe, e a leitura segue
  restrita a avatar e nick.

## Impact

- `backend/src/nucleo/trilhas/` — `regra.py` (derivação dos desafios em aberto) e `rotas.py`
  (`GET /v1/eu/desafios`).
- `backend/src/nucleo/equipes/` — `regra.py` (as equipes da persona em sessão) e `rotas.py`
  (`GET /v1/eu/equipes`).
- Nenhuma migração de esquema: a fatia é de leitura sobre entidades já de pé.
- `apps/app-05-guerreiro/src/` — bloco dos desafios, bloco das equipes, cliente de API e a
  navegação da `AreaDoGuerreiro`.
- Documentação: a linha da fatia 6 em `openspec/cronograma-de-fatias.md` — situação, slug e a
  troca do `RN-05-23` pelo `RN-05-12` no recorte.
